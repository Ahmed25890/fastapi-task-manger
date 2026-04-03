# 🐛 الأخطاء البرمجية في ملف `app/services/rate_limiter.py`

> **المسار:** `app/services/rate_limiter.py`

---

## 🔴 باغ #1: تعارض اسم المتغير مع الاستيراد (Name Shadowing)

### 📍 مكان الخطأ:
```python
from slowapi import Limiter
Limiter = Limiter(key_func=get_remote_address)
```

### 🔍 شرح المشكلة:
في السطر الأول، بتستورد **الكلاس** `Limiter`.
في السطر التاني، بتعمل **instance** وسميتها `Limiter` بنفس الاسم!
كده لو حد حاول يعمل `Limiter()` تاني، مش هيقدر لأن `Limiter` بقى instance مش class.
كمان، لو استوردت `Limiter` في `main.py`، أنت هتستورد الـ instance مش الكلاس.

### 💡 كيفية الحل:
- سمّ الـ instance اسم تاني بحرف صغير: `limiter = Limiter(key_func=get_remote_address)`.

---

## 🟡 باغ #2: `slowapi` مش في `requirements.txt`

### 🔍 شرح المشكلة:
الملف بيستخدم `slowapi` لكنه مش موجود في `requirements.txt`.

### 💡 كيفية الحل:
- ضيف `slowapi` في `requirements.txt`.

---

## 🟡 باغ #3: الـ Rate Limiter مش مستخدم

### 🔍 شرح المشكلة:
الـ Limiter معرّف لكن مش مضاف للـ app ومش مستخدم في أي endpoint.
عشان يشتغل، لازم تضيفه للـ FastAPI app وتضيف decorators على الـ endpoints.

### 💡 كيفية الحل:
- في `main.py`: ضيف `app.state.limiter = limiter`.
- ضيف `app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)`.
- على كل endpoint عايز تحدده: ضيف `@limiter.limit("5/minute")`.

---
