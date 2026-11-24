
from pathlib import Path
from indeksleme.belge_hazirla import belgeyi_hazirla

BASE_DIR = Path(__file__).resolve().parent

dosya = BASE_DIR / "belgeler" / "kayıt_belgeleri.txt"

parcalar = belgeyi_hazirla(dosya)

print("Hazırlanan parça sayısı:", len(parcalar))

for parca in parcalar[:3]:
    print("\n--- PARÇA ---")
    print(parca["metin"])
    print("Metadata:", parca["metadata"])
