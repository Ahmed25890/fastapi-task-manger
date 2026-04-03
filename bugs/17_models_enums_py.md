# 🐛 الأخطاء البرمجية في ملف `app/models/enums.py`

> **المسار:** `app/models/enums.py`

---

## 🟡 باغ #1: `StrEnum` محتاج Python 3.11+

### 📍 مكان الخطأ:
```python
from enum import StrEnum
```

### 🔍 شرح المشكلة:
`StrEnum` اتضاف في Python 3.11. لو حد شغّل المشروع على Python 3.10 أو أقل، هيطلع `ImportError`.
أنت مستخدم Python 3.12 في الـ Dockerfile فالمشكلة مش كبيرة، لكن لو حد تاني شغّل المشروع على نسخة أقدم هيقع.

### 💡 كيفية الحل:
- لو عايز تدعم نسخ أقدم: استخدم `str, Enum` بدل `StrEnum`.
- أو حدد الحد الأدنى لنسخة Python في `requirements.txt` أو `pyproject.toml`.

---

## 🟡 باغ #2: الـ Enums مش مستخدمين في Database Model

### 🔍 شرح المشكلة:
عندك `Priority` و `TaskStatus` enums جاهزين، لكن في `db/models.py` الأعمدة معرّفة كـ `String` مش كـ `Enum`.
يعني الـ validation على مستوى الداتابيز مش موجود.

### 💡 كيفية الحل:
- استخدم `Column(SQLAlchemyEnum(Priority))` بدل `Column(String(10))`.

---
