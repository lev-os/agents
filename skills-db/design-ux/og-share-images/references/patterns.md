# Share Image Visual Patterns

Extended patterns for creating distinctive share images.

## Flywheel Diagram (Tools/Dashboard)

Circular nodes connected to center hub, representing interconnected tools:

```tsx
<svg width="210" height="210" viewBox="0 0 100 100" fill="none"
  style={{ filter: "drop-shadow(0 0 28px rgba(34,211,238,0.4))" }}>
  <defs>
    <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stopColor="#22d3ee" />
      <stop offset="50%" stopColor="#a855f7" />
      <stop offset="100%" stopColor="#f472b6" />
    </linearGradient>
  </defs>

  {/* Outer ring */}
  <circle cx="50" cy="50" r="45" stroke="url(#ringGrad)" strokeWidth="2" fill="none" opacity="0.8" />

  {/* Inner ring */}
  <circle cx="50" cy="50" r="35" stroke="#22d3ee" strokeWidth="1" fill="none" opacity="0.4" />

  {/* Center hub */}
  <circle cx="50" cy="50" r="12" fill="url(#ringGrad)" opacity="0.9" />
  <circle cx="50" cy="50" r="8" fill="rgba(255,255,255,0.2)" />

  {/* Flywheel nodes - 10 around circle */}
  {[0, 36, 72, 108, 144, 180, 216, 252, 288, 324].map((angle, i) => {
    const rad = (angle * Math.PI) / 180;
    const x = 50 + 40 * Math.cos(rad);
    const y = 50 + 40 * Math.sin(rad);
    const colors = ["#22d3ee", "#a855f7", "#f472b6", "#22c55e", "#f59e0b",
                    "#22d3ee", "#a855f7", "#f472b6", "#22c55e", "#f59e0b"];
    return (
      <g key={i}>
        <line x1="50" y1="50" x2={x} y2={y} stroke={colors[i]} strokeWidth="1.5" opacity="0.5" />
        <circle cx={x} cy={y} r="5" fill={colors[i]} opacity="0.9" />
        <circle cx={x} cy={y} r="3" fill="rgba(255,255,255,0.3)" />
      </g>
    );
  })}

  {/* Motion arrows */}
  <path d="M50 8 L54 14 L46 14 Z" fill="#22d3ee" opacity="0.7" />
  <path d="M92 50 L86 54 L86 46 Z" fill="#a855f7" opacity="0.7" />
  <path d="M50 92 L46 86 L54 86 Z" fill="#f472b6" opacity="0.7" />
  <path d="M8 50 L14 46 L14 54 Z" fill="#22c55e" opacity="0.7" />
</svg>
```

## Document/Writing Visual (Blog/Essays)

Document with text lines, floating cards, and pen icon:

```tsx
<svg width="185" height="185" viewBox="0 0 100 100" fill="none"
  style={{ filter: "drop-shadow(0 0 22px rgba(236,72,153,0.38))" }}>
  <defs>
    <linearGradient id="writeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stopColor="#ec4899" />
      <stop offset="50%" stopColor="#f472b6" />
      <stop offset="100%" stopColor="#6366f1" />
    </linearGradient>
  </defs>

  {/* Main document frame */}
  <rect x="20" y="8" width="60" height="84" rx="4"
    stroke="url(#writeGrad)" strokeWidth="2" fill="none" opacity="0.7" />

  {/* Document header */}
  <rect x="20" y="8" width="60" height="14" rx="4" fill="url(#writeGrad)" opacity="0.12" />

  {/* Title line */}
  <rect x="28" y="28" width="44" height="5" rx="2.5" fill="#ec4899" opacity="0.8" />

  {/* Text lines */}
  <rect x="28" y="40" width="44" height="3" rx="1.5" fill="#f472b6" opacity="0.5" />
  <rect x="28" y="47" width="38" height="3" rx="1.5" fill="#f472b6" opacity="0.5" />
  <rect x="28" y="54" width="42" height="3" rx="1.5" fill="#f472b6" opacity="0.5" />

  {/* Floating cards */}
  <rect x="5" y="15" width="22" height="30" rx="3" fill="#ec4899" opacity="0.15" />
  <rect x="75" y="35" width="20" height="28" rx="3" fill="#f472b6" opacity="0.15" />

  {/* Pen icon */}
  <path d="M85 8 L92 15 L78 29 L74 30 L75 26 Z" fill="#ec4899" opacity="0.7" />
  <path d="M87 6 L94 13 L92 15 L85 8 Z" fill="#6366f1" opacity="0.8" />
</svg>
```

