# ez-tech-backend-test



## 🔧 Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (can be swapped with PostgreSQL/MySQL)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Email Verification**: Simulated (can integrate real service)
- **File Handling**: Supports `.pptx`, `.docx`, `.xlsx` uploads
- **Postman**: Collection available (see below)

---

## 👤 User Roles

### 🛠 Ops User
- Can **login**
- Can **upload** `.pptx`, `.docx`, `.xlsx` files

### 👥 Client User
- Can **sign up** (returns encrypted URL)
- Can **verify email**
- Can **login**
- Can **list** available files
- Can **request encrypted download links**
- Can **download files** via secure URLs

---

## 🚀 Features

- 🔐 Secure JWT-based authentication
- 📁 File upload with extension checks
- 🔗 Download via encrypted URL (access controlled)
- ❌ Access denied for unauthorized roles
- ✅ Simulated email verification flow

---

## 📂 API Endpoints

### Auth
- `POST /users/signup`
- `POST /users/login`
- `GET /users/verify-email/{new_user.id}`

### Files
- `POST /files/upload` *(Ops Only)*
- `GET /files/list` *(Client Only)*
- `GET /files/download-link/{file_id}` *(Client Only)*
- `GET /files/download/{encrypted_link}}` *(Client Only)*

---
