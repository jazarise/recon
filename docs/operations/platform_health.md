# Platform Health Score

Internal proprietary metric calculating instantaneous availability.

```python
score = (test_pass_rate * 0.3) + (availability * 0.4) + (coverage * 0.2) + (security * 0.1)
```

Target bounds: `> 95`.
