#!/usr/bin/env python3
"""
Session Scanner Framework for Lev Self-Learning

Extracts patterns from conversation history to propose new entities.
When hooked into conversation lifecycle events, this enables lev to evolve.

Scanner Types:
1. Synths     - Agent-created ephemeral entities (both old and new footer schemas)
2. Workflows  - Tool sequences and branching patterns
3. Skills     - Reusable operations and abstractions
4. Docs       - Stale/missing documentation signals
5. Memories   - Semantic/episodic/procedural knowledge

Usage:
    python scanner_framework.py [--type TYPE] [--session-dir DIR] [--output FORMAT]

Types: synth, workflow, skill, doc, memory, all
Formats: jsonl, yaml, summary

Version: 2.1.0 (2026-01-20) - Multi-schema footer support
Author: Lev Platform
"""

__version__ = "2.1.0"
__last_updated__ = "2026-01-20"

import json
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional, Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# Configuration loader
def load_validation_gates() -> dict:
    """Load validation gates config from YAML."""
    config_path = Path(__file__).parent.parent / "config" / "validation-gates.yaml"

    if not config_path.exists():
        return get_default_gates()

    if not HAS_YAML:
        print("Warning: PyYAML not installed, using default gates", file=sys.stderr)
        return get_default_gates()

    with open(config_path) as f:
        return yaml.safe_load(f)


def get_default_gates() -> dict:
    """Default validation gates if config not found."""
    return {
        "defaults": {"min_confidence": 0.5, "high_confidence": 0.8},
        "scanners": {
            "synth": {"base_confidence": 0.9},
            "workflow": {"base_confidence": 0.6, "min_sequence_length": 3},
            "skill": {"base_confidence": 0.5, "indicator_bonus": 0.1},
            "doc": {"base_confidence": 0.7},
            "memory": {"base_confidence": 0.5, "type_bonus": 0.1},
        },
        "routing": {
            "auto_route": {"threshold": 0.8},
            "review_queue": {"threshold": 0.6},
            "log_only": {"threshold": 0.0},
        }
    }


# Global config (loaded once)
GATES_CONFIG = load_validation_gates()


def route_finding(scanner_type: str, confidence: float) -> dict:
    """Determine routing destination based on confidence and type."""
    routing = GATES_CONFIG.get("routing", {})
    auto_threshold = routing.get("auto_route", {}).get("threshold", 0.8)
    review_threshold = routing.get("review_queue", {}).get("threshold", 0.6)

    # Auto-route high confidence findings
    if confidence >= auto_threshold:
        destinations = routing.get("auto_route", {}).get("destinations", {})
        return {
            "tier": "auto_route",
            "destination": destinations.get(scanner_type, "log"),
            "action": "execute"
        }

    # Queue medium confidence for review
    if confidence >= review_threshold:
        destinations = routing.get("review_queue", {}).get("destinations", {})
        return {
            "tier": "review_queue",
            "destination": destinations.get(scanner_type, "queue"),
            "action": "review"
        }

    # Log low confidence
    return {
        "tier": "log_only",
        "destination": routing.get("log_only", {}).get("destination", "~/.lev/scan-history.jsonl"),
        "action": "log"
    }


@dataclass
class ScanResult:
    """Base result from any scanner."""
    scanner_type: str
    entity_type: str
    name: str
    confidence: float  # 0.0-1.0
    source_session: str
    source_lines: list[int] = field(default_factory=list)
    context: dict = field(default_factory=dict)
    proposed_action: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    routing: dict = field(default_factory=dict)

    def __post_init__(self):
        """Auto-compute routing based on confidence."""
        if not self.routing:
            self.routing = route_finding(self.scanner_type, self.confidence)

    def to_dict(self) -> dict:
        return asdict(self)


