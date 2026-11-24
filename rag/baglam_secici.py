
from rag.turkce_metin import kelimeleri_normalize_et
from rag.belge_baglami import belge_baglamini_getir


def baglam_sec(soru, arama_sonuclari, limit=20):

    if not arama_sonuclari:
        return []

    soru_kelimeleri = kelimeleri_normalize_et(soru)

    dosya = arama_sonuclari[0]["dosya"]

    parcalar = belge_baglamini_getir(
        dosya,
        limit=1000
    )

    if not parcalar:
        return []

    puanlar = []

    for parca in parcalar:
        metin = parca["metin"]

        if "İçerik:" in metin:
            icerik = metin.split("İçerik:", 1)[1]
        elif "Bilgi:" in metin:
            icerik = metin.split("Bilgi:", 1)[1]
        else:
            icerik = metin

        kelimeler = kelimeleri_normalize_et(icerik)

        puan = len(soru_kelimeleri & kelimeler)

        puanlar.append(puan)

    # Dosya küçükse ve soru belgenin ana konusuyla
    # ilgiliyse tüm parçaları birlikte değerlendir.
    baslik = parcalar[0].get("baslik", "")

    baslik_kelimeleri = kelimeleri_normalize_et(
        baslik
    )

    baslik_eslesmesi = len(
        soru_kelimeleri & baslik_kelimeleri
    )

    if len(parcalar) <= 20 and baslik_eslesmesi >= 2:
        return [
            {**parca, "puan": puanlar[i]}
            for i, parca in enumerate(parcalar)
        ]

    # Diğer sorularda yalnızca içerikle eşleşen
    # parçaları seç.
    secilenler = []

    for i, parca in enumerate(parcalar):
        if puanlar[i] > 0:
            secilenler.append({
                **parca,
                "puan": puanlar[i]
            })

    secilenler.sort(
        key=lambda x: x["puan"],
        reverse=True
    )

    return secilenler[:limit]
