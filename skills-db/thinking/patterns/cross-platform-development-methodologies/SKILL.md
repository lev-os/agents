---
name: cross-platform-development-methodologies
description: Build applications for multiple platforms (iOS, Android, web) using shared codebases - evaluating native, cross-platform, hybrid, and PWA approaches
---

# Cross-Platform Development Methodologies

## Overview

Cross-platform development methodologies enable building applications for multiple operating systems (primarily iOS and Android) using a single unified codebase, achieving "write once, run anywhere" efficiency. Rather than maintaining separate native codebases, teams choose from four primary approaches: native (platform-specific code), cross-platform frameworks (Flutter, React Native), hybrid (web tech in native wrapper), or Progressive Web Apps (browser-based).

The methodology focuses on strategic trade-offs: native delivers maximum performance and platform integration but requires duplicate effort; cross-platform shares ~90% of code with near-native performance; hybrid maximizes code reuse but sacrifices performance; PWAs eliminate app stores but have limited device access. Leading frameworks include Flutter (170k GitHub stars, Dart, custom rendering engine) and React Native (121k stars, JavaScript, native components). The decision depends on performance needs, team skills, platform-specific requirements, and development speed priorities.

## When to Use

- Building mobile applications targeting both iOS and Android platforms
- Limited budget or timeline requiring faster development than dual native teams
- Team has web development expertise (JavaScript/TypeScript) but limited mobile experience
- Application requires consistent UI/UX across platforms
- Sharing business logic between mobile and web applications
- Rapid prototyping or MVP development for startups
- Evaluating framework selection for greenfield mobile projects

## The Process

### Step 1: Evaluate Application Requirements

Analyze performance needs, platform-specific features, and constraints before selecting approach. Requirements drive framework choice.

**Performance-critical needs:** Gaming, AR/VR, real-time video processing, complex animations - favor native or Flutter (custom rendering engine outperforms JavaScript bridge).

**Platform integration depth:** Camera, Bluetooth, payments, biometrics, background processing - native provides immediate access; cross-platform requires plugins or custom bridges.

**Team skills:** JavaScript expertise (20:1 ratio over Dart) favors React Native; native mobile developers favor Flutter or pure native; web developers favor hybrid/PWA.

**Budget/timeline:** Native requires 2x development effort (separate iOS/Android teams). Cross-platform shares 90% code but needs platform-specific work. Hybrid/PWA maximizes sharing.

**Output:** Requirements scorecard - performance (high/medium/low), platform features needed, team composition, budget constraints, timeline urgency.

### Step 2: Choose Cross-Platform Approach

Select methodology based on requirements analysis. Four primary approaches with distinct trade-offs.

**Native approach:** Separate Swift/Kotlin codebases. Maximum performance, full platform access, best UX, but 2x cost and slower iteration. Use when: performance critical, deep platform integration, budget allows, long-term investment.

**Cross-platform frameworks (Flutter/React Native):** Shared codebase compiles to native components. ~90% code sharing, near-native performance, fast iteration. **React Native** (JavaScript, uses native UI components, easier hiring, mature ecosystem) for: teams with JS skills, web code sharing, platform-specific behaviors. **Flutter** (Dart, custom rendering, consistent UI, superior animations) for: startups needing MVPs, visually rich apps, healthcare/finance apps requiring UI consistency.

**Hybrid (Ionic, Cordova):** Web technologies (HTML/CSS/JS) in native WebView wrapper. Maximum code sharing (95%+), leverage web skills, but performance lags, limited native feel. Use when: simple content apps, internal enterprise apps, web developers only.

**Progressive Web Apps (PWAs):** Browser-based apps with offline/push capabilities. No app store, instant updates, minimal cost, but limited device access and discoverability. Use when: content-focused, avoiding app store fees, web-first strategy.

### Step 3: Architect for Platform Differences

Design codebase to isolate shared logic from platform-specific code. Even "write once, run anywhere" requires platform adaptation.

**Shared business logic:** API clients, data models, state management, utilities - 70-90% of codebase. Store in framework-agnostic modules.

**Platform-specific UI:** Navigation patterns (iOS back gesture vs. Android back button), typography (San Francisco vs. Roboto), gestures, safe areas. Use platform detection and conditional rendering.

**Native bridges:** Features not supported by framework (advanced camera, Bluetooth, payments) require custom native modules. Write platform-specific Swift/Kotlin code with JavaScript bridge.

**Code organization:** Use feature-based structure with platform folders (`/shared`, `/ios`, `/android`). React Native: separate `.ios.js` and `.android.js` files. Flutter: platform channels for native code.

