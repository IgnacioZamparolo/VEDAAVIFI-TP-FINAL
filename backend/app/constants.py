import os
from dotenv import load_dotenv

load_dotenv()
 
# JWT
JWT_SECRET    = os.environ.get("JWT_SECRET", "clave_secreta_parrilla")
JWT_ALGORITHM = "HS256"
JWT_EXP_HORAS = int(os.environ.get("JWT_EXP_HORAS", "8"))
 
# Roles
ROL_ADMIN = "admin"
 
# Codigos de error
ERROR_CODE_INVALID_BODY         = "invalid.body"
ERROR_CODE_CAMPO_REQUERIDO      = "required.field"
ERROR_CODE_INVALID_MIN_VALUE    = "invalid.min.value"
ERROR_CODE_INVALID_MAX_VALUE    = "invalid.max.value"
ERROR_CODE_INVALID_EMAIL        = "invalid.email.format"
ERROR_CODE_CREDENCIALES         = "invalid.credentials"
ERROR_CODE_TOKEN_FALTANTE       = "auth.token.missing"
ERROR_CODE_TOKEN_INVALIDO       = "auth.token.invalid"
ERROR_CODE_TOKEN_EXPIRADO       = "auth.token.expired"
ERROR_CODE_ACCESO_NO_AUTORIZADO = "auth.forbidden"
ERROR_CODE_USUARIO_NOT_FOUND    = "usuario.not.found"
<<<<<<< HEAD

# Credenciales
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")
 
=======
 
# Credenciales
SMTP_USER=os.environ.get("SMTP_USER")
SMTP_PASSWORD=os.environ.get("SMTP_PASSWORD")

# Malas palabras
malas_palabras_raw = os.getenv("MALAS_PALABRAS", "")
MALAS_PALABRAS_LISTA = [
    palabra.strip().lower() 
    for palabra in malas_palabras_raw.split(",") 
    if palabra.strip()
]
>>>>>>> 0fb4130419988628cb995c4a683d96e8212c0524
