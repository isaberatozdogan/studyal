
import re


def normalize(metin):
    metin = metin.casefold()

    ceviri = str.maketrans({
        "ı": "i",
        "ş": "s",
        "ğ": "g",
        "ü": "u",
        "ö": "o",
        "ç": "c"
    })

    metin = metin.translate(ceviri)
    metin = re.sub(r"\s+", " ", metin)

    return metin.strip()


def islem_turu_belirle(metin):
    metin = normalize(metin)

    # Ders kaydı, ders seçimi, danışman onayı
    if re.search(
        r"ders\s*kayit|"
        r"derslerin\s*kayit|"
        r"ders\s*secim|"
        r"danisman\s*onay|"
        r"kayit\s*yenile",
        metin
    ):
        return "ders_kaydi"

    # Derslerin başlaması
    if re.search(
        r"derslerin\s*baslam|"
        r"dersler\s*ne zaman\s*basl|"
        r"dersleri\s*ne zaman\s*basl|"
        r"ders\s*baslangic|"
        r"derslerin\s*baslangic",
        metin
    ):
        return "ders_baslangici"

    # Sınav başvuruları
    if re.search(
        r"sinav\s*basvuru|"
        r"sinavlarina\s*basvuru",
        metin
    ):
        return "sinav_basvurusu"

    # Sınav sonuçları ve duyuruları
    if re.search(
        r"sinav\s*sonuc|"
        r"sinav.*duyuru|"
        r"not\s*giris",
        metin
    ):
        return "sinav_sonucu"

    # Sınavın yapıldığı tarihler
    if "sinav" in metin:
        return "sinav"

    return None


def satir_icerigini_al(metin):
    if "İçerik:" in metin:
        return metin.split("İçerik:", 1)[1].strip()

    if "Bilgi:" in metin:
        return metin.split("Bilgi:", 1)[1].strip()

    return metin.strip()


def takvim_sonuclarini_filtrele(soru, sonuclar):
    soru_turu = islem_turu_belirle(soru)

    if soru_turu is None:
        return sonuclar

    filtrelenen = []

    for sonuc in sonuclar:
        icerik = satir_icerigini_al(
            sonuc.get("metin", "")
        )

        sonuc_turu = islem_turu_belirle(icerik)

        if sonuc_turu == soru_turu:
            filtrelenen.append(sonuc)

    return filtrelenen
