# Plugin Development

Create a folder in `src/reconx/plugins/<name>` and subclass `ReconPlugin`.

```python
class MyPlugin(ReconPlugin):
    async def execute(self, target):
        return {"results": "found"}
```
