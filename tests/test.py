
import ollama

print("StudyAL Ollama bağlantısı test ediliyor...")

try:
    response = ollama.chat(
        model="qwen3.5:4b",
        messages=[
            {
                "role": "user",
                "content": "Merhaba! StudyAL nedir? Kısaca Türkçe cevap ver."
            }
        ]
    )

    print("\nYapay zekâ cevabı:")
    print(response["message"]["content"])

except Exception as error:
    print("Bağlantı hatası:", error)
