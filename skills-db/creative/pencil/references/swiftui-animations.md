# SwiftUI Animation Specs for ClawBuddy

## Orb View Component

```swift
import SwiftUI

enum OrbState: String, CaseIterable {
    case idle, thinking, speaking, listening, sleeping
    case error, bgProcessing, writing, researching, celebrating
    case connecting, warning
}

struct ClawBuddyOrb: View {
    let state: OrbState
    let audioLevel: CGFloat  // 0.0–1.0 for speaking/listening
    let size: CGFloat

    @State private var animating = false
    @State private var rotation: Double = 0

    var body: some View {
        ZStack {
            // Ambient glow
            Circle()
                .fill(glowGradient)
                .frame(width: size * 1.6, height: size * 1.6)
                .blur(radius: size * 0.4)
                .opacity(glowOpacity)

            // Main orb body
            Circle()
                .fill(orbGradient)
                .frame(width: size, height: size)
                .scaleEffect(scaleValue)
                .rotationEffect(.degrees(rotation))
                .offset(x: shakeOffset, y: floatOffset)

            // Eye highlights
            HStack(spacing: size * 0.15) {
                Circle()
                    .fill(.white.opacity(eyeOpacity))
                    .frame(width: size * 0.12, height: size * 0.12)
                Circle()
                    .fill(.white.opacity(eyeOpacity))
                    .frame(width: size * 0.12, height: size * 0.12)
            }
            .offset(y: -size * 0.05)

            // State-specific overlays
            stateOverlay
        }
        .onAppear { startAnimation() }
        .onChange(of: state) { _, _ in startAnimation() }
    }

    // MARK: - Computed Animation Values

    private var scaleValue: CGFloat {
        switch state {
        case .idle:
            return animating ? 1.02 : 0.98
        case .speaking:
            return 1.0 + audioLevel * 0.15
        case .celebrating:
            return animating ? 1.3 : 1.0
        case .sleeping:
            return animating ? 0.95 : 0.92
        default:
            return 1.0
        }
    }

    private var shakeOffset: CGFloat {
        state == .error && animating ? 4 : 0
    }

    private var floatOffset: CGFloat {
        state == .sleeping ? (animating ? -2 : 2) : 0
    }

    private var eyeOpacity: Double {
        switch state {
        case .sleeping: return 0.3
        case .error: return 0.9
        case .celebrating: return 1.0
        default: return 0.7
        }
    }

    private var glowOpacity: Double {
        switch state {
        case .sleeping: return 0.2
        case .speaking, .celebrating: return 0.6
        case .error: return 0.5
        default: return 0.35
        }
    }

    private var orbGradient: some ShapeStyle {
        RadialGradient(
            colors: gradientColors,
            center: .center,
            startRadius: 0,
            endRadius: size * 0.5
        )
    }

    private var glowGradient: some ShapeStyle {
        RadialGradient(
            colors: [gradientColors.first ?? .purple, .clear],
            center: .center,
            startRadius: 0,
            endRadius: size * 0.8
        )
    }

    private var gradientColors: [Color] {
        switch state {
        case .idle:         return [.purple, .indigo]
        case .thinking:     return [.purple, .orange.opacity(0.6)]
        case .speaking:     return [.blue, .purple]
        case .listening:    return [.blue, .cyan.opacity(0.6)]
        case .sleeping:     return [.indigo.opacity(0.6), .gray.opacity(0.3)]
        case .error:        return [.red, .orange]
        case .bgProcessing: return [.teal, .purple]
        case .writing:      return [.purple, .green.opacity(0.5)]
        case .researching:  return [.blue, .cyan]
        case .celebrating:  return [.purple, .pink, .yellow.opacity(0.5)]
        case .connecting:   return [.blue, .purple.opacity(0.7)]
        case .warning:      return [.orange, .yellow.opacity(0.6)]
        }
    }

    @ViewBuilder
    private var stateOverlay: some View {
        switch state {
        case .bgProcessing:
            Circle()
                .strokeBorder(style: StrokeStyle(lineWidth: 2, dash: [6, 4]))
                .foregroundStyle(.white.opacity(0.4))
                .frame(width: size * 1.2, height: size * 1.2)
                .rotationEffect(.degrees(rotation))

        case .listening:
            Circle()
                .stroke(.white.opacity(animating ? 0 : 0.4), lineWidth: 1)
                .frame(width: size * (animating ? 2.0 : 1.0),
                       height: size * (animating ? 2.0 : 1.0))

        case .connecting:
            ForEach(0..<3) { i in
                Circle()
                    .stroke(.white.opacity(0.2), lineWidth: 1)
                    .frame(width: size * (1.0 + CGFloat(i) * 0.3),
                           height: size * (1.0 + CGFloat(i) * 0.3))
                    .scaleEffect(animating ? 1.5 : 1.0)
                    .opacity(animating ? 0 : 0.4)
                    .animation(
                        .easeOut(duration: 1.5)
                        .repeatForever(autoreverses: false)
                        .delay(Double(i) * 0.3),
                        value: animating
                    )
            }

        default:
            EmptyView()
        }
    }

    // MARK: - Animation Control

    private func startAnimation() {
        animating = false
        rotation = 0

        withAnimation(animationForState) {
            animating = true
        }

        if state == .thinking || state == .bgProcessing {
            withAnimation(.linear(duration: 2).repeatForever(autoreverses: false)) {
                rotation = 360
            }
        }
    }

    private var animationForState: Animation {
        switch state {
        case .idle:
            return .easeInOut(duration: 3).repeatForever(autoreverses: true)
        case .thinking:
            return .easeInOut(duration: 1).repeatForever(autoreverses: true)
        case .speaking:
            return .spring(response: 0.1, dampingFraction: 0.5)
        case .listening:
            return .easeOut(duration: 1.5).repeatForever(autoreverses: false)
        case .sleeping:
            return .easeInOut(duration: 4).repeatForever(autoreverses: true)
        case .error:
            return .default.repeatCount(3, autoreverses: true).speed(4)
        case .bgProcessing:
            return .linear(duration: 1).repeatForever(autoreverses: false)
        case .writing:
            return .easeInOut(duration: 0.6).repeatForever(autoreverses: true)
        case .researching:
            return .easeInOut(duration: 2).repeatForever(autoreverses: true)
        case .celebrating:
            return .spring(response: 0.4, dampingFraction: 0.5)
        case .connecting:
            return .easeOut(duration: 1).repeatForever(autoreverses: false)
        case .warning:
            return .easeInOut(duration: 1.5).repeatForever(autoreverses: true)
        }
    }
}

// MARK: - Preview

#Preview("ClawBuddy States") {
    LazyVGrid(columns: [GridItem(.adaptive(minimum: 100))], spacing: 24) {
        ForEach(OrbState.allCases, id: \.self) { state in
            VStack(spacing: 8) {
                ClawBuddyOrb(state: state, audioLevel: 0.5, size: 48)
                    .frame(width: 80, height: 80)
                Text(state.rawValue)
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
        }
    }
    .padding()
    .background(.black)
    .preferredColorScheme(.dark)
}
```

## Screen Edge Blur Effect (Speaking Mode)

```swift
struct SpeechBlurOverlay: View {
    let isActive: Bool
    let blurRadius: CGFloat = 20

    var body: some View {
        ZStack {
            // Edge blur vignette
            Rectangle()
                .fill(.clear)
                .overlay {
                    LinearGradient(
                        colors: [.black.opacity(0.3), .clear, .clear, .clear, .black.opacity(0.3)],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                }
                .overlay {
                    LinearGradient(
                        colors: [.black.opacity(0.3), .clear, .clear, .clear, .black.opacity(0.3)],
                        startPoint: .top,
                        endPoint: .bottom
                    )
                }
                .blur(radius: blurRadius)
                .opacity(isActive ? 1 : 0)
                .animation(.easeInOut(duration: 0.2), value: isActive)
                .allowsHitTesting(false)
        }
    }
}
```
