---
name: human-interface-guidelines
description: Apple's comprehensive design principles and standards for creating consistent, intuitive experiences across all platforms
---

# Human Interface Guidelines (HIG)

## OVERVIEW
Apple's comprehensive design principles and standards for creating consistent, intuitive experiences across iOS, macOS, watchOS, tvOS, and visionOS. Unified in 2024 from platform-specific guides. Grounded in Clarity, Deference, and Depth principles. Following HIG increases App Store approval rates and ensures native platform feel.

**Why this matters**: Establishes user trust through familiarity, reduces development time with standard components, ensures accessibility compliance, aligns with platform conventions users expect.

## WHEN TO USE
- Designing applications for any Apple platform (iOS, macOS, watchOS, tvOS, visionOS)
- Establishing design system foundations for Apple ecosystem
- Making interface decisions requiring platform consistency
- Preparing apps for App Store submission and review
- Onboarding designers/developers new to Apple platforms
- Resolving design conflicts via canonical standards
- Ensuring accessibility compliance across platforms

**Trigger**: Building for Apple platforms or need to align with user expectations from Apple ecosystem.

## KEY PRINCIPLES

### 1. Clarity
**Concept**: Text is legible at every size, icons are precise, functionality is obvious, adornments are subtle and appropriate.

**Application**:
- Use system fonts (SF Pro, SF Compact) for optimal legibility
- Negative space, color, typography create clear hierarchy
- Interactive elements clearly indicate affordances
- Critical information stands out without decoration

**Implementation**: Dynamic Type for scalable text, SF Symbols for icons, semantic colors that adapt to light/dark mode.

### 2. Deference
**Concept**: UI helps people understand and interact with content but never competes with it.

**Application**:
- Fluid motion and crisp interface that recede during content consumption
- Translucent backgrounds that provide context without obscuring
- Minimal chrome that highlights content, not UI elements
- Full-screen experiences when appropriate

**Implementation**: Reduce UI chrome in reading modes, use translucent navigation bars, let content bleed to edges.

### 3. Depth
**Concept**: Visual layers and realistic motion convey hierarchy and facilitate understanding.

**Application**:
- Distinct visual layers communicate relationships
- Transitions provide sense of spatial awareness
- Shadows and translucency suggest elevation
- Parallax and physics-based animations feel natural

**Implementation**: Navigation hierarchies with depth, modal presentations over context, spring animations.

## EXECUTION STEPS

### Phase 1: Foundation Setup
1. **Study platform conventions** - Review HIG for target platform (iOS/macOS/watchOS/tvOS/visionOS)
2. **Establish visual system** - Adopt SF Symbols, system fonts, semantic colors
3. **Choose navigation pattern** - Tab bar (iOS), sidebar (macOS), complications (watchOS)
4. **Define accessibility baseline** - Dynamic Type support, VoiceOver labels, contrast ratios

### Phase 2: Component Implementation
5. **Use system components** - UIKit/AppKit/SwiftUI standard controls
6. **Implement dark mode** - Use semantic colors, test both appearances
7. **Add platform gestures** - Swipe actions, long press, platform-specific interactions
8. **Configure haptic feedback** - iOS haptics for meaningful moments

### Phase 3: Refinement & Testing
9. **Test accessibility** - VoiceOver, Dynamic Type (up to AX sizes), Reduce Motion
10. **Validate across devices** - All iPhone sizes, iPad orientations, Mac screen sizes
11. **Review against HIG** - Component usage, interaction patterns, visual hierarchy
12. **App Store preparation** - Screenshots, descriptions, compliance checklist

## SUCCESS METRICS
- **App Store approval** - First-submission approval rate ≥ 85%
- **Accessibility audit pass** - ≥ 95% compliance with automated/manual tests
- **User onboarding time** - Minimal learning curve for platform-familiar users
- **Platform NPS** - Higher satisfaction for "native-feeling" apps
- **Development velocity** - 40-60% reduction in custom UI development

## REAL-WORLD EXAMPLES

### Apple Mail (iOS)
Standard navigation bar with compose button (top-right), swipe gestures for delete/archive/flag, unified inbox with SF Symbols, full VoiceOver support.

