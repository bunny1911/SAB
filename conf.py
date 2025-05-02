import os

from dotenv import load_dotenv

# Loading all values from '.env' file
load_dotenv()

# Defined secret key
SECRET_KEY = os.getenv("SECRET_KEY")

# Defined encryption algorithm
ALGORITHM = os.getenv("ALGORITHM")

# Defined access token
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Defined refresh token
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

# Defined realtor password
REALTOR_PASSWORD = os.getenv("REALTOR_PASSWORD")

BOT_TOKEN = os.getenv("BOT_TOKEN")


# Defined DB URL
DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('DATABASE_USERNAME')}:"
    f"{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DATABASE_HOST')}:"
    f"{os.getenv('DATABASE_PORT')}/"
    f"{os.getenv('DATABASE_NAME')}"
)
