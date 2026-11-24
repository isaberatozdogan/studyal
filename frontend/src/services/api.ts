
import axios from 'axios'
import type { StudyALResponse } from '../types/chat'

const api = axios.create({
  baseURL: '/api',
  timeout: 300000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export async function studyalSor(
  soru: string
): Promise<StudyALResponse> {

  const response = await api.post<StudyALResponse>(
    '/soru',
    { soru }
  )

  return response.data
}

export async function sistemDurumu(): Promise<boolean> {

  try {
    const response = await api.get('/health', {
      timeout: 5000
    })

    return response.data.api === 'aktif'

  } catch {
    return false
  }
}
