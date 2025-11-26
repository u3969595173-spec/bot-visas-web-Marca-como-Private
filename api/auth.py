"""
Autenticación JWT para API
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
import config


SECRET_KEY = getattr(config, 'JWT_SECRET_KEY', "tu-clave-secreta-super-segura-cambiar-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas


def crear_token(data: Dict) -> str:
    """
    Crea un token JWT
    
    Args:
        data: Datos a incluir en el token (usuario, rol, etc)
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verificar_token(token: str) -> Optional[Dict]:
    """
    Verifica y decodifica un token JWT
    
    Args:
        token: Token JWT a verificar
        
    Returns:
        Datos del token si es válido, None si no
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("⚠️ Token expirado")
        return None
    except jwt.JWTError as e:
        print(f"❌ Error validando token: {e}")
        return None


def refrescar_token(token: str) -> Optional[str]:
    """
    Refresca un token JWT existente
    
    Args:
        token: Token actual
        
    Returns:
        Nuevo token o None si el actual no es válido
    """
    payload = verificar_token(token)
    
    if not payload:
        return None
    
    # Remover expiración antigua
    payload.pop('exp', None)
    
    # Crear nuevo token
    return crear_token(payload)
