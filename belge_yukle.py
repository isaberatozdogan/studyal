
from pathlib import Path
from pypdf import PdfReader
from docx import Document
import chromadb
import ollama

BASE_DIR = Path(__file__).resolve().parent
BELGE_KLASORU = BASE_DIR / "belgeler"
VERITABANI = BASE_DIR / "veritabani"

BELGE_KLASORU.mkdir(exist_ok=True)
VERITABANI.mkdir(exist_ok=True)

client = chromadb.PersistentClient(path=str(VERITABANI))

collection = client.get_or_create_collection(
    name="studyal_belgeler",
    metadata={"hnsw:space": "cosine"}
)


def parcalara_ayir(metin, boyut=900, ortusme=150):
    parcalar = []
    baslangic = 0

    while baslangic < len(metin):
        bitis = min(baslangic + boyut, len(metin))
        parca = metin[baslangic:bitis].strip()

        if parca:
            parcalar.append(parca)

        if bitis == len(metin):
            break

        baslangic = bitis - ortusme

    return parcalar



def belgeyi_oku(dosya):
    bolumler = []
    uzanti = dosya.suffix.lower()

    if uzanti == ".pdf":
        reader = PdfReader(str(dosya))

        for sayfa_no, sayfa in enumerate(reader.pages, 1):
            metin = sayfa.extract_text() or ""

            if metin.strip():
                bolumler.append((sayfa_no, metin))

    elif uzanti == ".docx":
        doc = Document(str(dosya))

        metinler = [
            p.text for p in doc.paragraphs
            if p.text.strip()
        ]

        for tablo in doc.tables:
            for satir in tablo.rows:
                metinler.append(
                    " | ".join(
                        hucre.text for hucre in satir.cells
                    )
                )

        metin = "\n".join(metinler)

        if metin.strip():
            bolumler.append((0, metin))

    elif uzanti in {".txt", ".md"}:
        try:
            metin = dosya.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            metin = dosya.read_text(encoding="cp1254")

        if metin.strip():
            bolumler.append((0, metin))

    return bolumler



def main():
    dosyalar = sorted(
        dosya for dosya in BELGE_KLASORU.iterdir()
        if dosya.suffix.lower() in {".pdf", ".docx", ".txt", ".md"}
    )

    if not dosyalar:
        print("Belgeler klasöründe PDF veya DOCX bulunamadı.")
        return

    # Bu ilk sürümde veritabanını yeniden oluşturuyoruz.
    # Böylece silinen veya güncellenen dosyalar da yansır.
    mevcut = collection.get(include=[])
    if mevcut["ids"]:
        collection.delete(ids=mevcut["ids"])

    toplam = 0

    for dosya in dosyalar:
        print(f"İşleniyor: {dosya.name}")

        for sayfa_no, metin in belgeyi_oku(dosya):
            for sira, parca in enumerate(parcalara_ayir(metin)):
                sonuc = ollama.embed(
                    model="embeddinggemma:latest",
                    input=parca
                )

                collection.add(
                    ids=[f"{dosya.name}:{sayfa_no}:{sira}"],
                    documents=[parca],
                    embeddings=[sonuc["embeddings"][0]],
                    metadatas=[{
                        "dosya": dosya.name,
                        "sayfa": sayfa_no
                    }]
                )

                toplam += 1

    print(f"\nTamamlandı! {toplam} belge parçası kaydedildi.")
    print(f"Veritabanı konumu: {VERITABANI}")


if __name__ == "__main__":
    main()

