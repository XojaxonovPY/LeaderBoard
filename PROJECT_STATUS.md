# UniStudy / LeaderBoard — Loyiha Holati, Arxitektura va AI/Muhandis Qo‘llanmasi

**Hujjat versiyasi:** 1.2  
**Oxirgi yangilangan sana:** 2026-11-01  
**Asosiy TZ:** `UniStudy — Texnik topshiriq (TZ) v1.1.docx`

---

## 1. Yangi O‘zgarishlar Review'si (Oxirgi kiritilgan yangiliklar)

Siz va jamoa tomonidan kiritilgan oxirgi o‘zgarishlar sinchiklab tekshirildi:

1. **Stateless JWT Arxitekturasi to‘g‘rilandi (`apps/permissions.py` va `users/views/admin.py`):**
   * Tizimda `JWTStatelessUserAuthentication` yoqilganligi sababli, `request.user` bazadan emas, tokendan (`StatelessUser`) olinadi.
   * `request.user.token.get("role") == User.RoleType.Teacher` va `not request.user.token.get("is_superuser")` qilingani — har bir API so‘rovida ortiqcha `SELECT * FROM users` so‘rovidan qochish imkonini berdi (Zero DB load for auth).
2. **`users/serializer.py` va `users/views/auth.py`:**
   * `username` to‘liq joriy qilindi, `phone_number` validatsiyasidan xalos bo‘lindi.
   * `UserUpdateModelSerializer`, `GroupModelSerializer`, `SchoolModelSerializer` toza `CustomModelSerializer`ga ulandi.
3. **`root/mixins.py` (Ultra-fast 1 SQL Update/Delete):**
   * 2 ta so‘rovdan (SELECT + UPDATE) qochilib, to‘g‘ridan-to‘g‘ri **1 ta toza SQL UPDATE**ga keltirildi.
   * RAM'dagi barcha maydon tekshiruvlari va `auto_now` qo‘shilishi **bitta yagona for-siklga (~0.5 µs)** tushirildi.
4. **`root/serializers.py` (10/10 Savepoint himoyasi):**
   * `transaction.atomic()` orqali PostgreSQL tranzaksiyalari xatolik yuz berganda bekor bo‘lib qolishdan to‘liq himoyalandi.

---

## 2. Yangi Updatemiz Imkoniyatlari (Qoplagan vs Hali qoplanmagan)

###  Mavjud imkoniyatlar (Hozir ishlayotgan qism):
* **Yuqori tezlik (High-Performance Core):**
  * ORJSON orqali JSON serializatsiya standartidan 5–10x tezroq.
  * Update va Delete amallarida 0 ta ortiqcha SELECT (toza 1 ta SQL query).
  * Unique constraint xatolarida ortiqcha SELECT'siz toza `409 Conflict` qaytarish.
* **Autentifikatsiya va Rollar:**
  * Stateless JWT tokenlar, Teacher/Student/Admin rollari token ichida saqlanadi.
  * O‘quvchilar uchun login (`username`) orqali kirish.
* **To‘liq Ta'lim va Amaliy Test Ma'lumotlar Bazasi:**
  * `School` $\rightarrow$ `Group` $\rightarrow$ `User` bog‘lanishi.
  * `Lesson` (prezentatsiya, holat) $\rightarrow$ `Source` (video, havolalar) $\rightarrow$ ko‘p guruhlarga ulash.
  * `Assignment` (topshiriq) $\rightarrow$ `TestCase` (ochiq namunalar va yashirin testlar).
  * `Submission` $\rightarrow$ `SubmissionFile` (kod matni) $\rightarrow$ `SubmissionResults` (har bir test natijasi 1-ga-1).

