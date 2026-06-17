from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from reconx.core.database.models import WorkflowExecution
from typing import Optional
import datetime


class StateManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_execution(
        self, name: str, target: str, user_id: str
    ) -> WorkflowExecution:
        exec_record = WorkflowExecution(
            workflow_name=name,
            target=target,
            user_id=user_id,
            status="RUNNING",
            started_at=datetime.datetime.now(datetime.timezone.utc),
        )
        self.db.add(exec_record)
        await self.db.commit()
        await self.db.refresh(exec_record)
        return exec_record

    async def update_status(
        self, exec_id: str, status: str, result_summary: Optional[str] = None
    ):
        result = await self.db.execute(
            select(WorkflowExecution).filter(WorkflowExecution.id == exec_id)
        )
        record = result.scalars().first()
        if record:
            record.status = status
            if result_summary:
                record.result_summary = result_summary
            if status in ["SUCCESS", "FAILED", "CANCELLED"]:
                record.finished_at = datetime.datetime.now(datetime.timezone.utc)
            self.db.add(record)
            await self.db.commit()

    async def get_execution(self, exec_id: str) -> Optional[WorkflowExecution]:
        result = await self.db.execute(
            select(WorkflowExecution).filter(WorkflowExecution.id == exec_id)
        )
        return result.scalars().first()
