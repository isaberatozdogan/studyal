
from rag.turkce_metin import kelimeleri_normalize_et


def kanitlari_degerlendir(soru, sonuclar):
    soru_kelimeleri = kelimeleri_normalize_et(soru)

    degerlendirmeler = []

    for sonuc in sonuclar:
        metin = sonuc.get("metin", "")

        # Başlık ve dosya adı yerine
        # yalnızca asıl içerikteki eşleşmeleri ölç.
        if "İçerik:" in metin:
            icerik = metin.split("İçerik:", 1)[1]
        elif "Bilgi:" in metin:
            icerik = metin.split("Bilgi:", 1)[1]
        else:
            icerik = metin

        icerik_kelimeleri = kelimeleri_normalize_et(
            icerik
        )

        eslesen = soru_kelimeleri & icerik_kelimeleri

        oran = (
            len(eslesen) / len(soru_kelimeleri)
            if soru_kelimeleri
            else 0
        )

        yeni_sonuc = dict(sonuc)
        yeni_sonuc["icerik_eslesme"] = round(oran, 3)
        yeni_sonuc["eslesen_icerik_kelimeleri"] = sorted(
            eslesen
        )

        degerlendirmeler.append(yeni_sonuc)

    return sorted(
        degerlendirmeler,
        key=lambda x: (
            x["icerik_eslesme"],
            x.get("rrf_puani", 0)
        ),
        reverse=True
    )
