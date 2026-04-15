# MT Research Foundations

> Key papers, real-world results, and the state of the art.

## Foundational Papers

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| Chen, Cheung & Yiu | 1998 | Invented metamorphic testing |
| Segura et al. "Survey on MT" | 2016 | First major survey (119 papers) |
| Chen et al. "MT: A Review" | 2018 | Definitive survey, ACM Computing Surveys |
| NIST "MT for Cybersecurity" | 2016 | MT for security testing (IEEE Computer) |
| Ying et al. "MR Patterns" | 2025 | Formal MRP taxonomy framework |

## Real-World Bug Counts

| System | Bugs Found | MR Type | Reference |
|--------|-----------|---------|-----------|
| GCC + LLVM | 147 confirmed (initial) + 132 more | Dead code equivalence | UC Davis |
| GPU drivers (GraphicsFuzz) | 100s including security vulns | Shader transformations | Google/Imperial College |
| Code obfuscators (NIST) | Bugs in ALL 4 tested tools | Functional equivalence | Cobfusc, Stunnix, Tigress, LLVM |
| Microsoft Live Search | Logic bug (OR returning 0 results) | Inclusive (broadening) | Chen et al. |
| Baidu Apollo (self-driving) | "thousands of erroneous behaviors" | Weather/lighting transforms | DeepTest |
| LLMs (Meta-Fair) | Bias in 29% of executions | Demographic swap | GPT, LLaMA, Gemini |
| Smart contracts | 89% mutant detection rate | Multiple categories | Blockchain MT |

## The Heartbleed Connection

MT naturally guides testers toward Heartbleed-class bugs:
- **The question MT asks:** "What if I change the length field to a different value?"
- **Heartbleed:** Server returns data beyond the intended buffer when length > actual payload
- **Why fuzzing missed it:** Heartbleed doesn't crash — it returns "valid" responses with leaked data
- **Why MT catches it:** MR checks the *relationship* between input length and response, not just whether it crashes

## MR Generation: State of the Art (2024)

Methods for automatically generating MRs:

| Method | How It Works | Maturity |
|--------|-------------|----------|
| Manual domain analysis | Expert identifies domain invariants | Gold standard |
| Code comment mining (MeMo) | Extract equality MRs from code comments | Prototype |
| Genetic programming (GenMorph) | Evolve MRs using GP | Research |
| LLM-based | Prompt frontier LLM to generate MRs from spec | Emerging |
| Search-based (SBMT) | Optimize MR parameters via search | Research |
| Specification mining | Extract MRs from formal specs | Established |

**LLM finding (2024-2025):** Frontier LLMs can produce structurally clear and occasionally novel MRs when prompted with domain context, but ALL LLM-generated MRs require mutation testing validation before trusting them.

## Application Domain Distribution (1998-2015)

From Segura et al. survey of 119 papers:

| Domain | % of Papers |
|--------|------------|
| Scientific computing | 25% |
| Web services/APIs | 15% |
| Machine learning | 12% |
| Embedded systems | 10% |
| Compilers | 8% |
| Databases | 7% |
| Graphics | 5% |
| Other | 18% |

Since 2020, ML/AI testing has become the dominant application domain.
