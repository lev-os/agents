---
name: laws-of-ux
description: Collection of 21 psychology-based design principles for building intuitive, human-centered products and interfaces
---

# Laws of UX

## Overview

Laws of UX, created by designer Jon Yablonski and published as a book in 2020, is a collection of 21 design principles grounded in psychology that explain how humans perceive and process digital interfaces. These laws are organized into four categories: Heuristics (predictive models like Fitts's Law and Hick's Law), Gestalt Principles (visual perception patterns), Cognitive Biases (mental shortcuts that influence decisions), and General Principles (foundational design concepts). Rather than arbitrary design opinions, these laws are based on decades of psychological research and empirical studies. They provide a scientific foundation for design decisions, helping practitioners create products that work within the "blueprint" of human cognition and perception.

## When to Use

- Making design decisions backed by psychological research rather than subjective preferences
- Reducing cognitive load and decision fatigue in complex interfaces
- Optimizing interaction patterns for speed and accuracy (buttons, navigation, forms)
- Explaining design choices to stakeholders with evidence-based reasoning
- Conducting heuristic evaluations of existing interfaces against known psychological principles
- Training designers on fundamental human-computer interaction patterns
- Prioritizing UX improvements with predictable impact on user behavior

## The Process

### Step 1: Apply Fitts's Law (Target Acquisition)

Fitts's Law states that the time to acquire a target is a function of the distance to and size of the target. Larger, closer targets are easier and faster to click. Design interactive elements (buttons, links, touch targets) to be appropriately sized for their importance and frequency of use. **Example:** Primary CTA buttons are 48x48px minimum (Apple recommends 60x60pt for touch), frequently-used navigation items are placed in thumb-reach zones on mobile, and pie menus place all options equidistant from cursor origin.

### Step 2: Apply Hick's Law (Choice Reduction)

Hick's Law states that decision time increases logarithmically with the number and complexity of choices. Reduce cognitive load by minimizing options, especially when response time is critical. Break complex tasks into smaller steps (progressive disclosure) rather than overwhelming users with all options at once. **Example:** Checkout flow broken into 4 steps (cart → shipping → payment → confirm) instead of one massive form. Navigation menus limited to 5-7 top-level items with subcategories revealed on demand.

### Step 3: Apply Jakob's Law (Familiar Patterns)

Jakob's Law states that users spend most of their time on other sites, so they prefer your site to work the same way. Leverage existing mental models by following common design conventions (logo in top-left links to home, shopping cart icon in top-right, hamburger menu for mobile navigation). **Example:** E-commerce site uses standard patterns: search bar top-center, account/cart top-right, breadcrumb navigation above product, "Add to Cart" button on product pages—all matching Amazon, Shopify, and other familiar sites.

### Step 4: Apply Miller's Law (Chunking Information)

Miller's Law states that the average person can hold 7±2 items in working memory. Chunk information into groups of 5-9 items to match human memory capacity. Use progressive disclosure, categorization, and visual hierarchy to prevent cognitive overload. **Example:** Phone numbers formatted as (555) 123-4567 instead of 5551234567. Dashboard displays 5-7 key metrics above the fold, with detailed reports accessible via progressive disclosure. Form fields grouped into logical sections (Personal Info, Shipping Address, Payment).

### Step 5: Apply Law of Proximity (Gestalt Principle)

The Law of Proximity states that objects near each other are perceived as related. Group related elements together and separate unrelated elements to create clear visual relationships and reduce ambiguity. **Example:** Form labels positioned directly above or beside their input fields (not far away). Card-based layouts group related content (image + title + description + CTA) with whitespace separating different cards. Navigation items grouped by category with divider lines.

### Step 6: Apply Law of Similarity (Gestalt Principle)

The Law of Similarity states that objects that share visual characteristics (color, shape, size, orientation) are perceived as related or belonging to the same group. Use consistent visual styling to indicate functionality or hierarchy. **Example:** All primary actions use blue buttons, all destructive actions use red buttons, all disabled states use gray. Links always underlined and blue. Icons always 24x24px. This consistency signals "these things behave the same way."

### Step 7: Apply Serial Position Effect (Primacy & Recency)

The Serial Position Effect states that users best remember the first and last items in a series. Position the most important information and actions at the beginning and end of lists, menus, or flows. **Example:** Navigation menu places most critical items first (Home, Products, Pricing) and secondary items (Blog, About) later. Email subject lines frontload keywords. Onboarding flow ends with key action reminder.

### Step 8: Apply Peak-End Rule (Memory & Satisfaction)

The Peak-End Rule states that people judge experiences based on their peak (most intense point) and end, not the average. Design memorable peak moments (delightful interactions, animations, micro-interactions) and ensure flows end on a positive note. **Example:** Signup flow includes a celebratory animation at completion (peak moment) and ends with immediate value delivery (end state). E-commerce checkout ends with order confirmation and estimated delivery date, not just "Payment processed."

### Step 9: Apply Aesthetic-Usability Effect

The Aesthetic-Usability Effect states that users perceive aesthetically pleasing designs as more usable, even if they're not objectively easier to use. Invest in visual polish, consistent styling, thoughtful typography, and delightful details—they create a halo effect that increases perceived usability and forgiveness of minor issues. **Example:** Stripe's checkout form uses elegant typography, smooth animations, and polished visuals—making the payment process feel trustworthy and professional, even though the actual form fields are standard.

