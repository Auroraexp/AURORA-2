import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [x0, setX0] = useState(10)
  const [contextJson, setContextJson] = useState(JSON.stringify({I:5,E:3,C:2,A:1,S:4,eps:0.1,deltaC:1.5,Hs:0.5,El:0.3,Psir:0.8,Tn:2,Lam:1.2},null,2))
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

  const runAurora = async () => {
    setLoading(true)
    try {
      const ctx = JSON.parse(contextJson)
      const resp = await axios.post(`${API_URL}/aurora`, { x0: parseFloat(x0), context: ctx, params: {} })
      setResult(resp.data)
    } catch (e) {
      alert('Грешка: ' + (e.message || e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-semibold mb-4">AURORA-2 Demo</h1>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium">Начално състояние x0</label>
            <input value={x0} onChange={e=>setX0(e.target.value)} className="mt-1 block w-full border p-2 rounded" />

            <label className="block text-sm font-medium mt-4">Контекст (JSON)</label>
            <textarea rows={12} value={contextJson} onChange={e=>setContextJson(e.target.value)} className="mt-1 block w-full border p-2 rounded font-mono text-sm"></textarea>

            <button onClick={runAurora} className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded" disabled={loading}>{loading? 'Running...':'Run AURORA'}</button>
          </div>

          <div>
            <h2 className="text-lg font-medium">Резултат</h2>
            <pre className="mt-2 bg-gray-100 p-3 rounded text-sm">{result? JSON.stringify(result, null, 2) : 'Няма резултат още'}</pre>

            <div className="mt-4">
              <h3 className="font-medium">Инфографика (символична)</h3>
              <div className="mt-2 p-3 bg-white border rounded">
                <p>KRE — логика (силата е конфигурируема)</p>
                <p>OmniSphere — идентичност</p>
                <p>AURELIA — етика и оценка на риск</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