## Code Window (Projects/Dev Tools)

Terminal-style window with code lines and git branch:

```tsx
<svg width="210" height="210" viewBox="0 0 100 100" fill="none"
  style={{ filter: "drop-shadow(0 0 22px rgba(249,115,22,0.38))" }}>
  <defs>
    <linearGradient id="projGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stopColor="#f97316" />
      <stop offset="50%" stopColor="#f59e0b" />
      <stop offset="100%" stopColor="#f43f5e" />
    </linearGradient>
  </defs>

  {/* Main window */}
  <rect x="10" y="15" width="80" height="70" rx="6"
    stroke="url(#projGrad)" strokeWidth="2.5" fill="none" opacity="0.75" />

  {/* Title bar */}
  <rect x="10" y="15" width="80" height="12" rx="6" fill="url(#projGrad)" opacity="0.18" />

  {/* Window dots */}
  <circle cx="18" cy="21" r="3" fill="#f43f5e" opacity="0.9" />
  <circle cx="27" cy="21" r="3" fill="#f59e0b" opacity="0.9" />
  <circle cx="36" cy="21" r="3" fill="#22c55e" opacity="0.9" />

  {/* Code lines */}
  <rect x="18" y="36" width="38" height="3.5" rx="1.75" fill="#f97316" opacity="0.75" />
  <rect x="22" y="45" width="52" height="3.5" rx="1.75" fill="#f59e0b" opacity="0.55" />
  <rect x="22" y="54" width="42" height="3.5" rx="1.75" fill="#f59e0b" opacity="0.55" />
  <rect x="18" y="63" width="30" height="3.5" rx="1.75" fill="#f97316" opacity="0.75" />

  {/* Git branch */}
  <path d="M5 38 Q 8 50, 5 62" stroke="#f97316" strokeWidth="2.5" fill="none" opacity="0.55" />
  <circle cx="5" cy="38" r="3.5" fill="#f97316" opacity="0.85" />
  <circle cx="5" cy="62" r="3.5" fill="#f59e0b" opacity="0.85" />
</svg>
```

## Network Hexagon (AI/Tech)

Hexagonal network representing connections:

```tsx
<svg width="200" height="200" viewBox="0 0 100 100" fill="none"
  style={{ filter: "drop-shadow(0 0 25px rgba(59,130,246,0.4))" }}>
  <defs>
    <linearGradient id="hexGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stopColor="#3b82f6" />
      <stop offset="50%" stopColor="#8b5cf6" />
      <stop offset="100%" stopColor="#06b6d4" />
    </linearGradient>
  </defs>

  {/* Main hexagon */}
  <polygon points="50,5 90,27 90,73 50,95 10,73 10,27"
    stroke="url(#hexGrad)" strokeWidth="2" fill="none" opacity="0.8" />

  {/* Inner hexagon */}
  <polygon points="50,20 75,35 75,65 50,80 25,65 25,35"
    stroke="url(#hexGrad)" strokeWidth="1.5" fill="none" opacity="0.4" />

  {/* Center core */}
  <circle cx="50" cy="50" r="12" fill="url(#hexGrad)" opacity="0.9" />
  <circle cx="50" cy="50" r="7" fill="rgba(255,255,255,0.25)" />

  {/* Corner nodes */}
  <circle cx="50" cy="5" r="4" fill="#3b82f6" opacity="0.9" />
  <circle cx="90" cy="27" r="4" fill="#8b5cf6" opacity="0.9" />
  <circle cx="90" cy="73" r="4" fill="#06b6d4" opacity="0.9" />
  <circle cx="50" cy="95" r="4" fill="#3b82f6" opacity="0.9" />
  <circle cx="10" cy="73" r="4" fill="#8b5cf6" opacity="0.9" />
  <circle cx="10" cy="27" r="4" fill="#06b6d4" opacity="0.9" />

  {/* Connection lines to center */}
  <line x1="50" y1="50" x2="50" y2="5" stroke="#3b82f6" strokeWidth="1" opacity="0.5" />
  <line x1="50" y1="50" x2="90" y2="27" stroke="#8b5cf6" strokeWidth="1" opacity="0.5" />
  <line x1="50" y1="50" x2="90" y2="73" stroke="#06b6d4" strokeWidth="1" opacity="0.5" />
</svg>
```

