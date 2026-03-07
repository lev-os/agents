---
name: interaction-design-patterns
description: Reusable solutions to common interface problems that ensure consistent, intuitive user experiences
---

# Interaction Design Patterns

## Overview

Interaction design patterns are documented solutions to recurring design problems in user interfaces. Pioneered by pattern language concepts from architecture (Christopher Alexander) and popularized in UI/UX by Jenifer Tidwell's "Designing Interfaces," these patterns provide a shared vocabulary and proven solutions that designers can adapt to their specific contexts. Each pattern describes a problem, the context in which it occurs, the forces at play, and a solution with examples across platforms (web, mobile, desktop).

## When to Use

- Starting a new interface design and need proven solutions to common problems
- Maintaining consistency across multiple screens or applications
- Solving specific interaction challenges (navigation, input, feedback, data display)
- Communicating design decisions to developers using shared terminology
- Conducting design critiques or reviews with standardized pattern names
- Building design systems or component libraries with documented behaviors
- Training junior designers on established interaction principles

## The Process

### Step 1: Identify the Design Problem

Articulate the specific user need or interface challenge you're addressing. **Example:** Users need to browse large product catalogs efficiently without feeling overwhelmed - this is a "Progressive Disclosure" problem.

### Step 2: Select Appropriate Pattern Categories

Choose from Navigation (wayfinding), Input/Forms (data entry), Feedback (system status), Content Display (information presentation), or Social (collaboration). **Example:** For dashboard design, select from Data Visualization patterns (charts, sparklines) and Content Display patterns (cards, lists, tables).

### Step 3: Apply Core Navigation Patterns

Use Hub and Spoke (central dashboard), Pyramid (hierarchical drill-down), Breadcrumbs (orientation), Tabs (parallel sections), or Modal Panels (focused tasks). **Example:** E-commerce app uses Tabs for main categories, Breadcrumbs for product hierarchy, Modal Panels for checkout flow.

### Step 4: Implement Input Patterns

Deploy Smart Defaults (pre-filled forms), Autocomplete (type-ahead suggestions), Forgiving Format (flexible date/phone entry), Input Hints (contextual help), or Good Defaults (sensible starting values). **Example:** Address form uses Autocomplete for street names, Forgiving Format for postal codes (accepts with/without spaces).

### Step 5: Design Feedback Patterns

Provide Progress Indicators (loading states), Confirmations (success messages), Undo (mistake recovery), Busy Indicators (system processing), or Empty States (no-data scenarios). **Example:** File upload shows Progress Indicator during transfer, Confirmation on success, Undo option for 5 seconds.

### Step 6: Structure Content Display Patterns

Organize with Cards (contained information units), Lists (sequential items), Grids (spatial layouts), Module Tabs (sectioned content), or Accordion (collapsible sections). **Example:** News feed uses Cards for articles, Grid for photo galleries, Accordion for FAQ sections.

### Step 7: Test Pattern Effectiveness

Validate that users recognize and successfully interact with chosen patterns through usability testing. **Example:** A/B test Modal Panel vs. Inline Expansion for product details to measure conversion rates and user preference.

## Example Application

**Situation:** SaaS analytics platform users struggle to find specific reports among 200+ options and abandon filter configurations.

**Application:**
- Navigation: Implemented Two-Panel Selector (categories left, items right) instead of overwhelming dropdown
- Input: Added Smart Defaults (pre-selected popular date range), Autocomplete for report search
- Feedback: Progress Indicator during report generation, Empty State with suggestions when filters return no results
- Content: Cards for report previews showing data snapshot, Module Tabs for switching chart types
- Social: Recent Reports pattern showing team activity, Favorites pattern for saved configurations

**Outcome:** Report discovery time reduced 65% (from 2m 15s to 45s), filter completion increased from 40% to 78%, user satisfaction score improved from 6.2 to 8.7/10.

## Anti-Patterns

- Inventing novel interactions when standard patterns exist (reinventing the wheel)
- Using patterns inappropriately (modal dialogs for non-critical notifications)
- Mixing contradictory patterns (inconsistent navigation metaphors across sections)
- Applying desktop patterns to mobile without adaptation (hover states on touchscreens)
- Overloading patterns with too many functions (tabs with 15+ options)
- Ignoring platform conventions (Android back button behavior on iOS)
- Using patterns without understanding their constraints (infinite scroll breaking pagination)
- Copying patterns superficially without adapting to your specific user needs

## Related

- Design Systems - Codified patterns into reusable components
- Component Libraries - Implementation of patterns (Material, Bootstrap, Ant Design)
- Nielsen's Heuristics - Principles underlying successful patterns
- UX Pattern Libraries - UI-Patterns.com, UIPatterns.io collections
- Designing Interfaces (Tidwell) - Canonical pattern catalog
- Atomic Design - Component hierarchy for building pattern systems
- Mobile Design Patterns - Platform-specific iOS/Android patterns
- Information Architecture - Structural patterns for content organization
