# 🐛 الأخطاء البرمجية في ملف `app/services/authentication/auth.py`

> **المسار:** `app/services/authentication/auth.py`

---

## 🔴 باغ #1: `get_current_user` مش موجود في الملف ده

### 🔍 شرح المشكلة:
ملفات `api/tasks.py` و `api/user.py` بيستوردوا `get_current_user` من `auth.py`، لكن الدالة دي مش موجودة هنا — هي في `get_current_user_file.py`.

### 💡 كيفية الحل:
- صلّح الاستيرادات في ملفات الـ API.
- أو انقل الدالة لهنا (لكن كده هيبقى فيه تكرار).

---

## 🟡 باغ #2: استخدام `datetime.utcnow()` المهملة

### 📍 مكان الخطأ:
```python
expire = datetime.utcnow() + engine_delta
expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
```

### 🔍 شرح المشكلة:
`datetime.utcnow()` مهملة في Python 3.12+. بترجع وقت بدون timezone.

### 💡 كيفية الحل:
- استخدم `datetime.now(timezone.utc)` بدلها.

---

## 🟡 باغ #3: تكرار قراءة الـ Configuration يدوي

### 📍 مكان الخطأ:
```python
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
```

### 🔍 شرح المشكلة:
عندك `Settings` في `config.py` بيقرأ كل ده. ليه تقرأه تاني يدوي؟

### 💡 كيفية الحل:
- استخدم `from app.core.config import settings` واقرأ القيم منه.

---

## 🟡 باغ #4: اسم البارامتر `engine_delta` مش واضح

### 📍 مكان الخطأ:
```python
def create_token(data: dict, engine_delta: Optional[timedelta] = None):
```

### 🔍 شرح المشكلة:
اسم `engine_delta` مش منطقي — المقصود هو `expires_delta` (مدة انتهاء الصلاحية).

### 💡 كيفية الحل:
- سمّيه `expires_delta` عشان يكون واضح.

---

## 🟡 باغ #5: مفيش معالجة لو `ACCESS_TOKEN_EXPIRE_MINUTES` مش موجود

### 📍 مكان الخطأ:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
```

### 🔍 شرح المشكلة:
لو المتغير مش في `.env`، `os.getenv` هيرجع `None` و `int(None)` هيطلع `TypeError`.

### 💡 كيفية الحل:
- ضيف قيمة افتراضية: `os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")`.
- أو استخدم `settings` من `config.py`.

---
