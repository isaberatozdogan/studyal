
import re


KELIME_GRUPLARI = {
    "burs": {
        "burs", "burslu", "burslar", "bursları",
        "bursların", "bursluluk"
    },
    "kayit": {
        "kayıt", "kaydı", "kayıtlar", "kayıtları",
        "kaydınızı", "kaydını"
    },
    "belge": {
        "belge", "belgeler", "belgeleri",
        "belgesi", "belgelerin"
    },
    "islem": {
        "işlem", "işlemler", "işlemleri",
        "işlemin", "işlemlerinin"
    },
    "odeme": {
        "ödeme", "ödemeler", "ödemesi",
        "ödemenin", "ödemenizi"
    },
    "ders": {
        "ders", "dersler", "dersleri",
        "derslerin"
    }
}


NORMALIZASYON = {}

for kok, kelimeler in KELIME_GRUPLARI.items():
    for kelime in kelimeler:
        NORMALIZASYON[kelime] = kok


DURAK_KELIMELER = {
    "ve", "veya", "ile", "için",
    "nasıl", "nedir", "hangi", "ne",
    "zaman", "yapılır", "gerekli",
    "öğrencilerin", "öğrenci",
    "üniversite", "üniversitenin"
}


def kelimeleri_normalize_et(metin):
    metin = metin.replace("İ", "i").replace("I", "ı")
    metin = metin.lower()

    kelimeler = re.findall(
        r"[a-zçğıöşü0-9]+",
        metin
    )

    sonuc = []

    for kelime in kelimeler:
        if kelime in DURAK_KELIMELER:
            continue

        sonuc.append(
            NORMALIZASYON.get(kelime, kelime)
        )

    return set(sonuc)
