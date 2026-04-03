# 🐛 الأخطاء البرمجية في ملف `app/models/tasks.py`

> **المسار:** `app/models/tasks.py`

---

## 🔴 باغ #1: مسار الاستيراد غلط (Incorrect Import Path)

### 📍 مكان الخطأ:
```python
# سطر 2
from enums import Priority, TaskStatus
```

### 🔍 شرح المشكلة:
الاستيراد بيحاول يجيب `Priority` و `TaskStatus` من `enums` مباشرة، لكن ملف `enums.py` موجود جوا مجلد `app/models/`.
يعني المسار الصحيح هو `app.models.enums` أو `.enums` (استيراد نسبي).
لو شغلت البرنامج، هيطلع لك `ModuleNotFoundError`.

### 💡 كيفية الحل:
- استخدم الاستيراد النسبي (Relative Import) بإنك تضيف نقطة قبل اسم المود يول.
- أو استخدم المسار الكامل (Absolute Import) اللي بيبدأ من `app`.

---

## 🔴 باغ #2: استخدام `@validator` المهملة بدل `@field_validator`

### 📍 مكان الخطأ:
```python
# سطر 20
@validator("description")
# سطر 27
@validator("due_date")
# سطر 35
@validator("StartDate")
```

### 🔍 شرح المشكلة:
في Pydantic V2 (اللي أنت مستخدمه — النسخة 2.10.3)، `@validator` بقت **مهملة (deprecated)** واتعوضت بـ `@field_validator`.
لو استخدمتها ممكن تشتغل دلوقتي لكن هتطلع تحذيرات (DeprecationWarning)، وفي نسخ Pydantic الجاية ممكن تتشال خالص.

### 💡 كيفية الحل:
- استبدل كل `@validator` بـ `@field_validator`.
- لاحظ إن `@field_validator` بتحتاج إنك تستخدم `@classmethod` معاها.
- وبدل `values` (اللي هو dict)، استخدم `info` من نوع `ValidationInfo`.

---

## 🔴 باغ #3: الـ Validator بتاع الـ description بيرفض `None` غلط

### 📍 مكان الخطأ:
```python
# سطر 20-26
@validator("description")
def val_description(cls, x: Optional[str]):
    if x is None: 
        raise ValueError("")
    x = x.strip()
    final = re.sub(" ", "_", x)
    return final
```

### 🔍 شرح المشكلة:
في الـ Schema، الـ `description` معرّف كـ `Optional[str]` يعني ينفع يكون `None`.
لكن الـ validator بيعمل `raise ValueError("")` لما يكون `None`!
ده تناقض — أنت بتقول إنه اختياري وفي نفس الوقت بترفضه لما يكون فاضي.
كمان، الـ ValueError فاضي بدون رسالة خطأ واضحة.

### 💡 كيفية الحل:
- لو فعلاً الـ description اختياري: ارجّع `None` من غير ما ترمي خطأ لما يكون `None`.
- لو مش اختياري: شيل `Optional` واخليه `str` بس.
- كمان لازم تدي رسالة خطأ واضحة مش فاضية.

---

## 🔴 باغ #4: عمل `raise` لـ string بدل Exception

### 📍 مكان الخطأ:
```python
# سطر 35-40
@validator("StartDate")
def val_start_date(cls, t: Optional[date]):
    if t is None: 
        return t
    if t < date.today():
        raise "date error"       # ← المشكلة هنا
    return t
```

### 🔍 شرح المشكلة:
`raise "date error"` ده **خطأ بايثون (TypeError)**!
في بايثون، `raise` لازم ياخد Exception object مش string.
لو التاريخ أقدم من اليوم، البرنامج هيقع بـ `TypeError: exceptions must derive from BaseException` بدل ما يدّي رسالة خطأ كويسة.

### 💡 كيفية الحل:
- استخدم `raise ValueError("date error")` بدل `raise "date error"`.
- يعني لازم ترمي كائن من نوع Exception مش مجرد نص.

---

## 🔴 باغ #5: الـ Validator بتاع `due_date` بيدور على مفتاح غلط

### 📍 مكان الخطأ:
```python
# سطر 27-34
@validator("due_date")
def val_due_date(cls, due, values):
    start = values.get("start_date")    # ← المشكلة هنا
    if start and due and due < start:
        raise ValueError("due_date must be after start_date")
    return due
```

### 🔍 شرح المشكلة:
الـ validator بيدور على `start_date` في الـ `values` لكن الحقل اسمه `StartDate` (بحرف كبير) في الـ Schema.
يعني `values.get("start_date")` هترجع `None` دايمًا ومش هتلاقي القيمة.
وبالتالي الـ validation مش هيشتغل أبدًا — يعني ممكن الـ `due_date` يكون قبل الـ `start_date` ومحدش يلاحظ.

### 💡 كيفية الحل:
- غيّر `values.get("start_date")` لـ `values.get("StartDate")` عشان يطابق اسم الحقل الفعلي.
- أو الأفضل: وحّد الأسماء كلها (خليها كلها `snake_case`).

---

## 🟡 باغ #6: الـ `description` validator بيبدّل المسافات بـ underscores

### 📍 مكان الخطأ:
```python
# سطر 25
final = re.sub(" ", "_", x)
```

### 🔍 شرح المشكلة:
الـ validator بيحول كل المسافات في الوصف لـ underscores.
مثلاً: `"Go to the mall"` هيتحول لـ `"Go_to_the_mall"`.
ده سلوك غريب ومش منطقي — المستخدم مش هيتوقع إن وصف المهمة بتاعه يتغير بالشكل ده.
كمان، استخدام `re.sub` لمجرد تبديل حرف واحد ده overhead — ممكن تستخدم `.replace()` العادية.

### 💡 كيفية الحل:
- فكر لو فعلاً محتاج تبدّل المسافات. في الغالب، المستخدم عايز الوصف زي ما هو.
- لو محتاج تنظف النص، ممكن تكتفي بـ `.strip()` بس.
- لو لازم تبدّل، استخدم `.replace(" ", "_")` بدل `re.sub`.

---

## 🟡 باغ #7: عدم تناسق أسماء الحقول (Naming Inconsistency)

### 📍 مكان الخطأ:
```python
# سطر 16
StartDate: Optional[date] = Field(None, alias="StartDate")
# سطر 19
task_status: Optional[TaskStatus] = Field(TaskStatus.ToDo)
```

### 🔍 شرح المشكلة:
في تناقض في تسمية الحقول:
- `StartDate` بـ PascalCase.
- `due_date` بـ snake_case.
- `task_status` بـ snake_case.
ده بيعمل لخبطة وصعب تعرف إيه الاسم الصحيح لكل حقل.
كمان، `StartDate` عنده `alias` بنفس اسمه وده ملوش لازمة.

### 💡 كيفية الحل:
- وحّد كل الأسماء بـ `snake_case` (زي `start_date`).
- شيل الـ `alias` اللي ملهاش لازمة.
- تأكد إن الأسماء في الـ Schema متوافقة مع الأسماء في الـ Database Model.

---
