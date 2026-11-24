
from rag.belge_baglami import belge_baglamini_getir


dosyalar = [
    "mali_kayit_islemleri.txt",
    "kayıt_belgeleri.txt"
]

for dosya in dosyalar:
    print("\n" + "=" * 65)
    print("DOSYA:", dosya)

    parcalar = belge_baglamini_getir(dosya)

    print("Bulunan parça sayısı:", len(parcalar))

    for i, parca in enumerate(parcalar, 1):
        print(f"\n--- PARÇA {i} ---")
        print(parca["metin"][:250])
