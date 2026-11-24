
import chromadb
from pathlib import Path

# StudyAL ana klasörü
BASE_DIR = Path(__file__).resolve().parent.parent

# Kalıcı veritabanı klasörü
DB_PATH = BASE_DIR / "veritabani"

# ChromaDB bağlantısı
def veritabanina_baglan():
    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    collection = client.get_or_create_collection(
        name="studyal_belgeler"
    )

    return collection
