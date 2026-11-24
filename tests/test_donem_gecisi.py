
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

for metin, metadata in parcalar:
    sira = metadata.get("parca_sirasi", -1)

    if 138 <= sira <= 150:
        print("\n" + "=" * 65)
        print("PARÇA:", sira)
        print("BAŞLIK:", metadata.get("baslik"))
        print("METİN:", metin)
