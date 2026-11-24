
import re


def satir_tipi_belirle(satir, onceki_bos=False):
    satir = satir.strip()

    if not satir:
        return "bos"

    if re.match(r"^#{1,6}\s+\S", satir):
        return "baslik"

    if "|" in satir:
        return "tablo"

    if re.match(r"^\d+(?:\.\d+)*[.)]\s+", satir):
        if len(satir) < 100:
            return "baslik"

    harfler = [
        karakter for karakter in satir
        if karakter.isalpha()
    ]

    if (
        harfler
        and len(satir) < 100
        and satir == satir.upper()
    ):
        return "baslik"

    if (
        onceki_bos
        and len(satir) < 100
        and not satir.endswith((".", ",", ";", ":"))
        and not re.search(r"\d", satir)
    ):
        return "olasi_baslik"

    return "paragraf"



def tablo_bolum_basligi_mi(satir):
    """
    Tablo içindeki akademik birim ve dönem
    başlıklarını tespit eder.

    Örnek:
    TIP FAKÜLTESİ | GÜZ YARIYILI
    """

    hucreler = [
        hucre.strip()
        for hucre in satir.split("|")
    ]

    if len(hucreler) != 2:
        return False

    if not all(hucreler):
        return False

    # Tablo sütun adları bölüm başlığı değildir.
    sutun_basliklari = {
        "BAŞLANGIÇ",
        "BİTİŞ",
        "TARİH",
        "TARİHLER",
        "AKADEMİK FAALİYET",
        "AKADEMİK BİRİM"
    }

    if all(
        hucre.upper() in sutun_basliklari
        for hucre in hucreler
    ):
        return False

    # Birinci hücre akademik birimi,
    # ikinci hücre dönemi belirtmeli.
    donemler = {
        "GÜZ YARIYILI",
        "BAHAR YARIYILI",
        "YAZ OKULU"
    }

    ikinci_hucre = hucreler[1].upper()

    if ikinci_hucre not in donemler:
        return False

    birinci_hucre = hucreler[0]

    # Akademik birim adı boş olmamalı
    # ve tarih içermemeli.
    if not any(
        karakter.isalpha()
        for karakter in birinci_hucre
    ):
        return False

    if any(
        karakter.isdigit()
        for karakter in birinci_hucre
    ):
        return False

    return True


def belge_yapisini_analiz_et(metin):
    bolumler = []

    aktif_baslik = "Genel"
    onceki_bos = True
    ilk_satir = True

    for satir in metin.splitlines():
        temiz_satir = satir.strip()

        if not temiz_satir:
            onceki_bos = True
            continue

        tip = satir_tipi_belirle(
            temiz_satir,
            onceki_bos=onceki_bos
        )

        if ilk_satir:
            if (
                len(temiz_satir) <= 120
                and tip != "tablo"
                and not temiz_satir.endswith(
                    (".", ",", ";")
                )
            ):
                tip = "baslik"

            ilk_satir = False

        # Tablo içindeki bölüm başlıklarını ayır
        if (
            tip == "tablo"
            and tablo_bolum_basligi_mi(temiz_satir)
        ):
            tip = "tablo_bolum_basligi"

        if tip in ("baslik", "tablo_bolum_basligi"):
            aktif_baslik = temiz_satir

        elif tip == "olasi_baslik":
            tip = "paragraf"

        bolumler.append({
            "tip": tip,
            "baslik": aktif_baslik,
            "icerik": temiz_satir
        })

        onceki_bos = False

    return bolumler
