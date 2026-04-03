# 🐛 الأخطاء البرمجية في ملف `app/services/user_service.py`

> **المسار:** `app/services/user_service.py`

---

## 🔴 باغ #1: مسارات الاستيراد غلط

### 📍 مكان الخطأ:
```python
from models import user, tasks
from db import models
from authentication.auth import HashPassword
```

### 🔍 شرح المشكلة:
نفس المشكلة المتكررة — الاستيرادات مش بتستخدم المسار الكامل (`app.`).

### 💡 كيفية الحل:
- حوّل لمسارات مطلقة: `from app.models import user` وهكذا.

---

## 🟡 باغ #2: استيراد `tasks` مش مستخدم

### 📍 مكان الخطأ:
```python
from models import user, tasks    # tasks مش مستخدم
import sqlalchemy as sq            # مش مستخدم في كل الدوال
```

### 🔍 شرح المشكلة:
`tasks` و `sq` مستوردين ومش مستخدمين.

### 💡 كيفية الحل:
- احذف الاستيرادات اللي مش مستخدمة.

---

## 🟡 باغ #3: `UpdateUser` بيحدّث كل الحقول حتى لو المستخدم مش عايز

### 📍 مكان الخطأ:
```python
def UpdateUser(db: Session, user_id: int, user: user.UserUpdate):
    get_user = GetUser(db, user_id)
    get_user.user_name = user.user_name
    get_user.email = user.email
    if user.password:
        get_user.password = HashPassword(user.password)
```

### 🔍 شرح المشكلة:
الدالة بتحدّث `user_name` و `email` دايمًا حتى لو المستخدم مبعتش قيم جديدة. لو الحقول فاضية هيمسح البيانات القديمة.

### 💡 كيفية الحل:
- استخدم `model.model_dump(exclude_unset=True)` وحدّث الحقول اللي اتبعتت بس.

---

## 🟡 باغ #4: مفيش تحقق من تكرار الإيميل عند التحديث

### 🔍 شرح المشكلة:
لو المستخدم غيّر الإيميل لإيميل موجود عند مستخدم تاني، هيطلع خطأ `IntegrityError` من الداتابيز بدل رسالة واضحة.

### 💡 كيفية الحل:
- قبل التحديث، تحقق إن الإيميل الجديد مش مستخدم.

---

## 🟡 باغ #5: `DelUserDB` مش بيحذف المهام أولاً

### 🔍 شرح المشكلة:
لو المستخدم عنده مهام، الحذف هيطلع `IntegrityError` بسبب الـ ForeignKey.

### 💡 كيفية الحل:
- ضيف `cascade` للعلاقة في الـ model أو احذف المهام أولاً.

---
