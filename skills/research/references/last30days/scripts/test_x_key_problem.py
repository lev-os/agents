#!/usr/bin/env python3
"""An xAI 403 "out of credits" is a key problem, not 0 X results, and must not stop X failover.

Run: python3 scripts/test_x_key_problem.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import health, http, pipeline, quality_nudge, xai_x

BODY = ('{"code":"permission-denied","error":"Your team T has either used all available '
        'credits or reached its monthly spending limit."}')

# 1. A 403 whose body says the credits are gone is payment-required, and says so.
err = http.HTTPError("HTTP 403: Forbidden", 403, BODY)
assert err.outcome_state == health.PAYMENT_REQUIRED, err.outcome_state
assert http.classify_failure(message=str(err)) == health.PAYMENT_REQUIRED, str(err)
# A plain 403 stays auth-failed.
assert http.HTTPError("HTTP 403: Forbidden", 403, '{"error":"bad key"}').outcome_state == health.AUTH_FAILED


# 2. A raising backend returns an error string (so the chain can fail over), not an exception.
def boom(*a, **k):
    raise err


xai_x.search_x = boom
items, msg = pipeline._fetch_x_backend("xai", "ai coup", "2026-10-17", "2026-11-16", "default",
                                       {"XAI_API_KEY": "k"})
assert items == [] and "payment required" in msg, (items, msg)

# 3. The fix line names the xAI key problem on every host.
x_error = f"All X backends failed — xai: {msg}"
for cfg in ({"XAI_API_KEY": "k"}, {"XAI_API_KEY": "k", "LAST30DAYS_HOST": "grok-bot"}):
    fix = quality_nudge._x_error_prescription(cfg, {"x_error": x_error})
    assert "key problem, not 0 results" in fix.fix_nl and "console.x.ai" in fix.fix_nl, (cfg, fix)

print("ok")
