from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Application, ApplicationStatus
from src.db.repositories.base import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    """Repository for performing database operations on Application models."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the application repository with the database session."""
        super().__init__(model=Application, session=session)

    async def get_unseen_vacancy_id(self, user_id: int) -> int | None:
        """Get the ID of the first unseen (NEW) vacancy for a user."""
        query = (
            select(self.model.vacancy_id)
            .where(self.model.user_id == user_id)
            .where(self.model.status == ApplicationStatus.NEW)
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
