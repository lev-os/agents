# Tool Filtering & Capability Gating

> **Principle**: Agents don't need all tools all the time. Adaptive tool exposure reduces context by ~70% for minimal profiles and prevents capability confusion.

## The Problem

Large tool menus degrade agent success rates by 85%. Agents:
- Get confused by irrelevant options
- Waste context on tool documentation they don't need
- Make mistakes choosing between similar-sounding tools

## Solution: Post-Registration Filtering

Filter tools AFTER registration based on settings and context:

```python
def _apply_tool_filter(mcp: FastMCP, settings: Settings) -> None:
    """
    Remove tools from registry based on profile settings.
    Called after all tools are registered but before server starts.
    """
    if not settings.tool_filter.enabled:
        return

    tool_manager = getattr(mcp, "_tool_manager", None)
    if tool_manager is None:
        return

    tools_registry = getattr(tool_manager, "_tools", None)
    if tools_registry is None:
        return

    to_remove: list[str] = []
    for tool_name in list(tools_registry.keys()):
        cluster = TOOL_CLUSTER_MAP.get(tool_name, "unclassified")
        if not _should_expose_tool(tool_name, cluster, settings):
            to_remove.append(tool_name)

    for tool_name in to_remove:
        del tools_registry[tool_name]

    logger.info(f"Tool filter removed {len(to_remove)} tools, "
                f"{len(tools_registry)} remaining")
```

## Tool Cluster Mapping

Organize tools into semantic clusters (≤7 per cluster):

```python
TOOL_CLUSTER_MAP = {
    # Core messaging cluster
    "send_message": "messaging",
    "reply_message": "messaging",
    "fetch_inbox": "messaging",
    "mark_message_read": "messaging",
    "acknowledge_message": "messaging",
    "search_messages": "messaging",

    # Identity cluster
    "ensure_project": "identity",
    "register_agent": "identity",
    "create_agent_identity": "identity",
    "whois": "identity",

    # Coordination cluster
    "file_reservation_paths": "coordination",
    "release_file_reservations": "coordination",
    "renew_file_reservations": "coordination",
    "force_release_file_reservation": "coordination",

    # Contact management cluster
    "request_contact": "contacts",
    "respond_contact": "contacts",
    "list_contacts": "contacts",
    "set_contact_policy": "contacts",

    # Workflow macros cluster
    "macro_start_session": "macros",
    "macro_prepare_thread": "macros",
    "macro_file_reservation_cycle": "macros",
    "macro_contact_handshake": "macros",

    # Analysis cluster
    "summarize_thread": "analysis",

    # Admin cluster
    "install_precommit_guard": "admin",
    "uninstall_precommit_guard": "admin",
    "health_check": "admin",
}
```

## Profile Definitions

Define profiles for different agent capabilities:

```python
@dataclass(slots=True, frozen=True)
class ToolFilterSettings:
    enabled: bool = False
    profile: str = "full"  # "full" | "core" | "minimal" | "messaging" | "custom"
    mode: str = "include"  # "include" | "exclude"
    clusters: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)

PROFILE_CLUSTERS = {
    "full": None,  # All tools
    "core": ["messaging", "identity", "coordination"],
    "minimal": ["messaging", "identity"],
    "messaging": ["messaging"],
    "custom": None,  # Use explicit clusters/tools
}
```

## Capability Metadata

Attach capability requirements to tools:

```python
TOOL_CAPABILITIES = {
    "send_message": {"requires": ["messaging"], "optional": ["attachments"]},
    "summarize_thread": {"requires": ["analysis"], "optional": ["llm"]},
    "file_reservation_paths": {"requires": ["coordination"]},
    "macro_start_session": {"requires": ["messaging", "identity"]},
}

def _should_expose_tool(tool_name: str, cluster: str, settings: Settings) -> bool:
    """Determine if tool should be exposed based on profile and capabilities."""
    profile = settings.tool_filter.profile

    # Full profile exposes everything
    if profile == "full":
        return True

    # Custom mode uses explicit include/exclude lists
    if profile == "custom":
        if settings.tool_filter.mode == "include":
            return (tool_name in settings.tool_filter.tools or
                    cluster in settings.tool_filter.clusters)
        else:  # exclude
            return (tool_name not in settings.tool_filter.tools and
                    cluster not in settings.tool_filter.clusters)

    # Named profiles use cluster membership
    allowed_clusters = PROFILE_CLUSTERS.get(profile, [])
    if allowed_clusters is None:
        return True
    return cluster in allowed_clusters
```

