# 🐛 الأخطاء البرمجية في ملف `app/core/config.py`

> **المسار:** `app/core/config.py`

---

## 🟡 باغ #1: مفيش قيم افتراضية (Default Values)

### 📍 مكان الخطأ:
```python
class Settings(BaseSettings):
    app_name: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
```

### 🔍 شرح المشكلة:
كل الحقول مطلوبة من غير قيم افتراضية. لو أي واحد فيهم مش موجود في `.env`، البرنامج هيقع فورًا بـ `ValidationError`.
ده مش مشكلة كبيرة (لأنه أحسن من إنه يشتغل بقيم غلط)، لكن بعض الحقول زي `ALGORITHM` ممكن يكون ليها قيمة افتراضية.

### 💡 كيفية الحل:
- ضيف قيم افتراضية للحقول اللي ينفع: مثلاً `ALGORITHM: str = "HS256"`.
- خلّي الحقول الحساسة زي `SECRET_KEY` و `DATABASE_URL` من غير default عشان تجبر المطوّر يعرّفها.

---

## 🟡 باغ #2: الـ `Settings` معرّف لكن مش مستخدم في كل الملفات

### 🔍 شرح المشكلة:
عندك `settings = Settings()` جاهز، لكن ملفات زي `auth.py` و `session.py` و `get_current_user_file.py` بتقرأ `.env` يدوي باستخدام `os.getenv()` و `load_dotenv()`.
يعني الـ configuration مقسومة على طريقتين مختلفتين وده ممكن يسبب تناقض.

### 💡 كيفية الحل:
- وحّد كل الملفات عشان تستخدم `settings` من `config.py`.
- شيل كل `load_dotenv()` و `os.getenv()` من الملفات التانية.

---
