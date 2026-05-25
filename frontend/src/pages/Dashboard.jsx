import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API = 'https://chatflow-api-oj45.onrender.com/api/v1'

export default function Dashboard() {
  const [chatbots, setChatbots] = useState([])
  const [form, setForm] = useState({ name: '', welcome_message: '¡Hola! ¿En qué puedo ayudarte?', personality: 'Eres un asistente amable y profesional.' })
  const [msg, setMsg] = useState('')
  const token = localStorage.getItem('token')
  const name = localStorage.getItem('name')
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) return navigate('/login')
    axios.get(`${API}/chatbots?token=${token}`).then(r => setChatbots(r.data)).catch(() => {})
  }, [])

  const create = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post(`${API}/chatbots?token=${token}`, form)
      setMsg(`Chatbot creado. Código: ${res.data.embed}`)
      setChatbots([...chatbots, res.data])
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Error')
    }
  }

  const logout = () => { localStorage.clear(); navigate('/') }

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'Arial' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Panel de {name}</h2>
        <button onClick={logout} style={{ background: '#EF4444', color: 'white', border: 'none', padding: '8px 16px', borderRadius: 6, cursor: 'pointer' }}>Salir</button>
      </div>

      <div style={{ background: '#F3F4F6', padding: 20, borderRadius: 8, marginBottom: 20 }}>
        <h3>Crear nuevo chatbot</h3>
        <form onSubmit={create}>
          <input placeholder="Nombre del chatbot" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required style={{ width: '100%', padding: 10, marginBottom: 10 }} />
          <input placeholder="Mensaje de bienvenida" value={form.welcome_message} onChange={e => setForm({...form, welcome_message: e.target.value})} style={{ width: '100%', padding: 10, marginBottom: 10 }} />
          <textarea placeholder="Personalidad del bot" value={form.personality} onChange={e => setForm({...form, personality: e.target.value})} style={{ width: '100%', padding: 10, marginBottom: 10 }} />
          <button type="submit" style={{ width: '100%', padding: 12, background: '#4F46E5', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer' }}>Crear Chatbot</button>
        </form>
        {msg && <p style={{ marginTop: 10, fontSize: 14, color: '#555' }}>{msg}</p>}
      </div>

      <h3>Mis chatbots</h3>
      {chatbots.length === 0 && <p>No tienes chatbots aún.</p>}
      {chatbots.map(c => (
        <div key={c.id} style={{ background: 'white', border: '1px solid #E5E7EB', padding: 15, borderRadius: 8, marginBottom: 10 }}>
          <strong>{c.name}</strong>
          <p style={{ fontSize: 12, color: '#555' }}>Chats: {c.total_chats || 0}</p>
        </div>
      ))}
    </div>
  )
}
