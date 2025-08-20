# backend/utils/jwt_helper.py
import jwt, datetime
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
JWT_EXPIRATION_HOURS = 24

def generate_jwt(user):
    payload = {
        "user_id": str(user.id),
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
