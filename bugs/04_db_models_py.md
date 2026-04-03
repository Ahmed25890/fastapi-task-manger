# 🐛 الأخطاء البرمجية في ملف `app/db/models.py`

> **المسار:** `app/db/models.py`

---

## 🟡 باغ #1: استخدام `datetime.utcnow` المهملة

### 📍 مكان الخطأ:
```python
# سطر 24
start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
```

### 🔍 شرح المشكلة:
`datetime.utcnow` بقت **مهملة (deprecated)** في Python 3.12+.
المشكلة إنها بترجع التوقيت من غير timezone info (naive datetime)، وده ممكن يسبب مشاكل لما تقارن أوقات من مناطق زمنية مختلفة.
Python الجديد بيحذرك ويقول لك استخدم `datetime.now(timezone.utc)` بدلها.

### 💡 كيفية الحل:
- استخدم `datetime.now(timezone.utc)` بدل `datetime.utcnow`.
- استورد `timezone` من `datetime`.
- أو استخدم `func.now()` من SQLAlchemy عشان الـ database server هو اللي يحدد الوقت.

---

## 🟡 باغ #2: اسم العمود `Task_status` مش متسق

### 📍 مكان الخطأ:
```python
# سطر 27
Task_status = Column(String(15), default="ToDo")
```

### 🔍 شرح المشكلة:
اسم العمود `Task_status` بيبدأ بحرف كبير وباقي الأعمدة بحرف صغير (`task_id`, `title`, `user_id`).
ده مش متسق مع باقي الـ naming convention في الملف.
كمان في ملف `services/tasks.py` سطر 42، بيستخدم `task_status` (بحرف صغير) وده هيعمل مشكلة لأن الأسماء مش متطابقة.

### 💡 كيفية الحل:
- غيّر اسم العمود لـ `task_status` (كله حروف صغيرة بـ snake_case).
- تأكد إن كل الأماكن اللي بتستخدم الاسم ده في الـ services والـ API بتستخدم نفس الاسم.
- لو محتاج تغير الاسم في قاعدة البيانات، اعمل Alembic migration.

---

## 🟡 باغ #3: مفيش validation على مستوى قاعدة البيانات

### 📍 مكان الخطأ:
```python
# سطر 26
priority = Column(String(10), default="medium")
# سطر 27
Task_status = Column(String(15), default="ToDo")
```

### 🔍 شرح المشكلة:
الأعمدة `priority` و `Task_status` معرفين كـ `String` عادي من غير أي قيود على القيم المسموحة.
يعني ممكن حد يدخل قيمة زي `"xyz"` كـ priority والداتابيز هيقبله عادي.
عندك Enums في `app/models/enums.py` لكنهم مش مستخدمين في تعريف الأعمدة.

### 💡 كيفية الحل:
- استخدم `Enum` من SQLAlchemy بدل `String` عشان تحدد القيم المسموحة.
- أو استخدم `CheckConstraint` عشان تضيف قيود على مستوى قاعدة البيانات.
- ده بيضمن إن حتى لو حد تجاوز الـ API validation، الداتابيز مش هيقبل قيم غلط.

---

## 🟢 باغ #4: العلاقة (Relationship) مش فيها `cascade`

### 📍 مكان الخطأ:
```python
# سطر 14
tasks = relationship("Tasks", back_populates="user")
```

### 🔍 شرح المشكلة:
لما تحذف مستخدم، المهام بتاعته هتفضل موجودة في قاعدة البيانات بـ `user_id` بتاع مستخدم محذوف.
ده هيسبب مشاكل (orphaned records) لأن المهام هتكون بتشير لمستخدم مش موجود.

### 💡 كيفية الحل:
- ضيف `cascade="all, delete-orphan"` للعلاقة عشان لما تحذف مستخدم، المهام بتاعته تتحذف تلقائيًا.
- أو ضيف `ondelete="CASCADE"` للـ ForeignKey في جدول الـ Tasks.

---