class SessionScanner(ABC):
    """Base class for all session scanners."""

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.session_files = list(session_dir.glob("*.jsonl"))

    @property
    @abstractmethod
    def scanner_type(self) -> str:
        """Unique identifier for this scanner type."""
        pass

    @abstractmethod
    def scan_message(self, message: dict, line_num: int, session_id: str) -> Iterator[ScanResult]:
        """Scan a single message for patterns."""
        pass

    def scan_all(self) -> Iterator[ScanResult]:
        """Scan all sessions in directory."""
        for session_file in self.session_files:
            session_id = session_file.stem
            with open(session_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        message = json.loads(line)
                        yield from self.scan_message(message, line_num, session_id)
                    except json.JSONDecodeError:
                        continue


class SynthScanner(SessionScanner):
    """Scan for ephemeral/synth entities in both old and new footer schemas."""

    # Old schema: synths: [name1, name2]
    OLD_SYNTH_PATTERN = re.compile(r'synths:\s*\[([^\]]*)\]', re.IGNORECASE | re.MULTILINE)

    # New schema: entities: [...] with lifecycle: ephemeral or type: synth
    ENTITIES_BLOCK = re.compile(r'entities:\s*(.*?)(?=\n\w+:|$)', re.DOTALL | re.MULTILINE)
    ENTITY_ENTRY = re.compile(r'-\s*type:\s*(\w+).*?id:\s*([^\n]+).*?lifecycle:\s*(\w+)', re.DOTALL)

    @property
    def scanner_type(self) -> str:
        return "synth"

    def scan_message(self, message: dict, line_num: int, session_id: str) -> Iterator[ScanResult]:
        content = self._extract_text(message)
        if not content:
            return

        # Try old schema first
        for match in self.OLD_SYNTH_PATTERN.finditer(content):
            synth_list = match.group(1).strip()
            if synth_list:
                synths = [s.strip().strip('"\'') for s in synth_list.split(',')]
                for synth_name in synths:
                    if synth_name:
                        yield ScanResult(
                            scanner_type=self.scanner_type,
                            entity_type="synth",
                            name=synth_name,
                            confidence=0.9,  # High confidence - explicit declaration
                            source_session=session_id,
                            source_lines=[line_num],
                            context={"schema": "v1_synths", "declaration": match.group(0)},
                            proposed_action="materialize_synth"
                        )

        # Try new schema (entities: with lifecycle: ephemeral)
        for entities_match in self.ENTITIES_BLOCK.finditer(content):
            entities_block = entities_match.group(1)
            for entity_match in self.ENTITY_ENTRY.finditer(entities_block):
                entity_type = entity_match.group(1).strip()
                entity_id = entity_match.group(2).strip().strip('"\'')
                lifecycle = entity_match.group(3).strip()

                # Detect ephemerals (synths) or explicit type: synth
                if lifecycle == "ephemeral" or entity_type == "synth":
                    yield ScanResult(
                        scanner_type=self.scanner_type,
                        entity_type="ephemeral" if lifecycle == "ephemeral" else "synth",
                        name=entity_id,
                        confidence=0.9,
                        source_session=session_id,
                        source_lines=[line_num],
                        context={
                            "schema": "v2_entities",
                            "entity_type": entity_type,
                            "lifecycle": lifecycle
                        },
                        proposed_action="materialize_ephemeral"
                    )

    def _extract_text(self, msg: dict) -> str:
        if isinstance(msg.get("message"), dict):
            content = msg["message"].get("content", "")
            if isinstance(content, list):
                return " ".join(c.get("text", "") for c in content if isinstance(c, dict))
            return str(content)
        return str(msg.get("content", ""))


class WorkflowScanner(SessionScanner):
    """Detect tool sequences that could become workflows."""

    TOOL_CALL_PATTERN = re.compile(r'tool_use.*?"name":\s*"([^"]+)"')
    WORKFLOW_MIN_SEQUENCE = 3  # Minimum tools to consider a workflow

    @property
    def scanner_type(self) -> str:
        return "workflow"

    def __init__(self, session_dir: Path):
        super().__init__(session_dir)
        self.tool_sequences: dict[str, list[tuple[str, int]]] = {}

    def scan_message(self, message: dict, line_num: int, session_id: str) -> Iterator[ScanResult]:
        content = json.dumps(message)
        tools = self.TOOL_CALL_PATTERN.findall(content)

        if tools:
            if session_id not in self.tool_sequences:
                self.tool_sequences[session_id] = []
            for tool in tools:
                self.tool_sequences[session_id].append((tool, line_num))

        # Check if we have a potential workflow
        seq = self.tool_sequences.get(session_id, [])
        if len(seq) >= self.WORKFLOW_MIN_SEQUENCE:
            tool_names = [t[0] for t in seq[-self.WORKFLOW_MIN_SEQUENCE:]]
            lines = [t[1] for t in seq[-self.WORKFLOW_MIN_SEQUENCE:]]

            # Only yield if it looks like a deliberate sequence (not just reads)
            if len(set(tool_names)) > 1:  # At least 2 different tools
                workflow_name = "_".join(tool_names[:3]) + "_workflow"
                yield ScanResult(
                    scanner_type=self.scanner_type,
                    entity_type="workflow_candidate",
                    name=workflow_name,
                    confidence=0.6,  # Medium confidence - needs validation
                    source_session=session_id,
                    source_lines=lines,
                    context={"tool_sequence": tool_names},
                    proposed_action="create_workflow"
                )
                # Clear to avoid duplicate detections
                self.tool_sequences[session_id] = []


class SkillScanner(SessionScanner):
    """Detect reusable operations that could become skills."""

    # Patterns that suggest skill candidates
    SKILL_INDICATORS = [
        re.compile(r'(?:reusable|should be|could be|pattern|abstraction)', re.I),
        re.compile(r'(?:always do|every time|repeatedly)', re.I),
        re.compile(r'(?:SKILL\.md|skill://|invoke skill)', re.I),
    ]

    @property
    def scanner_type(self) -> str:
        return "skill"

    def scan_message(self, message: dict, line_num: int, session_id: str) -> Iterator[ScanResult]:
        content = self._extract_text(message)
        if not content:
            return

        # Check for skill-suggesting language
        indicator_count = sum(1 for p in self.SKILL_INDICATORS if p.search(content))

        if indicator_count >= 2:
            # Try to extract a name
            name_match = re.search(r'(?:called?|named?)\s+["\']?(\w+(?:-\w+)*)["\']?', content, re.I)
            skill_name = name_match.group(1) if name_match else f"skill_candidate_{line_num}"

            yield ScanResult(
                scanner_type=self.scanner_type,
                entity_type="skill_candidate",
                name=skill_name,
                confidence=0.5 + (indicator_count * 0.1),
                source_session=session_id,
                source_lines=[line_num],
                context={"indicator_count": indicator_count, "snippet": content[:200]},
                proposed_action="create_skill"
            )

    def _extract_text(self, msg: dict) -> str:
        if isinstance(msg.get("message"), dict):
            content = msg["message"].get("content", "")
            if isinstance(content, list):
                return " ".join(c.get("text", "") for c in content if isinstance(c, dict))
            return str(content)
        return str(msg.get("content", ""))


class DocScanner(SessionScanner):
    """Detect stale or missing documentation signals."""

    DOC_PATTERNS = [
        (re.compile(r'(?:outdated|stale|wrong)\s+(?:doc|readme|documentation)', re.I), "stale_doc"),
        (re.compile(r'(?:missing|no|need)\s+(?:doc|readme|documentation)', re.I), "missing_doc"),
        (re.compile(r'(?:doesn\'t|does not)\s+(?:match|reflect|document)', re.I), "drift_doc"),
        (re.compile(r'ENOENT.*(?:md|readme|doc)', re.I), "broken_ref"),
    ]

    @property
    def scanner_type(self) -> str:
        return "doc"

    def scan_message(self, message: dict, line_num: int, session_id: str) -> Iterator[ScanResult]:
        content = self._extract_text(message)
        if not content:
            return

        for pattern, doc_type in self.DOC_PATTERNS:
            if match := pattern.search(content):
                # Try to extract the file path
                path_match = re.search(r'[\w/-]+\.(?:md|txt|rst)', content)
                doc_path = path_match.group(0) if path_match else f"unknown_doc_{line_num}"

                yield ScanResult(
                    scanner_type=self.scanner_type,
                    entity_type=doc_type,
                    name=doc_path,
                    confidence=0.7,
                    source_session=session_id,
                    source_lines=[line_num],
                    context={"match": match.group(0), "type": doc_type},
                    proposed_action="update_documentation"
                )

    def _extract_text(self, msg: dict) -> str:
        if isinstance(msg.get("message"), dict):
            content = msg["message"].get("content", "")
            if isinstance(content, list):
                return " ".join(c.get("text", "") for c in content if isinstance(c, dict))
            return str(content)
        return str(msg.get("content", ""))


class MemoryScanner(SessionScanner):
    """Extract knowledge worth persisting to memory systems."""

    MEMORY_PATTERNS = [
        (re.compile(r'(?:learned|discovered|realized|insight)', re.I), "semantic"),
        (re.compile(r'(?:did|completed|finished|accomplished)', re.I), "episodic"),
        (re.compile(r'(?:how to|steps to|procedure|process)', re.I), "procedural"),
        (re.compile(r'(?:prefer|always|never|rule)', re.I), "preference"),
    ]

    @property
    def scanner_type(self) -> str:
        return "memory"

    def scan_message(self, message: dict, line_num: int, session_id: str) -> Iterator[ScanResult]:
        content = self._extract_text(message)
        if not content or len(content) < 50:  # Skip very short messages
            return

        # Check for memory-worthy content
        memory_types = []
        for pattern, mem_type in self.MEMORY_PATTERNS:
            if pattern.search(content):
                memory_types.append(mem_type)

        if memory_types:
            primary_type = memory_types[0]
            yield ScanResult(
                scanner_type=self.scanner_type,
                entity_type=f"{primary_type}_memory",
                name=f"memory_{session_id}_{line_num}",
                confidence=0.5 + (len(memory_types) * 0.1),
                source_session=session_id,
                source_lines=[line_num],
                context={"memory_types": memory_types, "snippet": content[:300]},
                proposed_action="persist_to_memory"
            )

    def _extract_text(self, msg: dict) -> str:
        if isinstance(msg.get("message"), dict):
            content = msg["message"].get("content", "")
            if isinstance(content, list):
                return " ".join(c.get("text", "") for c in content if isinstance(c, dict))
            return str(content)
        return str(msg.get("content", ""))


# Scanner Registry
SCANNERS = {
    "synth": SynthScanner,
    "workflow": WorkflowScanner,
    "skill": SkillScanner,
    "doc": DocScanner,
    "memory": MemoryScanner,
}


def run_scanners(
    session_dir: Path,
    scanner_types: list[str] | None = None,
    min_confidence: float = 0.5
) -> Iterator[ScanResult]:
    """Run specified scanners on session directory."""

    types_to_run = scanner_types or list(SCANNERS.keys())

    for scanner_type in types_to_run:
        if scanner_type not in SCANNERS:
            print(f"Warning: Unknown scanner type '{scanner_type}'", file=sys.stderr)
            continue

        scanner = SCANNERS[scanner_type](session_dir)
        for result in scanner.scan_all():
            if result.confidence >= min_confidence:
                yield result


def persist_to_learning(results: list[ScanResult], output_path: Path = None) -> Path:
    """Persist scan results to learning system for rule evolution."""
    if output_path is None:
        output_path = Path.home() / ".lev" / "scan-history.jsonl"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "a") as f:
        for r in results:
            entry = {
                "timestamp": r.timestamp,
                "scanner_type": r.scanner_type,
                "entity_type": r.entity_type,
                "name": r.name,
                "confidence": r.confidence,
                "routing": r.routing,
                "source_session": r.source_session
            }
            f.write(json.dumps(entry) + "\n")

    return output_path


