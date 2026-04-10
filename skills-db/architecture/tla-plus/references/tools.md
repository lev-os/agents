# Tools and Surfaces

## Editors and IDEs

- VS Code extension is the fastest current path for most users.
  It supports syntax highlighting, PlusCal translation, TLC runs, result visualization, formatting, completion, and PDF generation.
- Toolbox still exists as the classic IDE surface.
  Current official repo docs describe it as available but unmaintained.

## CLI and official tools

The official tools ship through `tla2tools.jar` and require Java 11+.

- `tla2sany.SANY` — parser and early semantic checks
- `tlc2.TLC` — explicit-state model checker
- `tlc2.REPL` — TLA+ REPL
- `pcal.trans` — PlusCal translator
- `tla2tex.TLA` — LaTeX and PDF support
- XML exporter — parse tree export for external tooling

Running `java -jar tla2tools.jar` is aliased to TLC.

## Checker selection

- Use SANY when the question is “does this parse and level-check?”
- Use TLC when the question is “is this finite executable model behavior allowed?”
- Use Apalache when symbolic bounded checking is a better fit than explicit-state enumeration.
- Use TLAPS when the model has stabilized and you need mechanical proof support.

## Practical notes

- TLC and CLI automation are well suited for scripts and non-Java integrations.
- The VS Code extension is powered by the official tools, not a separate checker stack.
- The examples corpus and the wiki both assume TLC-first usage for most engineering work.
