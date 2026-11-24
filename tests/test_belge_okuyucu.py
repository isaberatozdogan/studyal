
from pathlib import Path
from veri_toplama.belge_okuyucu import belge_oku

BELGELER = Path(__file__).resolve().parent / "belgeler"

uzantilar = {".pdf", ".docx", ".txt", ".md"}

for dosya in sorted(BELGELER.iterdir()):
    if dosya.suffix.lower() not in uzantilar:
        continue

    print(f"\n--- {dosya.name} ---")

    try:
        bolumler = belge_oku(dosya)

        print("Okunan bölüm:", len(bolumler))

        for bolum in bolumler[:1]:
            print("Sayfa:", bolum["sayfa"])
            print("İlk 300 karakter:")
            print(bolum["metin"][:300])

    except Exception as hata:
        print("HATA:", hata)