def format_as_ideas(results: list[ScanResult]) -> list[dict]:
    """Format high-confidence findings as idea candidates."""
    ideas = []
    for r in results:
        if r.routing.get("tier") in ("auto_route", "review_queue"):
            ideas.append({
                "title": f"[{r.scanner_type}] {r.name}",
                "type": r.entity_type,
                "confidence": r.confidence,
                "action": r.proposed_action,
                "source": r.source_session,
                "priority": "high" if r.confidence >= 0.8 else "medium",
                "handler": "code" if r.scanner_type in ("workflow", "skill") else "research"
            })
    return ideas


# =============================================================================
# RALPH INTEGRATION
# =============================================================================

# Completion promise templates per scanner type
RALPH_PROMISES = {
    "synth": 'synth "{name}" materialized at ~/clawd/synth/{type}/{name}.yaml with valid schema',
    "workflow": 'workflow "{name}" created at ~/lev/workflows/{name}.yaml with ≥3 steps',
    "skill": 'skill "{name}" scaffolded at ~/.claude/skills/{name}/SKILL.md with working triggers',
    "doc": 'documentation for "{name}" updated and all links verified',
    "memory": 'memory "{name}" persisted to lev-memory with appropriate tier routing',
}

# Destinations for materialized entities
RALPH_DESTINATIONS = {
    "synth": "~/clawd/synth/{subtype}/",
    "workflow": "~/lev/workflows/",
    "skill": "~/.claude/skills/",
    "doc": "{original_path}",
    "memory": "lev-memory://",
}


