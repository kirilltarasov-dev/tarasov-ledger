from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.transaction import Transaction
from app.services import ocr, parser
from sqlalchemy.future import select
import uuid

router = APIRouter()


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    contents = await file.read()
    raw_text = ocr.extract_text_from_image(contents)
    parsed = parser.parse_text(raw_text)

    tx = Transaction(
        id=uuid.uuid4(),
        raw_text=raw_text,
        filename=file.filename,
        content_type=file.content_type,
        vendor=parsed.vendor,
        amount=parsed.amount,
        amount_currency=parsed.amount_currency,
        date=parsed.date,
        category=parsed.category,
    )
    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return {
        "id": str(tx.id),
        "raw_text": tx.raw_text,
        "vendor": tx.vendor,
        "amount": tx.amount,
        "amount_currency": tx.amount_currency,
        "date": tx.date,
        "category": tx.category,
    }
