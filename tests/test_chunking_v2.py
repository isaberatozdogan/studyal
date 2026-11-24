
from pathlib import Path

from belge_isleme.chunking import metni_parcala

dosya = Path(
    "belgeler/okan_akademik_takvim_2026_2027.txt"
)

metin = dosya.read_text(encoding="utf-8")

parcalar = metni_parcala(metin)

print("TOPLAM PARÇA:", len(parcalar))

aranan = [
    "Ders Kayıtlarının Yapılması",
    "Derslerin Başlaması"
]

for i, parca in enumerate(parcalar):
    if any(
        ifade in parca["metin"]
        for ifade in aranan
    ):
        print("\n" + "=" * 65)
        print("PARÇA:", i)
        print(
            "AKADEMİK BİRİM:",
            parca.get("akademik_birim")
        )
        print("DÖNEM:", parca.get("donem"))
        print("METİN:", parca["metin"])
