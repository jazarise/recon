# Finding Standard

The `Finding` class is the universal communication medium across all ReconX components.

```python
Finding(
    category="subdomain", # replaces old 'type' attribute
    value="api.example.com",
    source="subfinder",
    metadata={"confidence": "high"}
)
```
No plugin may output custom dictionaries or text objects.
