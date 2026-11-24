
import { useState, useEffect } from 'react'
import type { Sohbet, Mesaj } from '../types/chat'
import { studyalSor } from '../services/api'

const STORAGE_KEY = 'studyal_sohbetler'

function sohbetleriYukle(): Sohbet[] {
  try {
    return JSON.parse(
      localStorage.getItem(STORAGE_KEY) || '[]'
    )
  } catch {
    return []
  }
}

export function useChat() {

  const [sohbetler, setSohbetler] =
    useState<Sohbet[]>(sohbetleriYukle)

  const [aktifId, setAktifId] =
    useState<string | null>(null)

  const [yukleniyor, setYukleniyor] =
    useState(false)

  const [hata, setHata] =
    useState<string | null>(null)

  const aktifSohbet = sohbetler.find(
    s => s.id === aktifId
  )

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(sohbetler)
    )
  }, [sohbetler])

  function yeniSohbet() {
    setAktifId(null)
    setHata(null)
  }

  function sohbetSil(id: string) {
    setSohbetler(eski =>
      eski.filter(s => s.id !== id)
    )

    if (aktifId === id) {
      setAktifId(null)
    }
  }

  function sohbetAdlandir(id: string, baslik: string) {
    setSohbetler(eski =>
      eski.map(s =>
        s.id === id ? { ...s, baslik } : s
      )
    )
  }

  async function mesajGonder(soru: string) {

    if (!soru.trim() || yukleniyor) return

    setYukleniyor(true)
    setHata(null)

    const sohbetId =
      aktifSohbet?.id || crypto.randomUUID()

    const kullaniciMesaji: Mesaj = {
      id: crypto.randomUUID(),
      rol: 'user',
      icerik: soru.trim(),
      tarih: new Date().toISOString()
    }

    setSohbetler(eski => {

      const mevcut = eski.find(
        s => s.id === sohbetId
      )

      if (!mevcut) {
        return [{
          id: sohbetId,
          baslik: soru.trim().slice(0, 45),
          mesajlar: [kullaniciMesaji],
          tarih: new Date().toISOString()
        }, ...eski]
      }

      return eski.map(s =>
        s.id === sohbetId
          ? {
              ...s,
              mesajlar: [
                ...s.mesajlar,
                kullaniciMesaji
              ]
            }
          : s
      )
    })

    setAktifId(sohbetId)

    try {

      const sonuc = await studyalSor(soru.trim())

      if (sonuc.durum !== 'basarili') {
        throw new Error('API cevap oluşturamadı.')
      }

      const asistanMesaji: Mesaj = {
        id: crypto.randomUUID(),
        rol: 'assistant',
        icerik: sonuc.cevap.cevap,
        kaynaklar: sonuc.cevap.kaynaklar,
        tarih: new Date().toISOString()
      }

      setSohbetler(eski =>
        eski.map(s =>
          s.id === sohbetId
            ? {
                ...s,
                mesajlar: [
                  ...s.mesajlar,
                  asistanMesaji
                ]
              }
            : s
        )
      )

    } catch {
      setHata(
        'StudyAL cevap oluşturamadı. API bağlantısını kontrol edin.'
      )
    } finally {
      setYukleniyor(false)
    }
  }

  return {
    sohbetler,
    aktifSohbet,
    aktifId,
    setAktifId,
    yeniSohbet,
    sohbetSil,
    sohbetAdlandir,
    mesajGonder,
    yukleniyor,
    hata
  }
}
