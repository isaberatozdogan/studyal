
from pathlib import Path
from veri_toplama.belge_okuyucu import belge_oku


BASE_DIR = Path(__file__).resolve().parent.parent
BELGELER_KLASORU = BASE_DIR / "belgeler"

DESTEKLENEN_UZANTILAR = {
    ".pdf", ".docx", ".txt", ".md"
}


def belgeleri_kontrol_et():

    print("\nSTUDYAL - BELGE KALITE KONTROL")
    print("=" * 45)

    if not BELGELER_KLASORU.exists():
        print("HATA: Belgeler klasörü bulunamadı.")
        return

    dosyalar = [
        dosya
        for dosya in BELGELER_KLASORU.iterdir()
        if dosya.is_file()
        and dosya.suffix.lower() in DESTEKLENEN_UZANTILAR
    ]

    if not dosyalar:
        print("Kontrol edilecek belge bulunamadı.")
        return

    for dosya in sorted(dosyalar):

        print("\n" + "-" * 45)
        print("Dosya:", dosya.name)
        print("Boyut:", dosya.stat().st_size, "bayt")

        try:
            bolumler = belge_oku(dosya)

            metin = "\n".join(
                bolum["metin"]
                for bolum in bolumler
            )

            karakter_sayisi = len(metin)
            anlamli_karakter = len(metin.strip())

            print("Okunan bölüm:", len(bolumler))
            print("Karakter sayısı:", karakter_sayisi)
            print("Anlamlı metin uzunluğu:", anlamli_karakter)

            if anlamli_karakter == 0:
                print("DURUM: BOŞ VEYA METİN ÇIKARILAMADI")

            elif anlamli_karakter < 100:
                print("DURUM: ÇOK KISA - KONTROL EDİLMELİ")

            else:
                print("DURUM: METİN OKUNDU")

            if anlamli_karakter > 0:
                print("\nİlk 250 karakter:")
                print(metin.strip()[:250])

        except Exception as hata:
            print("DURUM: OKUMA HATASI")
            print("Hata:", hata)

    print("\n" + "=" * 45)
    print("Kalite kontrol tamamlandı.")


if __name__ == "__main__":
    belgeleri_kontrol_et()
