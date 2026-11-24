
import hashlib
from pathlib import Path

import chromadb

from indeksleme.belge_hazirla import belgeyi_hazirla
from rag.embedding import metni_vektore_cevir


BASE_DIR = Path(__file__).resolve().parent.parent
BELGELER_DIR = BASE_DIR / "belgeler"
DB_DIR = BASE_DIR / "veritabani"

KOLEKSIYON_ADI = "studyal_belgeler_v2"
UZANTILAR = {".pdf", ".docx", ".txt", ".md"}


def dosya_hash_hesapla(dosya):
    """Dosyanın içeriğinden SHA-256 kimliği üretir."""
    return hashlib.sha256(
        dosya.read_bytes()
    ).hexdigest()


def koleksiyona_baglan():
    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    return client.get_or_create_collection(
        name=KOLEKSIYON_ADI
    )


def belgeyi_indeksle(dosya, collection):
    dosya = Path(dosya)

    yeni_hash = dosya_hash_hesapla(dosya)

    # Dosyanın daha önce indekslenmiş
    # kayıtlarını bul.
    eski_kayitlar = collection.get(
        where={"dosya": dosya.name},
        include=["metadatas"]
    )

    eski_metadata = eski_kayitlar["metadatas"] or []

    # İçerik değişmemişse tekrar indeksleme.
    if eski_metadata and all(
        meta.get("dosya_hash") == yeni_hash
        for meta in eski_metadata
    ):
        print("Değişiklik yok:", dosya.name)
        return

    # Önce yeni parçaları hazırla.
    parcalar = belgeyi_hazirla(dosya)

    if not parcalar:
        print("UYARI: İçerik bulunamadı:", dosya.name)
        return

    ids = []
    metinler = []
    metadatalar = []
    vektorler = []

    for sira, parca in enumerate(parcalar):
        metin = parca["metin"]

        if not metin.strip():
            continue

        kimlik = hashlib.sha256(
            f"{dosya.name}:{yeni_hash}:{sira}".encode(
                "utf-8"
            )
        ).hexdigest()

        metadata = dict(parca["metadata"])
        metadata["dosya_hash"] = yeni_hash
        metadata["parca_sirasi"] = sira

        ids.append(kimlik)
        metinler.append(metin)
        metadatalar.append(metadata)
        vektorler.append(
            metni_vektore_cevir(metin)
        )

    if not ids:
        print("UYARI: Geçerli parça yok:", dosya.name)
        return

    # Önce yeni verileri kaydet.
    collection.upsert(
        ids=ids,
        documents=metinler,
        metadatas=metadatalar,
        embeddings=vektorler
    )

    # Yeni kayıtlar eklendikten sonra
    # eski sürümün kayıtlarını kaldır.
    eski_ids = [
        kayit_id
        for kayit_id in eski_kayitlar["ids"]
        if kayit_id not in set(ids)
    ]

    if eski_ids:
        collection.delete(ids=eski_ids)

    print(
        f"İndekslendi: {dosya.name} "
        f"({len(ids)} parça)"
    )


def tum_belgeleri_indeksle():
    collection = koleksiyona_baglan()

    print("Koleksiyon:", collection.name)

    for dosya in sorted(BELGELER_DIR.iterdir()):
        if (
            dosya.is_file()
            and dosya.suffix.lower() in UZANTILAR
        ):
            try:
                belgeyi_indeksle(dosya, collection)
            except Exception as hata:
                print(
                    f"HATA - {dosya.name}: {hata}"
                )

    print(
        "Toplam kayıt:",
        collection.count()
    )


if __name__ == "__main__":
    tum_belgeleri_indeksle()
