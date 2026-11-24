
from belge_isleme.chunking import metni_parcala
from belge_isleme.metadata import parcalara_metadata_ekle

ornek_metin = """
AKADEMİK TAKVİM
Ders Kayıtları | 14 Eylül 2026 | 25 Eylül 2026
Yatay Geçiş | 08 Temmuz 2026 | 15 Ağustos 2026
"""

parcalar = metni_parcala(ornek_metin)

sonuc = parcalara_metadata_ekle(
    parcalar=parcalar,
    dosya="akademik_takvim.pdf",
    sayfa=1,
    kaynak_url=(
        "https://www.okan.edu.tr/sayfa/"
        "9911/2026-2027-akademik-takvim/"
    )
)

for parca in sonuc:
    print("\n--- BİLGİ PARÇASI ---")
    print(parca["metin"])

    print("\nKAYNAK BİLGİLERİ:")
    for anahtar, deger in parca["metadata"].items():
        print(f"{anahtar}: {deger}")
