---
name: nielsen-heuristics
description: 10 foundational usability principles for evaluating and designing user interfaces
---

# Nielsen Norman Group's 10 Usability Heuristics

## Overview

Jakob Nielsen's 10 Usability Heuristics are broad rules of thumb for interaction design, created in 1990 and refined in 1994. They provide a systematic framework for evaluating interface usability without requiring extensive user testing. These heuristics form the foundation for heuristic evaluation - a discount usability method where evaluators examine interfaces against established principles to identify usability problems.

## When to Use

- Conducting rapid usability evaluations without formal user testing
- Designing new interfaces or redesigning existing ones
- Prioritizing design decisions when multiple approaches exist
- Training designers on fundamental usability principles
- Reviewing designs before user testing to catch obvious issues
- Communicating usability problems to stakeholders with standardized language

## The Process

### Step 1: Visibility of System Status

Keep users informed about what's happening through timely, appropriate feedback. **Example:** Progress bars during file uploads, loading spinners during data fetches, confirmation messages after form submissions.

### Step 2: Match Between System and Real World

Use familiar language, concepts, and conventions rather than technical jargon. Follow real-world conventions and present information in natural, logical order. **Example:** "Trash" instead of "Delete Buffer", calendar metaphors for scheduling, shopping cart for e-commerce.

### Step 3: User Control and Freedom

Provide clearly marked emergency exits for mistaken actions. Support undo/redo to let users reverse decisions without penalty. **Example:** Undo buttons, cancel options on dialogs, back navigation, "Are you sure?" confirmations for destructive actions.

### Step 4: Consistency and Standards

Follow platform conventions and maintain internal consistency. Users shouldn't wonder if different words, situations, or actions mean the same thing. **Example:** Submit buttons always in bottom-right, consistent icon meanings, standard keyboard shortcuts (Cmd+S for save).

### Step 5: Error Prevention

Design carefully to prevent problems before they occur. Eliminate error-prone conditions or present confirmation options before commitment. **Example:** Disable invalid form inputs, constraint-based calendars, confirmation dialogs for destructive actions, input validation as users type.

### Step 6: Recognition Rather Than Recall

Make objects, actions, and options visible. Minimize memory load by showing available choices rather than requiring users to remember information. **Example:** Visible menu options vs. command-line interfaces, autocomplete suggestions, recently used items, visual previews.

### Step 7: Flexibility and Efficiency of Use

Accelerate workflows for expert users while remaining accessible to novices. Allow customization for frequent actions. **Example:** Keyboard shortcuts alongside mouse actions, bulk operations, customizable toolbars, macros for power users.

### Step 8: Aesthetic and Minimalist Design

Eliminate irrelevant or rarely needed information. Every extra unit of information competes with relevant units and diminishes their visibility. **Example:** Progressive disclosure, hidden advanced settings, clean interfaces with clear visual hierarchy, contextual tools that appear when needed.

### Step 9: Help Users Recognize, Diagnose, and Recover from Errors

Express error messages in plain language, precisely indicate the problem, and constructively suggest solutions. **Example:** "Password must contain at least 8 characters including one number" instead of "Invalid input", specific field highlighting on form errors.

### Step 10: Help and Documentation

Provide searchable, task-focused documentation when needed. List concrete steps and avoid being overly large. **Example:** Contextual tooltips, searchable help centers, step-by-step tutorials, inline documentation, chatbots for common questions.

## Example Application

**Situation:** Designing a new banking app for money transfers.

**Application:**
- Heuristic 1: Show real-time transfer status ("Processing...", "Completed")
- Heuristic 3: Allow users to cancel pending transfers
- Heuristic 5: Prevent transfers to invalid account numbers with inline validation
- Heuristic 6: Show dropdown of recent recipients rather than requiring memorization
- Heuristic 9: If transfer fails, explain why ("Insufficient funds") and suggest action ("Add money to account")

**Outcome:** Reduced customer support calls by 40% and increased successful transfer completion rate by 25%.

## Anti-Patterns

- Designing without feedback mechanisms (silent failures, unclear loading states)
- Using technical jargon that users don't understand ("Exception 0x8000")
- Forcing users to memorize information across screens
- Inconsistent UI patterns that confuse users (submit button in different locations)
- Generic error messages that don't help users fix problems ("Error occurred")
- Hiding critical actions behind obscure gestures or undiscoverable features
- Cluttered interfaces with every possible option visible at once
- No way to undo or cancel destructive actions

## Related

- Don Norman's Design Principles (affordances, signifiers, feedback)
- WCAG Accessibility Guidelines (overlapping usability and accessibility)
- Design Systems (codifying heuristics into reusable patterns)
- Heuristic Evaluation Methodology (systematic application of these principles)
- Cognitive Load Theory (theoretical foundation for heuristics 6, 8)
- Progressive Disclosure Pattern (implements heuristics 6, 8)