## Journey Path (About/Career)

Path with milestone dots for timelines:

```tsx
<svg width="200" height="200" viewBox="0 0 100 100" fill="none"
  style={{ filter: "drop-shadow(0 0 22px rgba(16,185,129,0.38))" }}>
  <defs>
    <linearGradient id="pathGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stopColor="#10b981" />
      <stop offset="50%" stopColor="#14b8a6" />
      <stop offset="100%" stopColor="#22c55e" />
    </linearGradient>
  </defs>

  {/* Main path */}
  <path d="M10,85 Q25,70 30,50 T50,30 T70,50 T90,15"
    stroke="url(#pathGrad)" strokeWidth="3" fill="none" opacity="0.8"
    strokeLinecap="round" />

  {/* Milestone dots */}
  <circle cx="10" cy="85" r="6" fill="#10b981" opacity="0.95" />
  <circle cx="30" cy="50" r="6" fill="#14b8a6" opacity="0.95" />
  <circle cx="50" cy="30" r="6" fill="#22c55e" opacity="0.95" />
  <circle cx="70" cy="50" r="6" fill="#14b8a6" opacity="0.95" />
  <circle cx="90" cy="15" r="6" fill="#10b981" opacity="0.95" />

  {/* Inner dot highlights */}
  <circle cx="10" cy="85" r="3" fill="rgba(255,255,255,0.3)" />
  <circle cx="50" cy="30" r="3" fill="rgba(255,255,255,0.3)" />
  <circle cx="90" cy="15" r="3" fill="rgba(255,255,255,0.3)" />
</svg>
```

## Grid Pattern Background

Subtle grid overlay for depth:

```tsx
<div style={{
  position: "absolute",
  top: 0, left: 0, right: 0, bottom: 0,
  opacity: 0.025,
  backgroundImage: `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%2322d3ee' stroke-width='0.5'%3E%3Cpath d='M0 20h40M20 0v40'/%3E%3C/g%3E%3C/svg%3E")`,
  display: "flex",
}} />
```

Change the stroke color (`%2322d3ee`) to match your theme.

## Two-Column Layout

Standard layout with visual left, text right:

```tsx
<div style={{
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  justifyContent: "center",
  gap: 60,
  padding: "40px 60px",
  width: "100%",
}}>
  {/* Left - Visual */}
  <div style={{ display: "flex", position: "relative" }}>
    {/* Glow behind icon */}
    <div style={{
      position: "absolute",
      width: 270, height: 270,
      borderRadius: "50%",
      background: "radial-gradient(circle, rgba(34,211,238,0.25) 0%, transparent 70%)",
      filter: "blur(30px)",
      display: "flex",
    }} />
    {/* SVG Icon */}
  </div>

  {/* Right - Text */}
  <div style={{ display: "flex", flexDirection: "column", maxWidth: 640 }}>
    {/* Badge */}
    {/* Title */}
    {/* Subtitle */}
    {/* Description */}
    {/* Tags */}
  </div>
</div>
```

## URL Badge (Top Right)

```tsx
<div style={{
  position: "absolute",
  top: 28,
  right: 38,
  fontSize: 14,
  color: "#475569",
  display: "flex",
}}>
  <span style={{ display: "flex" }}>example.com/page</span>
</div>
```
