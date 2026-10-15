---
name: web-artifacts-builder
description: Suite of tools for creating elaborate, multi-component HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components.
---

# Web Artifacts Builder

To build powerful frontend artifacts, follow these steps:
1. Initialize the frontend repo using `scripts/init-artifact.sh`
2. Develop your artifact by editing the generated code
3. Bundle all code into a single HTML file using `scripts/bundle-artifact.sh`
4. Display artifact to user
5. (Optional) Test the artifact

**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## Design & Style Guidelines

VERY IMPORTANT: To avoid what is often referred to as "AI slop", avoid using excessive centered layouts, purple gradients, uniform rounded corners, and Inter font.

## Quick Start

### Step 1: Initialize Project

Run the initialization script to create a new React project:
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

This creates a fully configured project with:
- React + TypeScript (via Vite)
- Tailwind CSS 3.4.1 with shadcn/ui theming system
- Path aliases (`@/`) configured
- 40+ shadcn/ui components pre-installed
- All Radix UI dependencies included
- Parcel configured for bundling

### Step 2: Develop Your Artifact

Edit the generated files to build your artifact.

### Step 3: Bundle to Single HTML File

```bash
bash scripts/bundle-artifact.sh
```

Creates `bundle.html` - a self-contained artifact with all JavaScript, CSS, and dependencies inlined.

### Step 4: Share Artifact

Share the bundled HTML file so users can view it as an artifact.

## Reference

- **shadcn/ui components**: https://ui.shadcn.com/docs/components