### Step 10: Apply Tesler's Law (Complexity Conservation)

Tesler's Law states that every system has inherent complexity that cannot be removed, only moved. Don't eliminate complexity—redistribute it thoughtfully between system and user. Automate where possible, but give advanced users control when needed. **Example:** Email client provides simple "Smart Compose" by default (system handles complexity) but offers manual formatting toolbar for power users. Calendar app auto-detects time zones but allows manual override.

## Key Principles

**Psychology Over Opinion**: Design decisions backed by psychological research and empirical studies carry more weight than subjective preferences. Use Laws of UX to ground design critiques in science.

**Predictive Models Inform Trade-offs**: Fitts's Law and Hick's Law provide mathematical frameworks for evaluating design alternatives. Larger buttons improve accuracy but consume space—quantify the trade-off.

**Leverage Existing Mental Models**: Jakob's Law reminds us that users bring expectations from other interfaces. Fighting conventions forces users to relearn—only deviate when the benefit outweighs cognitive friction.

**Respect Cognitive Limits**: Miller's Law, Hick's Law, and Serial Position Effect all point to finite human attention and memory. Design within these constraints, not against them.

**Gestalt Principles Create Clarity**: Proximity, Similarity, Common Region, and other Gestalt laws explain how humans parse visual information. Use them to create unambiguous, scannable layouts.

## Common Pitfalls

**Ignoring Fitts's Law for Small Touch Targets**: Buttons/links smaller than 44x44px (iOS) or 48x48px (Material) are difficult to tap accurately, especially for users with motor impairments or on moving devices. Result: Mis-taps, user frustration, accessibility failures.

**Violating Jakob's Law with Novel Patterns**: Reinventing standard conventions (hamburger menu, shopping cart icon, logo-to-home link) forces users to relearn your interface. Result: Increased cognitive load, higher bounce rates, lower task completion.

**Overwhelming Users with Choices (Hick's Law)**: Presenting 20+ options at once (mega-menus, massive forms, crowded dashboards) paralyzes decision-making and increases abandonment. Result: Decision fatigue, analysis paralysis, task abandonment.

**Ignoring Chunking (Miller's Law)**: Displaying long lists, forms, or data sets without grouping exceeds working memory capacity and makes information unscannable. Result: Users miss critical information, skip form fields, abandon complex tasks.

**Breaking Visual Hierarchy (Gestalt Principles)**: Inconsistent spacing, arbitrary colors, or misaligned elements violate proximity and similarity laws, making interfaces ambiguous. Result: Users misinterpret relationships, click wrong elements, struggle to find information.

## Real-World Examples

**Stripe Checkout (Fitts's Law + Aesthetic-Usability)**: Large, visually prominent "Pay" button (easy to target), elegant typography and micro-interactions (aesthetic-usability effect), and single-column layout (Hick's Law—one clear path forward).

**Amazon Navigation (Jakob's Law + Hick's Law)**: Top-level categories limited to ~10 items (Hick's Law), standard e-commerce patterns (logo top-left, cart top-right, search bar top-center), and familiar mega-menu structure (Jakob's Law).

**Google Search (Miller's Law + Serial Position Effect)**: Shows 10 results per page (Miller's 7±2), positions most relevant results at top (Serial Position primacy), displays pagination with next/previous options (recency effect).

**Slack Sidebar (Proximity + Similarity)**: Groups channels by category (Proximity), uses consistent styling for all channels (Similarity), places starred/recent channels at top (Serial Position), and separates DMs with visual divider (Common Region).

**Headspace Onboarding (Peak-End Rule)**: Creates peak moment with delightful animation after first meditation session, ends onboarding with immediate access to curated meditation (positive end state), reinforcing commitment.

## Success Metrics

- **Task Completion Time**: Applying Fitts's Law (larger targets) and Hick's Law (fewer choices) measurably reduces task completion time
- **Click Accuracy**: Fitts's Law predicts that 48px+ touch targets reduce mis-taps by 30-50% compared to 32px targets
- **Decision Time**: Hick's Law shows that reducing options from 10 to 5 can cut decision time by ~30% (logarithmic relationship)
- **Error Rate**: Jakob's Law compliance (following conventions) reduces user errors by leveraging existing mental models
- **Cognitive Load (NASA TLX)**: Miller's Law (chunking) and progressive disclosure reduce subjective cognitive load scores by 20-40%
- **User Satisfaction**: Aesthetic-Usability Effect correlates visual polish with 10-15% higher NPS scores

## Additional Resources

- **Book**: "Laws of UX: Using Psychology to Design Better Products & Services" by Jon Yablonski (2020, O'Reilly)
- **Website**: lawsofux.com - Interactive reference with examples, research citations, and posters
- **Research Papers**: Original studies by Fitts (1954), Hick & Hyman (1952), Miller (1956), Nielsen (Jakob's Law)
- **Complementary Resources**: "100 Things Every Designer Needs to Know About People" by Susan Weinschenk, "Universal Principles of Design" by Lidwell/Holden/Butler
- **Tools**: Figma/Sketch plugins for checking Fitts's Law compliance (target size/spacing), cognitive load analysis tools
