#import modules

from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from database import user_db, session_db
from auth import (
    verify_passwd,
    create_accessToken,
    decode_token,
    generate_refresh_token,
    secrets
)

from models import Session

app = FastAPI()



# CSRF PROTECTION

def verify_csrf(request: Request):
    csrf_cookie = request.cookies.get("csrf_token")
    csrf_header = request.headers.get("X-CSRF-Token")

    if not csrf_cookie or not csrf_header:
        raise HTTPException(status_code=403, detail="CSRF missing")

    if csrf_cookie != csrf_header:
        raise HTTPException(status_code=403, detail="CSRF invalid")



# LOGIN

@app.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):

    user = user_db.get(form_data.username)

    if not user or not verify_passwd(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create session
    session = Session(user_id=user["id"])

    # Tokens
    access_token = create_accessToken({
        "sub": user["email"],
        "sid": session.id
    })

    refresh_token = generate_refresh_token()
    session.refresh_token = refresh_token

    # Store session
    session_db[session.id] = session

    # CSRF token
    csrf_token = secrets.token_urlsafe(16)

    # Cookies
    response.set_cookie("csrf_token", csrf_token)
    response.set_cookie("access_token", access_token, httponly=True, samesite="Strict")
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")
    response.set_cookie("session_id", session.id, httponly=True, samesite="Strict")

    return {"message": "logged in"}



# GET CURRENT USER

def get_current_user(request: Request):

    token = request.cookies.get("access_token")
    session_id = request.cookies.get("session_id")

    if not token or not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    session = session_db.get(session_id)

    if not session or not session.is_active:
        raise HTTPException(status_code=401, detail="Invalid session")

    email = payload.get("sub")

    return user_db.get(email)


@app.get("/me")
def me(user=Depends(get_current_user)):
    return user



# REFRESH TOKEN (ROTATION)

@app.post("/refresh")
def refresh(request: Request, response: Response):

    session_id = request.cookies.get("session_id")
    refresh_token = request.cookies.get("refresh_token")

    session = session_db.get(session_id)

    if not session or not session.is_active:
        raise HTTPException(status_code=401, detail="Invalid session")

    if session.refresh_token != refresh_token:
        session.is_active = False
        raise HTTPException(status_code=401, detail="Token reuse detected")

    # Rotate refresh token
    new_refresh_token = generate_refresh_token()
    session.refresh_token = new_refresh_token

    # New access token
    access_token = create_accessToken({
        "sub": session.user_id,
        "sid": session.id
    })

    response.set_cookie("access_token", access_token, httponly=True, samesite="Strict")
    response.set_cookie("refresh_token", new_refresh_token, httponly=True, samesite="Strict")

    return {"message": "Token refreshed"}



# LOGOUT

@app.post("/logout")
def logout(request: Request, response: Response):

    verify_csrf(request)  # MUST be first

    session_id = request.cookies.get("session_id")

    session = session_db.get(session_id)

    if session:
        session.is_active = False

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("session_id")
    response.delete_cookie("csrf_token")

    return {"message": "Logged out"}
