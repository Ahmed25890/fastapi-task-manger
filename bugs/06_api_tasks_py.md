# 🐛 الأخطاء البرمجية في ملف `app/api/tasks.py`

> **المسار:** `app/api/tasks.py`

---

## 🔴 باغ #1: مسارات الاستيراد غلط (Incorrect Import Paths)

### 📍 مكان الخطأ:
```python
# سطر 5
from db.session import engine, get_db
# سطر 6
from db import models
# سطر 7
from services import tasks
# سطر 9
from services.authentication import auth
# سطر 11
from models.tasks import TaskResponse, CreateTask, UpdateTask, DelTask
# سطر 12
from services.authentication.auth import get_current_user
```

### 🔍 شرح المشكلة:
كل الاستيرادات دي بتستخدم مسارات **نسبية بدون نقطة** وده مش هيشتغل لو شغلت البرنامج من المجلد الرئيسي.
المسار الصحيح لازم يبدأ بـ `app.` (مسار مطلق) أو يستخدم `.` (مسار نسبي).
مثلاً: `from db.session import get_db` لازم تكون `from app.db.session import get_db`.

### 💡 كيفية الحل:
- حوّل كل الاستيرادات لمسارات مطلقة تبدأ بـ `app.`.
- أو استخدم الاستيراد النسبي بنقطة (`.`).
- تأكد إن الـ PYTHONPATH أو طريقة تشغيل البرنامج متوافقة مع أسلوب الاستيراد.

---

## 🔴 باغ #2: استيراد `get_current_user` من مكان غلط

### 📍 مكان الخطأ:
```python
# سطر 12
from services.authentication.auth import get_current_user
```

### 🔍 شرح المشكلة:
دالة `get_current_user` مش موجودة في ملف `auth.py`!
هي موجودة في ملف `get_current_user_file.py`.
يعني لما البرنامج يحاول يستورد، هيطلع `ImportError`.

### 💡 كيفية الحل:
- غيّر الاستيراد عشان يجيب `get_current_user` من `get_current_user_file` بدل `auth`.
- أو انقل الدالة لملف `auth.py` وامسحها من الملف التاني.

---

## 🟡 باغ #3: استيراد `engine` مش مستخدم

### 📍 مكان الخطأ:
```python
# سطر 5
from db.session import engine, get_db
```

### 🔍 شرح المشكلة:
`engine` مستورد لكن مش مستخدم في أي مكان في الملف.
ده بيزوّد حجم الذاكرة ويخلي الكود مش نظيف.

### 💡 كيفية الحل:
- شيل `engine` من الاستيراد وخلّي بس `get_db`.

---

## 🔴 باغ #4: `GetAllUserTasks` بيتبعت لها `current_user` بدل `user_id`

### 📍 مكان الخطأ:
```python
# سطر 22-23
def get_all_tasks(db:Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    return tasks.GetAllUserTasks(db, current_user)
```

### 🔍 شرح المشكلة:
دالة `GetAllUserTasks` في `services/tasks.py` بتستقبل `user_id: int` (رقم).
لكن هنا بتبعت لها `current_user` (كائن Users كامل) مش `current_user.user_id`.
يعني الفلتر `models.Tasks.user_id == user_id` هيقارن رقم بكائن وده مش هيشتغل صح.

### 💡 كيفية الحل:
- ابعت `current_user.user_id` بدل `current_user` في استدعاء الدالة.

---

## 🔴 باغ #5: `UpdateTaskDB` بيتمناداها بشكل غلط

### 📍 مكان الخطأ:
```python
# سطر 35-36
def update_task(task: UpdateTask, db: Session = Depends(get_db), ...):
    return tasks.UpdateTaskDB(db, task)
```

### 🔍 شرح المشكلة:
في `services/tasks.py`، دالة `UpdateTaskDB` بتستقبل **3 برامترات**: `(db, task_id, task)`.
لكن هنا بتبعت لها **2 بس**: `(db, task)`.
يعني الـ `task_id` مش متبعت وده هيعمل `TypeError`.

### 💡 كيفية الحل:
- ابعت `task.task_id` كبارامتر تاني: `tasks.UpdateTaskDB(db, task.task_id, task)`.
- أو عدّل دالة `UpdateTaskDB` عشان تاخد الـ `task_id` من الـ `task` object نفسه.

---

## 🟡 باغ #6: مفيش تحقق من ملكية المهمة (Authorization)

### 📍 مكان الخطأ:
```python
# كل الـ endpoints
def get_task(task_id: int, db, current_user):
   return tasks.GetTask(db, task_id)

def delete_task(task: DelTask, db, current_user):
   return tasks.DelTaskDB(db, task.task_id)
```

### 🔍 شرح المشكلة:
رغم إنك بتتحقق إن المستخدم مسجل دخول (authenticated)، مفيش تحقق إن المهمة دي **بتاعت** المستخدم ده.
يعني أي مستخدم مسجل يقدر يشوف أو يحذف أو يعدّل مهام مستخدمين تانيين لو عرف الـ `task_id`.

### 💡 كيفية الحل:
- في كل endpoint، بعد ما تجيب المهمة، تحقق إن `task.user_id == current_user.user_id`.
- لو مش نفس المستخدم، ارجع `403 Forbidden`.
- ممكن تعمل دالة مشتركة للتحقق ده عشان متكررهوش في كل endpoint.

---
