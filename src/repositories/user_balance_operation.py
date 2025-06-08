from sqlalchemy import insert

from src.core.models import UserBalanceOperationModel
from src.schemas.dto.user_balance_operation import UserBalanceOperationCreateDTO

from .base import BaseRepository


class UserBalanceOperationRepository(BaseRepository[UserBalanceOperationModel]):
    _model_class = UserBalanceOperationModel

    async def create(
        self,
        user_id: int,
        operator_id: int,
        *,
        operation_create_dto: UserBalanceOperationCreateDTO,
    ) -> None:
        create_data = operation_create_dto.model_dump()
        query = (
            insert(UserBalanceOperationModel)
            .values(user_id=user_id, operator_id=operator_id, **create_data)
            .returning(UserBalanceOperationModel)
        )
        await self._execute(query)
