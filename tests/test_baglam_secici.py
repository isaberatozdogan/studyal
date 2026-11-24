
from rag.hibrit_arama import hibrit_ara
from rag.kanit_kontrol import kanitlari_degerlendir
from rag.baglam_secici import baglam_sec


sorular = [
    "Mali kayıt işlemleri nasıl yapılır?",
    "Üniversite kaydı için hangi belgeler gerekli?",
    "Öğrencilerin burs işlemleri nasıl yapılır?"
]


for soru in sorular:
    print("\n" + "=" * 65)
    print("SORU:", soru)

    sonuclar = hibrit_ara(
        soru,
        limit=20,
        aday_sayisi=40
    )

    sirali = kanitlari_degerlendir(
        soru,
        sonuclar
    )

    secilenler = baglam_sec(
        soru,
        sirali,
        limit=12
    )

    print("Seçilen parça sayısı:", len(secilenler))

    for i, parca in enumerate(secilenler, 1):
        print(f"\n--- PARÇA {i} ---")
        print("Dosya:", parca["dosya"])
        print("Puan:", parca["puan"])
        print("Metin:", parca["metin"][:250])
