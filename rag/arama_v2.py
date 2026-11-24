
from indeksleme.belge_indeksle import koleksiyona_baglan
from rag.embedding import metni_vektore_cevir


def belge_ara_v2(soru, limit=5):
    collection = koleksiyona_baglan()

    if collection.count() == 0:
        return []

    soru_vektoru = metni_vektore_cevir(soru)

    sonuc = collection.query(
        query_embeddings=[soru_vektoru],
        n_results=min(limit, collection.count()),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    bulunanlar = []

    for metin, metadata, uzaklik in zip(
        sonuc["documents"][0],
        sonuc["metadatas"][0],
        sonuc["distances"][0]
    ):
        bulunanlar.append({
            "metin": metin,
            "dosya": metadata.get("dosya", "Bilinmiyor"),
            "baslik": metadata.get("baslik", "Genel"),
            "sayfa": metadata.get("sayfa"),
            "uzaklik": uzaklik
        })

    return bulunanlar
