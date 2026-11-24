
from pathlib import Path

from pypdf import PdfReader
from docx import Document


def belge_oku(dosya_yolu):
    """
    PDF, DOCX, TXT ve MD belgelerini okur.

    Çıktı:
    [
        {
            "metin": "...",
            "sayfa": 1 veya None,
            "dosya": "belge.pdf"
        }
    ]
    """

    yol = Path(dosya_yolu)
    uzanti = yol.suffix.lower()
    bolumler = []

    if uzanti == ".pdf":
        pdf = PdfReader(str(yol))

        for sayfa_no, sayfa in enumerate(
            pdf.pages, start=1
        ):
            metin = sayfa.extract_text() or ""

            if metin.strip():
                bolumler.append({
                    "metin": metin,
                    "sayfa": sayfa_no,
                    "dosya": yol.name
                })

    elif uzanti == ".docx":
        belge = Document(str(yol))

        # Paragraflar
        paragraflar = [
            p.text.strip()
            for p in belge.paragraphs
            if p.text.strip()
        ]

        # Tablolar
        tablolar = []

        for tablo in belge.tables:
            satirlar = []

            for satir in tablo.rows:
                hucreler = [
                    hucre.text.strip()
                    for hucre in satir.cells
                ]
                satirlar.append(
                    " | ".join(hucreler)
                )

            tablolar.append(
                "\n".join(satirlar)
            )

        metin = "\n".join(
            paragraflar + tablolar
        )

        bolumler.append({
            "metin": metin,
            "sayfa": None,
            "dosya": yol.name
        })

    elif uzanti in {".txt", ".md"}:
        try:
            metin = yol.read_text(
                encoding="utf-8-sig"
            )
        except UnicodeDecodeError:
            metin = yol.read_text(
                encoding="cp1254"
            )

        bolumler.append({
            "metin": metin,
            "sayfa": None,
            "dosya": yol.name
        })

    else:
        raise ValueError(
            f"Desteklenmeyen dosya türü: {uzanti}"
        )

    return bolumler
