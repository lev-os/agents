# Tool skills in Lev and worker prompts

## Contents

- [Load the integration](#load-the-integration)
- [Resolve a skill reference](#resolve-a-skill-reference)
- [Pass it to a worker](#pass-it-to-a-worker)
- [FlowMind and Lev IR](#flowmind-and-lev-ir)
- [Verification boundary](#verification-boundary)

## Load the integration

For tool operations, load `skill://tools`, read its
[contents table](../../tools/SKILL.md), then load only the selected integration.
Each leaf carries its own `SKILL.md`, installation instructions and needed
resources. The Tools package is part of Lev's skill surface; it does not need
an additional plugin. Installing an executable and connecting a provider remain
separate effects from reading guidance.

## Resolve a skill reference

The loading form is `skill://<top-level-or-db-id>`. Top-level names are the
registered exposed skills. For a database skill, use the ID actually reported
by the current inventory, not a new URI made from a display title or guessed
filesystem path. Follow `skill://skill-discovery` when discovery is needed.

The current `lev-skills inventory --json` interface reports `skill_uri`, `path`
and `path_key`. Its owner rebuilds those derived fields through `lev-skills
inventory --rebuild`. Exact selection must match the intended package path;
zero matches are missing and distinct packages sharing an ID are ambiguous.
Do not silently pick the first ranked variant. A top-level `skill://tools`
plus its relative leaf pointer remains a valid route when a leaf ID is
ambiguous. Do not hand-edit the generated inventory or graph.

## Pass it to a worker

Before dispatch, the selected worker must receive either access to the same
installed skill/catalog tree or a complete staged copy of the selected package.
Record the selected URI, actual skill file, package base directory, relevant
reference paths and allowed task effects. Preserve relative layout, scripts,
licenses and executable bits. A remote worker needs an actual mounted/synced
package or supplied content; a path on the parent's Mac does not prove access.

The worker loads the selected skill and required references before acting. A
missing required resource stops that branch with its exact path; it is not a
reason to invent an installer, substitute a similarly named tool or broaden
permissions. Use the leaf's installation instructions for an explicitly
requested setup task. Credentials remain in the target runtime's existing
custody and are never copied into the skill package or worker prompt.

## FlowMind and Lev IR

The included [tools.flow.yaml](tools.flow.yaml) follows the existing FlowMind
agent-prompt convention: its sole node has `prompt: skill://tools`. The graph
ends when that guidance task returns. It has no unconditional next effect,
installation, MCP connection or plugin activation. The caller still supplies
the actual task, scoped context and a worker capable of the loading contract.

FlowMind carries the guidance reference; the host loads the instructions.
Use the same exact top-level/database-ID selection for other skill prompts.
`skill://` is not added to the Lev runtime URI registry. Effects are still
owned by the execution path and its actual `lev://exec/...` target.

When inspecting the Lev source checkout, the current source links are:

| Concern | Repository-relative owner source |
|---|---|
| Existing skill prompts in lifecycle declarations | `core/flowmind/system/lifecycle.flow.yaml` |
| Prompt reference and no-automatic-effect checks | `core/flowmind/src/__tests__/lifecycle-declaration-references.test.ts` |
| FlowMind-to-skill-pack projection | `core/flowmind/src/targets/skill-pack.ts` |
| Runtime versus prompt URI boundary | `dna/standards/uri-schemes.yaml` |

Resolve those paths from the actual Lev source checkout. This package's
FlowMind declaration is a local asset, not a newly registered CLI command.

## Verification boundary

Structural checks prove package links, inventory identity and FlowMind shape.
A fresh worker that reads the selected skill and resources proves loading on
that tested host. Neither proves remote visibility, universal host support,
provider credentials or an integration action. For a requested runtime task,
verify its actual worker receipt and the requested tool result independently.
