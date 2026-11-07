# Eval runner

Run:

```bash
python backend/evals/run_eval.py
```

Coverage:
- intake agent output validation
- extractor agent output validation
- draft agent output validation
- guardrail agent output validation

Purpose:
- catch schema drift
- catch prompt regressions
- catch invalid draft/export shapes earlier
