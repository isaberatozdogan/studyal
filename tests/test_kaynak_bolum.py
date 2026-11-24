
from pathlib import Path

dosya = Path("belgeler/okan_akademik_takvim_2026_2027.txt")

satirlar = dosya.read_text(
    encoding="utf-8"
).splitlines()

aranan = [
    "LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ",
    "BAHAR YARIYILI",
    "GÜZ YARIYILI"
]

print("TOPLAM SATIR:", len(satirlar))

for i, satir in enumerate(satirlar):

    if any(kelime in satir.upper() for kelime in aranan):

        print("\n" + "=" * 65)
        print("SATIR NUMARASI:", i + 1)

        baslangic = max(0, i - 2)
        bitis = min(len(satirlar), i + 4)

        for j in range(baslangic, bitis):
            print(f"{j + 1}: {satirlar[j]}")
