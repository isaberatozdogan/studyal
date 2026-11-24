
import re

from rank_bm25 import BM25Okapi

from indeksleme.belge_indeksle import koleksiyona_baglan
from rag.arama_v2 import belge_ara_v2


def kelimelere_ayir(metin):
    """Türkçe karakterleri koruyarak metni kelimelere ayırır."""
    return re.findall(
        r"[a-zçğıöşü0-9]+",
        metin.lower()
    )


def tum_kayitlari_getir():
    """Yeni ChromaDB koleksiyonundaki kayıtları getirir."""
    collection = koleksiyona_baglan()

    kayitlar = collection.get(
        include=["documents", "metadatas"]
    )

    sonuc = []

    for kimlik, metin, metadata in zip(
        kayitlar["ids"],
        kayitlar["documents"],
        kayitlar["metadatas"]
    ):
        sonuc.append({
            "id": kimlik,
            "metin": metin,
            "dosya": metadata.get("dosya", "Bilinmiyor"),
            "baslik": metadata.get("baslik", "Genel"),
            "sayfa": metadata.get("sayfa")
        })

    return sonuc


def bm25_ara(soru, limit=20):
    """Tüm indekslenmiş parçalarda BM25 araması yapar."""
    kayitlar = tum_kayitlari_getir()

    if not kayitlar:
        return []

    tokenlar = [
        kelimelere_ayir(
            kayit["metin"] + " " + kayit["dosya"]
        )
        for kayit in kayitlar
    ]

    bm25 = BM25Okapi(tokenlar)

    puanlar = bm25.get_scores(
        kelimelere_ayir(soru)
    )

    sirali_indeksler = sorted(
        range(len(kayitlar)),
        key=lambda i: puanlar[i],
        reverse=True
    )

    sonuclar = []

    for i in sirali_indeksler[:limit]:
        if puanlar[i] <= 0:
            continue

        kayit = dict(kayitlar[i])
        kayit["bm25_puani"] = float(puanlar[i])

        sonuclar.append(kayit)

    return sonuclar


def hibrit_ara(soru, limit=5, aday_sayisi=30):
    """Anlamsal arama ve BM25 sonuçlarını RRF ile birleştirir."""
    collection = koleksiyona_baglan()

    if collection.count() == 0:
        return []

    # Anlamsal arama
    soru_vektoru_sonuclari = belge_ara_v2(
        soru,
        limit=aday_sayisi
    )

    # Anlamsal sonuçlarda kimlik bulunmadığından,
    # burada ChromaDB'den kimlikleriyle tekrar alıyoruz.
    from rag.embedding import metni_vektore_cevir

    anlamsal_ham = collection.query(
        query_embeddings=[
            metni_vektore_cevir(soru)
        ],
        n_results=min(aday_sayisi, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    anlamsal = []

    for kimlik, metin, metadata, uzaklik in zip(
        anlamsal_ham["ids"][0],
        anlamsal_ham["documents"][0],
        anlamsal_ham["metadatas"][0],
        anlamsal_ham["distances"][0]
    ):
        anlamsal.append({
            "id": kimlik,
            "metin": metin,
            "dosya": metadata.get("dosya", "Bilinmiyor"),
            "baslik": metadata.get("baslik", "Genel"),
            "sayfa": metadata.get("sayfa"),
            "uzaklik": uzaklik
        })

    # Anahtar kelime araması
    bm25_sonuclari = bm25_ara(
        soru,
        limit=aday_sayisi
    )

    # RRF puanlarını hesapla
    birlesik = {}
    k = 60

    for liste in [anlamsal, bm25_sonuclari]:
        for sira, sonuc in enumerate(liste, start=1):
            kimlik = sonuc["id"]

            if kimlik not in birlesik:
                birlesik[kimlik] = dict(sonuc)
                birlesik[kimlik]["rrf_puani"] = 0.0

            birlesik[kimlik]["rrf_puani"] += (
                1 / (k + sira)
            )

    siralanmis = sorted(
        birlesik.values(),
        key=lambda x: x["rrf_puani"],
        reverse=True
    )

    return siralanmis[:limit]
