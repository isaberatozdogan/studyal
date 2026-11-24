
from belge_isleme.chunking import metni_parcala

ornek_metin = """
KAYIT İŞLEMLERİ
Öğrenciler kayıtlarını belirtilen tarihlerde yapmalıdır.

AKADEMİK TAKVİM
Ders Kayıtları | 14 Eylül 2026 | 25 Eylül 2026
Yatay Geçiş | 08 Temmuz 2026 | 15 Ağustos 2026

GEREKLİ BELGELER
Kimlik fotokopisi
Diploma
"""

parcalar = metni_parcala(ornek_metin)

print("Toplam parça:", len(parcalar))

for i, parca in enumerate(parcalar, 1):
    print(f"\n--- PARÇA {i} ---")
    print("Tür:", parca["tip"])
    print(parca["metin"])
