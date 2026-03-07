# Roadmap Item #2: Adapter Architecture - Research & Implementation Plan

> **Status**: Blocked - Depends on Build System (#1)
> **Created**: 2025-12-03
> **Roadmap Item**: #2 - Adapter Architecture
> **Depends on**: Roadmap Item #1 (Build System)

---

## Research Prompt

**Investigate how to integrate the two-adapter pattern for skills into the Leviathan ecosystem:**

### Research Questions

1. **Existing Adapter Patterns**
   - How are adapters currently implemented in `core/adapters/`?
   - What patterns exist in `plugins/jared-intelligence/src/infrastructure/AdapterRegistry.js`?
   - How does the `@lev-os/adapter-builder` concept relate to our needs?
   - What can we learn from `core/adapters/claude/commands/` structure?

2. **SKILL.md Format Analysis**
   - What is the exact structure of Claude Code SKILL.md files?
   - How does frontmatter metadata map to Leviathan context.yaml?
   - What content transformations are needed (SKILL.md → context.yaml)?
   - What content transformations are needed (context.yaml → SKILL.md)?

3. **Context Loading Integration**
   - How does Leviathan currently load contexts from `core/contexts/`?
   - Where is `agent/src/tools/context-validator.js` used?
   - How can we hook into the context loading pipeline?
   - What runtime APIs exist for dynamic context loading?

4. **Build System Integration**
   - How does the build system work (`pnpm build`, etc.)?
   - Where should build-time compilation happen?
   - How to integrate with existing build pipelines?
   - What caching mechanisms exist?

5. **File Structure & Location**
   - Where should `adapters/skills/` live? (`poc/skills/adapters/` or `core/adapters/skills/`?)
   - How to structure the adapter modules?
   - What naming conventions to follow?
   - How to register adapters dynamically?

### Research Sources

- `core/adapters/claude/` - Existing Claude adapter patterns
- `plugins/jared-intelligence/src/infrastructure/AdapterRegistry.js` - Adapter registry pattern
- `workshop/adapter-build-handoff/` - Adapter builder concepts
- `poc/skills/contexts/patterns/` - Example SKILL.md and context.yaml files
- `context/schema/src/contexts/` - Context schema definitions
- `agent/src/tools/context-validator.js` - Context validation logic

### Expected Research Output

1. **Architecture Diagram** - How adapters fit into existing system
2. **API Design** - Interface for loading and output adapters
3. **File Structure** - Where files live and how they're organized
4. **Integration Points** - How to hook into existing systems
5. **Implementation Sequence** - Step-by-step build order

---

## Implementation Plan

### Phase 1: Research & Design (Current)

- [ ] **1.1 Research existing adapter patterns**
  - Analyze `core/adapters/claude/` structure
  - Review `AdapterRegistry.js` implementation
  - Study adapter-builder concepts
  - Document findings

- [ ] **1.2 Analyze SKILL.md format**
  - Parse example SKILL.md files
  - Map frontmatter to context.yaml structure
  - Identify transformation requirements
  - Document mapping rules

- [ ] **1.3 Design adapter interfaces**
  - Define `SkillLoadingAdapter` interface
  - Define `SkillOutputAdapter` interface
  - Design error handling
  - Design configuration schema

- [ ] **1.4 Design integration points**
  - Context loading hook design
  - Build system integration design
  - File structure decisions
  - Naming conventions

**Deliverables**: Research document, architecture diagram, API design

---

### Phase 2: Loading Adapter Implementation

- [ ] **2.1 Create adapter structure**
  - Create `poc/skills/adapters/skills/` directory
  - Set up module structure
  - Create base adapter class

- [ ] **2.2 Implement ClaudeSkillLoader**
  - Parse SKILL.md frontmatter
  - Extract metadata (name, description)
  - Load markdown content
  - Convert to Leviathan context structure
  - Handle errors gracefully

- [ ] **2.3 Integration with context system**
  - Hook into context loading pipeline
  - Register adapter dynamically
  - Test with existing SKILL.md files
  - Validate output context.yaml

- [ ] **2.4 Testing**
  - Unit tests for parsing
  - Integration tests with real SKILL.md files
  - Error handling tests
  - Performance tests

**Deliverables**: Working loading adapter, tests, documentation

---

### Phase 3: Output Adapter Implementation

- [ ] **3.1 Implement ClaudeSkillOutput**
  - Read context.yaml structure
  - Extract metadata and content
  - Generate SKILL.md frontmatter
  - Format markdown content
  - Handle optional fields

- [ ] **3.2 Build system integration**
  - Create build command/script
  - Integrate with `pnpm build`
  - Add caching mechanism
  - Support multiple targets

- [ ] **3.3 Template system**
  - Design SKILL.md template
  - Support different skill types (pattern, workflow, etc.)
  - Handle optional sections
  - Optimize output format

- [ ] **3.4 Testing**
  - Unit tests for generation
  - Round-trip tests (context.yaml → SKILL.md → context.yaml)
  - Build system tests
  - Output validation

**Deliverables**: Working output adapter, build integration, tests

---

### Phase 4: Documentation & Polish

- [ ] **4.1 Update documentation**
  - Update `context-schema.md` with examples
  - Update `architecture.md` with implementation details
  - Create adapter usage guide
  - Document build process

- [ ] **4.2 Examples & Templates**
  - Create example adapter implementations
  - Document common patterns
  - Provide migration guide
  - Add troubleshooting guide

- [ ] **4.3 Validation**
  - Validate against existing skills
  - Test with multiple skill types
  - Performance optimization
  - Error message improvements

**Deliverables**: Complete documentation, examples, validated implementation

---

## Success Criteria

1. ✅ Loading adapter can parse any SKILL.md and convert to context.yaml
2. ✅ Output adapter can generate SKILL.md from any context.yaml
3. ✅ Round-trip conversion preserves essential information
4. ✅ Build system integration works seamlessly
5. ✅ Documentation is complete and clear
6. ✅ Tests cover all major use cases

---

## Dependencies

- Understanding of existing adapter patterns
- Context loading pipeline access
- Build system integration points
- SKILL.md format specification

---

## Next Steps After Completion

- Roadmap Item #2: Document Canonical context.yaml Format
- Roadmap Item #5: Pattern/Skill Migration (use adapters for existing skills)
- Roadmap Item #6: Core Schema Alignment (apply patterns to context/schema/)

---

## Notes

- Keep adapter implementations simple and focused
- Prioritize Claude format first, extend to others later
- Ensure backward compatibility with existing SKILL.md files
- Consider future extensibility (OpenAI, other formats)
