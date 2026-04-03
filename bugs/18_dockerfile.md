# 🐛 الأخطاء البرمجية في ملف `Dockerfile`

> **المسار:** `Dockerfile`

---

## 🟡 باغ #1: كود قديم متعلّق (Commented Out Code)

### 📍 مكان الخطأ:
```dockerfile
# FROM python:3.12
# ADD main.py .
# RUN pip install --no-cache-dir -r requirements.txt
# CMD ["python", "./main.py"]
```

### 🔍 شرح المشكلة:
أول 8 سطور كود متعلّق (commented out) من نسخة قديمة. ده بيعمل فوضى.

### 💡 كيفية الحل:
- احذف الأسطر المتعلقة — الكود الفعّال بيبدأ من سطر 9.

---

## 🟡 باغ #2: مفيش `.dockerignore`

### 🔍 شرح المشكلة:
`COPY . .` بينسخ **كل حاجة** للـ container — بما فيها `.git`, `__pycache__`, `.env`, `.vscode`.
ده بيزوّد حجم الـ image وممكن يكشف بيانات حساسة (`.env` فيه كلمة سر الداتابيز!).

### 💡 كيفية الحل:
- اعمل ملف `.dockerignore` وضيف فيه: `.git`, `__pycache__`, `.env`, `.vscode`, `*.pyc`.

---

## 🟡 باغ #3: مفيش مستخدم غير `root`

### 🔍 شرح المشكلة:
التطبيق بيشتغل بصلاحيات `root` جوا الـ container. ده مخاطرة أمنية.

### 💡 كيفية الحل:
- ضيف `RUN adduser --disabled-password appuser` و `USER appuser` قبل `CMD`.

---
