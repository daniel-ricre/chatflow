from app.database import engine, Base
from app.models import Conversation

# Eliminar la tabla conversations
Conversation.__table__.drop(engine, checkfirst=True)
print("Tabla 'conversations' eliminada.")

# Volver a crearla con la nueva estructura (incluye session_id)
Base.metadata.create_all(bind=engine)
print("Tabla 'conversations' recreada con la columna session_id.")
