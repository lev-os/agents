// Graph × World Engine · parity synthesis data
// All 13 impls × 12 flows. Cell values: 'direct' | 'family' | 'adjacent' | null
// Binding text is shown on hover.

window.PARITY_DATA = (() => {
  const FLOWS = [
    { id: 'f01', n: '01', name: 'world engine authority',       short: 'world.authority',   lane: 'canon',     blurb: 'Append-only truth, overlays, proposal/gate/apply, receipts. Common root for every projection.' },
    { id: 'f02', n: '02', name: 'execution graph',              short: 'exec.graph',        lane: 'exec',      blurb: 'Admitted runtime topology, action queues, reconcile passes, optimizer hooks, continuity.' },
    { id: 'f03', n: '03', name: 'personal wiki graph',          short: 'personal.wiki',     lane: 'personal',  blurb: 'Private/reviewed memory. Wiki/giki, note projection, personal context export.' },
    { id: 'f04', n: '04', name: 'project graph',                short: 'project.graph',     lane: 'project',   blurb: 'Repo-local entities, patterns, design state, artifacts, team collaboration context.' },
    { id: 'f05', n: '05', name: 'org graph',                    short: 'org.graph',         lane: 'org',       blurb: 'Cross-project / shared memory, analytics, coordination overlays, governance.' },
    { id: 'f06', n: '06', name: 'domain graph template',        short: 'domain.template',   lane: 'domain',    blurb: 'Per-domain typed graphs — stamped from the kernel, never a fork.' },
    { id: 'f07', n: '07', name: 'context retrieval + selection',short: 'context.select',    lane: 'selector', blurb: 'Deterministic selectors, bounded retrieval, BFS, summarization. Context-pack builder.' },
    { id: 'f08', n: '08', name: 'projection view export',       short: 'projection.view',   lane: 'view',      blurb: 'Prompt-context export, living docs, dashboards, browser views, static read-models.' },
    { id: 'f09', n: '09', name: 'artifact overlay + versioning',short: 'artifact.overlay',  lane: 'overlay',   blurb: 'Immutable artifacts + overlay packaging + integrity chains. Bake / compile / read separation.' },
    { id: 'f10', n: '10', name: 'collaboration shell + continuity', short: 'collab.shell',  lane: 'continuity',blurb: 'Repo-state handoffs, worktree/boundary guardrails, session bootstrap, PM continuity.' },
    { id: 'f11', n: '11', name: 'validation benchmark fabric',  short: 'bench.fabric',      lane: 'benchmark', blurb: 'Falsifiable harness: LongMemEval, hypothesis suites, parity tests, promotion gates.' },
    { id: 'f12', n: '12', name: 'optimizer reconcile sidecar',  short: 'optim.sidecar',     lane: 'optim',     blurb: 'Bounded eqsat / canonicalization / rewrite search. Optional, not canon-critical.' },
  ];

  // d=direct, f=family, a=adjacent, .=none
  // Order of flows: f01..f12
  const IMPLS = [
    { id: 'graphnosis',          kind: 'core',   lane: 'near',    uniq: 3,
      title: 'graph-native context retrieval + audit projection',
      take: 'selector + BFS retrieval · graph export · audit projection · evaluation loop',
      verdict: 'Anchor of projection + selector clusters. Clean promote with existing owner path.',
      owner: 'core/graph + plugins/context',
      cells: 'd d . f . f d d . a f .',
      bindings: {
        f01: 'Feeds admitted substrate. Projection-aware from day one.',
        f02: 'Graph runtime is the execution substrate.',
        f04: 'Repo graph projection is a first-class read-model.',
        f06: 'Ships typed subgraph stamps for common domains.',
        f07: 'Selector BFS + summarization — THE reference flow.',
        f08: 'Audit projection + agent-context export.',
        f10: 'Session bootstrap derives from selector receipts.',
        f11: 'Evaluation loop is part of the kernel, not a test.'
      }},
    { id: 'contextnest',         kind: 'adj',    lane: 'near',    uniq: 3,
      title: 'selector governance + agent config generator',
      take: 'selector query · integrity chain · context projection · agent config generation',
      verdict: 'Maintainer-safe selector path. Strengthens near-term plugins/context + plugins/writer.',
      owner: 'plugins/context + plugins/writer',
      cells: 'f . f f . . d d a . f .',
      bindings: {
        f01: 'Integrity chain maps onto append-only receipts.',
        f03: 'Private memory with maintainer-governed queries.',
        f04: 'Per-repo config generator reads from project graph.',
        f07: 'Selector query + governance is the canonical form.',
        f08: 'Agent config file IS a projection view.',
        f09: 'Integrity chain ≈ overlay versioning discipline.',
        f11: 'Selector hypothesis suite exists.'
      }},
    { id: 'kage',                kind: 'adj',    lane: 'near',    uniq: 3,
      title: 'tiered memory + reviewed public projection',
      take: 'tiered memory · reviewed context · static public projection',
      verdict: 'Strengthens personal_wiki + selector lane with review-gate discipline.',
      owner: 'core/memory + plugins/context',
      cells: 'f . d . f . d d f . . .',
      bindings: {
        f01: 'Review gate mirrors proposal/gate/apply flow.',
        f03: 'Tiered personal memory — private / reviewed / public.',
        f05: 'Reviewed public tier is a shared-memory projection.',
        f07: 'Review-gated selection.',
        f08: 'Static public projection is the canonical export.',
        f09: 'Reviewed tier is an overlay packaging move.'
      }},
    { id: 'larql',               kind: 'core',   lane: 'mid',     uniq: 4,
      title: 'immutable artifacts + overlay packaging',
      take: 'bake / compile / read split · overlay packaging · browse → infer → compile pipeline',
      verdict: 'Cleanest artifact-overlay stack in the corpus. Distinct from memory and query rows.',
      owner: 'core/graph + core/memory',
      cells: 'd . . f f d a f d . . a',
      bindings: {
        f01: 'Artifact is the append-only primitive.',
        f04: 'Project artifacts live under overlay.',
        f05: 'Org knowledge is shipped as versioned bundles.',
        f06: 'Domain templates ship as typed overlays.',
        f07: 'Browse/infer/compile is a retrieval form.',
        f08: 'Compiled view = read-model.',
        f09: 'THE reference artifact+overlay stack.',
        f12: 'Canonicalization during compile step.'
      }},
    { id: 'codemix-graph',       kind: 'core',   lane: 'mid',     uniq: 2,
      title: 'property-graph runtime + adapters',
      take: 'property graph adapter · collaborative projection · storage adapter',
      verdict: 'Overlay / adapter evidence only. Plugs in, does not replace canon.',
      owner: 'core/graph (adapter)',
      cells: 'a d f f a . . f . a . .',
      bindings: {
        f01: 'Property-graph adapter layered over canon.',
        f02: 'Runtime topology as property graph.',
        f03: 'Personal graph is one adapter target.',
        f04: 'Project graph is one adapter target.',
        f05: 'Shared graph is one adapter target.',
        f08: 'Collaborative projection view.',
        f10: 'Session state rides the adapter.'
      }},
    { id: 'create-context-graph',kind: 'core',   lane: 'far',     uniq: 2,
      title: 'graph-app generator + connector registry',
      take: 'graph-app generator · scaffold matrix · connector registry',
      verdict: 'Scaffolds new graph applications. Useful, but far-lane compiler work.',
      owner: 'core/graph + plugins/platforms',
      cells: 'a . . f . d . f f . . .',
      bindings: {
        f01: 'Scaffolds are stamped from canon.',
        f04: 'Generator emits project-graph scaffolds.',
        f06: 'THE domain-template generator.',
        f08: 'Scaffold matrix emits view projections.',
        f09: 'Connector registry is an overlay.'
      }},
    { id: 'deepdive',            kind: 'core',   lane: 'mid',     uniq: 3,
      title: 'investigation runtime + OSINT ingest',
      take: 'investigation runtime · OSINT ingest · case linking · operator reports',
      verdict: 'Continuity witness. Feeds collaboration lane without replacing kernel.',
      owner: 'continuity lane',
      cells: 'a d . f d f . f . d . .',
      bindings: {
        f01: 'Case records are append-only.',
        f02: 'Investigation runtime = specialized exec graph.',
        f04: 'Per-case project graphs.',
        f05: 'Team / org case-linking.',
        f06: 'Typed domain schema per investigation.',
        f08: 'Operator reports.',
        f10: 'Longest continuity witness in the corpus.'
      }},
    { id: 'design-graph',        kind: 'core',   lane: 'out',     uniq: 2,
      title: 'design canvas + eager parallel authoring',
      take: 'design canvas · browser projection · eager parallel authoring',
      verdict: 'Projection / export witness only. Not a kernel — feeds projection-view lane.',
      owner: 'feeds projection-view lane',
      cells: '. . . a . a . d . a . .',
      bindings: {
        f04: 'Design state overlays the project graph.',
        f06: 'Design tokens as a domain template.',
        f08: 'Canvas is a projection view.',
        f10: 'Eager parallel authoring = continuity flavor.'
      }},
    { id: 'e-graphs-primer',     kind: 'core',   lane: 'mid',     uniq: 5,
      title: 'eqsat / rewrite / canonicalization',
      take: 'bounded rewrite runtime · optimizer sidecar · canonicalization',
      verdict: 'Highest uniqueness leverage in the corpus. Promote as sidecar, not kernel.',
      owner: 'core/flowmind + core/graph (sidecar)',
      cells: 'a d . . . a . . a . f d',
      bindings: {
        f01: 'Canonicalization preserves append-only authority.',
        f02: 'Rewrite runtime sits beside exec graph.',
        f06: 'Domain-specific rulesets.',
        f09: 'Canonical form is an overlay discipline.',
        f11: 'Rewrite hypothesis testing.',
        f12: 'THE optimizer sidecar reference.'
      }},
    { id: 'nofs-dreamgraph',     kind: 'core',   lane: 'mid',     uniq: 5,
      title: 'graph-native substrate + living docs',
      take: 'graph-native substrate · living docs · autonomy modes · validation bundle',
      verdict: 'Philosophical mirror. Richest validation / living-docs bundle. Never adopt wholesale.',
      owner: 'projection + benchmark + optimizer lanes',
      cells: 'd d f f f f a d a f d a',
      bindings: {
        f01: 'Philosophical mirror of world-engine authority.',
        f02: 'Autonomy modes ride the execution graph.',
        f03: 'Personal notes → substrate edges.',
        f04: 'Project graph is substrate-native.',
        f05: 'Org graph is substrate-native.',
        f06: 'Domain typing is substrate-native.',
        f08: 'Living docs is the view export.',
        f10: 'Autonomy mode = continuity posture.',
        f11: 'Richest validation bundle in the corpus.',
        f12: 'Optimizer passes exist but unbounded.'
      }},
    { id: 'worldseed',           kind: 'core',   lane: 'far',     uniq: 5,
      title: 'world / runtime tick loop + scenario eval',
      take: 'world-runtime tick loop · inbox wakeup · scenario eval · operator dashboards',
      verdict: 'Strongest execution-graph contributor, but scope is too broad. World-model only.',
      owner: 'world-model + plugins/gameai',
      cells: 'f d . . d d . f . f d .',
      bindings: {
        f01: 'World model IS a projection of authority.',
        f02: 'Tick loop + inbox wakeup = reference exec topology.',
        f05: 'Scenario eval feeds org analytics.',
        f06: 'Per-scenario domain templates.',
        f08: 'Operator dashboards.',
        f10: 'Scenario handoff = continuity.',
        f11: 'Scenario harness is a benchmark fabric.'
      }},
    { id: 'egregore',            kind: 'ctrl',   lane: 'mid',     uniq: 4,
      title: 'collaboration shell + repo-state boundary',
      take: 'collaboration shell · repo-state handoff · worktree boundary · dashboards',
      verdict: 'Confirms collaboration lane as a real family. Control surface, above kernel.',
      owner: 'plugins/prompt-stack + dna/pm',
      cells: '. a . f f . . f . d . .',
      bindings: {
        f02: 'Shell coordinates with runtime but sits above.',
        f04: 'Repo-state boundary wraps project graph.',
        f05: 'Shared dashboards.',
        f08: 'Dashboards are projection views.',
        f10: 'THE collaboration-shell reference.'
      }},
    { id: 'agentfab',            kind: 'adj',    lane: 'adapter', uniq: 2,
      title: 'distributed control plane + task leases',
      take: 'distributed control plane · task leases · node admission · review loop',
      verdict: 'Graph-adjacent — adapter only. Strengthens execution + org coverage.',
      owner: 'adapter only — does not change minimum set',
      cells: 'a d . . f . . . . a f .',
      bindings: {
        f01: 'Admission events map to proposal/gate/apply.',
        f02: 'Distributed control plane = exec runtime variant.',
        f05: 'Leases / nodes live in org scope.',
        f10: 'Task handoff = continuity flavor.',
        f11: 'Review loop is a validation shape.'
      }},
  ];

  // Parse 'd d . f .' etc into cell objects aligned to FLOWS
  IMPLS.forEach(impl => {
    const tokens = impl.cells.trim().split(/\s+/);
    impl.cellMap = {};
    tokens.forEach((t, i) => {
      const flow = FLOWS[i];
      if (!flow) return;
      let kind = null;
      if (t === 'd') kind = 'direct';
      else if (t === 'f') kind = 'family';
      else if (t === 'a') kind = 'adjacent';
      impl.cellMap[flow.id] = {
        kind,
        binding: impl.bindings[flow.id] || null,
      };
    });
  });

  const LANES = [
    { id: 'all',     label: 'ALL',     count: 13 },
    { id: 'near',    label: 'NEAR',    count: 3 },
    { id: 'mid',     label: 'MID',     count: 6 },
    { id: 'far',     label: 'FAR',     count: 2 },
    { id: 'adapter', label: 'ADAPTER', count: 1 },
    { id: 'out',     label: 'STAYS·OUT', count: 1 },
  ];

  const PROJECTIONS = [
    { id: 'world',    label: 'WORLD · ENGINE',   sub: 'append-only · authority · canon', impls: null,  role: 'ROOT' },
    { id: 'exec',     label: 'EXECUTION · GRAPH',sub: 'runtime topology · action queues · reconcile', impls: 6, role: 'PROJECTION',
      examples: 'worldseed · nofs · e-graphs' },
    { id: 'personal', label: 'PERSONAL · WIKI',  sub: 'private memory · giki', impls: 5, role: 'PROJECTION',
      examples: 'kage · contextnest · graphnosis' },
    { id: 'project',  label: 'PROJECT · GRAPH',  sub: 'repo-local · artifacts · design state', impls: 9, role: 'PROJECTION',
      examples: 'graphnosis · larql · kage' },
    { id: 'org',      label: 'ORG · GRAPH',      sub: 'shared memory · governance · analytics', impls: 7, role: 'PROJECTION',
      examples: 'codemix · deepdive · worldseed' },
    { id: 'domain',   label: 'DOMAIN · GRAPH',   sub: 'typed scaffolds · per-domain templates', impls: 10, role: 'PROJECTION',
      examples: 'larql · design · e-graphs' },
  ];

  const PROMOTION_LANES = [
    { tier: 'NEAR', items: [
      { name: 'selector · projection lane', score: 5, owners: 'plugins/context · plugins/writer · core/memory · core/index' },
      { name: 'projection · view · export', score: 5, owners: 'core/graph · plugins/now · community/agentping · plugins/writer' },
      { name: 'validation · benchmark fabric', score: 4, owners: 'core/testing · plugins/bench · dna/testing · core/memory' },
    ]},
    { tier: 'MID', items: [
      { name: 'collaboration shell · continuity', score: 4, owners: 'plugins/prompt-stack · dna/pm · community/agentping' },
      { name: 'immutable artifact · overlay', score: 3, owners: 'core/graph · core/memory · plugins/graph-adapters' },
      { name: 'bounded optimizer · eqsat spike', score: 3, owners: 'core/flowmind · core/graph · plugins/code-graph' },
    ]},
    { tier: 'FAR', items: [
      { name: 'world-runtime · scene simulation', score: 2, owners: 'world-model · plugins/gameai · community/agentping' },
      { name: 'graph-app · generator · compiler', score: 2, owners: 'core/graph · core/index · plugins/platforms' },
    ]},
  ];

  return { FLOWS, IMPLS, LANES, PROJECTIONS, PROMOTION_LANES };
})();
