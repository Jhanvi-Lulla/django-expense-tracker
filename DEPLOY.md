# Expense Tracker: Local run + Deployment guide

## 1. Laptop pe chalana (pehli baar)

```
cd proj4
python -m venv venv
venv\Scripts\activate          (Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser     (optional, admin ke liye)
python manage.py runserver
```

Browser mein `http://127.0.0.1:8000/` kholo. Ab seedha welcome page aayega, wahan se Login / Sign Up.
(Pehle `/tracker/welcome` type karna padta tha, ab nahi.)

Tests chalane ke liye: `python manage.py test`

---

## 2. Online deploy: Option A, PythonAnywhere (sabse easy, beginners ke liye)

1. https://www.pythonanywhere.com pe free account banao (username yaad rakhna, URL banega `username.pythonanywhere.com`).
2. **Consoles → Bash** kholo aur apna code lao:
   ```
   git clone https://github.com/<your-username>/<your-repo>.git proj4
   cd proj4
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --no-input
   python manage.py createsuperuser
   ```
   (GitHub nahi hai toh **Files** tab se zip upload karke `unzip` kar sakti ho.)
3. **Web tab → Add a new web app → Manual configuration → Python 3.12** (jo version available ho).
4. Web tab mein:
   - **Source code**: `/home/<username>/proj4`
   - **Virtualenv**: `/home/<username>/proj4/venv`
   - **Static files**: URL `/static/` → Directory `/home/<username>/proj4/staticfiles`
5. **WSGI configuration file** kholo (Web tab mein link hai), sab kuch hata ke ye daalo:
   ```python
   import os, sys

   path = '/home/<username>/proj4'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'proj4.settings'
   os.environ['DEBUG'] = 'False'
   os.environ['SECRET_KEY'] = 'yahan-koi-lambi-random-string-daalo'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
6. Web tab pe **Reload** dabao. Ab `https://<username>.pythonanywhere.com/` pe tumhari site live hai.

Code update karna ho toh: Bash mein `cd proj4 && git pull && python manage.py migrate && python manage.py collectstatic --no-input`, phir Web tab pe Reload.

---

## 3. Online deploy: Option B, Render

1. Code GitHub pe push karo (`.gitignore` already `db.sqlite3` aur `venv` ko ignore karta hai).
2. Render pe **New → PostgreSQL** banao, uska **Internal Database URL** copy karo.
   (Free database ki limits/expiry Render ki current terms pe depend karti hain, ek baar check kar lena.)
3. **New → Web Service** → apna GitHub repo chuno:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn proj4.wsgi:application`
4. **Environment variables** add karo:
   - `SECRET_KEY` = koi lambi random string
   - `DEBUG` = `False`
   - `DATABASE_URL` = Postgres wala URL
5. Deploy dabao. Done, Render ek `https://<name>.onrender.com` URL dega.

Note: Render pe free web service kuch der idle rehne par so jati hai, pehla page khulne mein thoda time lagta hai.

---

## Important baatein

- `db.sqlite3` GitHub pe mat daalo. Server ka apna alag database hota hai, laptop ka data wahan automatically nahi jaata.
- Server pe `DEBUG=False` zaroor rakhna, warna errors mein tumhari settings dikh sakti hain.
- Purane 6 expenses (Basketball, Chai, etc.) ka koi owner nahi tha. Ab wo kisi user ko dikhenge nahi. Chaho toh admin panel (`/admin/`) mein jaake unka `user` set kar do.
