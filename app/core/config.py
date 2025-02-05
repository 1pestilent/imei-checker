from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Авторизация
PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
ALGORITHM: str = "RS256"

ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
REFRESH_TOKEN_EXPIRE_DAYS: int = 14

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"