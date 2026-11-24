
from rag.arama_v2 import belge_ara_v2

sorular = [
    "Üniversite kaydı için hangi belgeler gerekli?",
    "Mali kayıt işlemleri nasıl yapılır?",
    "2026-2027 güz dönemi ders kayıtları ne zaman?"
]

for soru in sorular:
    print("\n" + "=" * 60)
    print("SORU:", soru)

    sonuclar = belge_ara_v2(soru, limit=3)

    for i, sonuc in enumerate(sonuclar, 1):
        print(f"\n--- SONUÇ {i} ---")
        print("Dosya:", sonuc["dosya"])
        print("Başlık:", sonuc["baslik"])
        print("Sayfa:", sonuc["sayfa"])
        print("Uzaklık:", round(sonuc["uzaklik"], 4))
        print("Metin:", sonuc["metin"][:500])
