from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database, auth
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_pw = auth.hash_password(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Simulate encrypted URL
    verify_url = f"/users/verify-email/{new_user.id}"
    return JSONResponse(status_code=201, content={
        "id": new_user.id,
        "email": new_user.email,
        "role": new_user.role,
        "is_verified": new_user.is_verified,
        "verify_url": verify_url  # simulate "encrypted URL"
    })

@router.get("/verify-email/{user_id}")
def verify_email(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()
    return {"message": "Email successfully verified."}

@router.post("/login", response_model=schemas.Token)
def login(creds: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == creds.email).first()
    if not user or not auth.verify_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email.")

    access_token = auth.create_access_token(
        data={"user_id": user.id, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}
