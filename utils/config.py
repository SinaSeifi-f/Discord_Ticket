from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
TICKET_CATEGORY_ID = int(os.getenv("TICKET_CATEGORY_ID", 0))
SUPPORT_ROLE_ID = int(os.getenv("SUPPORT_ROLE_ID", 0))
