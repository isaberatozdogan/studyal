
import {
  Sparkles,
  CalendarDays,
  GraduationCap,
  Wallet,
  BookOpen,
  ArrowUpRight,
  MessageCircle
} from 'lucide-react'

import { motion } from 'motion/react'

interface Props {
  soruSor: (soru: string) => void
}

const kartlar = [
  {
    icon: CalendarDays,
    baslik: 'Akademik Takvim',
    aciklama: 'Ders kayıtları, sınavlar ve önemli tarihler.',
    renk: 'blue',
    soru: 'Akademik takvimdeki önemli tarihler nelerdir?'
  },
  {
    icon: GraduationCap,
    baslik: 'Kayıt İşlemleri',
    aciklama: 'Başvuru süreçleri ve gerekli belgeler.',
    renk: 'purple',
    soru: 'Üniversiteye kayıt için gerekli belgeler nelerdir?'
  },
  {
    icon: Wallet,
    baslik: 'Mali İşlemler',
    aciklama: 'Eğitim ücretleri ve ödeme yöntemleri.',
    renk: 'green',
    soru: 'Üniversite ücretini nasıl ödeyebilirim?'
  },
  {
    icon: BookOpen,
    baslik: 'Öğrenci Rehberi',
    aciklama: 'Üniversite yaşamı ve öğrenci hizmetleri.',
    renk: 'orange',
    soru: 'Üniversitedeki öğrenci hizmetleri nelerdir?'
  }
]

const oneriler = [
  'Güz dönemi ders kayıtları ne zaman?',
  'Kayıt için hangi belgeler gerekli?',
  'Mali kayıt işlemleri nasıl yapılır?'
]

export default function WelcomeScreen({ soruSor }: Props) {

  return (
    <motion.section
      className="welcome-screen"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >

      <div className="welcome-hero">

        <div className="hero-glow">
          <Sparkles size={43} />
        </div>

        <div className="hero-label">
          STUDYAL INTELLIGENCE
        </div>

        <h1>
          Üniversite hayatında
          <span> yanında.</span>
        </h1>

        <p>
          Akademik ve idari bilgilere yapay zekâ
          desteğiyle tek noktadan ulaş.
        </p>

      </div>

      <div className="feature-grid">

        {kartlar.map((kart, index) => (

          <motion.button
            key={kart.baslik}
            className={`feature-card ${kart.renk}`}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.08 }}
            whileHover={{ y: -4 }}
            onClick={() => soruSor(kart.soru)}
          >

            <div className="feature-icon">
              <kart.icon size={25} />
            </div>

            <h3>{kart.baslik}</h3>

            <p>{kart.aciklama}</p>

            <ArrowUpRight
              size={18}
              className="feature-arrow"
            />

          </motion.button>

        ))}

      </div>

      <div className="suggestions">

        <div className="menu-label">
          ÖNERİLEN SORULAR
        </div>

        {oneriler.map(soru => (

          <button
            key={soru}
            className="suggestion-button"
            onClick={() => soruSor(soru)}
          >
            <MessageCircle size={17} />
            <span>{soru}</span>
            <ArrowUpRight size={15} />
          </button>

        ))}

      </div>

    </motion.section>
  )
}
