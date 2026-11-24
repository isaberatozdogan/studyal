
from rag.hibrit_arama import hibrit_ara

sorular = [
    "Mali kayıt işlemleri nasıl yapılır?",
    "Üniversite kaydı için hangi belgeler gerekli?",
    "2026-2027 güz dönemi ders kayıtları ne zaman?",
    "Öğrencilerin burs işlemleri nasıl yapılır?"
]

for soru in sorular:
    print("\n" + "=" * 65)
    print("SORU:", soru)

    sonuclar = hibrit_ara(
        soru,
        limit=5
    )

    for i, sonuc in enumerate(sonuclar, 1):
        print(f"\n--- SONUÇ {i} ---")
        print("RRF:", round(sonuc["rrf_puani"], 5))
        print("Dosya:", sonuc["dosya"])
        print("Başlık:", sonuc["baslik"])
        print("Metin:", sonuc["metin"][:300])

