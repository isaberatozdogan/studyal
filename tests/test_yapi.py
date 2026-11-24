
from belge_isleme.yapi_analizi import belge_yapisini_analiz_et

ornek_metin = """
KAYIT İŞLEMLERİ
Öğrenciler kayıtlarını belirtilen tarihlerde yapmalıdır.

GEREKLİ BELGELER
Kimlik fotokopisi
Diploma

Ders Kayıtları | 14 Eylül 2026 | 25 Eylül 2026
"""

bolumler = belge_yapisini_analiz_et(ornek_metin)

for bolum in bolumler:
    print("Tür:", bolum["tip"])
    print("Başlık:", bolum["baslik"])
    print("İçerik:", bolum["icerik"])
    print("-" * 40)
