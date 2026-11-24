
from indeksleme.belge_indeksle import koleksiyona_baglan


def belge_baglamini_getir(dosya_adi, limit=30):
    koleksiyon = koleksiyona_baglan()

    kayitlar = koleksiyon.get(
        where={"dosya": dosya_adi},
        include=["documents", "metadatas"]
    )

    parcalar = []

    for metin, metadata in zip(
        kayitlar["documents"],
        kayitlar["metadatas"]
    ):
        parcalar.append({
            "metin": metin,
            "dosya": metadata.get("dosya", ""),
            "baslik": metadata.get("baslik", ""),
            "sayfa": metadata.get("sayfa"),
        })

    # Sayfa ve belge içindeki sıraya göre diz.
    parcalar.sort(
        key=lambda x: (
            x["sayfa"] if isinstance(x["sayfa"], int) else 0
        )
    )

    return parcalar[:limit]
