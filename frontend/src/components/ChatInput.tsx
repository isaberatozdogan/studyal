
import { useState } from 'react'

import {
  ArrowUp,
  Database,
  LoaderCircle
} from 'lucide-react'

interface Props {
  mesajGonder: (soru: string) => void
  yukleniyor: boolean
}

export default function ChatInput(props: Props) {

  const [soru, setSoru] = useState('')

  function gonder() {

    if (!soru.trim() || props.yukleniyor) return

    props.mesajGonder(soru.trim())

    setSoru('')
  }

  return (
    <div className="composer-container">

      <div className="chat-composer">

        <textarea
          value={soru}
          placeholder="StudyAL'a bir soru sorun..."
          onChange={e => setSoru(e.target.value)}
          rows={2}
          onKeyDown={e => {

            if (
              e.key === 'Enter' &&
              !e.shiftKey &&
              !e.nativeEvent.isComposing
            ) {
              e.preventDefault()
              gonder()
            }

          }}
        />

        <div className="composer-bottom">

          <div className="knowledge-label">
            <Database size={16} />
            Üniversite Bilgi Tabanı
          </div>

          <button
            className="send-button"
            onClick={gonder}
            disabled={!soru.trim() || props.yukleniyor}
            title="Soruyu gönder"
          >
            {props.yukleniyor
              ? <LoaderCircle className="spin" size={21} />
              : <ArrowUp size={22} />}
          </button>

        </div>

      </div>

      <div className="composer-disclaimer">
        StudyAL AI · Üniversite belgeleriyle desteklenen
        cevaplar. Önemli bilgileri resmi kaynaklardan doğrulayın.
      </div>

    </div>
  )
}
