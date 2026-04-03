# 🐛 الأخطاء البرمجية في ملف `app/services/register.py`

> **المسار:** `app/services/register.py`

---

## 🔴 باغ #1: مسارات الاستيراد غلط

### 📍 مكان الخطأ:
```python
from models.user import CreateUser
from db import models
from authentication import auth
from user_service import GetUserByEmailSafe
```

### 🔍 شرح المشكلة:
كل المسارات مش صحيحة — لازم تبدأ بـ `app.`.

### 💡 كيفية الحل:
- `from app.models.user import CreateUser`
- `from app.db import models`
- `from app.services.authentication import auth`
- `from app.services.user_service import GetUserByEmailSafe`

---

## 🟡 باغ #2: استيراد `sqlalchemy as sq` مش مستخدم

### 🔍 شرح المشكلة:
`sq` مستورد ومش مستخدم في أي مكان.

### 💡 كيفية الحل:
- احذف `import sqlalchemy as sq`.

---

## 🟡 باغ #3: الملف ده مكرر مع `user_service.py`

### 🔍 شرح المشكلة:
في `api/user.py`، الـ create user endpoint بيستدعي `user_service.CreateUserDB`.
لكن الملف ده فيه `CreateUserDB` تاني — يعني في نسختين من نفس الدالة!
الملف ده ملوش أي استخدام في المشروع.

### 💡 كيفية الحل:
- لو مش محتاجه: احذفه.
- لو محتاجه: وحّد الكود في مكان واحد.

---
