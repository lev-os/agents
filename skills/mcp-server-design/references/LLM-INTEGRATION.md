# LLM Integration Patterns

> **Principle**: MCP servers can leverage LLMs for intelligent features like summarization, but must handle provider diversity, cost tracking, and graceful degradation.

## Dual-Mode Summarization

Support both single-thread detail and multi-thread aggregate modes:

```python
async def summarize_thread(
    project_key: str,
    thread_id: str,
    include_examples: bool = False,
    llm_mode: bool = True,
    llm_model: str | None = None,
    per_thread_limit: int = 50,
) -> dict:
    """
    Single-thread mode (thread_id is a single ID):
    - Returns detailed summary with optional example messages
    - Response: { thread_id, summary: {participants[], key_points[], action_items[]}, examples[] }

    Multi-thread mode (thread_id is comma-separated IDs like "TKT-1,TKT-2,TKT-3"):
    - Returns aggregate digest across all threads
    - Response: { threads: [{thread_id, summary}], aggregate: {top_mentions[], key_points[], action_items[]} }
    """
    # Detect mode from thread_id format
    thread_ids = [t.strip() for t in thread_id.split(",") if t.strip()]

    if len(thread_ids) == 1:
        return await _summarize_single_thread(
            project_key, thread_ids[0], include_examples, llm_mode, llm_model
        )
    else:
        return await _summarize_multi_thread(
            project_key, thread_ids, llm_mode, llm_model, per_thread_limit
        )
```

## Model Alias Resolution

Map user-friendly nicknames to canonical model IDs:

```python
MODEL_ALIASES = {
    # OpenAI aliases
    "gpt4": "gpt-4-turbo-preview",
    "gpt4o": "gpt-4o",
    "gpt4o-mini": "gpt-4o-mini",
    "gpt3": "gpt-3.5-turbo",

    # Anthropic aliases
    "opus": "claude-3-opus-20240229",
    "sonnet": "claude-3-5-sonnet-20241022",
    "haiku": "claude-3-5-haiku-20241022",
    "claude": "claude-3-5-sonnet-20241022",  # Default to latest Sonnet

    # Google aliases
    "gemini": "gemini-1.5-pro",
    "gemini-flash": "gemini-1.5-flash",
    "gemini-pro": "gemini-1.5-pro",

    # Meta aliases
    "llama": "llama-3.1-70b-instruct",
    "llama-small": "llama-3.1-8b-instruct",
}

def resolve_model_alias(model: str) -> str:
    """
    Resolve model alias to canonical model ID.

    Examples:
    - "opus" -> "claude-3-opus-20240229"
    - "gpt4" -> "gpt-4-turbo-preview"
    - "claude-3-opus-20240229" -> "claude-3-opus-20240229" (passthrough)
    """
    normalized = model.lower().strip()
    return MODEL_ALIASES.get(normalized, model)
```

## Provider Environment Bridge

Map common environment variable names to provider-specific ones:

```python
PROVIDER_ENV_MAPPING = {
    "google": {
        # Users often set GEMINI_API_KEY but litellm expects GOOGLE_API_KEY
        "GEMINI_API_KEY": "GOOGLE_API_KEY",
        "GEMINI_API_BASE": "GOOGLE_API_BASE",
    },
    "anthropic": {
        # No mapping needed, ANTHROPIC_API_KEY is standard
    },
    "openai": {
        # No mapping needed, OPENAI_API_KEY is standard
    },
    "azure": {
        "AZURE_API_KEY": "AZURE_OPENAI_API_KEY",
        "AZURE_ENDPOINT": "AZURE_OPENAI_ENDPOINT",
    },
}

def setup_provider_environment():
    """
    Set up environment variables for LLM providers.
    Maps common names to provider-specific ones.
    """
    for provider, mappings in PROVIDER_ENV_MAPPING.items():
        for source, target in mappings.items():
            if source in os.environ and target not in os.environ:
                os.environ[target] = os.environ[source]
                logger.debug(f"Mapped {source} -> {target}")
```

## Cost Logging Callbacks

Track token usage and costs for observability:

```python
@dataclass
class LLMUsageLog:
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    duration_ms: float
    timestamp: datetime

class CostTracker:
    """Track LLM costs per agent/project."""

    # Cost per 1K tokens (input, output) by model
    COSTS = {
        "gpt-4-turbo-preview": (0.01, 0.03),
        "gpt-4o": (0.005, 0.015),
        "gpt-4o-mini": (0.00015, 0.0006),
        "claude-3-opus": (0.015, 0.075),
        "claude-3-5-sonnet": (0.003, 0.015),
        "claude-3-5-haiku": (0.0008, 0.004),
        "gemini-1.5-pro": (0.00125, 0.005),
        "gemini-1.5-flash": (0.000075, 0.0003),
    }

    def __init__(self):
        self.logs: list[LLMUsageLog] = []

    def log_completion(
        self,
        model: str,
        response: dict,
        duration_ms: float,
    ) -> LLMUsageLog:
        """Log a completion with cost calculation."""
        usage = response.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        cost = self._calculate_cost(model, prompt_tokens, completion_tokens)

        log = LLMUsageLog(
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            cost_usd=cost,
            duration_ms=duration_ms,
            timestamp=datetime.now(UTC),
        )
        self.logs.append(log)
        return log

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost in USD."""
        # Normalize model name for lookup
        for key in self.COSTS:
            if key in model.lower():
                input_cost, output_cost = self.COSTS[key]
                return (prompt_tokens * input_cost + completion_tokens * output_cost) / 1000
        return 0.0  # Unknown model
```

