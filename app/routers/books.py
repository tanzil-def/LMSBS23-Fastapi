from fastapi import (
    APIRouter, Depends, HTTPException, status, Request,
    UploadFile, File, Form
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os, shutil

from app.db.session import get_db
from app.schemas.book import BookResponse, BookFormatEnum
from app.crud import book as crud_book
from app.dependencies import require_admin
from app.models.user import User

router = APIRouter(tags=["Book Management📖"])

# ------------------------------
# Media directories
# ------------------------------
MEDIA_DIR = os.path.join(os.getcwd(), "media")
COVER_DIR = os.path.join(MEDIA_DIR, "covers")
PDF_DIR = os.path.join(MEDIA_DIR, "pdfs")
AUDIO_DIR = os.path.join(MEDIA_DIR, "audio")

os.makedirs(COVER_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)


def save_file(upload_file: UploadFile, folder: str) -> str:
    """Save uploaded file into media folder and return filename."""
    filename = upload_file.filename
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return filename  # only filename is stored in DB


# ------------------------------
# Public Endpoints
# ------------------------------

@router.get("/list", response_model=List[dict])
def list_books(db: Session = Depends(get_db), request: Request = None):
    books = crud_book.get_all_books(db)
    return [BookResponse.as_response(b, request) for b in books]


@router.get("/{id}/is_available")
def check_availability(id: int, db: Session = Depends(get_db)):
    available = crud_book.is_book_available(db, id)
    if available is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book_id": id, "is_available": available}


@router.get("/search", response_model=List[dict])
def search_books(q: str, db: Session = Depends(get_db), request: Request = None):
    all_books = crud_book.get_all_books(db)
    filtered = [b for b in all_books if q.lower() in b.title.lower() or q.lower() in b.author.lower()]
    return [BookResponse.as_response(b, request) for b in filtered]


@router.get("/retrieve/{id}", response_model=dict)
def retrieve_book(id: int, db: Session = Depends(get_db), request: Request = None):
    book = crud_book.get_book(db, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.as_response(book, request)


@router.get("/recommended-books", response_model=List[dict])
def recommended_books(db: Session = Depends(get_db), request: Request = None):
    books = crud_book.get_recommended_books(db)
    return [BookResponse.as_response(b, request) for b in books]


@router.get("/popular-books", response_model=List[dict])
def popular_books(db: Session = Depends(get_db), request: Request = None):
    books = crud_book.get_popular_books(db)
    return [BookResponse.as_response(b, request) for b in books]


@router.get("/new-collection", response_model=List[dict])
def new_collection(db: Session = Depends(get_db), request: Request = None):
    books = crud_book.get_new_collection(db)
    return [BookResponse.as_response(b, request) for b in books]


@router.get("/category/{categoryId}", response_model=List[dict])
def filter_by_category(categoryId: int, db: Session = Depends(get_db), request: Request = None):
    books = crud_book.get_books_by_category(db, categoryId)
    return [BookResponse.as_response(b, request) for b in books]


@router.get("/available", response_model=List[dict])
def available_books(db: Session = Depends(get_db), request: Request = None):
    all_books = crud_book.get_all_books(db)
    books = [b for b in all_books if b.copies_available > 0]
    return [BookResponse.as_response(b, request) for b in books]


# ------------------------------
# Admin-only Endpoints
# ------------------------------

@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(
    title: str = Form(...),
    author: str = Form(...),
    category_id: int = Form(1),
    format: BookFormatEnum = Form(...),
    copies_total: int = Form(1),
    copies_available: int = Form(1),
    description: Optional[str] = Form(None),

    # URL or File
    cover: Optional[str] = Form(None),
    pdf_file: Optional[str] = Form(None),
    audio_file: Optional[str] = Form(None),

    cover_file: Optional[UploadFile] = File(None),
    pdf_upload: Optional[UploadFile] = File(None),
    audio_upload: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
    request: Request = None,
):
    data = {
        "title": title,
        "author": author,
        "category_id": category_id,
        "format": format,
        "copies_total": copies_total,
        "copies_available": copies_available,
        "description": description,
    }

    # File upload > URL fallback
    if cover_file:
        data["cover"] = save_file(cover_file, COVER_DIR)
    elif cover:
        data["cover"] = cover

    if pdf_upload:
        data["pdf_file"] = save_file(pdf_upload, PDF_DIR)
    elif pdf_file:
        data["pdf_file"] = pdf_file

    if audio_upload:
        data["audio_file"] = save_file(audio_upload, AUDIO_DIR)
    elif audio_file:
        data["audio_file"] = audio_file

    book = crud_book.create_book(db, data)
    return BookResponse.as_response(book, request)


@router.put("/edit/{id}", response_model=dict)
def edit_book(
    id: int,
    title: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    format: Optional[BookFormatEnum] = Form(None),
    copies_total: Optional[int] = Form(None),
    copies_available: Optional[int] = Form(None),
    description: Optional[str] = Form(None),

    cover: Optional[str] = Form(None),
    pdf_file: Optional[str] = Form(None),
    audio_file: Optional[str] = Form(None),

    cover_file: Optional[UploadFile] = File(None),
    pdf_upload: Optional[UploadFile] = File(None),
    audio_upload: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
    request: Request = None,
):
    book_data = {}

    if title: book_data["title"] = title
    if author: book_data["author"] = author
    if category_id is not None: book_data["category_id"] = category_id
    if format: book_data["format"] = format
    if copies_total is not None: book_data["copies_total"] = copies_total
    if copies_available is not None: book_data["copies_available"] = copies_available
    if description: book_data["description"] = description

    if cover_file:
        book_data["cover"] = save_file(cover_file, COVER_DIR)
    elif cover:
        book_data["cover"] = cover

    if pdf_upload:
        book_data["pdf_file"] = save_file(pdf_upload, PDF_DIR)
    elif pdf_file:
        book_data["pdf_file"] = pdf_file

    if audio_upload:
        book_data["audio_file"] = save_file(audio_upload, AUDIO_DIR)
    elif audio_file:
        book_data["audio_file"] = audio_file

    book = crud_book.update_book(db, id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.as_response(book, request)


@router.delete("/delete/{id}")
def delete_book_endpoint(id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    result = crud_book.delete_book(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted successfully"}


# ------------------------------
# Serve PDF & Audio
# ------------------------------

@router.get("/download/pdf/{id}")
def download_pdf(id: int, db: Session = Depends(get_db)):
    book = crud_book.get_book(db, id)
    if not book or not book.pdf_file:
        raise HTTPException(status_code=404, detail="PDF not found")

    if book.pdf_file.startswith("http"):
        return {"pdf_url": book.pdf_file}

    return FileResponse(
        os.path.join(PDF_DIR, book.pdf_file),
        media_type="application/pdf",
        filename=os.path.basename(book.pdf_file)
    )

@router.get("/play/audio/{id}")
def play_audio(id: int, db: Session = Depends(get_db)):
    book = crud_book.get_book(db, id)
    if not book or not book.audio_file:
        raise HTTPException(status_code=404, detail="Audio not found")

    if book.audio_file.startswith("http"):
        return {"audio_url": book.audio_file}

    return FileResponse(
        os.path.join(AUDIO_DIR, book.audio_file),
        media_type="audio/mpeg",
        filename=os.path.basename(book.audio_file)
    )
