
export interface Kaynak {
  metin: string
  dosya: string
  baslik: string
  sayfa: number | null
  puan: number
}

export interface StudyALResponse {
  durum: string
  soru: string
  cevap: {
    cevap: string
    kaynaklar: Kaynak[]
  }
}

export interface Mesaj {
  id: string
  rol: 'user' | 'assistant'
  icerik: string
  kaynaklar?: Kaynak[]
  tarih: string
}

export interface Sohbet {
  id: string
  baslik: string
  mesajlar: Mesaj[]
  tarih: string
}
