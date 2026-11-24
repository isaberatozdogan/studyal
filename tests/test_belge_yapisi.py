
from indeksleme.belge_indeksle import koleksiyona_baglan


koleksiyon = koleksiyona_baglan()

dosya_adi = "okan_akademik_takvim_2026_2027.txt"

sonuc = koleksiyon.get(
    where={"dosya": dosya_adi},
    include=["documents", "metadatas"]
)

belgeler = sonuc["documents"]
metadatalar = sonuc["metadatas"]

print("=" * 75)
print("DOSYA:", dosya_adi)
print("TOPLAM PARÇA:", len(belgeler))

print("\nİLK 20 PARÇA:")

for i, (metin, metadata) in enumerate(
    zip(belgeler[:20], metadatalar[:20]),
    1
):
    print("\n" + "-" * 65)
    print("PARÇA:", i)
    print("METADATA:", metadata)
    print("METİN:", metin[:500])


print("\n" + "=" * 75)
print("YANLIŞ BAŞLIK ŞÜPHESİ OLAN PARÇALAR:")

sayac = 0

for metin, metadata in zip(belgeler, metadatalar):

    baslik = str(metadata.get("baslik", "")).upper()
    icerik = metin.upper()

    if (
        "BAHAR" in baslik
        and "GÜZ DÖNEMİ" in icerik
    ):
        sayac += 1

        print("\n" + "-" * 65)
        print("METADATA:", metadata)
        print("METİN:", metin[:500])

        if sayac >= 5:
            break

print("\nGösterilen şüpheli parça sayısı:", sayac)


