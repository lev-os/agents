# Quick

1. Run `lev research <query> -s quick --no-wikify`.
2. Accept only a result containing at least one source URL.
3. If the strategy returns zero URLs, use its configured fallback; do not silently select another provider.
4. Return the answer and source URL. Stop.
