import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API = 'https://chatflow-api-oj45.onrender.com/api/v1'

export default function Dashboard() {
  const [chatbots, setChatbots] = useState([])
  const [form, setForm] = useState({ name: '', welcome_message: '¡Hola! ¿En qué puedo ayudarte?', personality: 'Eres un asistente amable y profesional.' })
  const [msg, setMsg] = useState('')
  const [activeChat, setActiveChat] = useState(null)
  const [chatInput, setChatInput] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [chatLoading, setChatLoading] = useState(false)
  const chatEndRef = useRef(null)
  const token = localStorage.getItem('token')
  const name = localStorage.getItem('name')
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) return navigate('/login')
    axios.get(`${API}/chatbots?token=${token}`).then(r => setChatbots(r.data)).catch(() => {})
  }, [])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatHistory])

  const create = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post(`${API}/chatbots?token=${token}`, form)
      setMsg(`Chatbot creado. Código: ${res.data.embed}`)
      setChatbots([...chatbots, res.data])
      setForm({ name: '', welcome_message: '¡Hola! ¿En qué puedo ayudarte?', personality: 'Eres un asistente amable y profesional.' })
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Error')
    }
  }

  const sendMessage = async () => {
    if (!chatInput.trim() || !activeChat) return
    const userMsg = chatInput
    setChatHistory([...chatHistory, { role: 'user', text: userMsg }])
    setChatInput('')
    setChatLoading(true)
    try {
      const res = await axios.post(`${API}/chat`, { chatbot_id: activeChat.id, message: userMsg })
      setChatHistory(prev => [...prev, { role: 'bot', text: res.data.response }])
    } catch (err) {
      setChatHistory(prev => [...prev, { role: 'bot', text: 'Error al responder.' }])
    }
    setChatLoading(false)
  }

  const logout = () => { localStorage.clear(); navigate('/') }

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', fontFamily: 'Arial', padding: 20 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h2>Panel de {name}</h2>
        <button onClick={logout} style={{ background: '#EF4444', color: 'white', border: 'none', padding: '8px 16px', borderRadius: 6, cursor: 'pointer' }}>Salir</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Columna izquierda: crear + lista */}
        <div>
          <div style={{ background: '#F3F4F6', padding: 20, borderRadius: 8, marginBottom: 20 }}>
            <h3>Crear nuevo chatbot</h3>
            <form onSubmit={create}>
              <input placeholder="Nombre del chatbot" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required style={{ width: '100%', padding: 10, marginBottom: 10, border: '1px solid #ddd', borderRadius: 4 }} />
              <input placeholder="Mensaje de bienvenida" value={form.welcome_message} onChange={e => setForm({...form, welcome_message: e.target.value})} style={{ width: '100%', padding: 10, marginBottom: 10, border: '1px solid #ddd', borderRadius: 4 }} />
              <textarea placeholder="Personalidad del bot" value={form.personality} onChange={e => setForm({...form, personality: e.target.value})} style={{ width: '100%', padding: 10, marginBottom: 10, border: '1px solid #ddd', borderRadius: 4 }} />
              <button type="submit" style={{ width: '100%', padding: 12, background: '#4F46E5', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer' }}>Crear Chatbot</button>
            </form>
            {msg && <p style={{ marginTop: 10, fontSize: 14, color: '#555' }}>{msg}</p>}
          </div>

          <h3>Mis chatbots</h3>
          {chatbots.map(c => (
            <div key={c.id} onClick={() => { setActiveChat(c); setChatHistory([]) }}
              style={{ background: activeChat?.id === c.id ? '#EEF2FF' : 'white', border: '1px solid #E5E7EB', padding: 15, borderRadius: 8, marginBottom: 10, cursor: 'pointer' }}>
              <strong>{c.name}</strong>
              <p style={{ fontSize: 12, color: '#555' }}>Chats: {c.total_chats || 0}</p>
            </div>
          ))}
        </div>

        {/* Columna derecha: chat en vivo */}
        <div style={{ background: 'white', border: '1px solid #E5E7EB', borderRadius: 8, display: 'flex', flexDirection: 'column', height: 500 }}>
          <div style={{ background: '#4F46E5', color: 'white', padding: 15, borderRadius: '8px 8px 0 0' }}>
            <strong>{activeChat ? activeChat.name : 'Selecciona un chatbot'}</strong>
          </div>
          <div style={{ flex: 1, overflow: 'auto', padding: 15, background: '#F9FAFB' }}>
            {!activeChat && <p style={{ color: '#999', textAlign: 'center', marginTop: 100 }}>Selecciona un chatbot de la izquierda para probarlo</p>}
            {chatHistory.map((m, i) => (
              <div key={i} style={{ marginBottom: 10, textAlign: m.role === 'user' ? 'right' : 'left' }}>
                <span style={{ background: m.role === 'user' ? '#4F46E5' : '#E5E7EB', color: m.role === 'user' ? 'white' : '#333', padding: '8px 14px', borderRadius: 12, display: 'inline-block', maxWidth: '80%', fontSize: 14 }}>
                  {m.text}
                </span>
              </div>
            ))}
            {chatLoading && <p style={{ color: '#999', fontSize: 12 }}>Escribiendo...</p>}
            <div ref={chatEndRef} />
          </div>
          {activeChat && (
            <div style={{ display: 'flex', padding: 10, borderTop: '1px solid #E5E7EB' }}>
              <input value={chatInput} onChange={e => setChatInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendMessage()}
                placeholder="Escribe un mensaje..." style={{ flex: 1, padding: 10, border: '1px solid #ddd', borderRadius: 4 }} />
              <button onClick={sendMessage} style={{ marginLeft: 10, padding: '10px 20px', background: '#4F46E5', color: 'white', border: 'none', borderRadius: 4, cursor: 'pointer' }}>Enviar</button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
