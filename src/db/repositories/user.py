from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for performing database operations on User models."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the user repository with the database session."""
        super().__init__(model=User, session=session)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Retrieve a user by their Telegram ID.

        Args:
            telegram_id: The Telegram ID of the user.

        Returns:
            The User instance if found, otherwise None.
        """
        query = select(self.model).where(self.model.telegram_id == telegram_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
