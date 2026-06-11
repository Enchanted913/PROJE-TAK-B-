"""
TürkTicaret / cPanel Python uygulaması giriş dosyası.
cPanel > Setup Python App > Application startup file: passenger_wsgi.py
"""
import os
import sys

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HOME = os.environ.get('HOME', os.path.expanduser('~'))

# tun53comtr — cPanel kullanıcı adı (düzeltildi)
VENV_PYTHON = os.path.join('/home/tun53comtr', 'virtualenv', 'projetakip', '3.11', 'bin', 'python3')
if not os.path.exists(VENV_PYTHON):
    # Farklı Python versiyonlarını da dene
    for ver in ['3.11', '3.10', '3.9', '3.12']:
        candidate = os.path.join(HOME, 'virtualenv', 'projetakip', ver, 'bin', 'python3')
        if os.path.exists(candidate):
            VENV_PYTHON = candidate
            break

if os.path.exists(VENV_PYTHON) and sys.executable != VENV_PYTHON:
    os.execl(VENV_PYTHON, VENV_PYTHON, *sys.argv)

sys.path.insert(0, APP_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# PyMySQL (cPanel'de mysqlclient derlenemezse)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
