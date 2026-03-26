# PCRE2 Pattern Reference

PCRE2 patterns available with `rg -P` after building with PCRE2 support.

## Lookahead & Lookbehind

| Pattern | Meaning | Example |
|---------|---------|---------|
| `(?=...)` | Positive lookahead | `foo(?=bar)` matches "foo" in "foobar" |
| `(?!...)` | Negative lookahead | `foo(?!bar)` matches "foo" NOT followed by "bar" |
| `(?<=...)` | Positive lookbehind | `(?<=\$)\d+` matches digits after "$" |
| `(?<!...)` | Negative lookbehind | `(?<!\$)\d+` matches digits NOT after "$" |

### Examples

```bash
# Find 'function' only when followed by 'async'
rg -P 'function(?=.*async)'

# Find imports NOT from node_modules
rg -P "from '(?!node_modules)"

# Find prices (digits after $)
rg -P '(?<=\$)\d+(\.\d{2})?'

# Find words NOT preceded by 'not '
rg -P '(?<!not )important'
```

---

## Backreferences

```bash
# Duplicate words
rg -P '\b(\w+)\s+\1\b'

# Matching quotes (same quote char on both ends)
rg -P '(["\']).*?\1'

# Repeated patterns
rg -P '(\d{3})-\1'  # matches "123-123"
```

---

## Atomic Groups & Possessive Quantifiers

Prevent backtracking for performance:

```bash
# Atomic group
rg -P '(?>a+)ab'  # Never matches (a+ is atomic, won't backtrack)

# Possessive quantifier (PCRE2 syntax)
rg -P 'a++ab'  # Same as above
```

---

## Unicode Properties

```bash
# Unicode letters
rg -P '\p{L}+'

# Unicode digits
rg -P '\p{N}+'

# Specific scripts
rg -P '\p{Greek}+'
rg -P '\p{Han}+'

# Em-dashes specifically
rg -P '[\x{2014}]'

# En-dashes
rg -P '[\x{2013}]'

# All dashes (em, en, hyphen)
rg -P '[\x{2014}\x{2013}-]'
```

---

## Conditionals

```bash
# If group 1 matched, match 'yes', else 'no'
rg -P '(foo)?(?(1)bar|baz)'

# Named condition
rg -P '(?<word>foo)?(?(word)bar|baz)'
```

---

## Recursion

```bash
# Match balanced parentheses
rg -P '\((?:[^()]|(?R))*\)'

# Match nested braces
rg -P '\{(?:[^{}]|(?R))*\}'
```

---

## Subroutines

```bash
# Define and reuse pattern
rg -P '(?<num>\d+).*(?P>num)'  # Two numbers with same format
```

---

## Flags Inside Pattern

```bash
# Case insensitive for part of pattern
rg -P '(?i)error(?-i) CODE'  # "error" case-insensitive, "CODE" case-sensitive

# Multi-line mode
rg -P '(?m)^start'  # ^ matches at line starts
```

---

## Performance Tips

1. **Prefer Rust regex when possible** — PCRE2 is slower for simple patterns
2. **Use atomic groups** — Prevent catastrophic backtracking
3. **Anchor when possible** — `^pattern` faster than `pattern`
4. **Avoid `.*` at start** — Use `^.*pattern` or be specific

---

## Differences from Rust Regex

| Feature | Rust regex | PCRE2 (`-P`) |
|---------|-----------|--------------|
| Lookahead | No | Yes |
| Lookbehind | No | Yes |
| Backreferences | No | Yes |
| Recursion | No | Yes |
| Unicode categories | `\pL` | `\p{L}` |
| Atomic groups | No | Yes |
| Conditionals | No | Yes |
