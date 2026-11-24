
import { useState, useEffect, useRef } from 'react'
import { Sparkles, X, AlertCircle, LoaderCircle } from 'lucide-react'

import Sidebar from './components/Sidebar'
import Header from './components/Header'
import WelcomeScreen from './components/WelcomeScreen'
import ChatMessage from './components/ChatMessage'
import ChatInput from './components/ChatInput'

import { useChat } from './hooks/useChat'
import { sistemDurumu } from './services/api'

export default function App() {

  const chat = useChat()

  const [apiAktif, setApiAktif] = useState(false)

  const [menuAcik, setMenuAcik] = useState(
    window.innerWidth > 768
  )

  const [ayarlarAcik, setAyarlarAcik] = useState(false)

  const [koyuTema, setKoyuTema] = useState(
    () => localStorage.getItem('studyal_tema') !== 'light'
  )

  const mesajSonu = useRef<HTMLDivElement>(null)

  useEffect(() => {
    let aktif = true

    async function kontrolEt() {
      const durum = await sistemDurumu()
      if (aktif) setApiAktif(durum)
    }

    kontrolEt()

    const interval = window.setInterval(kontrolEt, 15000)

    return () => {
      aktif = false
      window.clearInterval(interval)
    }
  }, [])

  useEffect(() => {
    document.documentElement.setAttribute(
      'data-theme',
      koyuTema ? 'dark' : 'light'
    )

    localStorage.setItem(
      'studyal_tema',
      koyuTema ? 'dark' : 'light'
    )
  }, [koyuTema])

  useEffect(() => {
    mesajSonu.current?.scrollIntoView({
      behavior: 'smooth'
    })
  }, [chat.aktifSohbet?.mesajlar, chat.yukleniyor])

  function mobilMenuKapat() {
    if (window.innerWidth <= 768) {
      setMenuAcik(false)
    }
  }

  function soruSor(soru: string) {
    mobilMenuKapat()
    void chat.mesajGonder(soru)
  }

  function yeniSohbet() {
    chat.yeniSohbet()
    mobilMenuKapat()
  }

  return (
    <div className="app-layout">

      {menuAcik && (
        <>
          <div
            className="mobile-overlay"
            onClick={() => setMenuAcik(false)}
          />

          <Sidebar
            sohbetler={chat.sohbetler}
            aktifId={chat.aktifId}
            yeniSohbet={yeniSohbet}
            sohbetSec={id => {
              chat.setAktifId(id)
              mobilMenuKapat()
            }}
            sohbetSil={chat.sohbetSil}
            sohbetAdlandir={chat.sohbetAdlandir}
            soruSor={soruSor}
            ayarlariAc={() => setAyarlarAcik(true)}
            kapat={() => setMenuAcik(false)}
          />
        </>
      )}

      <main className="main-area">

        <Header
          aktif={apiAktif}
          koyuTema={koyuTema}
          temaDegistir={() => setKoyuTema(t => !t)}
          menuAc={() => setMenuAcik(t => !t)}
        />

        <div className="main-scroll">

          {!chat.aktifSohbet ? (

            <WelcomeScreen soruSor={soruSor} />

          ) : (

            <div className="conversation">

              {chat.aktifSohbet.mesajlar.map(mesaj => (
                <ChatMessage
                  key={mesaj.id}
                  mesaj={mesaj}
                />
              ))}

              {chat.yukleniyor && (
                <div className="thinking-message">

                  <div className="message-avatar">
                    <Sparkles size={21} />
                  </div>

                  <div>
                    <strong>StudyAL</strong>

                    <div className="thinking-text">
                      <LoaderCircle
                        size={17}
                        className="spin"
                      />
                      Üniversite belgeleri inceleniyor...
                    </div>
                  </div>

                </div>
              )}

              {chat.hata && (
                <div className="error-message">
                  <AlertCircle size={19} />
                  {chat.hata}
                </div>
              )}

              <div ref={mesajSonu} />

            </div>

          )}

        </div>

        <ChatInput
          mesajGonder={soruSor}
          yukleniyor={chat.yukleniyor}
        />

      </main>

      {ayarlarAcik && (

        <div
          className="modal-overlay"
          onClick={() => setAyarlarAcik(false)}
        >

          <section
            className="settings-modal"
            onClick={e => e.stopPropagation()}
          >

            <div className="modal-header">
              <h2>StudyAL Ayarları</h2>

              <button
                className="icon-button"
                onClick={() => setAyarlarAcik(false)}
                title="Kapat"
              >
                <X size={22} />
              </button>
            </div>

            <div className="setting-row">
              <div>
                <strong>Görünüm</strong>
                <p>Uygulama renk temasını değiştir.</p>
              </div>

              <button
                className="secondary-button"
                onClick={() => setKoyuTema(t => !t)}
              >
                {koyuTema ? 'Açık Tema' : 'Koyu Tema'}
              </button>
            </div>

            <div className="setting-row">
              <div>
                <strong>Merkezi API</strong>
                <p>StudyAL bağlantı durumu</p>
              </div>

              <span className={
                `system-status ${apiAktif ? 'online' : 'offline'}`
              }>
                {apiAktif ? 'Aktif' : 'Çevrimdışı'}
              </span>
            </div>

            <div className="setting-row">
              <div>
                <strong>Sohbet geçmişi</strong>
                <p>Tarayıcıda kayıtlı sohbet sayısı</p>
              </div>

              <span>{chat.sohbetler.length}</span>
            </div>

            <div className="setting-row">
              <div>
                <strong>Uygulama sürümü</strong>
                <p>StudyAL Intelligence Platform</p>
              </div>

              <span>v1.0</span>
            </div>

          </section>

        </div>

      )}

    </div>
  )
}
