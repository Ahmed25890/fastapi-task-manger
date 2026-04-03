# 🐛 الأخطاء البرمجية في ملف `app/services/cache.py`

> **المسار:** `app/services/cache.py`

---

## 🔴 باغ #1: دوال الكاش فاضية (Not Implemented)

### 📍 مكان الخطأ:
```python
def get_cache(key: str):
    pass

def set_cache(key: str, value: str):
    pass
```

### 🔍 شرح المشكلة:
الدالتين `get_cache` و `set_cache` معرّفين لكن مفيش أي كود جواهم (`pass`).
كمان، الـ `cache` و الـ `cache_lock` معرّفين فوق لكن مش مستخدمين.
يعني الموديول ده مش بيعمل أي حاجة.

### 💡 كيفية الحل:
- اكتب كود الدوال: `get_cache` تقرأ من الـ cache و `set_cache` تكتب فيه.
- استخدم `cache_lock` عشان الـ thread safety.
- أو لو مش محتاج caching دلوقتي: احذف الملف.

---

## 🟡 باغ #2: `cachetools` مش في `requirements.txt`

### 🔍 شرح المشكلة:
الملف بيستخدم `cachetools` لكنه مش موجود في `requirements.txt`.
يعني لما حد يعمل `pip install -r requirements.txt`، مش هيتنصّب.

### 💡 كيفية الحل:
- ضيف `cachetools` في `requirements.txt`.

---
