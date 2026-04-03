# 🐛 الأخطاء البرمجية في ملف `app/models/user.py`

> **المسار:** `app/models/user.py`

---

## 🟡 باغ #1: استخدام `class Config` القديم بدل `model_config`

### 📍 مكان الخطأ:
```python
# سطر 9-12
class UserBase(BaseModel):
    user_name: str = Field(min_length=1, max_length=80)
    class Config:
         str_strip_whitespace = True
```

### 🔍 شرح المشكلة:
في Pydantic V2، الطريقة القديمة `class Config` لسه بتشتغل لكنها **مهملة (deprecated)**.
الطريقة الجديدة هي استخدام `model_config = ConfigDict(...)` زي ما عملت في ملفات تانية (مثلاً `TaskBase`).
الغريب إنك في ملف `tasks.py` استخدمت الطريقة الجديدة وهنا استخدمت القديمة — يعني مفيش توحيد.

### 💡 كيفية الحل:
- استبدل `class Config` بـ `model_config = ConfigDict(str_strip_whitespace=True)`.
- تأكد إنك مستورد `ConfigDict` من `pydantic`.
- وحّد الأسلوب في كل الملفات.

---

## 🟡 باغ #2: الـ `CreateUser` بيورّث من `UserPrivate` وده مشكلة

### 📍 مكان الخطأ:
```python
# سطر 18-19
class UserPrivate(UserPublic):
    email: EmailStr
# سطر 24-25
class CreateUser(UserPrivate):
    password: str = Field(min_length=6, max_length=100)
```

### 🔍 شرح المشكلة:
`CreateUser` بيورّث من `UserPrivate` اللي بدوره بيورّث من `UserPublic`.
`UserPublic` فيه `user_id: int` — يعني `CreateUser` بيطلب `user_id` كمان!
لكن لما المستخدم بيعمل تسجيل، هو مش المفروض يبعت `user_id` لأن الـ ID بيتولّد تلقائي من قاعدة البيانات.
ده معناه إن الـ API هيرفض الطلب لو المستخدم مبعتش `user_id`، أو هيبعت قيمة وممكن تتعارض مع الـ auto-increment.

### 💡 كيفية الحل:
- خلّي `CreateUser` يورّث من `UserBase` مباشرة وزوّد عليه الحقول اللي محتاجها بس (`email` و `password`).
- أو اعمل Schema جديد مخصوص لإنشاء المستخدم من غير `user_id`.

---

## 🟡 باغ #3: `UserInDB` معرّف لكن مش مستخدم

### 📍 مكان الخطأ:
```python
# سطر 20-21
class UserInDB(UserPrivate):
    hashed_password: str
```

### 🔍 شرح المشكلة:
الـ Schema ده معرّف لكن مش مستخدم في أي مكان في المشروع.
كمان، عنده مشكلة تصميم: بيورّث من `UserPrivate` اللي فيه `user_id` و `email`،
وبيضيف `hashed_password` — لكن مفيش أي حد بيستخدمه.

### 💡 كيفية الحل:
- لو مش محتاجه: احذفه عشان تنظف الكود.
- لو محتاجه: استخدمه في الأماكن المناسبة (مثلاً للتعامل مع بيانات المستخدم الداخلية).

---

## 🟡 باغ #4: `UserUpdate` بيورّث من `CreateUser` وده مش مناسب

### 📍 مكان الخطأ:
```python
# سطر 28-29
class UserUpdate(CreateUser):
    pass
```

### 🔍 شرح المشكلة:
`UserUpdate` بيورّث من `CreateUser` بدون أي تعديل (`pass`).
لكن `CreateUser` فيه `user_id` (بسبب سلسلة الوراثة)، وكل الحقول **مطلوبة (required)**.
في عملية التحديث، المفروض الحقول تكون **اختيارية (Optional)** — يعني المستخدم يقدر يحدّث الحقول اللي عايز يغيرها بس.

### 💡 كيفية الحل:
- اعمل Schema منفصل للتحديث فيه الحقول كلها `Optional`.
- شيل `user_id` من الـ Schema لأنه بيجي من الـ authentication.
- استخدم `model.model_dump(exclude_unset=True)` عشان تحدّث الحقول اللي المستخدم بعتها بس.

---
