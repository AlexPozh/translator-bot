from db.base import BaseModel

from sqlalchemy import Integer, BigInteger, Column, String, ForeignKey


class TelegramUser(BaseModel):
    __tablename__ = "telegram_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # telegram user's id
    tg_user = Column(BigInteger, unique=True, nullable=False)
    # native lang of user
    lang_code = Column(String(8), nullable=False, default='en')
    # currrent target lang
    targ_lang_code = Column(String(8), nullable=False, default='en')
    
    def __str__(self):
        return f"Class TelegramUser.\nid - {self.id};\ntg_user - {self.tg_user};\nlang_code - {self.lang_code};\ntarg_lang_code - {self.targ_lang_code}."
    