def create_completion_promise(result: ScanResult) -> str:
    """Create appropriate completion promise for a scanner finding."""
    template = RALPH_PROMISES.get(result.scanner_type, 'task "{name}" completed successfully')

    # Substitute variables
    promise = template.format(
        name=result.name,
        type=result.entity_type,
        subtype=result.entity_type.split("_")[0] if "_" in result.entity_type else "eph"
    )

    return promise


def generate_ralph_command(result: ScanResult, max_iterations: int = None) -> Optional[str]:
    """Generate /ralph invocation command for a scanner finding."""
    tier = result.routing.get("tier", "log_only")

    if tier == "log_only":
        return None

    promise = create_completion_promise(result)

    if tier == "auto_route":
        # High confidence: direct execution with strict promise
        iterations = max_iterations or 3
        return f'/ralph "{promise}" --max-iterations {iterations}'

    elif tier == "review_queue":
        # Medium confidence: refinement loop
        iterations = max_iterations or 5
        return f'/ralph "investigate and refine {result.name} to ≥0.8 confidence, then {promise}" --max-iterations {iterations}'

    return None


def generate_bd_task(result: ScanResult) -> dict:
    """Convert scanner finding to BD task format."""
    tier = result.routing.get("tier", "log_only")

    priority = "high" if result.confidence >= 0.8 else "medium" if result.confidence >= 0.6 else "low"

    task = {
        "subject": f"[{result.scanner_type}] {result.name}",
        "description": f"""## Scanner Detection

- **Type:** {result.entity_type}
- **Confidence:** {result.confidence:.2f}
- **Source Session:** {result.source_session}
- **Proposed Action:** {result.proposed_action}
- **Routing Tier:** {tier}

## Context
```json
{json.dumps(result.context, indent=2)}
```

## Routing
- **Tier:** {result.routing.get('tier')}
- **Destination:** {result.routing.get('destination')}
- **Action:** {result.routing.get('action')}

## Next Steps
- [ ] Review finding validity
- [ ] Execute proposed action
- [ ] Verify outcome
""",
        "labels": [result.scanner_type, tier, result.entity_type],
        "priority": priority,
        "metadata": {
            "scanner_type": result.scanner_type,
            "confidence": result.confidence,
            "source_session": result.source_session,
            "timestamp": result.timestamp
        }
    }

    return task


