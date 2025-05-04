import jwt
import datetime

SECRET_KEY = "jwtpass"

def generate_token(days_valid: int):
    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(days=days_valid)
    payload = {
        "created_at": now.isoformat(),
        "exp": exp  # JWT 标准字段
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
