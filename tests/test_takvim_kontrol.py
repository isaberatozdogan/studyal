
from rag.hibrit_arama import hibrit_ara
from rag.takvim_kontrol import takvim_sonuclarini_filtrele


sorular = [
    "2026-2027 güz dönemi dersleri ne zaman başlıyor?",
    "2026-2027 bahar dönemi ders kayıtları ne zaman?",
    "Üniversitenin akademik takviminde sınav tarihleri nelerdir?"
]


for soru in sorular:
    print("\n" + "=" * 70)
    print("SORU:", soru)

    sonuclar = hibrit_ara(
        soru,
        limit=40,
        aday_sayisi=80
    )

    filtrelenen = takvim_sonuclarini_filtrele(
        soru,
        sonuclar
    )

    print("İlk sonuç sayısı:", len(sonuclar))
    print("Filtrelenen sonuç sayısı:", len(filtrelenen))

    for i, sonuc in enumerate(filtrelenen[:8], 1):
        print(f"\n--- SONUÇ {i} ---")
        print("Dosya:", sonuc["dosya"])
        print("Başlık:", sonuc.get("baslik"))
        print("Metin:", sonuc["metin"][:350])
