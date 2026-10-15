---
name: wireframe-prototyping
description: >
  Create wireframes and interactive prototypes to visualize user interfaces and
  gather feedback early. Use tools and techniques to communicate design ideas
  before development.
---

# Wireframe Prototyping

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Reference Guides](#reference-guides)
- [Best Practices](#best-practices)

## Overview

Wireframes and prototypes bridge the gap between ideas and implementation, enabling teams to test concepts, get feedback, and refine designs before costly development.

## When to Use

- Early concept validation
- Stakeholder alignment
- User testing and feedback
- Developer handoff
- Feature exploration
- UX problem-solving
- Rapid iteration

## Quick Start

Minimal working example:

```yaml
Wireframe Principles:

Low Fidelity (Sketches):
  Tools: Paper, whiteboard, Balsamiq
  Time: 30 minutes - 2 hours
  Detail: Basic layout, no colors/fonts
  Best For: Brainstorming, exploration
  Cost: Free

Medium Fidelity:
  Tools: Figma, Sketch, Adobe XD
  Time: 2-8 hours
  Detail: Layout, content, basic interaction
  Best For: Team alignment, feedback
  Cost: Low

High Fidelity:
  Tools: Figma, Framer, web dev tools
  Time: 8+ hours
  Detail: Visual design, interactions, animations
  Best For: Developer handoff, user testing
  Cost: Medium

---
## Wireframe Components
// ... (see reference guides for full implementation)
```

## Reference Guides

Detailed implementations in the `references/` directory:

| Guide | Contents |
|---|---|
| [Prototyping Tools & Techniques](references/prototyping-tools-techniques.md) | Prototyping Tools & Techniques |
| [Wireframe Examples](references/wireframe-examples.md) | Wireframe Examples |
| [Prototype Testing](references/prototype-testing.md) | Prototype Testing |

## Best Practices

### ✅ DO

- Start with low-fidelity sketches
- Get feedback early and often
- Test with real users
- Iterate based on feedback
- Use consistent grids and spacing
- Document interaction flows
- Include edge cases (empty states, errors)
- Create mobile-first wireframes
- Share prototypes for collaboration
- Keep wireframes simple and focused

### ❌ DON'T

- Jump directly to high-fidelity
- Over-design before validation
- Ignore mobile/responsive needs
- Create wireframes without user input
- Leave interactions undefined
- Make wireframes too detailed
- Test only with team members
- Ignore accessibility
- Lock into designs too early
- Create unrealistic user flows


---

# Wireframe Examples


# Wireframe Examples

## Wireframe Examples

```yaml
Example: E-commerce Product Page

Header:
  [Logo] [Search bar] [Cart] [Account]

Hero Section:
  [Product image] [Price] [Add to cart] [Reviews: 4.5★]

Product Details:
  Description | Specs | Size guide

Product Images:
  [Main] [Thumb1] [Thumb2] [Thumb3]

Related Products:
  [Product card] [Product card] [Product card]

Footer:
  Contact | FAQ | Returns | Shipping info
```


---

# Prototyping Tools & Techniques


# Prototyping Tools & Techniques

## Prototyping Tools & Techniques

```python
# Create interactive prototypes

class PrototypeFramework:
    TOOLS = {
        'Figma': {
            'fidelity': 'Medium-High',
            'interactivity': 'Full',
            'collaboration': 'Real-time',
            'cost': 'Free-$30/month'
        },
        'Framer': {
            'fidelity': 'High',
            'interactivity': 'Advanced',
            'collaboration': 'Limited',
            'cost': '$12+/month'
        },
        'Adobe XD': {
            'fidelity': 'High',
            'interactivity': 'Full',
            'collaboration': 'Good',
            'cost': '$20/month'
        }
    }

    def create_prototype_flow(self):
        """Define user interaction flows"""
        return {
            'screens': [
                {'name': 'Login', 'interactions': ['Email input', 'Password input', 'Submit button']},
                {'name': 'Dashboard', 'interactions': ['View projects', 'Create new', 'Search']},
                {'name': 'Project Detail', 'interactions': ['View tasks', 'Edit project', 'Share']}
            ],
            'flows': [
                {'from': 'Login', 'to': 'Dashboard', 'trigger': 'Valid credentials'},
                {'from': 'Dashboard', 'to': 'Project Detail', 'trigger': 'Click project'},
                {'from': 'Project Detail', 'to': 'Dashboard', 'trigger': 'Back button'}
            ]
        }

    def define_interactions(self, screen):
        """Map user interactions"""
        return {
            'screen': screen,
            'interactions': [
                {
                    'element': 'Submit button',
                    'trigger': 'Click',
                    'action': 'Validate form and submit'
                },
                {
                    'element': 'Email field',
                    'trigger': 'Focus',
                    'action': 'Show placeholder, hint text'
                }
            ]
        }

    def test_prototype(self, prototype):
        """Gather feedback on prototype"""
        return {
            'testing_method': 'Unmoderated user testing',
            'participants': 5,
            'duration': '30 minutes each',
            'tasks': [
                'Complete user registration',
                'Create first project',
                'Invite team member'
            ],
            'metrics': [
                'Task completion rate',
                'Time to complete',
                'Error rate',
                'User satisfaction'
            ]
        }
```


---

# Prototype Testing


# Prototype Testing

## Prototype Testing

```yaml
Testing Plan:

Objective: Validate primary user flows and UX clarity

Test Method: Unmoderated remote testing

Participants:
  - 5 representative users
  - Mix of experience levels
  - Similar to target persona

Tasks: 1. Register a new account
  2. Create your first project
  3. Invite a team member
  4. Edit project settings

Success Criteria:
  - 80%+ task completion rate
  - Average time <5 min per task
  - SUS score >70
  - No critical usability issues

Feedback Areas:
  - Navigation clarity
  - Button placement
  - Form fields
  - Visual hierarchy
  - Error handling

Analysis:
  - Top 3 friction points
  - User quotes
  - Design recommendations
```
