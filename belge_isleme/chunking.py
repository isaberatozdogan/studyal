
from belge_isleme.yapi_analizi import (
    belge_yapisini_analiz_et
)


DONEMLER = {
    "GÜZ YARIYILI": "Güz Yarıyılı",
    "BAHAR YARIYILI": "Bahar Yarıyılı",
    "YAZ OKULU": "Yaz Okulu"
}


def donem_belirle(metin):
    return DONEMLER.get(metin.strip().upper())


def metni_parcala(metin, max_uzunluk=900):
    """
    Belgeyi başlık ve tablo bağlamını koruyarak parçalar.

    Her parça:
    - tip
    - baslik
    - metin
    - akademik_birim
    - donem
    alanlarını içerir.
    """

    bolumler = belge_yapisini_analiz_et(metin)

    parcalar = []

    aktif_baslik = "Genel"
    aktif_akademik_birim = None
    aktif_donem = None

    for bolum in bolumler:
        tip = bolum["tip"]
        icerik = bolum["icerik"]

        if tip == "tablo_bolum_basligi":
            hucreler = [
                hucre.strip()
                for hucre in icerik.split("|")
            ]

            aktif_akademik_birim = hucreler[0]
            aktif_donem = donem_belirle(hucreler[1])

            continue

        
        if tip == "baslik":
            yeni_donem = donem_belirle(icerik)

            if yeni_donem:
                # Aynı akademik birimin yeni dönemi
                aktif_donem = yeni_donem

            elif icerik.strip().upper().startswith("TABLO "):
                # Yeni tablo başladığında önceki bağlamı temizle
                aktif_baslik = icerik
                aktif_akademik_birim = None
                aktif_donem = None

            else:
                # Yeni genel başlık
                aktif_baslik = icerik
                aktif_akademik_birim = None
                aktif_donem = None

            continue


        baglam_satirlari = [
            f"Başlık: {aktif_baslik}"
        ]

        if aktif_akademik_birim:
            baglam_satirlari.append(
                f"Akademik Birim: {aktif_akademik_birim}"
            )

        if aktif_donem:
            baglam_satirlari.append(
                f"Dönem: {aktif_donem}"
            )

        baglam = "\n".join(baglam_satirlari)

        if tip == "tablo":
            parcalar.append({
                "tip": "tablo",
                "baslik": aktif_baslik,
                "akademik_birim": aktif_akademik_birim,
                "donem": aktif_donem,
                "metin": (
                    f"{baglam}\n"
                    f"Bilgi: {icerik}"
                )
            })
            continue

        if tip == "paragraf":
            if len(icerik) <= max_uzunluk:
                metin_parcalari = [icerik]
            else:
                metin_parcalari = [
                    icerik[i:i + max_uzunluk]
                    for i in range(
                        0,
                        len(icerik),
                        max_uzunluk
                    )
                ]

            for parca_metni in metin_parcalari:
                parcalar.append({
                    "tip": "paragraf",
                    "baslik": aktif_baslik,
                    "akademik_birim": aktif_akademik_birim,
                    "donem": aktif_donem,
                    "metin": (
                        f"{baglam}\n"
                        f"İçerik: {parca_metni}"
                    )
                })

    return parcalar
