
from pathlib import Path

from veri_toplama.belge_okuyucu import belge_oku
from belge_isleme.chunking import metni_parcala
from belge_isleme.metadata import parcalara_metadata_ekle


def belgeyi_hazirla(dosya_yolu):
    dosya = Path(dosya_yolu)

    if not dosya.is_file():
        raise FileNotFoundError(
            f"Belge bulunamadı: {dosya}"
        )

    tum_parcalar = []

    bolumler = belge_oku(dosya)

    for bolum in bolumler:
        metin = bolum["metin"]

        if not metin.strip():
            continue

        parcalar = metni_parcala(metin)

        parcalar = parcalara_metadata_ekle(
            parcalar=parcalar,
            dosya=dosya.name,
            sayfa=bolum.get("sayfa")
        )

        tum_parcalar.extend(parcalar)

    return tum_parcalar
