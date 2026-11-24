
from pathlib import Path

from belge_isleme.yapi_analizi import (
    belge_yapisini_analiz_et
)

dosya = Path(
    "belgeler/okan_akademik_takvim_2026_2027.txt"
)

metin = dosya.read_text(encoding="utf-8")

bolumler = belge_yapisini_analiz_et(metin)

for i, bolum in enumerate(bolumler):
    if bolum["tip"] in (
        "baslik",
        "tablo_bolum_basligi"
    ):
        print("\n" + "=" * 60)
        print("BÖLÜM:", i)
        print("TİP:", bolum["tip"])
        print("BAŞLIK:", bolum["baslik"])
