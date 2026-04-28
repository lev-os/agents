// data-fixtures.js — three datasets for the matrix-widget demo harness.
// Dataset #1 is the real GXW 13×12 parity matrix (adapted from graph-world-engine/data.js).

// ── DATASET 1 · GXW 13×12 parity matrix ──────────────────────────────────

const GXW_FLOWS = [
  { id: 'f01', n: '01', short: 'world.authority',  lane: 'canon',      name: 'world engine authority',          blurb: 'Append-only truth, overlays, proposal/gate/apply, receipts.' },
  { id: 'f02', n: '02', short: 'exec.graph',       lane: 'exec',       name: 'execution graph',                  blurb: 'Admitted runtime topology, action queues, reconcile passes.' },
  { id: 'f03', n: '03', short: 'personal.wiki',    lane: 'personal',   name: 'personal wiki graph',              blurb: 'Private/reviewed memory. Wiki/giki, note projection.' },
  { id: 'f04', n: '04', short: 'project.graph',    lane: 'project',    name: 'project graph',                    blurb: 'Repo-local entities, patterns, design state, artifacts.' },
  { id: 'f05', n: '05', short: 'org.graph',        lane: 'org',        name: 'org graph',                        blurb: 'Cross-project / shared memory, analytics, coordination.' },
  { id: 'f06', n: '06', short: 'domain.template',  lane: 'domain',     name: 'domain graph template',            blurb: 'Per-domain typed graphs — stamped from the kernel.' },
  { id: 'f07', n: '07', short: 'context.select',   lane: 'selector',   name: 'context retrieval + selection',    blurb: 'Deterministic selectors, bounded retrieval, summarization.' },
  { id: 'f08', n: '08', short: 'projection.view',  lane: 'view',       name: 'projection view export',           blurb: 'Prompt-context export, living docs, dashboards.' },
  { id: 'f09', n: '09', short: 'artifact.overlay', lane: 'overlay',    name: 'artifact overlay + versioning',    blurb: 'Immutable artifacts + overlay packaging + integrity chains.' },
  { id: 'f10', n: '10', short: 'collab.shell',     lane: 'continuity', name: 'collaboration shell + continuity', blurb: 'Repo-state handoffs, worktree guardrails, session bootstrap.' },
  { id: 'f11', n: '11', short: 'bench.fabric',     lane: 'benchmark',  name: 'validation benchmark fabric',      blurb: 'Falsifiable harness: hypothesis suites, parity tests.' },
  { id: 'f12', n: '12', short: 'optim.sidecar',    lane: 'optim',      name: 'optimizer reconcile sidecar',      blurb: 'Bounded eqsat / canonicalization / rewrite search.' },
];

