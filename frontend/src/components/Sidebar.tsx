
import {
  Sparkles,
  Plus,
  CalendarDays,
  GraduationCap,
  Wallet,
  BookOpen,
  MessageSquare,
  Trash2,
  Settings,
  PanelLeftClose,
  Pencil
} from 'lucide-react'

import type { Sohbet } from '../types/chat'

interface Props {
  sohbetler: Sohbet[]
  aktifId: string | null
  yeniSohbet: () => void
  sohbetSec: (id: string) => void
  sohbetSil: (id: string) => void
  sohbetAdlandir: (id: string, baslik: string) => void
  soruSor: (soru: string) => void
  ayarlariAc: () => void
  kapat: () => void
}

const kategoriler = [
  {
    icon: CalendarDays,
    baslik: 'Akademik Takvim',
    soru: 'Akademik takvimdeki önemli tarihler nelerdir?'
  },
  {
    icon: GraduationCap,
    baslik: 'Kayıt İşlemleri',
    soru: 'Üniversiteye kayıt için gerekli belgeler nelerdir?'
  },
  {
    icon: Wallet,
    baslik: 'Mali İşlemler',
    soru: 'Üniversite ödeme yöntemleri nelerdir?'
  },
  {
    icon: BookOpen,
    baslik: 'Öğrenci Rehberi',
    soru: 'Üniversitenin öğrenci hizmetleri nelerdir?'
  }
]

export default function Sidebar(props: Props) {
  return (
    <aside className="sidebar">

      <div className="sidebar-brand">
        <div className="brand-icon">
          <Sparkles size={25} />
        </div>

        <div>
          <h1>Study<span>AL</span></h1>
          <small>AI Intelligence Platform</small>
        </div>

        <button
          className="icon-button sidebar-close"
          onClick={props.kapat}
          title="Menüyü kapat"
        >
          <PanelLeftClose size={18} />
        </button>
      </div>

      <button
        className="new-chat-button"
        onClick={props.yeniSohbet}
      >
        <Plus size={20} />
        Yeni Sohbet
      </button>

      <div className="menu-label">
        ÇALIŞMA ALANI
      </div>

      <button
        className="nav-item active"
        onClick={props.yeniSohbet}
      >
        <Sparkles size={19} />
        AI Asistan
      </button>

      {kategoriler.map(kategori => (
        <button
          key={kategori.baslik}
          className="nav-item"
          onClick={() => props.soruSor(kategori.soru)}
        >
          <kategori.icon size={19} />
          {kategori.baslik}
        </button>
      ))}

      <div className="menu-label history-label">
        SOHBET GEÇMİŞİ
      </div>

      <div className="chat-history">

        {props.sohbetler.length === 0 && (
          <p className="empty-history">
            Henüz sohbet bulunmuyor.
          </p>
        )}

        {props.sohbetler.map(sohbet => (
          <div
            key={sohbet.id}
            className={`history-item ${
              props.aktifId === sohbet.id
                ? 'selected'
                : ''
            }`}
          >
            <button
              className="history-title"
              onClick={() => props.sohbetSec(sohbet.id)}
            >
              <MessageSquare size={16} />
              <span>{sohbet.baslik}</span>
            </button>

            <button
              className="icon-button"
              title="Yeniden adlandır"
              onClick={() => {
                const baslik = window.prompt(
                  'Sohbet başlığı',
                  sohbet.baslik
                )

                if (baslik?.trim()) {
                  props.sohbetAdlandir(
                    sohbet.id,
                    baslik.trim()
                  )
                }
              }}
            >
              <Pencil size={14} />
            </button>

            <button
              className="icon-button delete-button"
              title="Sohbeti sil"
              onClick={() => {
                if (window.confirm('Sohbet silinsin mi?')) {
                  props.sohbetSil(sohbet.id)
                }
              }}
            >
              <Trash2 size={15} />
            </button>
          </div>
        ))}
      </div>

      <div className="sidebar-footer">

        <button
          className="nav-item"
          onClick={props.ayarlariAc}
        >
          <Settings size={19} />
          Ayarlar
        </button>

        <div className="university-profile">
          <div className="profile-avatar">O</div>
          <div>
            <strong>İstanbul Okan Üniversitesi</strong>
            <small>Öğrenci Destek Sistemi</small>
          </div>
        </div>

        <div className="version-text">
          StudyAL v1.0
        </div>

      </div>
    </aside>
  )
}
