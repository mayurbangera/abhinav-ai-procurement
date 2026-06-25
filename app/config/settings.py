from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

META_VERIFY_TOKEN = os.getenv(
    "META_VERIFY_TOKEN"
)

META_ACCESS_TOKEN = os.getenv(
    "META_ACCESS_TOKEN"
)

META_PHONE_NUMBER_ID = os.getenv(
    "META_PHONE_NUMBER_ID"
)


print("PHONE NUMBER ID:", META_PHONE_NUMBER_ID)

if META_ACCESS_TOKEN:
    print("TOKEN LOADED: YES")
else:
    print("TOKEN LOADED: NO")
    
    