const GXW_IMPLS_RAW = [
  { id: 'graphnosis',          lane: 'near',    uniq: 3, cells: 'd d . f . f d d . a f .', bindings: { f01: 'Feeds admitted substrate. Projection-aware from day one.', f02: 'Graph runtime is the execution substrate.', f04: 'Repo graph projection is a first-class read-model.', f06: 'Ships typed subgraph stamps for common domains.', f07: 'Selector BFS + summarization — THE reference flow.', f08: 'Audit projection + agent-context export.', f10: 'Session bootstrap derives from selector receipts.', f11: 'Evaluation loop is part of the kernel, not a test.' } },
  { id: 'contextnest',         lane: 'near',    uniq: 3, cells: 'f . f f . . d d a . f .', bindings: { f01: 'Integrity chain maps onto append-only receipts.', f03: 'Private memory with maintainer-governed queries.', f04: 'Per-repo config generator reads from project graph.', f07: 'Selector query + governance is the canonical form.', f08: 'Agent config file IS a projection view.', f09: 'Integrity chain ≈ overlay versioning discipline.', f11: 'Selector hypothesis suite exists.' } },
  { id: 'kage',                lane: 'near',    uniq: 3, cells: 'f . d . f . d d f . . .', bindings: { f01: 'Review gate mirrors proposal/gate/apply flow.', f03: 'Tiered personal memory — private / reviewed / public.', f05: 'Reviewed public tier is a shared-memory projection.', f07: 'Review-gated selection.', f08: 'Static public projection is the canonical export.', f09: 'Reviewed tier is an overlay packaging move.' } },
  { id: 'larql',               lane: 'mid',     uniq: 4, cells: 'd . . f f d a f d . . a', bindings: { f01: 'Artifact is the append-only primitive.', f04: 'Project artifacts live under overlay.', f05: 'Org knowledge is shipped as versioned bundles.', f06: 'Domain templates ship as typed overlays.', f07: 'Browse/infer/compile is a retrieval form.', f08: 'Compiled view = read-model.', f09: 'THE reference artifact+overlay stack.', f12: 'Canonicalization during compile step.' } },
  { id: 'codemix-graph',       lane: 'mid',     uniq: 2, cells: 'a d f f a . . f . a . .', bindings: { f01: 'Property-graph adapter layered over canon.', f02: 'Runtime topology as property graph.', f03: 'Personal graph is one adapter target.', f04: 'Project graph is one adapter target.', f05: 'Shared graph is one adapter target.', f08: 'Collaborative projection view.', f10: 'Session state rides the adapter.' } },
  { id: 'create-context-graph',lane: 'far',     uniq: 2, cells: 'a . . f . d . f f . . .', bindings: { f01: 'Scaffolds are stamped from canon.', f04: 'Generator emits project-graph scaffolds.', f06: 'THE domain-template generator.', f08: 'Scaffold matrix emits view projections.', f09: 'Connector registry is an overlay.' } },
  { id: 'deepdive',            lane: 'mid',     uniq: 3, cells: 'a d . f d f . f . d . .', bindings: { f01: 'Case records are append-only.', f02: 'Investigation runtime = specialized exec graph.', f04: 'Per-case project graphs.', f05: 'Team / org case-linking.', f06: 'Typed domain schema per investigation.', f08: 'Operator reports.', f10: 'Longest continuity witness in the corpus.' } },
  { id: 'design-graph',        lane: 'out',     uniq: 2, cells: '. . . a . a . d . a . .', bindings: { f04: 'Design state overlays the project graph.', f06: 'Design tokens as a domain template.', f08: 'Canvas is a projection view.', f10: 'Eager parallel authoring = continuity flavor.' } },
  { id: 'e-graphs-primer',     lane: 'mid',     uniq: 5, cells: 'a d . . . a . . a . f d', bindings: { f01: 'Canonicalization preserves append-only authority.', f02: 'Rewrite runtime sits beside exec graph.', f06: 'Domain-specific rulesets.', f09: 'Canonical form is an overlay discipline.', f11: 'Rewrite hypothesis testing.', f12: 'THE optimizer sidecar reference.' } },
  { id: 'nofs-dreamgraph',     lane: 'mid',     uniq: 5, cells: 'd d f f f f a d a f d a', bindings: { f01: 'Philosophical mirror of world-engine authority.', f02: 'Autonomy modes ride the execution graph.', f03: 'Personal notes → substrate edges.', f04: 'Project graph is substrate-native.', f05: 'Org graph is substrate-native.', f06: 'Domain typing is substrate-native.', f08: 'Living docs is the view export.', f10: 'Autonomy mode = continuity posture.', f11: 'Richest validation bundle in the corpus.', f12: 'Optimizer passes exist but unbounded.' } },
  { id: 'worldseed',           lane: 'far',     uniq: 5, cells: 'f d . . d d . f . f d .', bindings: { f01: 'World model IS a projection of authority.', f02: 'Tick loop + inbox wakeup = reference exec topology.', f05: 'Scenario eval feeds org analytics.', f06: 'Per-scenario domain templates.', f08: 'Operator dashboards.', f10: 'Scenario handoff = continuity.', f11: 'Scenario harness is a benchmark fabric.' } },
  { id: 'egregore',            lane: 'mid',     uniq: 4, cells: '. a . f f . . f . d . .', bindings: { f02: 'Shell coordinates with runtime but sits above.', f04: 'Repo-state boundary wraps project graph.', f05: 'Shared dashboards.', f08: 'Dashboards are projection views.', f10: 'THE collaboration-shell reference.' } },
  { id: 'agentfab',            lane: 'adapter', uniq: 2, cells: 'a d . . f . . . . a f .', bindings: { f01: 'Admission events map to proposal/gate/apply.', f02: 'Distributed control plane = exec runtime variant.', f05: 'Leases / nodes live in org scope.', f10: 'Task handoff = continuity flavor.', f11: 'Review loop is a validation shape.' } },
];

function expandCells(flows, rows) {
  const cells = {};
  const map = { d: 'direct', f: 'family', a: 'adjacent' };
  rows.forEach(row => {
    const tokens = row.cells.trim().split(/\s+/);
    cells[row.id] = {};
    tokens.forEach((t, i) => {
      const flow = flows[i];
      if (!flow) return;
      const kind = map[t] || null;
      if (!kind) return;
      cells[row.id][flow.id] = {
        kind,
        binding: (row.bindings && row.bindings[flow.id]) || null,
      };
    });
  });
  return cells;
}

const gxwCells = expandCells(GXW_FLOWS, GXW_IMPLS_RAW);
const gxwRows = GXW_IMPLS_RAW.map(r => ({ id: r.id, label: r.id, lane: r.lane, uniq: r.uniq }));

const GXW_LANE_FILTERS = [
  { id: 'all',     label: 'ALL',       count: 13 },
  { id: 'near',    label: 'NEAR',      count: 3 },
  { id: 'mid',     label: 'MID',       count: 6 },
  { id: 'far',     label: 'FAR',       count: 2 },
  { id: 'adapter', label: 'ADAPTER',   count: 1 },
  { id: 'out',     label: 'STAYS·OUT', count: 1 },
];

