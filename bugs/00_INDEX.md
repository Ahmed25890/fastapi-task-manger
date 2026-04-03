# 📋 فهرس الأخطاء البرمجية (Bugs Index)

> **مشروع:** Task Manager FastAPI App
> **تاريخ التحليل:** 2026-04-02

---

## 📊 إحصائيات سريعة

| النوع | العدد |
|------|------|
| 🔴 أخطاء حرجة (Critical) | 18 |
| 🟡 أخطاء متوسطة (Medium) | 25 |
| 🟢 ملاحظات (Low) | 4 |
| **المجموع** | **47** |

---

## 📁 قائمة الملفات

| # | الملف | عدد الأخطاء | الأخطاء الحرجة | ملف التقرير |
|---|-------|-------------|---------------|------------|
| 01 | `main.py` | 4 | 2 | [01_main_py.md](./01_main_py.md) |
| 02 | `app/models/tasks.py` | 7 | 4 | [02_models_tasks_py.md](./02_models_tasks_py.md) |
| 03 | `app/models/user.py` | 4 | 0 | [03_models_user_py.md](./03_models_user_py.md) |
| 04 | `app/db/models.py` | 4 | 0 | [04_db_models_py.md](./04_db_models_py.md) |
| 05 | `app/db/session.py` | 4 | 0 | [05_db_session_py.md](./05_db_session_py.md) |
| 06 | `app/api/tasks.py` | 6 | 4 | [06_api_tasks_py.md](./06_api_tasks_py.md) |
| 07 | `app/api/user.py` | 8 | 3 | [07_api_user_py.md](./07_api_user_py.md) |
| 08 | `app/services/tasks.py` | 5 | 3 | [08_services_tasks_py.md](./08_services_tasks_py.md) |
| 09 | `app/services/user_service.py` | 5 | 1 | [09_services_user_service_py.md](./09_services_user_service_py.md) |
| 10 | `app/services/authentication/auth.py` | 5 | 1 | [10_auth_py.md](./10_auth_py.md) |
| 11 | `app/services/authentication/get_current_user_file.py` | 3 | 1 | [11_get_current_user_file_py.md](./11_get_current_user_file_py.md) |
| 12 | `app/services/login.py` | 4 | 2 | [12_services_login_py.md](./12_services_login_py.md) |
| 13 | `app/services/register.py` | 3 | 1 | [13_services_register_py.md](./13_services_register_py.md) |
| 14 | `app/services/cache.py` | 2 | 1 | [14_services_cache_py.md](./14_services_cache_py.md) |
| 15 | `app/services/rate_limiter.py` | 3 | 1 | [15_services_rate_limiter_py.md](./15_services_rate_limiter_py.md) |
| 16 | `app/core/config.py` | 2 | 0 | [16_core_config_py.md](./16_core_config_py.md) |
| 17 | `app/models/enums.py` | 2 | 0 | [17_models_enums_py.md](./17_models_enums_py.md) |
| 18 | `Dockerfile` | 3 | 0 | [18_dockerfile.md](./18_dockerfile.md) |
| 19 | `requirements.txt` و `.env` | 3 | 0 | [19_requirements_and_env.md](./19_requirements_and_env.md) |

---

## 🔥 أهم المشاكل اللي لازم تتحل الأول

### 1. مسارات الاستيراد (Import Paths) — في كل الملفات تقريبًا
كل الملفات بتستخدم مسارات استيراد غلط (مش بتبدأ بـ `app.`). ده **أهم مشكلة** لأن البرنامج مش هيشتغل أصلاً بدون حلها.

### 2. `get_current_user_file.py` — معطّل بالكامل
الملف ده بيستخدم أسماء قديمة (`database`, `crud`) مش موجودة. لازم يتحدّث أو ينقل لملف `auth.py`.

### 3. `raise "date error"` في `models/tasks.py`
بايثون مش بيقبل `raise` لـ string. ده `TypeError` مباشر.

### 4. Shadowing في `main.py`
`tasks` بيتغطى على نفسه ومش هتقدر تستخدم الـ service والـ router صح.

### 5. مفيش Authorization (التحقق من الملكية)
أي مستخدم مسجّل يقدر يشوف أو يعدّل أو يحذف بيانات أي مستخدم تاني.

---

## 📖 دليل الرموز

| الرمز | المعنى |
|------|--------|
| 🔴 | خطأ حرج — البرنامج مش هيشتغل أو هيطلع خطأ runtime |
| 🟡 | خطأ متوسط — ممكن يسبب مشاكل أو سلوك غير متوقع |
| 🟢 | ملاحظة — تحسين أو best practice |

---
