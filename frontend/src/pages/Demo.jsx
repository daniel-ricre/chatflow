import { useEffect } from 'react'

export default function Demo() {
  useEffect(() => {
    // Cargar el widget al entrar en la página
    const script = document.createElement('script')
    script.src = '/widget.js'
    script.setAttribute('data-chatbot', '1')
    document.body.appendChild(script)
    return () => {
      document.body.removeChild(script)
    }
  }, [])

  return (
    <div style={{ fontFamily: 'Arial', background: '#f5f5f5', minHeight: '100vh' }}>
      <header style={{ background: '#4F46E5', color: 'white', padding: '2rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2rem' }}>🍞 Pan Caliente</h1>
        <p>El mejor pan de la ciudad</p>
      </header>
      <div style={{ maxWidth: 800, margin: '2rem auto', padding: '1rem' }}>
        <div style={{ background: 'white', borderRadius: 8, padding: '2rem', marginBottom: '1rem', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h2 style={{ color: '#4F46E5' }}>Nuestros productos</h2>
          <p>Pan fresco, pasteles, dulces y café. Todos los días de 7am a 7pm.</p>
        </div>
        <div style={{ background: 'white', borderRadius: 8, padding: '2rem', marginBottom: '1rem', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h2 style={{ color: '#4F46E5' }}>Contacto</h2>
          <p>📞 +53 5 1234567</p>
          <p>📍 Calle Principal #123, La Habana</p>
        </div>
      </div>
      <footer style={{ background: '#1F2937', color: 'white', textAlign: 'center', padding: '1rem', marginTop: '2rem' }}>
        <p>© 2026 Pan Caliente - Powered by <strong>ChatFlow AI</strong></p>
      </footer>
    </div>
  )
}