### Xcode (macOS)
macOS window patterns with source list sidebar, tabbed documents, inspector panels, extensive keyboard shortcuts—hallmarks of macOS design.

### Fitness (watchOS)
Complications on watch face for glanceable data, Digital Crown scrolling, haptic feedback for achievements, SF Compact Rounded for tiny screen.

### Apple TV App (tvOS)
Focus-driven navigation, parallax on focused items, Siri Remote gestures, large high-contrast text readable from 10+ feet.

### Vision Pro (visionOS)
Spatial windows in 3D space, gaze + gesture input, depth hierarchy with z-axis, fully immersive environments.

## ANTI-PATTERNS
**What NOT to do**:
- **Ignoring platform conventions** - One-size-fits-all UI that violates iOS/macOS differences
- **Custom components without reason** - Reinventing buttons/pickers breaks accessibility/dark mode
- **Skipping accessibility testing** - Designing only for default settings excludes 25% of users
- **Inconsistent visual language** - Mixing custom icons with SF Symbols creates disjointed feel
- **Over-designing for novelty** - Unnecessary animations/gestures degrade performance
- **Breaking standard gestures** - Swipe behavior that conflicts with system expectations
- **Fixed text sizes** - Not supporting Dynamic Type limits accessibility

## EDGE CASES
- **Cross-platform apps** - Respect iOS vs. macOS interaction models (touch vs. pointer)
- **Games** - May deviate from HIG but accessibility still required
- **Professional tools** - Custom UI justified for specialized workflows (Final Cut Pro)
- **Branded experiences** - Custom visuals OK if interaction patterns remain standard
- **iPad multitasking** - Support split view, slide over, drag and drop

## INTEGRATION
**Pairs well with**:
- **SwiftUI/UIKit/AppKit** - Native frameworks implement HIG by default
- **SF Symbols** - 5,000+ icons designed for Apple platforms
- **Design tokens** - System color/typography tokens
- **Accessibility APIs** - VoiceOver, Dynamic Type, Reduce Motion
- **Figma/Sketch kits** - Official Apple design templates

**Contrasts with**:
- **Material Design** - Google's design system for Android/web
- **Fluent Design** - Microsoft's design system for Windows
- **Custom design systems** - Bespoke vs. platform-standard approach

## 2025 UPDATE: Liquid Glass Design Language
Announced for iOS 26, iPadOS 26, macOS 26, watchOS 26, tvOS 26:
- Most significant visual redesign since 2013
- Translucent UI components with "optical qualities of glass"
- Refraction effects that react to motion, content, inputs
- Rounded, fluid elements with depth and responsiveness
- Emphasis on depth, translucency, and tactile feedback

## TOOLS & RESOURCES
- **Official site**: developer.apple.com/design/human-interface-guidelines
- **SF Symbols app**: 5,000+ configurable icons
- **Design kits**: Official Figma/Sketch UI templates
- **Accessibility Inspector**: Xcode tool for auditing compliance
- **WWDC sessions**: Annual design updates and best practices
- **Apple Design Awards**: Showcase of exemplary implementations

## FURTHER READING
- **Primary Source**: Apple HIG documentation (developer.apple.com/design)
- **WWDC Sessions**: "What's New in HIG", platform-specific design talks
- **Related**: *Designing for iOS* - Apple's design resources
- **Accessibility**: Apple Accessibility Programming Guide
- **Advanced**: Apple Design Awards case studies

## SCORING RATIONALE
**Total: 49/50**

| Criterion | Score | Reasoning |
|-----------|-------|-----------|
| Practitioner | 10/10 | Apple ships billions of devices; HIG defines platform standards |
| Clarity | 10/10 | Comprehensive docs, code examples, design kits, platform-specific guidance |
| ROI | 10/10 | Higher App Store approval, 40-60% faster development, accessibility built-in |
| Novelty | 9/10 | Continuously evolving (Liquid Glass 2025); sets industry standards |
| Cross-Domain | 10/10 | Works across iOS, macOS, watchOS, tvOS, visionOS, accessories |

**Evidence**: App Store ecosystem, billions of devices, continuous evolution (unified HIG 2024, Liquid Glass 2025), industry-leading accessibility standards.
