
from rag.turkce_metin import kelimeleri_normalize_et


def kaynaklari_kontrol_et(soru, sonuclar):
    soru_kelimeleri = kelimeleri_normalize_et(soru)

    kontrol_edilenler = []

    for sonuc in sonuclar:
        metin = sonuc.get("metin", "")
        baslik = sonuc.get("baslik", "")
        dosya = sonuc.get("dosya", "")

        kaynak_kelimeleri = kelimeleri_normalize_et(
            metin + " " + baslik + " " + dosya
        )

        eslesenler = (
            soru_kelimeleri & kaynak_kelimeleri
        )

        if soru_kelimeleri:
            eslesme_orani = (
                len(eslesenler) / len(soru_kelimeleri)
            )
        else:
            eslesme_orani = 0

        yeni_sonuc = dict(sonuc)

        yeni_sonuc["eslesen_kelimeler"] = sorted(
            eslesenler
        )

        yeni_sonuc["eslesme_orani"] = round(
            eslesme_orani, 3
        )

        kontrol_edilenler.append(yeni_sonuc)

    return sorted(
        kontrol_edilenler,
        key=lambda x: (
            x["eslesme_orani"],
            x.get("rrf_puani", 0)
        ),
        reverse=True
    )
