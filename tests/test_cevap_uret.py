
from rag.cevap_uret import cevap_uret


sorular = [
    "Mali kayıt işlemleri nasıl yapılır?",
    "Üniversite kaydı için hangi belgeler gerekli?",
    "Öğrencilerin burs işlemleri nasıl yapılır?"
]


for soru in sorular:
    print("\n" + "=" * 70)
    print("SORU:", soru)

    sonuc = cevap_uret(soru)

    print("\nSTUDYAL CEVABI:")
    print(sonuc["cevap"])

    print("\nKULLANILAN KAYNAKLAR:")

    for i, kaynak in enumerate(
        sonuc["kaynaklar"], 1
    ):
        print(
            f"[Kaynak {i}] "
            f"{kaynak['dosya']}"
        )
