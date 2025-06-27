from sqlalchemy.orm import Session
from apps.sheily_light_api.models import TokenBalance, User


def get_balance(db: Session, user: User) -> int:
    balance_row = db.query(TokenBalance).filter(TokenBalance.user_id == user.id).first()
    return balance_row.balance if balance_row else 0


def add_tokens(db: Session, user: User, amount: int):
    row = db.query(TokenBalance).filter(TokenBalance.user_id == user.id).first()
    if not row:
        row = TokenBalance(user_id=user.id, balance=0)
        db.add(row)
    row.balance += amount
    db.commit()
    return row.balance
