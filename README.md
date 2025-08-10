# 🏆 Leader-Board

## 📌 Loyihaning qisqacha tavsifi
**LeaderBoard**-bu Django Rest Framework(DRF) asosoda qurilgan bolajak dasturchilarni oqitish va oquv jarayonida
ular haqida va ular ozlarini darsdagi va darsdan keyin vazivalarni qanday tarzda bajarayotganlariga qarab 
shakillantiriladigan loyiha.


## ⚙️ Asosiy xususiyatlar

- **Rest API**: Yuqori samaradorlikka ega va kop imkoniyatli web freymorki.
- **Docker**: Ilovani konteynerlash va uni turli muhitlarda ishlatish imkonini beradi.
- **pytest**: Testlarni yozish va bajarish uchun vosita.
- **AI kpnfiguratsiyasi** oqvchilarni vazifalarini tekshirish va leaderboard shakllantirish


## 🛠 Texnologiyalar

| Texnologiya      | Tavsifi                                                         |
|------------------|-----------------------------------------------------------------|
| Python 3.12      | Asosiy dasturlash tili                                          |
| Django REST      | Backend API yaratish freymvorki                                 |
| PostgreSQL       | Ma’lumotlar bazasi                                              |
| Docker           | Konteynerizatsiya                                               |
| AI Config        | Sun’iy intellekt konfiguratsiya vazivalarni tahlil qilish uchun |

3. Docker yordamida ishga tushirish

```bash
docker-compose up --build
```

4. Ma'lumotlar bazasini migratsiya qilish

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Ilovani ishga tushirish

```bash
python manage.py runserver 0.0.0.0:8000
```

## 🔧 Env File konfiguratsiyasi

Ilova ishlashi uchun `.env` faylida quyidagi parametrlarni sozlash kerak:

```env
# Django konfiguratsiyasi
DB_DJANGO=your_db_config
DEBUG=False
SECRET_KEY=your_secret_key
DB_NAME=your_db_name
DB_USER=your_db_host
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=port
API_KEY=
```
Ilova http://127.0.0.1:8000 manzilida ishga tushadi.

## 📊 Ma’lumotlar bazasi modeli

[DrawSQL’da model sxemasini ko‘rish](https://drawsql.app/teams/gayrat-1/diagrams/leadrboard)


## 📄 Litsenziya

Loyiha MIT litsenziyasi asosida tarqatiladi.
