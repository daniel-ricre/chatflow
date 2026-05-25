import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import axios from 'axios'

const API = 'https://chatflow-api-oj45.onrender.com/api/v1'

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' })
  const [msg, setMsg] = useState('')
  const navigate = useNavigate()

  const handle = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post(`${API}/login`, form)
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('name', res.data.name)
      navigate('/dashboard')
    } catch (err) {
      setMsg('Credenciales inválidas')
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto', fontFamily: 'Arial' }}>
      <h2>Iniciar sesión</h2>
      <form onSubmit={handle}>
        <input placeholder="Email" onChange={e => setForm({...form, email: e.target.value})} required style={{ width: '100%', padding: 10, marginBottom: 10 }} />
        <input type="password" placeholder="Contraseña" onChange={e => setForm({...form, password: e.target.value})} required style={{ width: '100%', padding: 10, marginBottom: 10 }} />
        <button type="submit" style={{ width: '100%', padding: 12, background: '#10B981', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer' }}>Entrar</button>
      </form>
      {msg && <p style={{ marginTop: 10, color: 'red' }}>{msg}</p>}
      <p style={{ marginTop: 15 }}>¿No tienes cuenta? <Link to="/register">Regístrate gratis</Link></p>
    </div>
  )
}
