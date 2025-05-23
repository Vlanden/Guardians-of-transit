from urllib.parse import urlparse
import pymysql
import os

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

def parse_db_url(db_url):
    parsed = urlparse(db_url)
    return {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": parsed.username,
        "password": parsed.password,
        "database": parsed.path.lstrip('/').split('?')[0]
    }

try:
    config = parse_db_url(os.getenv('DATABASE_URL'))
    conn = pymysql.connect(**config, cursorclass=pymysql.cursors.DictCursor)
    print("✅ ¡Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")