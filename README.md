# 🔐 Secure Session Management System (FastAPI)

A security-focused authentication system built with FastAPI, implementing **robust session management, JWT authentication, token rotation, and CSRF protection**.

This project demonstrates how modern web applications defend against common attack vectors such as **session hijacking, token replay, and CSRF attacks**.

---

## 🚀 Features

* ✅ User Login with secure password hashing (bcrypt)
* ✅ Server-side session management (database-backed)
* ✅ JWT Access Tokens (short-lived)
* ✅ Refresh Tokens with **rotation**
* ✅ Session invalidation on logout
* ✅ CSRF protection using **double-submit cookie pattern**
* ✅ Protected routes (`/me`)
* ✅ Secure cookie handling (`HttpOnly`, `SameSite`)

---

## 🧠 Security Concepts Demonstrated

This project focuses on **real-world attack surfaces**:

| Concept                 | Implementation                              |
| ----------------------- | ------------------------------------------- |
| Session Management      | Server-side session store (`session_db`)    |
| Token Rotation          | Refresh tokens replaced on every `/refresh` |
| Token Replay Detection  | Invalidates session on reuse                |
| CSRF Protection         | Cookie + Header validation                  |
| Session Invalidation    | Logout + token mismatch                     |
| Secure Password Storage | bcrypt hashing                              |

---

## 🏗️ Architecture Overview

```
Client (Browser)
   ↓
FastAPI Backend
   ↓
Session Store (In-Memory DB)
```

### Flow:

1. User logs in → session created
2. Access + refresh tokens issued as cookies
3. Protected routes validate:

   * JWT token
   * Session ID
4. Refresh endpoint rotates tokens
5. Logout invalidates session

---

## 📂 Project Structure

```
.
├── main.py        # FastAPI routes
├── auth.py        # Authentication logic (JWT, hashing)
├── models.py      # Session model
├── database.py    # In-memory database
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/Devine-byte/SecureAuth_FastAPI.git
cd SecureAuth_FastAPI
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn python-jose passlib[bcrypt]
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

---

## 🧪 Testing the Application

### 1. Open API docs

```
http://127.0.0.1:8000/docs
```

### 2. Test flow:

* `POST /login`
* `GET /me`
* `POST /refresh`
* `POST /logout`

---

## CSRF Testing

To successfully call `/logout`, include:

```
Header: X-CSRF-Token = csrf_token (from cookies)
```

---

## Security Notes

* Tokens are stored in **HttpOnly cookies** to reduce XSS risk
* CSRF protection prevents unauthorized requests from external sites
* Refresh token reuse triggers **session invalidation**
* Sessions are server-controlled (not purely stateless)

---

## Limitations (Intentional for Learning)

* In-memory database (not persistent)
* No HTTPS (required for `Secure` cookies in production)
* No rate limiting or brute-force protection

---

## Author

**Oghosa Divine Osaigbovo**

* GitHub: https://github.com/DeVine-byte

---

##  Why This Project Matters

Many applications implement authentication incorrectly.

This project demonstrates:

* How attackers exploit weak session logic
* How to properly defend against them
* How to design **secure authentication flows from scratch**

---

## Bonus: Threat Model (Simplified)

| Threat              | Mitigation                            |
| ------------------- | ------------------------------------- |
| Session Hijacking   | HttpOnly cookies + session validation |
| Token Replay        | Refresh token rotation                |
| CSRF                | Double-submit cookie                  |
| Credential Theft    | bcrypt hashing                        |
| Unauthorized Access | Session + JWT validation              |

---
