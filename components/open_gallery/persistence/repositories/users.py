from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from open_gallery.identity.entities import User, UserId, VerificationCode
from open_gallery.identity.repository import UserRepository
from open_gallery.persistence.repository import SQLAlchemyRepository
from open_gallery.persistence.tables.users import users, verification_codes


class SQLAlchemyUserRepository(SQLAlchemyRepository[UserId, User], UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, table=users, entity=User)

    @override
    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(users.c.email == email)
        result = await self._session.execute(stmt)
        return result.scalar()

    @override
    async def get_by_code(self, code: str) -> User | None:
        stmt = (
            select(User)
            .join(
                VerificationCode,
                onclause=users.c.id == verification_codes.c.user_id,
            )
            .where(verification_codes.c.code == code)
            .options(contains_eager(User.verification_codes))  # type: ignore[arg-type]
        )
        result = await self._session.execute(stmt)
        return result.scalar()
