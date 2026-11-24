
from indeksleme.belge_indeksle import koleksiyona_baglan


koleksiyon = koleksiyona_baglan()

sonuc = koleksiyon.get(
    where={
        "dosya": "okan_akademik_takvim_2026_2027.txt"
    },
    include=["documents", "metadatas"]
)

parcalar = list(zip(
    sonuc["documents"],
    sonuc["metadatas"]
))

parcalar.sort(
    key=lambda x: x[1].get("parca_sirasi", 0)
)

anahtarlar = [
    "YARIYILI",
    "AKADEMİK BİRİM",
    "FAKÜLTESİ",
    "FAKÜLTESİ /",
    "ÖN LİSANS",
    "LİSANSÜSTÜ",
    "YAZ OKULU",
    "DERS KAYITLARININ YAPILMASI"
]

print("TOPLAM PARÇA:", len(parcalar))

for i, (metin, metadata) in enumerate(parcalar):

    icerik = metin.split("\n", 1)[-1].upper()

    if any(anahtar in icerik for anahtar in anahtarlar):

        print("\n" + "=" * 65)
        print("PARÇA SIRASI:", metadata.get("parca_sirasi"))
        print("BAŞLIK:", metadata.get("baslik"))
        print("METİN:", metin[:350])

        # Başlığın çevresindeki bir önceki ve sonraki parçayı göster
        if i > 0:
            print(
                "ÖNCEKİ:",
                parcalar[i - 1][0][-180:]
            )

        if i + 1 < len(parcalar):
            print(
                "SONRAKİ:",
                parcalar[i + 1][0][-180:]
            )
