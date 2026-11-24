
from rag.arama_v2 import belge_ara_v2
from rag.reranking import sonuclari_sirala

sorular = [
    "Mali kayıt işlemleri nasıl yapılır?",
    "2026-2027 güz dönemi ders kayıtları ne zaman?"
]

for soru in sorular:
    print("\n" + "=" * 60)
    print("SORU:", soru)

    # Daha fazla aday getir
    sonuclar = belge_ara_v2(soru, limit=20)

    # Yeniden sırala
    siralanmis = sonuclari_sirala(
        soru,
        sonuclar
    )

    for i, sonuc in enumerate(
        siralanmis[:5], 1
    ):
        print(f"\n--- SONUÇ {i} ---")
        print("Puan:", round(sonuc["puan"], 3))
        print("Dosya:", sonuc["dosya"])
        print("Başlık:", sonuc["baslik"])
        print("Metin:", sonuc["metin"][:350])
