
from rag.hibrit_arama import hibrit_ara
from rag.kanit_kontrol import kanitlari_degerlendir
from rag.baglam_secici import baglam_sec


sorular = [
    "2026-2027 güz dönemi dersleri ne zaman başlıyor?",
    "2026-2027 bahar dönemi ders kayıtları ne zaman?",
    "Üniversite kaydı için hangi belgeler gerekli?",
    "Mali kayıt işlemleri nasıl yapılır?",
    "Öğrencilerin burs başvurusu nasıl yapılır?",
    "Üniversitenin akademik takviminde sınav tarihleri nelerdir?"
]


for soru in sorular:

    print("\n" + "=" * 75)
    print("SORU:", soru)

    sonuclar = hibrit_ara(
        soru,
        limit=20,
        aday_sayisi=40
    )

    degerlendirmeler = kanitlari_degerlendir(
        soru,
        sonuclar
    )

    print("\nEN İYİ 5 ARAMA SONUCU:")

    for i, sonuc in enumerate(degerlendirmeler[:5], 1):
        print(
            f"{i}. {sonuc['dosya']} | "
            f"Başlık: {sonuc.get('baslik', '')} | "
            f"Eşleşme: {sonuc.get('icerik_eslesme', 0)}"
        )

    secilenler = baglam_sec(
        soru,
        degerlendirmeler,
        limit=20
    )

    print("\nSEÇİLEN BAĞLAM:")
    print("Parça sayısı:", len(secilenler))

    for i, parca in enumerate(secilenler[:5], 1):
        print(f"\n--- PARÇA {i} ---")
        print("Dosya:", parca["dosya"])
        print("Başlık:", parca.get("baslik", ""))
        print("Metin:", parca["metin"][:350])
