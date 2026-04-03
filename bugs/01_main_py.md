# 🐛 الأخطاء البرمجية في ملف `main.py`

> **المسار:** `main.py`

---

## 🔴 باغ #1: تعارض في أسماء الاستيراد (Name Shadowing)

### 📍 مكان الخطأ:
```python
# سطر 3
from app.services import login , register, tasks, user_service
# سطر 6
from app.api import tasks , user
```

### 🔍 شرح المشكلة:
في السطر 3، تم استيراد `tasks` من `app.services`، وبعدها في السطر 6 تم استيراد `tasks` مرة تانية من `app.api`.
المشكلة هنا إن الاستيراد الثاني بيعمل **تغطية (shadowing)** على الاستيراد الأول. يعني لما تستخدم `tasks` في أي مكان بعد كده، هيكون بيشير لـ `app.api.tasks` مش `app.services.tasks`.
وبنفس الطريقة، `user` هيغطي على أي حاجة اسمها `user` لو كانت موجودة قبل كده.

### 💡 كيفية الحل:
- استخدم **أسماء بديلة (aliases)** عند الاستيراد باستخدام `as` عشان تفرق بين الموديولات.
- مثلاً: استورد الـ routers بأسماء واضحة زي `tasks_router` و `user_router`.
- أو استورد الـ `router` مباشرة من كل ملف API بدل ما تستورد الموديول كله.

---

## 🔴 باغ #2: الـ `include_router` بيستقبل موديول مش Router

### 📍 مكان الخطأ:
```python
# سطر 9-10
app.include_router(user)
app.include_router(tasks)
```

### 🔍 شرح المشكلة:
`app.include_router()` بتحتاج كائن من نوع `APIRouter`، لكن هنا بتبعت لها الموديول نفسه (`user` و `tasks`) مش الـ `router` اللي جوا الموديول.
لازم تبعت `user.router` و `tasks.router` مش الموديول كامل.

### 💡 كيفية الحل:
- الطريقة الأولى: غيّر السطرين عشان يبعتوا `.router` من كل موديول.
- الطريقة الثانية (الأفضل): استورد الـ `router` بشكل مباشر من كل ملف API واديه اسم مميز.

---

## 🟡 باغ #3: استيراد حاجات مش مستخدمة (Unused Imports)

### 📍 مكان الخطأ:
```python
# سطر 1
from fastapi import FastAPI, HTTPException, Depends, status
# سطر 2
from app.db import session
# سطر 3
from app.services import login , register, tasks, user_service
# سطر 4
from app.services.authentication import auth , get_current_user_file
# سطر 5
from app.services.rate_limiter import Limiter
```

### 🔍 شرح المشكلة:
في استيرادات كتير مش مستخدمة في الملف ده خالص:
- `HTTPException`, `Depends`, `status` من `fastapi` — مش مستخدمين.
- `session` من `app.db` — مش مستخدم.
- `login`, `register`, `user_service` من `app.services` — مش مستخدمين (لأن الـ logic اتنقل للـ API routers).
- `auth`, `get_current_user_file` من `app.services.authentication` — مش مستخدمين.
- `Limiter` من `app.services.rate_limiter` — مش مستخدم.

### 💡 كيفية الحل:
- احذف كل الاستيرادات اللي مش مستخدمة.
- خلّي الملف نظيف ومن غير أي حاجة زيادة.
- الملف لازم يحتوي بس على: `FastAPI` و الـ routers اللي هتضيفهم.

---

## 🟡 باغ #4: مفيش Prefix أو Tags للـ Routers

### 📍 مكان الخطأ:
```python
app.include_router(user)
app.include_router(tasks)
```

### 🔍 شرح المشكلة:
مفيش `prefix` ولا `tags` متعرفين للـ routers. ده معناه إن:
- الـ endpoints بتاعت الـ tasks والـ users ممكن تتعارض لو عندهم نفس المسارات.
- صفحة الـ Swagger (التوثيق التلقائي) هتكون غير منظمة.

### 💡 كيفية الحل:
- ضيف `prefix` لكل router (مثلاً `/api/v1/users` و `/api/v1/tasks`).
- ضيف `tags` لكل router عشان التوثيق يكون منظم.
- ممكن تعمل ده في `include_router()` أو في تعريف الـ `APIRouter()` نفسه في كل ملف API.

---
