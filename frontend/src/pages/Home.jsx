import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div style={{ textAlign: 'center', padding: '4rem 1rem', fontFamily: 'Arial' }}>
      <h1 style={{ fontSize: '2.5rem', color: '#4F46E5' }}>ChatFlow AI</h1>
      <p style={{ fontSize: '1.2rem', color: '#555', marginBottom: '2rem' }}>
        Crea un chatbot con IA para tu negocio en 2 minutos.
      </p>
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
        <Link to="/register" style={{ background: '#4F46E5', color: 'white', padding: '12px 24px', borderRadius: '8px', textDecoration: 'none' }}>
          Comenzar gratis
        </Link>
        <Link to="/login" style={{ background: '#10B981', color: 'white', padding: '12px 24px', borderRadius: '8px', textDecoration: 'none' }}>
          Iniciar sesión
        </Link>
      </div>
    </div>
  )
}
