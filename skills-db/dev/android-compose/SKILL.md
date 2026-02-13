---
name: android-compose
description: Develop Android apps with Jetpack Compose and Material 3. Use for Kingly Android app development, theming, UI components, and catching up to iOS/macOS feature parity.
---

# Android Compose Development Skill

## Stack Overview

**Kingly Android App:** `apps/android/`

| Technology | Version | Purpose |
|------------|---------|---------|
| Kotlin | 2.x | Primary language |
| Jetpack Compose | BOM 2024+ | Declarative UI |
| Material 3 | Dynamic colors | Design system |
| compileSdk | 36 (Android 16) | Target platform |
| minSdk | 31 (Android 12) | Minimum support |

## Project Structure

```
apps/android/
├── app/
│   ├── build.gradle.kts           ← Dependencies, versions
│   └── src/main/java/bot/molt/android/
│       ├── MainActivity.kt        ← Entry point
│       ├── MainViewModel.kt       ← App state
│       ├── NodeRuntime.kt         ← Gateway node
│       ├── chat/                  ← Chat models/controller
│       ├── gateway/               ← GatewaySession, discovery, TLS
│       ├── node/                  ← Camera, location, canvas
│       ├── protocol/              ← A2UI actions, constants
│       ├── ui/                    ← Compose UI components
│       │   ├── KinglyBotTheme.kt  ← Theme (Material 3)
│       │   ├── RootScreen.kt      ← Main screen
│       │   ├── ChatSheet.kt       ← Chat bottom sheet
│       │   ├── SettingsSheet.kt   ← Settings UI
│       │   └── chat/              ← Chat UI components
│       └── voice/                 ← Voice/wake word
└── gradle/                        ← Gradle wrapper
```

## Build Commands

```bash
# Build debug APK
cd apps/android && ./gradlew assembleDebug

# Run tests
./gradlew test

# Lint check
./gradlew lint

# Install on connected device
./gradlew installDebug

# Clean build
./gradlew clean assembleDebug
```

## Theme System (Aligned with iOS/macOS)

The theme uses Material 3 dynamic colors. To align with OCDesignKit:

```kotlin
// Current: apps/android/app/src/main/java/bot/molt/android/ui/KinglyBotTheme.kt
@Composable
fun KinglyBotTheme(content: @Composable () -> Unit) {
    val isDark = isSystemInDarkTheme()

    // Custom color scheme to match OCColors
    val colorScheme = if (isDark) {
        darkColorScheme(
            background = Color(0xFF0D0D14),      // OCColors.background dark
            surface = Color(0xFF14121E),          // OCColors.surface dark
            primary = Color(0xFF6366F1),          // Indigo accent
            onBackground = Color.White,
            onSurface = Color.White.copy(alpha = 0.7f)
        )
    } else {
        lightColorScheme(
            background = Color(0xFFFAFAF8),       // OCColors.background light (cream)
            surface = Color(0xFFFFFFFF),          // OCColors.surface light
            primary = Color(0xFF6366F1),          // Indigo accent
            onBackground = Color(0xFF1A1A1A),
            onSurface = Color(0xFF6B6B6B)
        )
    }

    MaterialTheme(colorScheme = colorScheme, content = content)
}
```

## SwiftUI → Compose Mapping

| SwiftUI (iOS) | Compose (Android) |
|---------------|-------------------|
| `VStack` | `Column` |
| `HStack` | `Row` |
| `ZStack` | `Box` |
| `List` | `LazyColumn` |
| `NavigationStack` | `NavHost` |
| `@State` | `remember { mutableStateOf() }` |
| `@Observable` | `ViewModel` + `StateFlow` |
| `.sheet()` | `ModalBottomSheet` |
| `.background()` | `Modifier.background()` |
| `.padding()` | `Modifier.padding()` |
| `RoundedRectangle` | `RoundedCornerShape` |
| `Color.indigo` | `Color(0xFF6366F1)` |

## Component Patterns

### Card (matching OCCard)

```kotlin
@Composable
fun KinglyCard(
    modifier: Modifier = Modifier,
    content: @Composable ColumnScope.() -> Unit
) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            content = content
        )
    }
}
```

### List Item (matching OCToggleRow)

```kotlin
@Composable
fun KinglyToggleRow(
    icon: ImageVector,
    iconTint: Color,
    title: String,
    subtitle: String?,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(44.dp)
                .background(
                    color = if (checked) iconTint.copy(alpha = 0.15f)
                           else MaterialTheme.colorScheme.surfaceVariant,
                    shape = RoundedCornerShape(12.dp)
                ),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = if (checked) iconTint else Color.Gray
            )
        }

        Spacer(modifier = Modifier.width(16.dp))

        Column(modifier = Modifier.weight(1f)) {
            Text(text = title, style = MaterialTheme.typography.titleMedium)
            subtitle?.let {
                Text(text = it, style = MaterialTheme.typography.bodySmall)
            }
        }

        Switch(checked = checked, onCheckedChange = onCheckedChange)
    }
}
```

## Spacing Tokens (matching OCSpacing)

```kotlin
object KinglySpacing {
    val xs = 4.dp
    val sm = 8.dp
    val md = 12.dp
    val lg = 16.dp
    val xl = 20.dp
    val xxl = 24.dp
}

object KinglyRadius {
    val sm = 8.dp
    val md = 12.dp
    val lg = 16.dp
    val xl = 20.dp
}
```

## Feature Parity Checklist (vs iOS)

| Feature | iOS | Android | Priority |
|---------|-----|---------|----------|
| Chat UI | ✅ | ✅ | - |
| Voice chat | ✅ | ✅ | - |
| Gateway connection | ✅ | ✅ | - |
| Sessions list | ✅ | ⚠️ Basic | P1 |
| Sidebar/drawer | ✅ | ❌ | P1 |
| Onboarding flow | ✅ | ❌ | P1 |
| Settings UI | ✅ | ⚠️ Basic | P2 |
| Marketplace | ✅ | ❌ | P3 |
| Design tokens aligned | ✅ | ❌ | P0 |

## Testing

```bash
# Unit tests
./gradlew test

# Run specific test
./gradlew test --tests "bot.molt.android.gateway.*"

# UI tests (requires emulator)
./gradlew connectedAndroidTest
```

## ADB Commands

```bash
# List devices
adb devices

# Install APK
adb install -r app/build/outputs/apk/debug/app-debug.apk

# View logs
adb logcat -s "KinglyBot"

# Clear app data
adb shell pm clear bot.molt.android

# Screenshot
adb exec-out screencap -p > screenshot.png
```

## Common Issues

**Compose preview not rendering:**
- Clean build: `./gradlew clean`
- Invalidate caches in Android Studio

**Dynamic colors not working:**
- Requires Android 12+ (API 31)
- Fallback to custom colors on older devices

**Gateway connection fails:**
- Check network security config: `res/xml/network_security_config.xml`
- Ensure TLS pinning matches iOS

## Post-MVP Work

1. **P0:** Align theme colors with OCDesignKit (cream light mode)
2. **P1:** Add sidebar navigation (ChatGPT-style drawer)
3. **P1:** Build onboarding flow matching iOS
4. **P2:** Port SettingsView sections from iOS
5. **P3:** Add marketplace UI (TikTok swipe cards → ViewPager2)

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for android-compose domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Dependency missing—degrade gracefully; note in output. Ambiguous request—clarify before proceeding.
