from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.transaction import Transaction
from app.services.ocr import extract_text_from_image
from sqlalchemy.future import select
import uuid

router = APIRouter()


@router.post("/")
async def upload_image(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Only JPEG and PNG formats are supported"
        )

    content = await file.read()
    raw_text = extract_text_from_image(content)

    transaction = Transaction(
        id=uuid.uuid4(),
        raw_text=raw_text,
        filename=file.filename,
        content_type=file.content_type,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)

    return {"id": str(transaction.id), "raw_text": raw_text}
