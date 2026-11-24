
from rag.vektor_db import veritabanina_baglan
from rag.embedding import metni_vektore_cevir


def belge_ara(soru, limit=5):
    """
    ChromaDB üzerinde anlamsal arama yapar.
    """

    collection = veritabanina_baglan()

    kayit_sayisi = collection.count()

    if kayit_sayisi == 0:
        return []

    # Soruyu vektöre dönüştür
    soru_vektoru = metni_vektore_cevir(soru)

    # ChromaDB üzerinde arama
    sonuc = collection.query(
        query_embeddings=[soru_vektoru],
        n_results=min(limit, kayit_sayisi),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    bulunan_belgeler = []

    for metin, metadata, uzaklik in zip(
        sonuc["documents"][0],
        sonuc["metadatas"][0],
        sonuc["distances"][0]
    ):
        bulunan_belgeler.append({
            "metin": metin,
            "dosya": (metadata or {}).get(
                "dosya", "Bilinmiyor"
            ),
            "sayfa": (metadata or {}).get(
                "sayfa", 0
            ),
            "uzaklik": uzaklik
        })

    return bulunan_belgeler
