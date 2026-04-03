# 🐛 الأخطاء البرمجية في ملف `app/db/session.py`

> **المسار:** `app/db/session.py`

---

## 🟡 باغ #1: مفيش معالجة لحالة إن `DATABASE_URL` مش موجود

### 📍 مكان الخطأ:
```python
# سطر 8
DATABASE_URL = os.getenv("DATABASE_URL")
# سطر 10
engine = create_engine(DATABASE_URL, echo=False, future=True)
```

### 🔍 شرح المشكلة:
لو ملف `.env` مش موجود أو المتغير `DATABASE_URL` مش معرّف، `os.getenv` هيرجع `None`.
بعدها `create_engine(None)` هتطلع خطأ مش واضح:
`ArgumentError: Could not parse SQLAlchemy URL from string 'None'`.
المستخدم مش هيفهم إيه المشكلة بالظبط.

### 💡 كيفية الحل:
- ضيف شرط يتحقق إن `DATABASE_URL` مش `None` قبل ما تعمل `create_engine`.
- لو `None`، ارمي خطأ واضح بيقول إن المتغير مش معرّف في ملف `.env`.
- أو استخدم `Settings` من `config.py` بدل ما تقرأ الـ env يدوي — كده هتستفيد من تحقق Pydantic التلقائي.

---

## 🟡 باغ #2: تكرار في قراءة الـ Configuration

### 📍 مكان الخطأ:
```python
# session.py
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
```

### 🔍 شرح المشكلة:
عندك ملف `config.py` فيه `Settings` class بيقرأ كل الإعدادات من `.env` باستخدام `pydantic-settings`.
لكن في `session.py` بتقرأ `DATABASE_URL` تاني يدوي باستخدام `os.getenv()` و `load_dotenv()`.
ده تكرار (DRY violation) وممكن يسبب تناقض لو الإعدادات اتغيرت.

### 💡 كيفية الحل:
- استخدم `settings.DATABASE_URL` من `app.core.config` بدل ما تقرأ `.env` يدوي.
- شيل استيراد `os` و `dotenv` لأنك مش محتاجهم.
- كده كل الإعدادات بتيجي من مكان واحد.

---

## 🟢 باغ #3: استخدام `declarative_base()` القديمة

### 📍 مكان الخطأ:
```python
# سطر 19
Base = declarative_base()
```

### 🔍 شرح المشكلة:
في SQLAlchemy 2.0+، `declarative_base()` بقت مهملة (deprecated).
الطريقة الجديدة هي استخدام `DeclarativeBase` class.
هتشتغل عادي دلوقتي لكن ممكن تتشال في نسخ جاية.

### 💡 كيفية الحل:
- اعمل class جديد يورّث من `DeclarativeBase` بدل ما تستخدم `declarative_base()`.
- استورد `DeclarativeBase` من `sqlalchemy.orm`.

---

## 🟢 باغ #4: `future=True` ملهوش لازمة

### 📍 مكان الخطأ:
```python
# سطر 10
engine = create_engine(DATABASE_URL, echo=False, future=True)
# سطر 16
future=True
```

### 🔍 شرح المشكلة:
في SQLAlchemy 2.0، `future=True` هو السلوك الافتراضي خلاص.
كان مهم في SQLAlchemy 1.4 عشان تفعّل الأسلوب الجديد، لكن دلوقتي مش محتاجه.

### 💡 كيفية الحل:
- ممكن تشيله عشان تنظف الكود — مش هيأثر على أي حاجة.

---
