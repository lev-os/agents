# Lottie Motion Specs for ClawBuddy

## State Animation Parameters

### Idle (Breathing)

```json
{
  "name": "clawbuddy_idle",
  "duration": 3000,
  "loop": true,
  "layers": [
    {
      "name": "orb_body",
      "properties": {
        "scale": {
          "keyframes": [
            { "time": 0, "value": [98, 98], "easing": "ease-in-out" },
            { "time": 1500, "value": [102, 102], "easing": "ease-in-out" },
            { "time": 3000, "value": [98, 98], "easing": "ease-in-out" }
          ]
        },
        "opacity": {
          "keyframes": [
            { "time": 0, "value": 85, "easing": "ease-in-out" },
            { "time": 1500, "value": 100, "easing": "ease-in-out" },
            { "time": 3000, "value": 85, "easing": "ease-in-out" }
          ]
        }
      }
    },
    {
      "name": "glow",
      "properties": {
        "scale": {
          "keyframes": [
            { "time": 0, "value": [140, 140], "easing": "ease-in-out" },
            { "time": 1500, "value": [160, 160], "easing": "ease-in-out" },
            { "time": 3000, "value": [140, 140], "easing": "ease-in-out" }
          ]
        },
        "opacity": {
          "keyframes": [
            { "time": 0, "value": 30, "easing": "ease-in-out" },
            { "time": 1500, "value": 40, "easing": "ease-in-out" },
            { "time": 3000, "value": 30, "easing": "ease-in-out" }
          ]
        }
      }
    }
  ]
}
```

### Thinking (Orbital Rotation)

```json
{
  "name": "clawbuddy_thinking",
  "duration": 2000,
  "loop": true,
  "layers": [
    {
      "name": "orb_body",
      "properties": {
        "rotation": {
          "keyframes": [
            { "time": 0, "value": 0, "easing": "linear" },
            { "time": 2000, "value": 360, "easing": "linear" }
          ]
        }
      }
    },
    {
      "name": "inner_glow",
      "properties": {
        "opacity": {
          "keyframes": [
            { "time": 0, "value": 60, "easing": "ease-in-out" },
            { "time": 1000, "value": 100, "easing": "ease-in-out" },
            { "time": 2000, "value": 60, "easing": "ease-in-out" }
          ]
        }
      }
    }
  ]
}
```

### Error (Shake)

```json
{
  "name": "clawbuddy_error",
  "duration": 500,
  "loop": false,
  "layers": [
    {
      "name": "orb_body",
      "properties": {
        "position_x": {
          "keyframes": [
            { "time": 0, "value": 0, "easing": "ease-in-out" },
            { "time": 83, "value": -4, "easing": "ease-in-out" },
            { "time": 167, "value": 4, "easing": "ease-in-out" },
            { "time": 250, "value": -4, "easing": "ease-in-out" },
            { "time": 333, "value": 4, "easing": "ease-in-out" },
            { "time": 417, "value": -4, "easing": "ease-in-out" },
            { "time": 500, "value": 0, "easing": "ease-in-out" }
          ]
        },
        "fill_color": {
          "keyframes": [
            { "time": 0, "value": "#8B5CF6", "easing": "ease-in" },
            { "time": 200, "value": "#FF4444", "easing": "ease-in" },
            { "time": 500, "value": "#8B5CF6", "easing": "ease-out" }
          ]
        }
      }
    }
  ]
}
```

### Celebrating (Burst)

```json
{
  "name": "clawbuddy_celebrating",
  "duration": 1500,
  "loop": false,
  "layers": [
    {
      "name": "orb_body",
      "properties": {
        "scale": {
          "keyframes": [
            { "time": 0, "value": [100, 100], "easing": "spring(0.5)" },
            { "time": 400, "value": [130, 130], "easing": "spring(0.5)" },
            { "time": 1000, "value": [100, 100], "easing": "ease-out" }
          ]
        }
      }
    },
    {
      "name": "particles",
      "type": "particle_emitter",
      "properties": {
        "emit_at": 200,
        "count": 12,
        "spread": 360,
        "velocity": 200,
        "life": 1000,
        "fade_out": 500,
        "colors": ["#8B5CF6", "#EC4899", "#F59E0B", "#10B981"]
      }
    }
  ]
}
```

## Onboarding Step Animations

### Welcome Wave

```json
{
  "name": "onboard_welcome",
  "duration": 2000,
  "loop": false,
  "sequence": [
    { "action": "scale_up", "from": [0, 0], "to": [100, 100], "duration": 400, "easing": "spring(0.6)" },
    { "action": "bounce_x", "amplitude": 8, "count": 3, "duration": 800 },
    { "action": "sparkle_trail", "particles": 6, "color": "#8B5CF6", "duration": 800 }
  ]
}
```

### Provider Thinking

```json
{
  "name": "onboard_provider",
  "duration": 3000,
  "loop": true,
  "layers": [
    { "name": "orb", "rotation": { "speed": 180, "easing": "linear" } },
    { "name": "orbit_icons", "count": 3, "radius": 40, "rotation": { "speed": -90 } }
  ]
}
```

### API Key Lock

```json
{
  "name": "onboard_apikey",
  "duration": 1500,
  "loop": false,
  "sequence": [
    { "action": "shield_glow", "color": "#F59E0B", "grow_from": 1.0, "grow_to": 1.4, "duration": 600 },
    { "action": "lock_icon_fade_in", "duration": 400, "delay": 400 },
    { "action": "pulse_gold", "count": 2, "duration": 500 }
  ]
}
```

### Permissions Handshake

```json
{
  "name": "onboard_permissions",
  "duration": 2000,
  "loop": false,
  "layers": [
    { "name": "orb_left", "position": [-30, 0], "scale": [80, 80] },
    { "name": "orb_right", "position": [30, 0], "scale": [80, 80] },
    { "name": "light_bridge", "from": "orb_left", "to": "orb_right", "grow_duration": 800, "delay": 400 }
  ]
}
```

### Connected Celebration

```json
{
  "name": "onboard_connected",
  "duration": 2500,
  "loop": false,
  "sequence": [
    { "action": "scale_pulse", "to": [120, 120], "duration": 300, "easing": "spring" },
    { "action": "confetti_burst", "count": 20, "spread": 360, "at": 300 },
    { "action": "rainbow_rim", "duration": 1500, "delay": 500 },
    { "action": "settle_idle", "duration": 700 }
  ]
}
```
