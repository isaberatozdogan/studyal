
def tablo_satirini_ayir(satir):
    """
    | karakteriyle ayrılmış tablo
    satırını hücrelere böler.
    """
    return [
        hucre.strip()
        for hucre in satir.split("|")
        if hucre.strip()
    ]


def tabloyu_yapilandir(satirlar):
    """
    İlk satırı sütun başlıkları kabul eder.
    Sonraki satırları sözlük olarak kaydeder.
    """
    if not satirlar:
        return []

    basliklar = tablo_satirini_ayir(satirlar[0])
    kayitlar = []

    for satir in satirlar[1:]:
        hucreler = tablo_satirini_ayir(satir)

        if not hucreler:
            continue

        kayit = {}

        for i, baslik in enumerate(basliklar):
            kayit[baslik] = (
                hucreler[i]
                if i < len(hucreler)
                else None
            )

        # Fazladan hücreleri kaybetme
        if len(hucreler) > len(basliklar):
            kayit["_ek_hucreler"] = hucreler[
                len(basliklar):
            ]

        kayitlar.append(kayit)

    return kayitlar
