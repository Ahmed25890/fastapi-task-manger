# 🐛 الأخطاء البرمجية في ملف `requirements.txt`

> **المسار:** `requirements.txt`

---

## 🟡 باغ #1: مكتبات ناقصة

### 🔍 شرح المشكلة:
المكتبات دي مستخدمة في الكود لكن مش موجودة في `requirements.txt`:
- **`slowapi`** — مستخدم في `rate_limiter.py`.
- **`cachetools`** — مستخدم في `cache.py`.

### 💡 كيفية الحل:
- ضيف `slowapi` و `cachetools` في `requirements.txt`.

---

## 🟡 باغ #2: مكتبات مش مستخدمة

### 🔍 شرح المشكلة:
- **`psycopg2-binary`** — driver لـ PostgreSQL لكن أنت بتستخدم MySQL (`pymysql`).
- **`numpy`** — مش مستخدم في أي مكان في المشروع.

### 💡 كيفية الحل:
- لو مش محتاجهم: احذفهم عشان تقلل حجم التثبيت.

---

## 🟡 باغ #3: ملف `.env` فيه كلمة سر محطوطة صريح

### 📍 مكان الخطأ:
```
DATABASE_URL="mysql+pymysql://root:aking#192nightgoshowlight@localhost:3306/tasks"
```

### 🔍 شرح المشكلة:
كلمة سر الداتابيز موجودة في ملف `.env` وده عادي، **لكن** لو الملف متتبّع بـ Git (مش في `.gitignore`)، هتتعرض للكل.

### 💡 كيفية الحل:
- تأكد إن `.env` موجود في `.gitignore`.
- اعمل `.env.example` فيه الهيكل من غير القيم الحقيقية.

---
