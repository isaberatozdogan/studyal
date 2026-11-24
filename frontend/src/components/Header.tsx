
import {
  PanelLeftOpen,
  Sun,
  Moon,
  Sparkles
} from 'lucide-react'

interface Props {
  aktif: boolean
  koyuTema: boolean
  temaDegistir: () => void
  menuAc: () => void
}

export default function Header(props: Props) {
  return (
    <header className="top-header">

      <div className="header-left">

        <button
          className="icon-button"
          onClick={props.menuAc}
          title="Menüyü aç veya kapat"
        >
          <PanelLeftOpen size={21} />
        </button>

        <div className="header-divider" />

        <div>
          <div className="header-title">
            <Sparkles size={17} />
            StudyAL Assistant
          </div>

          <small>
            Kurumsal Yapay Zekâ Platformu
          </small>
        </div>

      </div>

      <div className="header-right">

        <div className={
          `system-status ${props.aktif ? 'online' : 'offline'}`
        }>
          <span className="status-dot" />

          {props.aktif
            ? 'API Aktif'
            : 'Bağlantı Yok'}
        </div>

        <button
          className="icon-button theme-button"
          onClick={props.temaDegistir}
          title="Temayı değiştir"
        >
          {props.koyuTema
            ? <Sun size={21} />
            : <Moon size={21} />}
        </button>

      </div>

    </header>
  )
}
