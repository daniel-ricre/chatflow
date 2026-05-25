import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import axios from 'axios'

const API = 'https://chatflow-api-oj45.onrender.com/api/v1'

export default function Register() {
  const [form, setForm] = useState({ email: '', password: '', company_name: '', business_type: '' })
  const [msg, setMsg] = useState('')
  const navigate = useNavigate()

  const handle = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post(`${API}/register`, form)
      setMsg(res.data.message)
      setTimeout(() => navigate('/login'), 1500)
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Error')
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto', fontFamily: 'Arial' }}>
      <h2>Registrar mi negocio</h2>
      <form onSubmit={handle}>
        <input placeholder="Email" onChange={e => setForm({...form, email: e.target.value})} required style={{ width: '100%', padding: 10, marginBottom: 10 }} />
        <input type="password" placeholder="Contraseña" onChange={e => setForm({...form, password: e.target.value})} required style={{ width: '100%', padding: 10, marginBottom: 10 }} />
        <input placeholder="Nombre del negocio" onChange={e => setForm({...form, company_name: e.target.value})} required style={{ width: '100%', padding: 10, marginBottom: 10 }} />
        <input placeholder="Tipo de negocio (ej: panadería)" onChange={e => setForm({...form, business_type: e.target.value})} required style={{ width: '100%', padding: 10, marginBottom: 10 }} />
        <button type="submit" style={{ width: '100%', padding: 12, background: '#4F46E5', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer' }}>Crear cuenta gratis</button>
      </form>
      {msg && <p style={{ marginTop: 10, color: msg.includes('Error') ? 'red' : 'green' }}>{msg}</p>}
      <p style={{ marginTop: 15 }}>¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
    </div>
  )
}
