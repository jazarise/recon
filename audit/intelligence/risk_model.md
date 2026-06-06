# Risk Model

The Risk Engine calculates unified Asset Risk profiles.
Scoring Mapping:
- Critical = 95
- High = 80
- Medium = 55
- Low = 20
- Info = 5

**Calculation Methodology:**
`Base Score` = max(Severity of all Asset Findings)
`Addon Penalty` = sum(Severity * 0.1)
`Final Asset Score` = min(100, Base Score + Addon Penalty)
