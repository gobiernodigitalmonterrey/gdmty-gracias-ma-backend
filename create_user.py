from app.db.database import SessionLocal
from app.db.models import User
from sqlalchemy.exc import IntegrityError
from getpass import getpass
from app.hashing import Hash

def create_user(username: str, email: str, password: str):
    db = SessionLocal()
    try:
        user = User(
            username=username,
            email=email,
            password=Hash.hash_password(password)  # ✅ Aquí usas bcrypt
        )
        db.add(user)
        db.commit()
        print(f"✅ Usuario '{username}' creado con éxito.")
    except IntegrityError:
        db.rollback()
        print("❌ Error: Email o usuario ya existente.")
    finally:
        db.close()

if __name__ == "__main__":
    username = input("Nombre de usuario: ")
    email = input("Correo electrónico: ")
    password = getpass("Contraseña: ")
    create_user(username, email, password)