## Resource-Based Capability Query

Let agents discover available capabilities:

```python
@mcp.resource("resource://tooling/capabilities")
def capabilities_resource() -> str:
    """
    Query available tool capabilities.

    Returns JSON with:
    - enabled_clusters: list of active tool clusters
    - available_tools: list of exposed tool names
    - profile: current filter profile
    - total_tools: number of exposed tools
    """
    tool_manager = getattr(mcp, "_tool_manager", None)
    tools = list(getattr(tool_manager, "_tools", {}).keys())

    # Group by cluster
    clusters = set()
    for tool in tools:
        cluster = TOOL_CLUSTER_MAP.get(tool, "unclassified")
        clusters.add(cluster)

    return json.dumps({
        "profile": settings.tool_filter.profile,
        "enabled_clusters": sorted(clusters),
        "available_tools": sorted(tools),
        "total_tools": len(tools),
    }, indent=2)
```

## Context Reduction Metrics

| Profile | Tools | Clusters | Context Reduction |
|---------|-------|----------|-------------------|
| full | 25+ | 7 | 0% |
| core | 12-15 | 3 | ~40% |
| minimal | 5-7 | 2 | ~70% |
| messaging | 6 | 1 | ~75% |

## Dynamic Capability Adjustment

Adjust capabilities based on agent behavior:

```python
class CapabilityTracker:
    """Track which capabilities agents actually use."""

    def __init__(self):
        self.usage: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def record_tool_call(self, agent_name: str, tool_name: str):
        cluster = TOOL_CLUSTER_MAP.get(tool_name, "unclassified")
        self.usage[agent_name][cluster] += 1

    def suggest_profile(self, agent_name: str) -> str:
        """Suggest optimal profile based on usage patterns."""
        used_clusters = set(self.usage[agent_name].keys())

        if len(used_clusters) <= 2:
            return "minimal"
        elif used_clusters <= {"messaging", "identity", "coordination"}:
            return "core"
        else:
            return "full"
```

## Do / Don't

**Do:**
- Start with minimal profile, expand if needed
- Use cluster-based filtering for maintainability
- Expose capability query resource
- Log filtering decisions for debugging

**Don't:**
- Filter tools during registration (use post-registration)
- Create overly fine-grained profiles
- Remove identity cluster (agents need to register)
- Filter without providing capability discovery

## Configuration Examples

Environment variables:
```bash
# Minimal agent setup
TOOL_FILTER_ENABLED=true
TOOL_FILTER_PROFILE=minimal

# Custom cluster selection
TOOL_FILTER_ENABLED=true
TOOL_FILTER_PROFILE=custom
TOOL_FILTER_MODE=include
TOOL_FILTER_CLUSTERS=messaging,coordination

# Exclude specific tools
TOOL_FILTER_ENABLED=true
TOOL_FILTER_PROFILE=custom
TOOL_FILTER_MODE=exclude
TOOL_FILTER_TOOLS=install_precommit_guard,uninstall_precommit_guard
```

## Integration with Settings Hierarchy

Tool filtering integrates with the broader settings system:

```python
@dataclass(slots=True, frozen=True)
class Settings:
    # ... other settings ...
    tool_filter: ToolFilterSettings = field(default_factory=ToolFilterSettings)

def load_settings() -> Settings:
    """Load settings with tool filter configuration."""
    return Settings(
        tool_filter=ToolFilterSettings(
            enabled=_bool(os.getenv("TOOL_FILTER_ENABLED", "false")),
            profile=os.getenv("TOOL_FILTER_PROFILE", "full"),
            mode=os.getenv("TOOL_FILTER_MODE", "include"),
            clusters=os.getenv("TOOL_FILTER_CLUSTERS", "").split(","),
            tools=os.getenv("TOOL_FILTER_TOOLS", "").split(","),
        ),
        # ... other settings ...
    )
```
