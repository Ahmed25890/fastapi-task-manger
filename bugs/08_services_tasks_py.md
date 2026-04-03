# 🐛 الأخطاء البرمجية في ملف `app/services/tasks.py`

> **المسار:** `app/services/tasks.py`

---

## 🔴 باغ #1: مسارات الاستيراد غلط

### 📍 مكان الخطأ:
```python
from models import tasks, user
from db import models, session
from authentication import auth, get_current_user_file
```

### 🔍 شرح المشكلة:
الاستيرادات مش بتستخدم المسار الكامل اللي يبدأ بـ `app.`. ده هيسبب `ModuleNotFoundError`.

### 💡 كيفية الحل:
- صلّح كل الاستيرادات عشان تبدأ بـ `app.` (مسار مطلق).

---

## 🔴 باغ #2: `GetTask` مش بيتعامل مع حالة المهمة مش موجودة

### 📍 مكان الخطأ:
```python
def GetTask(db: Session, task_id: int):
    get_task = db.query(models.Tasks).filter(models.Tasks.task_id == task_id).first()
    return get_task
```

### 🔍 شرح المشكلة:
لو الـ `task_id` مش موجود، هيرجع `None` والدوال التانية هتقع بـ `AttributeError`.

### 💡 كيفية الحل:
- ضيف شرط: لو `None`، ارمي `HTTPException(404)`.

---

## 🔴 باغ #3: `task_status` مش متوافق مع اسم العمود `Task_status`

### 🔍 شرح المشكلة:
العمود في الداتابيز `Task_status` (حرف T كبير) لكن الكود بيستخدم `task_status` (حرف t صغير).

### 💡 كيفية الحل:
- وحّد الأسماء كلها بـ `snake_case`.

---

## 🟡 باغ #4: استيرادات مش مستخدمة

### 🔍 شرح المشكلة:
`user`, `session`, `auth`, `get_current_user_file`, `sq` كلهم مستوردين ومش مستخدمين.

### 💡 كيفية الحل:
- احذف الاستيرادات اللي مش مستخدمة.

---

## 🟡 باغ #5: `DelTaskDB` بيرجع كائن محذوف

### 🔍 شرح المشكلة:
بعد الحذف، الكائن بيكون detached وممكن يطلع `DetachedInstanceError`.

### 💡 كيفية الحل:
- احفظ البيانات في dict قبل الحذف أو ارجع رسالة نجاح.

---
