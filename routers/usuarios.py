from fastapi import APIRouter, HTTPException
from db import get_connection
from auth import hash_password, verify_password, create_access_token
from schemas import UsuarioLogin, UsuarioRegistro

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/registro")
def registrar_usuario(usuario: UsuarioRegistro):
    conn = get_connection()
    cursor = conn.cursor()

    # Comprobar si existe el email
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (usuario.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed = hash_password(usuario.password)

    cursor.execute("""
        INSERT INTO usuarios (nombre, email, pass_hash, rol, telefono)
        VALUES (%s, %s, %s, %s, %s)
    """, (usuario.nombre, usuario.email, hashed, usuario.rol, usuario.telefono))

    conn.commit()
    return {"mensaje": "Usuario registrado correctamente"}


@router.post("/login")
def login(datos: UsuarioLogin):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (datos.email,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Compara contraseña enviada con la contraseña hash guardada
    if not verify_password(datos.password, user["pass_hash"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Crear token JWT
    token = create_access_token({"id": user["id"], "rol": user["rol"]})

    return {
        "token": token,
        "rol": user["rol"],
        "nombre": user["nombre"]
    }
