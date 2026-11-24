
def satir_icerigi(metin):
    if "Bilgi:" in metin:
        return metin.split("Bilgi:", 1)[1].strip()

    if "İçerik:" in metin:
        return metin.split("İçerik:", 1)[1].strip()

    return metin.strip()


def donem_bul(metin):
    metin = metin.strip().upper()

    if "GÜZ YARIYILI" in metin:
        return "Güz Yarıyılı"

    if "BAHAR YARIYILI" in metin:
        return "Bahar Yarıyılı"

    if "YAZ OKULU" in metin:
        return "Yaz Okulu"

    return None


def akademik_birim_bul(metin):
    metin = metin.upper()

    if "ÖN LİSANS / LİSANS" in metin:
        return "Ön Lisans / Lisans (Tıp ve Diş Hekimliği Hariç)"

    if "TIP FAKÜLTESİ" in metin:
        return "Tıp Fakültesi"

    if "DİŞ HEKİMLİĞİ FAKÜLTESİ" in metin:
        return "Diş Hekimliği Fakültesi"

    if "LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ" in metin:
        return "Lisansüstü Eğitim Enstitüsü"

    return None


def tablo_baglamini_olustur(parcalar):
    sirali = sorted(
        parcalar,
        key=lambda x: x[1].get("parca_sirasi", 0)
    )

    aktif_birim = None
    aktif_donem = None
    onceki_baslik = None

    sonuc = []

    for metin, metadata in sirali:
        icerik = satir_icerigi(metin)

        hucreler = [
            hucre.strip()
            for hucre in icerik.split("|")
        ]

        baslik = str(
            metadata.get("baslik", "")
        ).strip().upper()

        # Önce içerikteki açık birim ve dönemleri kontrol et.
        yeni_birim = None
        yeni_donem = None

        for hucre in hucreler[:2]:
            if yeni_birim is None:
                yeni_birim = akademik_birim_bul(hucre)

            if yeni_donem is None:
                yeni_donem = donem_bul(hucre)

        if yeni_birim:
            aktif_birim = yeni_birim

        if yeni_donem:
            aktif_donem = yeni_donem

        # Metadata başlığını yalnızca değiştiğinde kullan.
        elif baslik != onceki_baslik:
            if baslik in (
                "GÜZ YARIYILI",
                "BAHAR YARIYILI",
                "YAZ OKULU"
            ):
                aktif_donem = donem_bul(baslik)

        onceki_baslik = baslik

        sonuc.append({
            "metin": metin,
            "metadata": metadata,
            "akademik_birim": aktif_birim,
            "donem": aktif_donem
        })

    return sonuc
