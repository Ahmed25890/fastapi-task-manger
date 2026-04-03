# 🐛 الأخطاء البرمجية في ملف `app/services/authentication/get_current_user_file.py`

> **المسار:** `app/services/authentication/get_current_user_file.py`

---

## 🔴 باغ #1: مسارات الاستيراد كلها غلط

### 📍 مكان الخطأ:
```python
from database import get_db          # ← الاسم الصحيح db.session
from database import get_db          # ← مكرر!
from crud import GetUserByEmailSafe  # ← الاسم الصحيح services.user_service
```

### 🔍 شرح المشكلة:
- `database` مش اسم موديول موجود — الاسم الصحيح `app.db.session`.
- `crud` مش اسم موديول موجود — الاسم الصحيح `app.services.user_service`.
- السطر `from database import get_db` **مكرر مرتين** (سطر 4 و 7).
الملف ده مش هيشتغل أبدًا بسبب مشاكل الاستيراد دي.

### 💡 كيفية الحل:
- صلّح المسارات: `from app.db.session import get_db` و `from app.services.user_service import GetUserByEmailSafe`.
- احذف السطر المكرر.

---

## 🟡 باغ #2: تكرار تعريف `oauth2_scheme`

### 📍 مكان الخطأ:
```python
# في auth.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# في get_current_user_file.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
```

### 🔍 شرح المشكلة:
`oauth2_scheme` معرّف في **ملفين مختلفين** بنفس القيمة. ده تكرار وممكن يسبب لخبطة.

### 💡 كيفية الحل:
- عرّفه في مكان واحد (مثلاً `auth.py`) واستورده في الملفات التانية.

---

## 🟡 باغ #3: تكرار قراءة الـ Configuration يدوي

### 📍 مكان الخطأ:
```python
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
```

### 🔍 شرح المشكلة:
نفس الكود في `auth.py` بالظبط — تكرار! ونفس مشكلة `int(None)`.

### 💡 كيفية الحل:
- استخدم `settings` من `config.py` في الملفين.

---

## 🟢 ملاحظة: الملف كان من كود قديم

### 🔍 شرح المشكلة:
الملف ده فيه أسماء قديمة (`database`, `crud`) اللي يظهر إنه كان من نسخة قديمة من المشروع ومتحدّثش مع باقي الكود.
**الملف ده معطّل بالكامل** ومش هيشتغل بسبب مشاكل الاستيراد.

### 💡 كيفية الحل:
- الأفضل: انقل دالة `get_current_user` لملف `auth.py` واحذف الملف ده.
- أو: صلّح كل الاستيرادات وحدّث الأسماء.

---
