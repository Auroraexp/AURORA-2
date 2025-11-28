import { useState } from 'react'

export default function Home() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const runSolver = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/proxy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          kre: 405.223485661,
          os: 56.12332211,
          aurelia: 500.000555112233,
          modifiers: { alpha: 1.1, beta: 0.9, eta: 1.02 }
        })
      })
      const data = await res.json()
      setResult(data.AURORA2_output)
    } catch (e) {
      setResult('Error: ' + e.message)
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: 40, fontFamily: 'Inter, sans-serif' }}>
      <h1>AURORA-2 MVP Demo</h1>
      <p>Click the button to run the solver (demo inputs prefilled).</p>
      <button onClick={runSolver} disabled={loading} style={{ padding: '10px 20px', fontSize: 16 }}>
        {loading ? 'Running...' : 'Run Solver'}
      </button>
      {result && (
        <div style={{ marginTop: 20 }}>
          <strong>Result:</strong> {result}
        </div>
      )}
      <p style={{ marginTop: 24, color: '#666' }}>Backend proxy is configured in Next.js API route.</p>
    </div>
  )
}
