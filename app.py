
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="StudyAL",
    page_icon="🎓",
    layout="wide"
)


def sistem_durumu():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )
        return response.ok
    except requests.RequestException:
        return False


def studyal_sor(soru):
    response = requests.post(
        f"{API_URL}/soru",
        json={"soru": soru},
        timeout=300
    )

    response.raise_for_status()
    veri = response.json()

    return veri["cevap"]


def kaynaklari_goster(kaynaklar):
    if kaynaklar:
        with st.expander("📚 Kullanılan kaynaklar"):
            for i, kaynak in enumerate(kaynaklar, 1):

                st.markdown(
                    f"**Kaynak {i}: "
                    f"{kaynak.get('dosya', 'Bilinmiyor')}**"
                )

                if kaynak.get("baslik"):
                    st.caption(kaynak["baslik"])

                if kaynak.get("sayfa"):
                    st.caption(
                        f"Sayfa: {kaynak['sayfa']}"
                    )

                st.write(kaynak.get("metin", ""))
                st.divider()


if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []


with st.sidebar:

    st.title("🎓 StudyAL")

    st.caption(
        "İstanbul Okan Üniversitesi"
    )

    st.divider()

    if sistem_durumu():
        st.success("Merkezi API aktif")
    else:
        st.error("Merkezi API bağlantısı yok")

    st.markdown("### Bilgi Sistemi")

    st.write("• Akademik takvim")
    st.write("• Kayıt işlemleri")
    st.write("• Mali işlemler")
    st.write("• Üniversite belgeleri")

    st.divider()

    if st.button(
        "➕ Yeni Sohbet",
        use_container_width=True
    ):
        st.session_state.mesajlar = []
        st.rerun()

    st.caption(
        "StudyAL | Kurumsal Yapay Zekâ"
    )


st.title("🎓 StudyAL")

st.subheader(
    "Kurumsal Akıllı Öğrenci Destek Asistanı"
)

st.caption(
    "Üniversite hakkında merak ettiğiniz "
    "soruları sorabilirsiniz."
)

st.divider()


if not st.session_state.mesajlar:

    with st.chat_message("assistant"):

        st.markdown(
            "Merhaba! Ben StudyAL, üniversite "
            "öğrenci destek asistanınız.\n\n"
            "Size nasıl yardımcı olabilirim?"
        )


for mesaj in st.session_state.mesajlar:

    with st.chat_message(mesaj["rol"]):

        st.markdown(mesaj["icerik"])

        if mesaj["rol"] == "assistant":

            kaynaklari_goster(
                mesaj.get("kaynaklar", [])
            )


soru = st.chat_input(
    "StudyAL'a sorunuzu yazın..."
)


if soru and soru.strip():

    st.session_state.mesajlar.append({
        "rol": "user",
        "icerik": soru
    })

    with st.chat_message("user"):
        st.markdown(soru)

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "Üniversite belgeleri inceleniyor..."
            ):

                sonuc = studyal_sor(soru)

                cevap = sonuc["cevap"]
                kaynaklar = sonuc.get(
                    "kaynaklar", []
                )

            st.markdown(cevap)

            kaynaklari_goster(kaynaklar)

            st.session_state.mesajlar.append({
                "rol": "assistant",
                "icerik": cevap,
                "kaynaklar": kaynaklar
            })

        except requests.exceptions.Timeout:

            st.error(
                "Cevap oluşturma süresi aşıldı. "
                "Lütfen tekrar deneyin."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "StudyAL merkezi API bağlantısı "
                "kurulamadı."
            )

        except Exception as hata:

            st.error(
                f"Bir hata oluştu: {hata}"
            )
