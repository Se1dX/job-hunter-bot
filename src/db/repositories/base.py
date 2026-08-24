from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Base


class BaseRepository[ModelType: Base]:
    """Base repository providing generic CRUD operations."""

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        """Initialize the repository with a specific model and database session.

        Args:
            model: The SQLAlchemy declarative model class.
            session: The active asynchronous database session.
        """
        self.model = model
        self.session = session

    async def get_by_id(self, id: int) -> ModelType | None:
        """Retrieve a single record by its primary key.

        Args:
            id: The primary key of the record.

        Returns:
            The model instance if found, otherwise None.
        """
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, obj: ModelType) -> ModelType:
        """Add a new record to the database.

        Args:
            obj: The model instance to add.

        Returns:
            The added model instance.
        """
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def delete(self, obj: ModelType) -> None:
        """Delete a record from the database.

        Args:
            obj: The model instance to delete.
        """
        await self.session.delete(obj)
        await self.session.flush()
