
from rag.hibrit_arama import hibrit_ara
from rag.kaynak_kontrol import kaynaklari_kontrol_et


sorular = [
    "Mali kayıt işlemleri nasıl yapılır?",
    "Üniversite kaydı için hangi belgeler gerekli?",
    "2026-2027 güz dönemi ders kayıtları ne zaman?",
    "Öğrencilerin burs işlemleri nasıl yapılır?"
]


for soru in sorular:
    print("\n" + "=" * 65)
    print("SORU:", soru)

    # İlk 5 yerine 20 aday getiriyoruz.
    sonuclar = hibrit_ara(
        soru,
        limit=20,
        aday_sayisi=40
    )

    kontrol_edilenler = kaynaklari_kontrol_et(
        soru,
        sonuclar
    )

    for i, sonuc in enumerate(
        kontrol_edilenler[:5], 1
    ):
        print(f"\n--- SONUÇ {i} ---")
        print("Dosya:", sonuc["dosya"])
        print("Başlık:", sonuc["baslik"])
        print(
            "Eşleşme oranı:",
            sonuc["eslesme_orani"]
        )
        print(
            "Eşleşen kelimeler:",
            sonuc["eslesen_kelimeler"]
        )
        print("Metin:", sonuc["metin"][:300])
