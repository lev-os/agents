# Claude Agent SDK - Production Patterns

## Pattern 1: Message Processing Pipeline

Automate processing when new data arrives (like new iMessage URLs):

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, tool, create_sdk_mcp_server

@tool("get_new_messages", "Fetch new messages since last check", {"since_id": int})
async def get_new_messages(args: dict) -> dict:
    # Your message fetching logic
    messages = fetch_from_db(args["since_id"])
    return {"content": [{"type": "text", "text": json.dumps(messages)}]}

@tool("extract_urls", "Extract URLs from message text", {"text": str})
async def extract_urls(args: dict) -> dict:
    urls = re.findall(r'https?://[^\s]+', args["text"])
    return {"content": [{"type": "text", "text": json.dumps(urls)}]}

@tool("process_url", "Scrape and store URL content", {"url": str})
async def process_url(args: dict) -> dict:
    # Your scraping logic
    result = scrape_url(args["url"])
    return {"content": [{"type": "text", "text": f"Processed: {args['url']}"}]}

pipeline_server = create_sdk_mcp_server(
    name="message-pipeline",
    version="1.0.0",
    tools=[get_new_messages, extract_urls, process_url]
)

async def run_intake_pipeline():
    async for msg in query(
        prompt="""
        1. Get new messages since last check
        2. Extract all URLs from messages
        3. Process each URL (scrape and store)
        4. Report summary
        """,
        options=ClaudeAgentOptions(
            mcp_servers={"message-pipeline": pipeline_server},
            allowed_tools=[
                "mcp__message-pipeline__get_new_messages",
                "mcp__message-pipeline__extract_urls",
                "mcp__message-pipeline__process_url"
            ],
            permission_mode="bypassPermissions"
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

## Pattern 2: Orchestrator + Specialist Subagents

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def analyze_codebase():
    async for msg in query(
        prompt="Analyze this codebase for quality and security issues",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Task"],
            agents={
                "security-scanner": AgentDefinition(
                    description="Scans code for security vulnerabilities (SQL injection, XSS, auth issues)",
                    prompt="""You are a security expert. Scan for:
                    - SQL injection
                    - XSS vulnerabilities
                    - Authentication bypasses
                    - Hardcoded secrets
                    Report findings with severity levels.""",
                    tools=["Read", "Grep", "Glob"],
                    model="sonnet"
                ),
                "performance-analyst": AgentDefinition(
                    description="Analyzes code for performance issues",
                    prompt="""You are a performance expert. Look for:
                    - N+1 queries
                    - Memory leaks
                    - Inefficient algorithms
                    - Missing caching opportunities""",
                    tools=["Read", "Grep", "Glob"],
                    model="haiku"
                ),
                "documentation-checker": AgentDefinition(
                    description="Checks documentation completeness",
                    prompt="Check for missing docstrings, outdated README, incomplete API docs.",
                    tools=["Read", "Glob"],
                    model="haiku"
                )
            }
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

## Pattern 3: Scheduled Agent Runner

```python
import asyncio
import schedule
from claude_agent_sdk import query, ClaudeAgentOptions

async def daily_health_check():
    async for msg in query(
        prompt="""
        Run daily health check:
        1. Check all services are running
        2. Verify database connectivity
        3. Check disk space
        4. Review error logs from last 24h
        Generate a summary report.
        """,
        options=ClaudeAgentOptions(
            allowed_tools=["Bash", "Read", "Grep"],
            permission_mode="bypassPermissions"
        )
    ):
        if hasattr(msg, "result"):
            send_slack_notification(msg.result)

def run_scheduled_agents():
    schedule.every().day.at("06:00").do(
        lambda: asyncio.run(daily_health_check())
    )

    while True:
        schedule.run_pending()
        time.sleep(60)
```

## Pattern 4: File-Based Delegation (Context Optimization)

Reduce context usage by having subagents write to files:

```python
async def large_codebase_analysis():
    async for msg in query(
        prompt="""
        Analyze this large codebase:

        1. First, delegate to security-scanner agent. Have it write findings to /tmp/security_report.md
        2. Then, delegate to performance-analyst agent. Have it write to /tmp/perf_report.md
        3. Finally, read both reports and create a unified summary.

        This approach prevents context overflow from full report contents.
        """,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Task"],
            agents={
                "security-scanner": AgentDefinition(
                    description="Security analysis, writes to file",
                    prompt="Analyze security and write full report to the specified file.",
                    tools=["Read", "Grep", "Write"],
                    model="sonnet"
                ),
                "performance-analyst": AgentDefinition(
                    description="Performance analysis, writes to file",
                    prompt="Analyze performance and write full report to the specified file.",
                    tools=["Read", "Grep", "Write"],
                    model="sonnet"
                )
            }
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

## Pattern 5: Interactive Agent with User Feedback

```python
async def interactive_refactoring():
    session_id = None

    # Phase 1: Analysis
    async for msg in query(
        prompt="Analyze this module and suggest refactoring improvements",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "AskUserQuestion"]
        )
    ):
        if hasattr(msg, 'session_id'):
            session_id = msg.session_id
        if hasattr(msg, "result"):
            print("Analysis:", msg.result)

    # User reviews suggestions...
    user_choice = input("Which refactoring to apply? ")

    # Phase 2: Implementation (with context from phase 1)
    async for msg in query(
        prompt=f"Apply refactoring option: {user_choice}",
        options=ClaudeAgentOptions(
            resume=session_id,  # Full context preserved
            allowed_tools=["Read", "Edit", "Bash"],
            permission_mode="acceptEdits"
        )
    ):
        if hasattr(msg, "result"):
            print("Completed:", msg.result)
```

## Pattern 6: Multi-Project Coordinator

```python
async def cross_project_analysis():
    async for msg in query(
        prompt="""
        Analyze consistency across these related projects:
        1. ~/cb - ClaudeBrowser scraping engine
        2. ~/cb3 - CB version 3
        3. ~/josh-imessage - iMessage analyzer

        Check for:
        - Shared code that could be extracted
        - Inconsistent patterns between projects
        - Dependency version mismatches
        """,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Bash"],
            permission_mode="bypassPermissions"
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

## Pattern 7: Audit Trail Hook

```python
from claude_agent_sdk import HookMatcher
from datetime import datetime
import json

audit_log = []

async def audit_hook(input_data, tool_use_id, context):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": input_data.get("tool_name"),
        "input": input_data.get("tool_input"),
        "tool_use_id": tool_use_id
    }
    audit_log.append(entry)

    # Write to file for persistence
    with open("agent_audit.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

    return {}

async def audited_operation():
    async for msg in query(
        prompt="Refactor the authentication module",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash"],
            hooks={
                "PostToolUse": [HookMatcher(matcher=".*", hooks=[audit_hook])]
            }
        )
    ):
        if hasattr(msg, "result"):
            print(f"Completed. {len(audit_log)} operations logged.")
            return msg.result
```

## Pattern 8: Graceful Degradation

```python
async def robust_agent_operation():
    try:
        async for msg in query(
            prompt="Process these URLs",
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Bash", "WebFetch"],
                max_turns=50  # Prevent runaway
            )
        ):
            if hasattr(msg, "error"):
                logging.warning(f"Agent reported error: {msg.error}")
                # Continue - agent may recover
                continue

            if hasattr(msg, "result"):
                return {"status": "success", "result": msg.result}

    except asyncio.TimeoutError:
        logging.error("Agent timed out")
        return {"status": "timeout", "result": None}

    except Exception as e:
        logging.error(f"Agent failed: {e}")
        return {"status": "error", "error": str(e)}
```

## Application to josh-imessage

### Automatic URL Intake Agent

```python
# agents/url_intake_agent.py
from claude_agent_sdk import query, ClaudeAgentOptions, tool, create_sdk_mcp_server
from tools.batch_url_processor import BatchURLProcessor

processor = BatchURLProcessor()

@tool("check_new_messages", "Check for new messages with URLs", {})
async def check_new_messages(args: dict) -> dict:
    result = processor.extract_urls_from_conversations(limit_conversations=50)
    return {"content": [{"type": "text", "text": f"Found {len(result.urls)} URLs"}]}

@tool("process_url_batch", "Process a batch of URLs", {"urls": list})
async def process_url_batch(args: dict) -> dict:
    result = await processor.process_urls_in_batches(args["urls"])
    return {"content": [{"type": "text", "text": result.to_dict()}]}

intake_server = create_sdk_mcp_server(
    name="url-intake",
    version="1.0.0",
    tools=[check_new_messages, process_url_batch]
)

async def run_url_intake():
    async for msg in query(
        prompt="Check for new messages and process any URLs found",
        options=ClaudeAgentOptions(
            mcp_servers={"url-intake": intake_server},
            allowed_tools=[
                "mcp__url-intake__check_new_messages",
                "mcp__url-intake__process_url_batch"
            ],
            permission_mode="bypassPermissions"
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

## Application to CB3 (~/cb3)

CB3 is ClaudeBrowser v3 - a multi-engine web scraping orchestration system.

### Multi-Engine Scraping Orchestrator

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, tool, create_sdk_mcp_server

# CB3 engine selector as custom tool
@tool("select_engine", "Select best scraping engine for URL", {"url": str, "requirements": dict})
async def select_engine(args: dict) -> dict:
    url = args["url"]
    # Logic from cb3/src/core/orchestration
    if "twitter.com" in url or "x.com" in url:
        return {"content": [{"type": "text", "text": "twitter_api"}]}
    elif "youtube.com" in url:
        return {"content": [{"type": "text", "text": "youtube_api"}]}
    elif args.get("requirements", {}).get("js_render"):
        return {"content": [{"type": "text", "text": "playwright"}]}
    return {"content": [{"type": "text", "text": "requests"}]}

@tool("execute_scrape", "Execute scrape with selected engine", {"url": str, "engine": str})
async def execute_scrape(args: dict) -> dict:
    # Wrap cb3 scraping logic
    result = await cb3_orchestrator.scrape(args["url"], engine=args["engine"])
    return {"content": [{"type": "text", "text": json.dumps(result)}]}

cb3_server = create_sdk_mcp_server(
    name="cb3-orchestrator",
    version="1.0.0",
    tools=[select_engine, execute_scrape]
)

async def intelligent_scraping():
    async for msg in query(
        prompt="""
        For each URL in the queue:
        1. Select best engine using select_engine tool
        2. Execute scrape with execute_scrape
        3. Handle failures with fallback engines
        4. Store results in organized structure
        """,
        options=ClaudeAgentOptions(
            mcp_servers={"cb3": cb3_server},
            allowed_tools=[
                "mcp__cb3__select_engine",
                "mcp__cb3__execute_scrape",
                "Read", "Write"
            ],
            permission_mode="bypassPermissions"
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

### CB3 MCP Server Bridge

Expose CB3 as an MCP server for Claude Code:

```python
# cb3/src/api/mcp_server.py
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("cb3_scrape", "Scrape URL with CB3 multi-engine system", {
    "url": str,
    "engine": {"type": "string", "default": "auto"},
    "wait_for_js": {"type": "boolean", "default": False}
})
async def cb3_scrape(args: dict) -> dict:
    from cb3.core import Orchestrator
    orchestrator = Orchestrator()
    result = await orchestrator.scrape(
        url=args["url"],
        engine=args.get("engine", "auto"),
        options={"wait_for_js": args.get("wait_for_js", False)}
    )
    return {"content": [{"type": "text", "text": json.dumps(result)}]}

@tool("cb3_batch", "Batch scrape multiple URLs", {"urls": list, "parallel": int})
async def cb3_batch(args: dict) -> dict:
    from cb3.core import BatchProcessor
    processor = BatchProcessor(max_workers=args.get("parallel", 3))
    results = await processor.process(args["urls"])
    return {"content": [{"type": "text", "text": json.dumps(results)}]}

# Export as MCP server
cb3_mcp = create_sdk_mcp_server(
    name="cb3",
    version="3.0.0",
    tools=[cb3_scrape, cb3_batch]
)
```

## Application to TimeTravel (~/lev/research/timetravel)

TimeTravel is a research orchestration platform with DAG/FSM job execution.

### TimeTravel Job Runner Agent

```python
from claude_agent_sdk import query, ClaudeAgentOptions, tool, create_sdk_mcp_server

@tool("run_job", "Execute a TimeTravel job manifest", {
    "job_file": str,
    "vars": {"type": "object", "default": {}},
    "mode": {"type": "string", "enum": ["dag", "fsm"], "default": "dag"}
})
async def run_job(args: dict) -> dict:
    import subprocess
    cmd = ["npx", "ts-node", "src/cli/run-job.ts", args["job_file"]]
    if args.get("mode") == "fsm":
        cmd.append("--mode=fsm")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd="~/lev/research/timetravel")
    return {"content": [{"type": "text", "text": result.stdout}]}

@tool("list_adapters", "List available TimeTravel adapters", {})
async def list_adapters(args: dict) -> dict:
    adapters = ["perplexity", "github", "firecrawl", "arxiv", "hackernews", "scholar", "reddit", "cli"]
    return {"content": [{"type": "text", "text": json.dumps(adapters)}]}

@tool("create_job", "Generate a TimeTravel job manifest", {
    "name": str,
    "sources": list,
    "mode": {"type": "string", "default": "dag"}
})
async def create_job(args: dict) -> dict:
    # Generate YAML job manifest
    job = {
        "version": "2.0" if args.get("mode") == "fsm" else "1.0",
        "name": args["name"],
        "sources": args["sources"]
    }
    return {"content": [{"type": "text", "text": yaml.dump(job)}]}

timetravel_server = create_sdk_mcp_server(
    name="timetravel",
    version="1.0.0",
    tools=[run_job, list_adapters, create_job]
)
```

### Research Orchestration with Subagents

```python
async def deep_research(topic: str):
    async for msg in query(
        prompt=f"""
        Research "{topic}" using TimeTravel multi-source pipeline:

        1. Use perplexity adapter for initial discovery
        2. Search GitHub for related repositories
        3. Check arxiv for academic papers
        4. Search HackerNews for discussions
        5. Synthesize findings into comprehensive report
        """,
        options=ClaudeAgentOptions(
            mcp_servers={"timetravel": timetravel_server},
            allowed_tools=[
                "mcp__timetravel__run_job",
                "mcp__timetravel__create_job",
                "Read", "Write"
            ],
            agents={
                "academic-researcher": AgentDefinition(
                    description="Searches academic sources (arxiv, scholar)",
                    prompt="Focus on peer-reviewed papers and citations.",
                    tools=["mcp__timetravel__run_job", "Read"],
                    model="sonnet"
                ),
                "code-researcher": AgentDefinition(
                    description="Searches code repositories (GitHub)",
                    prompt="Find implementations, libraries, and examples.",
                    tools=["mcp__timetravel__run_job", "Read"],
                    model="haiku"
                ),
                "discussion-researcher": AgentDefinition(
                    description="Searches discussions (HackerNews, Reddit)",
                    prompt="Find community insights and practical experiences.",
                    tools=["mcp__timetravel__run_job", "Read"],
                    model="haiku"
                )
            }
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

### Dynamic Job Generation

```python
async def generate_research_pipeline(research_question: str):
    """Generate and execute a TimeTravel job based on natural language query"""
    async for msg in query(
        prompt=f"""
        Create a TimeTravel job manifest to research: "{research_question}"

        Steps:
        1. Analyze the question to determine relevant sources
        2. Use create_job tool to generate appropriate YAML
        3. Save job to jobs/generated-{timestamp}.yaml
        4. Execute job with run_job tool
        5. Return synthesized results

        Consider:
        - Use FSM mode for iterative deepening
        - Include academic sources for technical topics
        - Add GitHub search for implementation-focused questions
        """,
        options=ClaudeAgentOptions(
            mcp_servers={"timetravel": timetravel_server},
            allowed_tools=[
                "mcp__timetravel__create_job",
                "mcp__timetravel__run_job",
                "mcp__timetravel__list_adapters",
                "Write", "Read"
            ],
            permission_mode="acceptEdits"
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

## Cross-Project Integration

### Unified Research + Scraping Pipeline

Combine TimeTravel research with CB3 scraping:

```python
async def full_research_pipeline(topic: str):
    """
    1. TimeTravel finds relevant URLs via multi-source research
    2. CB3 scrapes and extracts content from found URLs
    3. Agent synthesizes into final report
    """
    async for msg in query(
        prompt=f"""
        Deep research on "{topic}":

        Phase 1 - Discovery (TimeTravel):
        - Search perplexity, github, arxiv for relevant resources
        - Collect URLs from search results

        Phase 2 - Content Extraction (CB3):
        - Scrape collected URLs with appropriate engines
        - Extract and clean content

        Phase 3 - Synthesis:
        - Analyze all collected content
        - Generate comprehensive research report
        """,
        options=ClaudeAgentOptions(
            mcp_servers={
                "timetravel": timetravel_server,
                "cb3": cb3_server
            },
            allowed_tools=[
                "mcp__timetravel__run_job",
                "mcp__cb3__cb3_scrape",
                "mcp__cb3__cb3_batch",
                "Write", "Read"
            ],
            permission_mode="bypassPermissions"
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```
