from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Vacancy
from src.db.repositories.base import BaseRepository


class VacancyRepository(BaseRepository[Vacancy]):
    """Repository for performing database operations on Vacancy models."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the vacancy repository with the database session."""
        super().__init__(model=Vacancy, session=session)

    async def get_by_hh_id(self, hh_id: str) -> Vacancy | None:
        """Retrieve a vacancy by its HH.ru ID."""
        query = select(self.model).where(self.model.hh_id == hh_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
