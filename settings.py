from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv('API_KEY')
PROXY_username = os.getenv("PROXY_username")
PROXY_password = os.getenv("PROXY_password")
chrome_path = os.getenv('chrome_path')
chaika_address = os.getenv('chaika_address')
