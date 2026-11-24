
import ollama

EMBED_MODEL = "embeddinggemma:latest"


def metni_vektore_cevir(metin):
    """
    Metni Ollama kullanarak
    embedding vektörüne dönüştürür.
    """

    sonuc = ollama.embed(
        model=EMBED_MODEL,
        input=metin
    )

    return sonuc["embeddings"][0]
