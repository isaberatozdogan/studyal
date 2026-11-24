
from indeksleme.belge_indeksle import koleksiyona_baglan
from belge_isleme.tablo_baglam import tablo_baglamini_olustur


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

kayitlar = tablo_baglamini_olustur(parcalar)

kontrol_siralari = [
    4, 12, 16, 38, 60, 65, 68,
    79, 93, 95, 110, 127, 130, 148
]

for kayit in kayitlar:

    sira = kayit["metadata"].get("parca_sirasi")

    if sira not in kontrol_siralari:
        continue

    print("\n" + "=" * 65)
    print("PARÇA:", sira)
    print("AKADEMİK BİRİM:", kayit["akademik_birim"])
    print("DÖNEM:", kayit["donem"])
    print("METİN:", kayit["metin"][:250])
