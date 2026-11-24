
import re


def kelimeleri_ayir(metin):
    return set(
        re.findall(
            r"[a-zçğıöşü0-9]+",
            metin.lower()
        )
    )


def sonuclari_sirala(soru, sonuclar):
    soru_kelimeleri = kelimeleri_ayir(soru)

    siralanmis = []

    for sonuc in sonuclar:
        metin = sonuc.get("metin", "")
        baslik = sonuc.get("baslik", "")
        dosya = sonuc.get("dosya", "")

        metin_kelimeleri = kelimeleri_ayir(
            metin + " " + baslik
        )

        eslesen = len(
            soru_kelimeleri & metin_kelimeleri
        )

        puan = eslesen * 2

        # Dosya adıyla konu eşleşmesi
        dosya_kelimeleri = kelimeleri_ayir(
            dosya.replace("_", " ")
        )

        puan += len(
            soru_kelimeleri & dosya_kelimeleri
        ) * 3

        # Anlamsal yakınlığı da hesaba kat
        uzaklik = sonuc.get("uzaklik", 1)

        puan += 1 / (1 + max(uzaklik, 0))

        yeni_sonuc = dict(sonuc)
        yeni_sonuc["puan"] = puan

        siralanmis.append(yeni_sonuc)

    return sorted(
        siralanmis,
        key=lambda x: x["puan"],
        reverse=True
    )
