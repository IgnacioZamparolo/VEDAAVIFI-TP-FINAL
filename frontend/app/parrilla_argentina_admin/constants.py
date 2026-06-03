import os
from dotenv import load_dotenv
 
load_dotenv()
 
API_BASE_URL    = os.getenv('API_BASE_URL', 'http://localhost:5000')
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))