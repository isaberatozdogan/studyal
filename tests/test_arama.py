
from rag.arama import belge_ara

soru = "2026-2027 güz dönemi ders kayıtları ne zaman?"

print("Soru:", soru)
print("\nChromaDB'de aranıyor...\n")

sonuclar = belge_ara(soru, limit=5)

if not sonuclar:
    print("Hiç belge bulunamadı.")

for i, belge in enumerate(sonuclar, 1):
    print(f"\n--- KAYNAK {i} ---")
    print("Dosya:", belge["dosya"])
    print("Sayfa:", belge["sayfa"])
    print("Uzaklık:", round(belge["uzaklik"], 4))
    print("Metin:", belge["metin"][:700])
