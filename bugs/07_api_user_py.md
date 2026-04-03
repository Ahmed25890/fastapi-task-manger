# 🐛 الأخطاء البرمجية في ملف `app/api/user.py`

> **المسار:** `app/api/user.py`

---

## 🔴 باغ #1: تكرار الاستيرادات (Duplicate Imports)

### 📍 مكان الخطأ:
```python
# سطر 1-6
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status       # ← مكرر
from fastapi.security import OAuth2PasswordRequestForm              # ← مكرر
from sqlalchemy.orm import Session                                   # ← مكرر
```

### 🔍 شرح المشكلة:
أول 3 سطور مكررة تاني في السطور 4-6! نفس الاستيرادات بالظبط.
بايثون مش هيطلع خطأ، لكن ده كود زيادة بدون فايدة وبيدل على إن في نسخ ولصق حصل غلط.

### 💡 كيفية الحل:
- احذف السطور المكررة (سطر 4، 5، و 6).
- كده الملف هيكون نضيف.

---

## 🔴 باغ #2: مسارات الاستيراد غلط

### 📍 مكان الخطأ:
```python
# سطر 8
from db.session import engine, get_db
# سطر 9
from db import models
# سطر 10
from services import tasks
# سطر 12
from services.authentication import auth
# سطر 13
from services import user_service
# سطر 15
from models.user import UserLogin, UserResponse, DelUser, UserUpdate, CreateUser
# سطر 16
from models.token import Token
# سطر 18
from services.authentication.auth import get_current_user
```

### 🔍 شرح المشكلة:
نفس مشكلة ملف `api/tasks.py` — الاستيرادات مش بتستخدم المسار الكامل اللي يبدأ بـ `app.`.
ده هيسبب `ModuleNotFoundError` لما تشغل البرنامج.

### 💡 كيفية الحل:
- حوّل كل المسارات لمسارات مطلقة تبدأ بـ `app.`.

---

## 🔴 باغ #3: `get_current_user` مش موجود في `auth.py`

### 📍 مكان الخطأ:
```python
# سطر 18
from services.authentication.auth import get_current_user
```

### 🔍 شرح المشكلة:
نفس المشكلة اللي في `api/tasks.py`. دالة `get_current_user` مش في ملف `auth.py`، هي في `get_current_user_file.py`.

### 💡 كيفية الحل:
- غيّر الاستيراد للمكان الصحيح.

---

## 🟡 باغ #4: استيراد `tasks` مش مستخدم

### 📍 مكان الخطأ:
```python
# سطر 10
from services import tasks
```

### 🔍 شرح المشكلة:
`tasks` مستورد لكن مش مستخدم في الملف ده خالص. الملف ده بتاع الـ user endpoints بس.

### 💡 كيفية الحل:
- احذف السطر ده.

---

## 🟡 باغ #5: استيراد `OAuth2PasswordRequestForm` مش مستخدم

### 📍 مكان الخطأ:
```python
# سطر 2
from fastapi.security import OAuth2PasswordRequestForm
```

### 🔍 شرح المشكلة:
`OAuth2PasswordRequestForm` مستورد لكن مش مستخدم. الـ login بيستخدم `UserLogin` schema بدلها.

### 💡 كيفية الحل:
- لو عايز تستخدم OAuth2 form-based login: استخدم `OAuth2PasswordRequestForm` بدل `UserLogin`.
- لو عايز تخلي الـ login بـ JSON body: شيل الاستيراد ده لأنه مش محتاجه.

---

## 🟡 باغ #6: استيراد `engine` مش مستخدم

### 📍 مكان الخطأ:
```python
# سطر 8
from db.session import engine, get_db
```

### 🔍 شرح المشكلة:
`engine` مستورد وملوش أي استخدام في الملف.

### 💡 كيفية الحل:
- شيل `engine` من الاستيراد.

---

## 🟡 باغ #7: أي مستخدم يقدر يشوف بيانات مستخدم تاني

### 📍 مكان الخطأ:
```python
# سطر 43-45
@router.get("/user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return user_service.GetUser(db, user_id)
```

### 🔍 شرح المشكلة:
أي مستخدم مسجّل يقدر يشوف بيانات أي مستخدم تاني بس عن طريق إنه يغير الـ `user_id` في الـ URL.
مفيش تحقق إن المستخدم بيشوف بياناته هو بس.

### 💡 كيفية الحل:
- تحقق إن `user_id == current_user.user_id` أو إن المستخدم عنده صلاحيات Admin.
- أو اعمل endpoint `/user/me` يرجع بيانات المستخدم الحالي بس.

---

## 🟡 باغ #8: حذف المستخدم مش بيتحقق من الملكية

### 📍 مكان الخطأ:
```python
# سطر 62-64
@router.delete("/user", response_model=UserResponse)
def del_user_main(user: DelUser, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return user_service.DelUserDB(db, user)
```

### 🔍 شرح المشكلة:
المستخدم بيبعت `user_id` في الـ body (`DelUser`)، لكن مفيش تحقق إن ده الـ `user_id` بتاعه.
يعني أي مستخدم يقدر يحذف أي مستخدم تاني!

### 💡 كيفية الحل:
- استخدم `current_user.user_id` بدل ما تاخد الـ `user_id` من الـ body.
- أو تحقق إن `user.user_id == current_user.user_id`.

---