export const FIXTURE_GXW = {
  rowLabel: 'IMPL',
  colLabel: 'FLOW',
  laneFilterLabel: 'Filter · lane',
  bindingHint: 'Hover a cell to see the exact binding. 13 impls × 12 flows = 156 comparisons.',
  laneLabels: { near: 'near', mid: 'mid', far: 'far', adapter: 'adapter', out: 'stays·out' },
  rows: gxwRows,
  cols: GXW_FLOWS,
  cells: gxwCells,
  laneFilters: GXW_LANE_FILTERS,
};

// ── DATASET 2 · synthetic 5×5 tools × capabilities ───────────────────────

export const FIXTURE_TOOLS = {
  rowLabel: 'TOOL',
  colLabel: 'CAP',
  bindingHint: 'Hover any cell to see tool × capability binding.',
  rows: [
    { id: 'ripgrep', label: 'ripgrep',  lane: 'near', uniq: 3 },
    { id: 'fd',      label: 'fd',       lane: 'near', uniq: 2 },
    { id: 'ast',     label: 'ast-grep', lane: 'mid',  uniq: 4 },
    { id: 'lsp',     label: 'lsp',      lane: 'mid',  uniq: 5 },
    { id: 'tree',    label: 'treesit',  lane: 'far',  uniq: 3 },
  ],
  cols: [
    { id: 'search',  n: 'C1', short: 'search',  lane: 'read',  name: 'text search',      blurb: 'Raw string / regex over file trees.' },
    { id: 'struct',  n: 'C2', short: 'struct',  lane: 'read',  name: 'structural query', blurb: 'AST-aware match patterns.' },
    { id: 'rename',  n: 'C3', short: 'rename',  lane: 'write', name: 'safe rename',      blurb: 'Symbol rename across files.' },
    { id: 'refs',    n: 'C4', short: 'refs',    lane: 'read',  name: 'find references',  blurb: 'Locate symbol usages.' },
    { id: 'diag',    n: 'C5', short: 'diag',    lane: 'read',  name: 'diagnostics',      blurb: 'Type + lint errors per file.' },
  ],
  cells: {
    ripgrep: { search: 'direct',  struct: 'adjacent', refs: 'family',   diag: 'none',     rename: 'none' },
    fd:      { search: 'family',  struct: 'none',     refs: 'none',     diag: 'none',     rename: 'none' },
    ast:     { search: 'family',  struct: 'direct',   refs: 'family',   diag: 'adjacent', rename: 'family' },
    lsp:     { search: 'adjacent',struct: 'family',   refs: 'direct',   diag: 'direct',   rename: 'direct' },
    tree:    { search: 'none',    struct: 'direct',   refs: 'adjacent', diag: 'none',     rename: 'adjacent' },
  },
  laneFilters: [
    { id: 'all',  label: 'ALL',  count: 5 },
    { id: 'near', label: 'NEAR', count: 2 },
    { id: 'mid',  label: 'MID',  count: 2 },
    { id: 'far',  label: 'FAR',  count: 1 },
  ],
};

// ── DATASET 3 · synthetic 3×8 CI × Local ─────────────────────────────────

export const FIXTURE_CI = {
  rowLabel: 'ENV',
  colLabel: 'CHECK',
  bindingHint: 'Three envs, eight checks — direct/family/adjacent/none.',
  rows: [
    { id: 'local', label: 'local-dev',     lane: 'near' },
    { id: 'pr',    label: 'pr-ci',         lane: 'mid'  },
    { id: 'main',  label: 'main-pipeline', lane: 'mid'  },
  ],
  cols: [
    { id: 'lint',   n: '1', short: 'lint',     name: 'linter' },
    { id: 'unit',   n: '2', short: 'unit',     name: 'unit tests' },
    { id: 'int',    n: '3', short: 'integ',    name: 'integration' },
    { id: 'e2e',    n: '4', short: 'e2e',      name: 'end-to-end' },
    { id: 'type',   n: '5', short: 'types',    name: 'type check' },
    { id: 'build',  n: '6', short: 'build',    name: 'production build' },
    { id: 'sec',    n: '7', short: 'security', name: 'security scan' },
    { id: 'deploy', n: '8', short: 'deploy',   name: 'deploy gate' },
  ],
  cells: {
    local: { lint: 'direct', unit: 'direct', int: 'family',   e2e: 'adjacent', type: 'direct', build: 'family',  sec: 'none',     deploy: 'none'   },
    pr:    { lint: 'direct', unit: 'direct', int: 'direct',   e2e: 'family',   type: 'direct', build: 'direct',  sec: 'family',   deploy: 'none'   },
    main:  { lint: 'family', unit: 'family', int: 'direct',   e2e: 'direct',   type: 'family', build: 'direct',  sec: 'direct',   deploy: 'direct' },
  },
  laneFilters: [
    { id: 'all',  label: 'ALL',  count: 3 },
    { id: 'near', label: 'NEAR', count: 1 },
    { id: 'mid',  label: 'MID',  count: 2 },
  ],
};
