
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup

URL = "https://www.okan.edu.tr/sayfa/9911/2026-2027-akademik-takvim/"

KLASOR = Path(__file__).resolve().parent / "belgeler"
KLASOR.mkdir(exist_ok=True)

def akademik_takvim_oku():
    cevap = requests.get(
        URL,
        timeout=30,
        headers={"User-Agent": "StudyAL/1.0"}
    )
    cevap.raise_for_status()

    soup = BeautifulSoup(cevap.content, "html.parser")

    # Farklı HTML yapılarında içerik ara.
    seciciler = [
        "main",
        "article",
        ".content",
        ".page-content",
        ".entry-content",
        ".detail",
        ".page-detail"
    ]

    alan = None

    for secici in seciciler:
        aday = soup.select_one(secici)
        if aday and len(aday.get_text(strip=True)) > 100:
            alan = aday
            print("Bulunan içerik alanı:", secici)
            break

    if alan is None:
        print("Özel içerik alanı bulunamadı.")
        print("Sayfa gövdesi kontrol ediliyor...")
        alan = soup.body

    if alan is None:
        raise ValueError("HTML gövdesi bulunamadı.")

    for etiket in alan.select(
        "script, style, nav, footer, header, "
        "aside, noscript, form"
    ):
        etiket.decompose()

   
    # Tabloları satır ve sütun ilişkilerini
    # koruyarak metne dönüştür.
    tablo_metinleri = []

    for tablo_no, tablo in enumerate(
        alan.find_all("table"), 1
    ):
        satirlar = []

        for satir in tablo.find_all("tr"):
            hucreler = [
                hucre.get_text(" ", strip=True)
                for hucre in satir.find_all(
                    ["th", "td"],
                    recursive=False
                )
            ]

            if hucreler:
                satirlar.append(" | ".join(hucreler))

        if satirlar:
            tablo_metinleri.append(
                f"TABLO {tablo_no}\n"
                + "\n".join(satirlar)
            )

        tablo.decompose()

    diger_metin = alan.get_text(
        separator="\n",
        strip=True
    )

    metin = (
        "\n\n".join(tablo_metinleri)
        + "\n\n"
        + diger_metin
    ).strip()


    # Sayfanın tamamı menüyle doluysa
    # yanlış bilgi indekslememek için dur.
    if len(metin) < 100:
        raise ValueError("Yeterli içerik bulunamadı.")

    dosya = KLASOR / "okan_akademik_takvim_2026_2027.txt"

    icerik = (
        "Başlık: 2026-2027 Akademik Takvim\n"
        f"Kaynak URL: {URL}\n"
        f"Çekilme tarihi: {datetime.now().isoformat()}\n\n"
        + metin
    )

    dosya.write_text(icerik, encoding="utf-8")

    print("\nMetin dosyası oluşturuldu.")
    print("Karakter sayısı:", len(metin))
    print("Dosya:", dosya)
    print("\nİlk 1000 karakter:\n")
    print(metin[:1000])

if __name__ == "__main__":
    akademik_takvim_oku()
