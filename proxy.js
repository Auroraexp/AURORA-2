// Proxy route to backend (useful for Vercel to avoid CORS)
export default async function handler(req, res) {
  const payload = req.body
  const BACKEND_URL = process.env.AURORA_BACKEND_URL || 'http://localhost:8000'
  try {
    const r = await fetch(BACKEND_URL + '/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await r.json()
    res.status(200).json(data)
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
}
