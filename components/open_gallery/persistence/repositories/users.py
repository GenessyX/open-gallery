from typing import override

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from open_gallery.hashing.interface import HashedValue
from open_gallery.identity.entities import RefreshToken, User, UserId, VerificationCode
from open_gallery.identity.repository import UserRepository
from open_gallery.persistence.repository import SQLAlchemyRepository
from open_gallery.persistence.tables.users import refresh_tokens, users, verification_codes
from open_gallery.shared.types import Email, SecretValue


class SQLAlchemyUserRepository(SQLAlchemyRepository[UserId, User], UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, table=users, entity=User)

    @override
    async def get_by_email(self, email: str) -> list[User]:
        stmt = select(User).where(users.c.email == email)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    @override
    async def get_verified_by_email(self, email: Email) -> User | None:
        stmt = select(User).where(and_(users.c.email == email, users.c.verified.is_(True)))
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

    @override
    async def get_by_refresh_token(self, hashed_token: SecretValue[HashedValue]) -> User | None:
        stmt = (
            select(User)
            .join(
                RefreshToken,
                onclause=users.c.id == refresh_tokens.c.user_id,
            )
            .where(refresh_tokens.c.token_hash == hashed_token)
            .options(contains_eager(User.refresh_tokens))  # type: ignore[arg-type]
        )
        result = await self._session.execute(stmt)
        return result.scalar()
