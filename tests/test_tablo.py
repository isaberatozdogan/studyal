
from belge_isleme.tablo_isleme import tabloyu_yapilandir

ornek_tablo = [
    "Faaliyet | Başlangıç | Bitiş",
    "Ders Kayıtları | 14 Eylül 2026 | 25 Eylül 2026",
    "Yatay Geçiş | 08 Temmuz 2026 | 15 Ağustos 2026",
    "Akademik Açılış | 21 Eylül 2026 |"
]

kayitlar = tabloyu_yapilandir(ornek_tablo)

for kayit in kayitlar:
    print("\n--- KAYIT ---")

    for alan, deger in kayit.items():
        print(f"{alan}: {deger}")
