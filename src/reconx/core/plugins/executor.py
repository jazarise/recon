import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from reconx.core.plugins.base import ReconXPlugin, PluginResult
from reconx.core.plugins.sandbox import PluginSandbox
from reconx.core.database.models import PluginExecution
from reconx.core.plugins.exceptions import PluginError


class PluginExecutor:
    def __init__(self, db: AsyncSession, sandbox: PluginSandbox):
        self.db = db
        self.sandbox = sandbox

    async def run(
        self, plugin: ReconXPlugin, target_id: str, target_val: str
    ) -> PluginResult:
        execution = PluginExecution(
            plugin_name=plugin.name,
            target_id=target_id,
            status="running",
            started_at=datetime.datetime.now(datetime.timezone.utc),
        )
        self.db.add(execution)
        await self.db.commit()
        await self.db.refresh(execution)

        try:
            valid = await plugin.validate()
            if valid is False:  # if True or None we proceed
                raise PluginError(f"Validation failed for {plugin.name}")

            result = await self.sandbox.execute(plugin, target_val)

            execution.status = "completed"
            execution.output = (
                f"Findings: {len(result.findings)}, Assets: {len(result.assets)}"
            )

        except PluginError as e:
            result = PluginResult(status="error", errors=[str(e)])
            execution.status = "error"
            execution.output = str(e)

        finally:
            execution.finished_at = datetime.datetime.now(datetime.timezone.utc)
            self.db.add(execution)
            await self.db.commit()

            try:
                await plugin.cleanup()
            except Exception:
                pass  # nosec B110

        return result