**Testing strategy:** Unit tests on shared logic (cross-platform), integration tests per platform (UI/navigation), E2E tests on physical devices (both platforms).

### Step 4: Optimize Performance and User Experience

Ensure cross-platform app meets performance expectations and feels native on each platform. Avoid "uncanny valley" UX.

**Performance optimization:** Flutter - minimize widget rebuilds, use const constructors, profile with DevTools. React Native - use FlatList for long lists, memoize components, enable Hermes JavaScript engine, profile with Flipper.

**Platform conventions:** iOS - follow Human Interface Guidelines (navigation, gestures, typography). Android - follow Material Design (FABs, bottom navigation, ripple effects). Don't force iOS UX onto Android or vice versa.

**Hot reload workflow:** Both Flutter and React Native support hot reload - update UI instantly without losing state. Shortens feedback loops from minutes to seconds during development.

**Native modules when needed:** Performance-critical code (image processing, cryptography) should use native implementations with framework bridges, not pure JavaScript/Dart.

**Measure with real devices:** Test on low-end Android devices (budget phones, not flagship). iOS simulator doesn't reflect real performance. Use production-like data volumes.

### Step 5: Maintain Cross-Platform Codebase

Establish practices for managing shared code, framework updates, and platform parity over time.

**Dependency management:** Lock framework versions in production. Test updates in staging before upgrading (breaking changes common). React Native updates historically painful; improved with New Architecture (0.76+).

**Platform parity monitoring:** Track feature availability across iOS/Android. Maintain matrix of features and platform support. Avoid iOS-first development that leaves Android behind.

**Code sharing metrics:** Measure actual code sharing percentage (target 85-90%). High platform-specific code percentage signals framework mismatch or architecture issues.

**Team structure:** Shared cross-platform team vs. platform specialists? Depends on scale. Startups: one team. Scale-ups: platform experts reviewing platform-specific code.

**Framework community:** React Native backed by Meta (Facebook), massive ecosystem, mature. Flutter backed by Google, growing rapidly, strong in healthcare/fintech. Both have thriving communities and plugin ecosystems.

## Example Application

**Situation:** Healthcare startup needs HIPAA-compliant telemedicine app for iOS and Android. 6-month timeline, $400K budget, JavaScript team.

**Step 1 - Requirements:** Medium performance (video calls), high security (HIPAA), platform features (camera, notifications, biometrics), JavaScript team, tight budget/timeline. No gaming or complex animations.

**Step 2 - Choice:** Selected React Native over Flutter. Reasoning: (1) team has React/JS skills, (2) video SDK has React Native support, (3) mature ecosystem for HIPAA compliance (encrypted storage, secure networking), (4) easier hiring for growth.

**Step 3 - Architecture:** Shared: API client, state management (Redux), business logic, UI components (90% shared). Platform-specific: biometric auth (FaceID vs. fingerprint), push notifications (APNs vs. FCM), navigation (iOS back gesture).

**Step 4 - Optimization:** Used Hermes for better startup time, FlatList virtualization for patient lists, native video SDK (Twilio) for calls, followed iOS HIG and Material Design per platform, tested on iPhone SE and budget Android (Galaxy A32).

**Step 5 - Maintenance:** Locked React Native 0.71 in production, quarterly upgrade cycles, automated E2E tests per platform, 87% code sharing achieved, dedicated iOS/Android reviewers for platform PRs.

**Outcome:** Shipped both platforms in 5.5 months (vs. 11 months estimated for dual native). React Native shared 87% code. Performance metrics: app startup <2s, video calls 99.5% uptime. Passed HIPAA audit. Saved estimated $350K vs. native approach.

## Anti-Patterns

- ❌ Forcing identical UI across platforms - ignoring platform conventions creates poor UX
- ❌ Choosing cross-platform for highly performance-critical apps (games, AR) - native delivers better experience
- ❌ Ignoring platform-specific bugs - "works on iOS" doesn't mean works on Android
- ❌ Over-abstracting platform differences - sometimes duplicating code is cleaner than complex abstraction
- ❌ Treating framework as pure "write once" - always requires platform-specific work (10-15%)
- ❌ Selecting framework based solely on popularity - evaluate against specific requirements
- ❌ Building custom native bridges for everything - defeats cross-platform purpose, use established plugins

## Related

- react-native-architecture (specific framework methodology)
- flutter-architecture (alternative framework approach)
- progressive-web-apps (browser-based alternative)
- native-vs-hybrid (decision framework)
- mobile-performance-optimization (platform-specific tuning)
- platform-design-guidelines (iOS HIG, Material Design)
- continuous-integration-mobile (CI/CD for cross-platform)