## LLM Refinement with Fallback

Use LLM to refine heuristic results with JSON parsing fallback:

```python
async def _llm_refine_summary(
    raw_summary: dict,
    messages: list[dict],
    model: str,
) -> dict:
    """
    Use LLM to refine a heuristic summary.

    Falls back to heuristic result if:
    - LLM call fails
    - JSON parsing fails
    - Response is malformed
    """
    prompt = f"""Given these messages and initial summary, provide a refined summary.

Initial summary:
{json.dumps(raw_summary, indent=2)}

Messages:
{_format_messages_for_llm(messages)}

Respond with valid JSON:
{{
    "participants": ["name1", "name2"],
    "key_points": ["point1", "point2"],
    "action_items": ["action1", "action2"]
}}
"""

    try:
        response = await litellm.acompletion(
            model=resolve_model_alias(model),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            timeout=30,
        )

        content = response.choices[0].message.content
        refined = _parse_json_with_fallback(content)

        # Validate required fields
        if all(k in refined for k in ["participants", "key_points", "action_items"]):
            return refined

    except Exception as e:
        logger.warning(f"LLM refinement failed, using heuristic: {e}")

    return raw_summary  # Fallback to heuristic


def _parse_json_with_fallback(content: str) -> dict:
    """
    Parse JSON with multiple fallback strategies.

    1. Direct JSON parse
    2. Extract JSON from markdown code block
    3. Regex extraction of JSON object
    """
    # Strategy 1: Direct parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Strategy 2: Extract from code block
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", content)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Strategy 3: Find JSON object
    match = re.search(r"\{[\s\S]*\}", content)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from: {content[:100]}...")
```

## LLM Settings Configuration

Comprehensive settings for LLM integration:

```python
@dataclass(slots=True, frozen=True)
class LLMSettings:
    enabled: bool = True
    default_model: str = "gpt-4o-mini"
    fallback_model: str = "gpt-3.5-turbo"
    timeout_seconds: int = 30
    max_retries: int = 2
    cost_tracking: bool = True
    max_cost_per_request_usd: float = 0.10
    max_daily_cost_usd: float = 10.0

def load_llm_settings() -> LLMSettings:
    return LLMSettings(
        enabled=_bool(os.getenv("LLM_ENABLED", "true")),
        default_model=os.getenv("LLM_DEFAULT_MODEL", "gpt-4o-mini"),
        fallback_model=os.getenv("LLM_FALLBACK_MODEL", "gpt-3.5-turbo"),
        timeout_seconds=_int(os.getenv("LLM_TIMEOUT", "30")),
        max_retries=_int(os.getenv("LLM_MAX_RETRIES", "2")),
        cost_tracking=_bool(os.getenv("LLM_COST_TRACKING", "true")),
        max_cost_per_request_usd=_float(os.getenv("LLM_MAX_COST_REQUEST", "0.10")),
        max_daily_cost_usd=_float(os.getenv("LLM_MAX_COST_DAILY", "10.0")),
    )
```

## Graceful Degradation

Always provide useful output even when LLM is unavailable:

```python
async def summarize_with_fallback(
    messages: list[dict],
    llm_enabled: bool = True,
    llm_model: str | None = None,
) -> dict:
    """
    Summarize messages with graceful degradation.

    1. Try LLM summarization if enabled
    2. Fall back to heuristic summarization
    3. Always return valid structure
    """
    # Heuristic summary (always works)
    heuristic = _heuristic_summary(messages)

    if not llm_enabled:
        return {"summary": heuristic, "method": "heuristic"}

    try:
        refined = await _llm_refine_summary(
            heuristic,
            messages,
            llm_model or settings.llm.default_model,
        )
        return {"summary": refined, "method": "llm"}
    except Exception as e:
        logger.warning(f"LLM unavailable, using heuristic: {e}")
        return {"summary": heuristic, "method": "heuristic_fallback"}


def _heuristic_summary(messages: list[dict]) -> dict:
    """
    Generate summary using heuristics (no LLM).

    Extracts:
    - Participants from sender/recipient fields
    - Key points from message subjects
    - Action items from patterns like "TODO:", "ACTION:", bullets
    """
    participants = set()
    subjects = []
    action_items = []

    for msg in messages:
        participants.add(msg.get("from", ""))
        participants.update(msg.get("to", []))

        if subject := msg.get("subject"):
            subjects.append(subject)

        if body := msg.get("body_md", ""):
            # Extract action items from common patterns
            for line in body.split("\n"):
                line = line.strip()
                if any(line.upper().startswith(p) for p in ["TODO:", "ACTION:", "- [ ]"]):
                    action_items.append(line)

    return {
        "participants": sorted(p for p in participants if p),
        "key_points": subjects[:5],  # First 5 subjects as key points
        "action_items": action_items[:10],
    }
```

## Do / Don't

**Do:**
- Always provide heuristic fallback
- Validate LLM responses before using
- Track costs per agent/project
- Use model aliases for user convenience
- Set reasonable timeouts and cost limits

**Don't:**
- Depend on LLM for core functionality
- Expose raw LLM errors to agents
- Allow unbounded LLM costs
- Hardcode model IDs (use aliases)
- Skip JSON validation on LLM output
