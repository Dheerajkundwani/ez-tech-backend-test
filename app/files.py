from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, database, auth
from app.auth import get_current_user
import shutil, os
import uuid
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Only OPS can upload
    if current_user.role != models.Role.ops:
        raise HTTPException(status_code=403, detail="Only Ops users can upload.")

    # Check file extension
    if not file.filename.endswith((".pptx", ".docx", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only pptx, docx, xlsx files allowed.")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id + "_" + file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.File(
        filename=file.filename,
        path=file_path,
        uploader_id=current_user.id
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"message": "File uploaded", "file_id": new_file.id}

@router.get("/list", response_model=list[schemas.FileOut])
def list_files(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != models.Role.client:
        raise HTTPException(status_code=403, detail="Only client users can view files.")
    return db.query(models.File).all()

@router.get("/download-link/{file_id}", response_model=schemas.DownloadLink)
def get_download_link(
    file_id: int,
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != models.Role.client:
        raise HTTPException(status_code=403, detail="Only clients can get download link.")

    encrypted_path = str(uuid.uuid4())  # simulate encryption
    download_map[encrypted_path] = {
        "file_id": file_id,
        "user_id": current_user.id
    }
    return {
        "download_link": f"/files/download/{encrypted_path}",
        "message": "success"
    }

# Temporary store for download links
download_map = {}

@router.get("/download/{encrypted_link}")
def download_file(
    encrypted_link: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    entry = download_map.get(encrypted_link)
    if not entry:
        raise HTTPException(status_code=404, detail="Invalid or expired link")

    if entry["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    file = db.query(models.File).filter(models.File.id == entry["file_id"]).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = file.path  # already saved during upload

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    return FileResponse(
        path=file_path,
        filename=file.filename,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file.filename}"'}
    ) 