
from rag.embedding import metni_vektore_cevir

soru = "2026-2027 güz dönemi ders kayıtları ne zaman?"

print("Embedding oluşturuluyor...")

vektor = metni_vektore_cevir(soru)

print("Embedding başarılı!")
print("Vektör boyutu:", len(vektor))
print("İlk 5 değer:", vektor[:5])