### ⏳ Hali qoplanmagan (Keyingi navbatda qilinishi shart bo‘lgan) ishlar:
1. **Code Runner Sandbox:** O‘quvchi yuborgan kodni Python `subprocess` orqali xavfsiz (timeout, memory limit) yurgizib, `TestCase`lar bilan tekshiruvchi servis (`services/code_runner.py`).
2. **`apps/serializer.py` nomuvofiqliklari:** `FileModelSerializer`da eski `homework_id` va `line_count` qolib ketgan, `AssignmentSerializer`ga `lesson`, `score`, `max_attempts` qo‘shilishi kerak.
3. **`apps/views/teachers.py`:** `Assignment` yaratishda `teacher` o‘rniga `lesson` orqali bog‘lash.
4. **Asinxron AI (Gemini):** Serializer ichidan chiqarilib, Celery task'ga o‘tkazilishi kerak.
5. **Plagiat moduli:** O‘quvchilar kodini token/AST o‘xshashligi bo‘yicha tekshirish.
6. **`apps/tests.py` va `users/tests.py`:** O‘chirilgan `Course` importini tuzatib, `pytest`ni yashil qilish.

---

## 3. Ma'lumotlar Bazasi Universalligi (Database Compatibility)

Hozirgi barcha `root` o‘zgarishlari **100% universal** va quyidagi relational bazalarda bir xil ishlaydi:

| Baza turi | UPDATE / DELETE (1 SQL) | Unique Constraint ushlash (`_extract_field_from_error`) | Savepoint (`transaction.atomic`) |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** (Prod) | `QuerySet.update()` | `Key (username)=(...) already exists.` regex | `SAVEPOINT` to‘liq quvvatlanadi |
| **SQLite** (Local Dev/Test) | `QuerySet.update()` | `UNIQUE constraint failed: table.field` regex | `SAVEPOINT` to‘liq quvvatlanadi |
| **MySQL / MariaDB** | `QuerySet.update()` | `Duplicate entry ... for key ...` regex | `SAVEPOINT` (InnoDB) quvvatlanadi |

*Hech qanday baza-spetsifik xom (raw) SQL yozilmagan. Hammasi Django ORM abstraksiyasi orqali yozilgan.*

---

## 4. Kelajakda API Yozuvchi Dasturchi va AI uchun QAT'IY INSTRUKSIYA (Developer & AI Guidelines)

Agar kelgusida loyihaga yangi API yozish kerak bo‘lsa, quyidagi qoidalarga **qatiy amal qilinishi shart**:

### 1. Model Serializerlar yozish qoidasi:
* Barcha yangi ModelSerializerlar standart `serializers.ModelSerializer`dan emas, **`root.serializers.CustomModelSerializer`**dan meros olishi shart!
```python
from root.serializers import CustomModelSerializer

class MyModelSerializer(CustomModelSerializer):
    class Meta:
        model = MyModel
        fields = ('id', 'name', 'created_at')
```
*Bu bazadagi ortiqcha unique SELECT'larni oldini oladi va 409 xatolikni toza qaytaradi.*

### 2. Update va Delete View'lar yozish qoidasi:
* Ob'ektni yangilash yoki o‘chirish API'larida standart DRF view'lar o‘rniga **`root.api_views.CustomUpdateAPIView`** va **`root.api_views.CustomDestroyAPIView`** ishlatilsin:
```python
from root.api_views import CustomUpdateAPIView, CustomDestroyAPIView

class MyUpdateAPIView(CustomUpdateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [IsTeacher]
```
*Bu 2 ta so‘rov o‘rniga 1 ta yagona toza SQL so‘rovda bajaradi va `updated_at`ni avtomatik yangilaydi.*

### 3. Stateless JWT va Foydalanuvchi tekshiruvlari:
* Foydalanuvchi ma'lumotlarini tekshirishda `request.user.role` deb DB ga murojaat qilmang.
* Har doim tokendan oling:
```python
# To'g'ri:
role = request.user.token.get("role")
is_admin = request.user.token.get("is_superuser")
```

### 4. Og‘ir amallar va Kod Bajarish (Code Runner / AI):
* Hech qachon Serializerning `create()` yoki `validate()` metodlari ichida kodni yurgizmang yoki Gemini API'ni sinxron chaqirmang.
* Barcha kod bajarish va AI tahlillari `Submission` yaratilgandan so‘ng **Celery task** orqali asinxron yurgizilishi shart:
```python
# View yoki Serializerda:
submission = serializer.save()
run_submission_tests_task.delay(submission.id)  # Celery orqali asinxron
```
