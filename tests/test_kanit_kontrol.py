
from rag.hibrit_arama import hibrit_ara
from rag.kanit_kontrol import kanitlari_degerlendir


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
        limit=30,
        aday_sayisi=50
    )

    degerlendirmeler = kanitlari_degerlendir(
        soru,
        sonuclar
    )

    for i, sonuc in enumerate(
        degerlendirmeler[:5], 1
    ):
        print(f"\n--- SONUÇ {i} ---")
        print("Dosya:", sonuc["dosya"])
        print("Başlık:", sonuc["baslik"])
        print("İçerik eşleşmesi:", sonuc["icerik_eslesme"])
        print(
            "Eşleşen kelimeler:",
            sonuc["eslesen_icerik_kelimeleri"]
        )
        print("Metin:", sonuc["metin"][:350])
