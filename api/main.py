
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag.cevap_uret import cevap_uret


app = FastAPI(
    title="StudyAL API",
    description="Üniversite Yapay Zekâ Bilgi Sistemi",
    version="1.0.0"
)


class SoruModel(BaseModel):
    soru: str = Field(min_length=1)


@app.get("/")
def ana_sayfa():
    return {
        "sistem": "StudyAL",
        "durum": "aktif",
        "versiyon": "1.0.0"
    }


@app.get("/health")
def sistem_durumu():
    return {
        "api": "aktif"
    }


@app.post("/soru")
def soru_cevapla(veri: SoruModel):

    soru = veri.soru.strip()

    if not soru:
        raise HTTPException(
            status_code=400,
            detail="Soru boş olamaz."
        )

    try:
        cevap = cevap_uret(soru)

        return {
            "durum": "basarili",
            "soru": soru,
            "cevap": cevap
        }

    except Exception as hata:
        print(f"StudyAL API hatası: {hata}")

        raise HTTPException(
            status_code=500,
            detail="Cevap oluşturulamadı."
        )

