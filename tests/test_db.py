
from rag.vektor_db import veritabanina_baglan

print("ChromaDB bağlantısı test ediliyor...")

collection = veritabanina_baglan()

print("Bağlantı başarılı!")
print("Koleksiyon:", collection.name)
print("Kayıt sayısı:", collection.count())

if collection.count() > 0:
    sonuc = collection.peek(limit=1)
    print("Örnek kayıt:", sonuc["documents"][0][:200])
else:
    print("Koleksiyon şu anda boş.")
