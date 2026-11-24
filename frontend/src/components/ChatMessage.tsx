
import { useState } from 'react'

import {
  Sparkles,
  UserRound,
  Copy,
  Check,
  BookOpen,
  ChevronDown,
  FileText
} from 'lucide-react'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

import type { Mesaj } from '../types/chat'

export default function ChatMessage(
  { mesaj }: { mesaj: Mesaj }
) {

  const [kopyalandi, setKopyalandi] = useState(false)
  const [kaynakAcik, setKaynakAcik] = useState(false)

  const asistan = mesaj.rol === 'assistant'

  async function kopyala() {
    try {
      await navigator.clipboard.writeText(mesaj.icerik)

      setKopyalandi(true)

      setTimeout(() => {
        setKopyalandi(false)
      }, 1800)
    } catch {
      window.alert('Mesaj kopyalanamadı.')
    }
  }

  return (
    <article className={
      `message-row ${asistan ? 'assistant' : 'user'}`
    }>

      <div className="message-avatar">
        {asistan
          ? <Sparkles size={21} />
          : <UserRound size={21} />}
      </div>

      <div className="message-body">

        <div className="message-author">
          {asistan ? 'StudyAL' : 'Sen'}

          <span>
            {new Date(mesaj.tarih).toLocaleTimeString(
              'tr-TR',
              {
                hour: '2-digit',
                minute: '2-digit'
              }
            )}
          </span>
        </div>

        <div className="message-content">

          {asistan ? (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {mesaj.icerik}
            </ReactMarkdown>
          ) : (
            <p>{mesaj.icerik}</p>
          )}

        </div>

        {asistan && (
          <div className="message-actions">

            <button
              className="icon-button"
              onClick={kopyala}
              title="Cevabı kopyala"
            >
              {kopyalandi
                ? <Check size={17} />
                : <Copy size={17} />}
            </button>

          </div>
        )}

        {asistan && !!mesaj.kaynaklar?.length && (

          <div className="sources-panel">

            <button
              className="sources-toggle"
              onClick={() => setKaynakAcik(!kaynakAcik)}
            >

              <BookOpen size={18} />

              <span>
                Kullanılan Kaynaklar
              </span>

              <span className="source-count">
                {mesaj.kaynaklar.length}
              </span>

              <ChevronDown
                size={17}
                style={{
                  transform: kaynakAcik
                    ? 'rotate(180deg)'
                    : 'none'
                }}
              />

            </button>

            {kaynakAcik && (

              <div className="sources-list">

                {mesaj.kaynaklar.map((kaynak, i) => (

                  <details
                    className="source-card"
                    key={i}
                  >

                    <summary>
                      <FileText size={19} />

                      <div>
                        <strong>
                          Kaynak {i + 1}
                        </strong>

                        <small>{kaynak.dosya}</small>
                      </div>
                    </summary>

                    <h4>{kaynak.baslik}</h4>

                    {kaynak.sayfa !== null && (
                      <small>Sayfa: {kaynak.sayfa}</small>
                    )}

                    <p>{kaynak.metin}</p>

                  </details>

                ))}

              </div>

            )}

          </div>

        )}

      </div>

    </article>
  )
}
