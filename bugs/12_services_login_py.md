# 🐛 الأخطاء البرمجية في ملف `app/services/login.py`

> **المسار:** `app/services/login.py`

---

## 🔴 باغ #1: مسارات الاستيراد غلط

### 📍 مكان الخطأ:
```python
from models import user
from db import session
from user_service import GetUserByEmailSafe
```

### 🔍 شرح المشكلة:
المسارات مش صحيحة — لازم تبدأ بـ `app.`.

### 💡 كيفية الحل:
- `from app.models import user`
- `from app.db import session`
- `from app.services.user_service import GetUserByEmailSafe`

---

## 🔴 باغ #2: تعارض اسم المتغير مع اسم الموديول (Shadowing)

### 📍 مكان الخطأ:
```python
from models import user                  # ← استيراد الموديول user

def login(data: user.UserLogin, ...):    # ← استخدام user كموديول
    user = GetUserByEmailSafe(...)       # ← تعريف متغير بنفس الاسم!
```

### 🔍 شرح المشكلة:
في الدالة، سمّيت المتغير `user` وده نفس اسم الموديول `user` اللي مستورد فوق.
بايثون هياخد الاسم المحلي `user` (المتغير) وهيغطي على الموديول.
ده مشكلة لو حاولت تستخدم `user.UserLogin` بعد السطر ده.

### 💡 كيفية الحل:
- سمّ المتغير اسم تاني زي `db_user` أو `found_user`.

---

## 🟡 باغ #3: الملف ده مكرر مع الكود في `api/user.py`

### 🔍 شرح المشكلة:
نفس كود الـ login موجود في `api/user.py` (السطور 24-40).
يعني الملف ده **مش مستخدم** والكود فيه متكرر.

### 💡 كيفية الحل:
- لو مش محتاجه: احذفه.
- لو محتاجه: استخدمه في الـ router بدل ما تكتب الكود مرتين.

---

## 🟡 باغ #4: استخدام `Depends` في دالة service عادية

### 📍 مكان الخطأ:
```python
def login(data: user.UserLogin, db: Session = Depends(session.get_db)):
```

### 🔍 شرح المشكلة:
`Depends()` بتشتغل بس في FastAPI endpoints (أو sub-dependencies).
لو ناديت الدالة دي عادي (مش من router)، `db` مش هيتملى تلقائي.

### 💡 كيفية الحل:
- شيل `Depends()` واخلي `db` بارامتر عادي: `db: Session`.
- الـ dependency injection يكون في الـ router بس.

---
