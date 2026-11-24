
from datetime import datetime, timezone


def metadata_olustur(
    dosya,
    baslik="Genel",
    tip="paragraf",
    sayfa=None,
    kaynak_url=None
):
    """
    Belge parçası için kaynak bilgileri oluşturur.
    ChromaDB ile uyumlu değerler döndürür.
    """

    metadata = {
        "dosya": str(dosya),
        "baslik": str(baslik),
        "tip": str(tip),
        "indeksleme_tarihi": datetime.now(
            timezone.utc
        ).isoformat()
    }

    if sayfa is not None:
        metadata["sayfa"] = int(sayfa)

    if kaynak_url:
        metadata["kaynak_url"] = str(kaynak_url)

    return metadata


def parcalara_metadata_ekle(
    parcalar,
    dosya,
    sayfa=None,
    kaynak_url=None
):
    """
    Chunking sonucundaki tüm parçalara
    kaynak bilgisi ekler.
    """

    sonuc = []

    for parca in parcalar:
        yeni_parca = dict(parca)

        yeni_parca["metadata"] = metadata_olustur(
            dosya=dosya,
            baslik=parca.get("baslik", "Genel"),
            tip=parca.get("tip", "paragraf"),
            sayfa=sayfa,
            kaynak_url=kaynak_url
        )

        sonuc.append(yeni_parca)

    return sonuc
