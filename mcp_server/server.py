
from mcp.server.mcpserver import MCPServer
import requests

mcp = MCPServer("StudyAL")

API_URL = "http://127.0.0.1:8000"


@mcp.tool()
def universiteye_sor(soru: str) -> dict:
    """
    İstanbul Okan Üniversitesi hakkında merkezi
    StudyAL bilgi sisteminden cevap alır.
    """

    try:
        response = requests.post(
            f"{API_URL}/soru",
            json={"soru": soru},
            timeout=300
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as hata:
        return {
            "durum": "hata",
            "mesaj": str(hata)
        }


@mcp.tool()
def sistem_durumu() -> dict:
    """
    StudyAL API bağlantısını kontrol eder.
    """

    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as hata:
        return {
            "durum": "hata",
            "mesaj": str(hata)
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")