def format_as_ralph_commands(results: list[ScanResult]) -> list[dict]:
    """Format findings as Ralph commands for batch execution."""
    commands = []
    for r in results:
        cmd = generate_ralph_command(r)
        if cmd:
            commands.append({
                "name": r.name,
                "scanner_type": r.scanner_type,
                "confidence": r.confidence,
                "tier": r.routing.get("tier"),
                "ralph_command": cmd,
                "completion_promise": create_completion_promise(r)
            })
    return commands


def format_as_bd_tasks(results: list[ScanResult]) -> list[dict]:
    """Format findings as BD tasks."""
    tasks = []
    for r in results:
        if r.routing.get("tier") in ("auto_route", "review_queue"):
            tasks.append(generate_bd_task(r))
    return tasks


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Scan session history for entity candidates")
    parser.add_argument("--type", "-t", dest="scanner_types", action="append",
                       choices=list(SCANNERS.keys()) + ["all"],
                       help="Scanner type(s) to run")
    parser.add_argument("--session-dir", "-d", type=Path,
                       default=Path.home() / ".claude/projects",
                       help="Directory containing session JSONL files")
    parser.add_argument("--output", "-o",
                       choices=["jsonl", "yaml", "summary", "ideas", "ralph-commands", "bd-tasks"],
                       default="summary", help="Output format")
    parser.add_argument("--min-confidence", type=float, default=0.5,
                       help="Minimum confidence threshold")
    parser.add_argument("--persist", action="store_true",
                       help="Persist results to learning system")
    parser.add_argument("--tier", choices=["auto_route", "review_queue", "log_only", "all"],
                       default="all", help="Filter by routing tier")
    parser.add_argument("--max-results", type=int, default=None,
                       help="Limit number of results")

    args = parser.parse_args()

    # Handle "all" scanner type
    scanner_types = args.scanner_types
    if scanner_types and "all" in scanner_types:
        scanner_types = list(SCANNERS.keys())

    results = list(run_scanners(args.session_dir, scanner_types, args.min_confidence))

    # Filter by tier if specified
    if args.tier != "all":
        results = [r for r in results if r.routing.get("tier") == args.tier]

    # Limit results if specified
    if args.max_results:
        results = sorted(results, key=lambda x: -x.confidence)[:args.max_results]

    # Persist to learning system if requested
    if args.persist:
        log_path = persist_to_learning(results)
        print(f"Persisted {len(results)} results to {log_path}", file=sys.stderr)

    if args.output == "jsonl":
        for r in results:
            print(json.dumps(r.to_dict()))
    elif args.output == "yaml":
        if HAS_YAML:
            print(yaml.dump([r.to_dict() for r in results], default_flow_style=False))
        else:
            print(json.dumps([r.to_dict() for r in results], indent=2))
    elif args.output == "ideas":
        # Output as idea candidates for BD planning
        ideas = format_as_ideas(results)
        print(json.dumps({"ideas": ideas, "count": len(ideas)}, indent=2))
    elif args.output == "ralph-commands":
        # Output as Ralph commands for batch execution
        commands = format_as_ralph_commands(results)
        print(json.dumps({"commands": commands, "count": len(commands)}, indent=2))
    elif args.output == "bd-tasks":
        # Output as BD task definitions
        tasks = format_as_bd_tasks(results)
        print(json.dumps({"tasks": tasks, "count": len(tasks)}, indent=2))
    else:  # summary
        print(f"\n{'='*60}")
        print(f"Session Scanner Results (with routing)")
        print(f"{'='*60}\n")

        # Group by routing tier
        by_tier: dict[str, list[ScanResult]] = {}
        for r in results:
            tier = r.routing.get("tier", "unknown")
            by_tier.setdefault(tier, []).append(r)

        for tier in ["auto_route", "review_queue", "log_only"]:
            tier_results = by_tier.get(tier, [])
            if tier_results:
                icon = "⚡" if tier == "auto_route" else "📋" if tier == "review_queue" else "📝"
                print(f"\n{icon} {tier.upper()} ({len(tier_results)} findings)\n")
                for r in sorted(tier_results, key=lambda x: -x.confidence)[:5]:
                    print(f"  [{r.scanner_type}] {r.name}")
                    print(f"    confidence: {r.confidence:.2f} → {r.routing.get('action')}")
                    print(f"    destination: {r.routing.get('destination')}")
                    ralph_cmd = generate_ralph_command(r)
                    if ralph_cmd:
                        print(f"    ralph: {ralph_cmd[:60]}...")
                    print()

        print(f"\n{'='*60}")
        print(f"Total: {len(results)} | Auto: {len(by_tier.get('auto_route', []))} | Review: {len(by_tier.get('review_queue', []))} | Log: {len(by_tier.get('log_only', []))}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
