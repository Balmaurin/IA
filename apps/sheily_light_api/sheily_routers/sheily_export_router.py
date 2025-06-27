"""Router to trigger export of training batches to SHEILY-CORE."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db_dep
from ..models import User
from ..sheily_modules.sheily_learning_exporter.exporter import export_training_batch

router = APIRouter(prefix="/export", tags=["export"])


@router.post("/batch")
def export_batch(user: User = Depends(get_current_user), db: Session = Depends(get_db_dep)):
    return export_training_batch(user, db)
