# Figma Wireframe Specifications
## GDM Care MVP - 5 Screens

> **Estimated build time:** 2 hours  
> **Tool:** Figma (free account)  
> **Deliverable:** Clickable prototype showing user flows

---

## Design System

### Colors
```
Primary Blue:    #2563EB
Primary Dark:    #1E40AF
Success Green:   #10B981
Warning Orange:  #F59E0B
Danger Red:      #EF4444
Gray 50:         #F9FAFB (background)
Gray 900:        #111827 (text)
```

### Typography
- **Headings:** Inter Bold, 32px (H1), 24px (H2), 18px (H3)
- **Body:** Inter Regular, 16px
- **Small:** Inter Regular, 14px
- **Download Inter:** https://fonts.google.com/specimen/Inter

### Components to Create
1. **Button Primary** - 180x48px, #2563EB, white text, 6px radius
2. **Button Secondary** - 180x48px, #E5E7EB, gray text, 6px radius
3. **Input Field** - Full width, 48px height, 1px border #D1D5DB, 6px radius
4. **Stat Card** - White background, 8px radius, 24px padding
5. **Nav Link** - Inter Medium 16px, gray text, primary on active

---

## Screen 1: Login (375x812 mobile)

### Layout
```
┌─────────────────────────────────┐
│                                 │
│        GDM Care (logo)          │  ← 32px from top
│                                 │
│                                 │
│      Welcome Back               │  ← H1, center
│   Sign in to continue...        │  ← Body gray, center
│                                 │
│   ┌──────────────────────┐     │
│   │ Email                │     │  ← Input
│   └──────────────────────┘     │
│                                 │
│   ┌──────────────────────┐     │
│   │ Password             │     │  ← Input
│   └──────────────────────┘     │
│                                 │
│   ┌──────────────────────┐     │
│   │     Sign In          │     │  ← Button Primary
│   └──────────────────────┘     │
│                                 │
│   Don't have an account?        │
│      Register here              │  ← Link (blue)
│                                 │
└─────────────────────────────────┘
```

### Measurements
- Container: 375x812px
- Content area: 327px wide (24px margins)
- Logo: Center, 48px height
- Title spacing: 80px from logo
- Input spacing: 16px between fields
- Button: Full width, 48px height
- Footer link: 24px below button

### Interactions
- **Hotspot:** "Register here" → Links to Screen 2 (Register)
- **Hotspot:** "Sign In" button → Links to Screen 3 (Dashboard)

---

## Screen 2: Register (375x812 mobile, scrollable)

### Layout
```
┌─────────────────────────────────┐
│     Create Your Account         │  ← H1
│  Join GDM Care to start...      │  ← Subtitle
│                                 │
│   ┌──────────────────────┐     │
│   │ Full Name            │     │
│   └──────────────────────┘     │
│   ┌──────────────────────┐     │
│   │ Email                │     │
│   └──────────────────────┘     │
│   ┌──────────────────────┐     │
│   │ Password             │     │
│   └──────────────────────┘     │
│   ┌──────────────────────┐     │
│   │ Due Date             │     │
│   └──────────────────────┘     │
│   ┌──────────────────────┐     │
│   │ Weeks Pregnant       │     │
│   └──────────────────────┘     │
│   ┌──────────────────────┐     │
│   │ Region ▼             │     │  ← Dropdown
│   └──────────────────────┘     │
│                                 │
│   ┌──────────────────────┐     │
│   │   Create Account     │     │  ← Button Primary
│   └──────────────────────┘     │
│                                 │
│   Already have an account?      │
│      Sign in here              │  ← Link
│                                 │
└─────────────────────────────────┘
```

### Measurements
- Same container as Login
- Form fields: 16px spacing
- Scrollable content area

### Interactions
- **Hotspot:** "Sign in here" → Links back to Screen 1 (Login)
- **Hotspot:** "Create Account" → Links to Screen 3 (Dashboard)

---

## Screen 3: Dashboard (375x812 mobile, scrollable)

### Layout
```
┌─────────────────────────────────┐
│ GDM Care  [Dash][Chat][History] │  ← Nav bar
├─────────────────────────────────┤
│                                 │
│ Welcome, Priya                  │  ← H1
│ 24 weeks pregnant • Due Jun 15  │  ← Subtitle
│                                 │
│ ┌─────────┬─────────┬─────────┐│
│ │Today's  │Today's  │7-Day    ││
│ │Readings │Average  │Average  ││  ← 3 Stat cards
│ │   3     │  112    │  108    ││
│ └─────────┴─────────┴─────────┘│
│                                 │
│ ┌─────────────────────────┐   │
│ │   +                     │   │
│ │   Log Glucose           │   │  ← Action card
│ │   Record a new reading  │   │
│ └─────────────────────────┘   │
│                                 │
│ ┌─────────────────────────┐   │
│ │   💬                    │   │
│ │   Ask Questions         │   │  ← Action card
│ │   Get Kerala diet...    │   │
│ └─────────────────────────┘   │
│                                 │
│ Recent Readings                 │  ← H2
│ ┌─────────────────────────────┐│
│ │ Today 7:00 AM              ││
│ │ Fasting: 92 mg/dL  [Normal]││  ← Reading row
│ ├─────────────────────────────┤│
│ │ Today 10:00 AM             ││
│ │ Post-Breakfast: 118 [Normal]││
│ └─────────────────────────────┘│
│                                 │
│ View all readings →             │  ← Link
│                                 │
└─────────────────────────────────┘
```

### Measurements
- Nav bar: 56px height, white background, border bottom
- Stats grid: 3 cards, 8px gap
- Stat card: 100px wide, 80px height
- Action cards: Full width, 100px height, 16px spacing
- Recent readings table: 8px padding per row

### Interactions
- **Nav:** "Chat" → Links to Screen 4 (Chat)
- **Nav:** "History" → Links to Screen 5 (Glucose History)
- **Hotspot:** "+ Log Glucose" card → Links to Log Form (not in 5 screens)
- **Hotspot:** "Ask Questions" card → Links to Screen 4 (Chat)
- **Hotspot:** "View all readings" → Links to Screen 5

---

## Screen 4: Chat (375x812 mobile)

### Layout
```
┌─────────────────────────────────┐
│ GDM Care  [Dash][Chat][History] │  ← Nav bar
├─────────────────────────────────┤
│                                 │
│   Ask About Kerala Foods        │  ← H1, center
│   Get personalized diet...      │  ← Subtitle
│                                 │
│ ┌─────────────────────────────┐│
│ │                             ││
│ │ [Bot bubble]                ││
│ │ Welcome! I'm here to help   ││
│ │ with your GDM questions.    ││
│ │ Ask me about Kerala foods!  ││
│ │                       10:05 ││
│ │                             ││
│ │              [User bubble]  ││
│ │         Can I eat dosa?     ││
│ │                   10:06     ││
│ │                             ││
│ │ [Bot bubble]                ││
│ │ One medium dosa has 20-25g  ││
│ │ carbs. Pair with sambar...  ││
│ │                       10:06 ││
│ │                             ││
│ └─────────────────────────────┘│
│                                 │
│ ┌─────────────────────┬─────┐ │
│ │ Ask about Kerala...│ Send│ │  ← Input + button
│ └─────────────────────┴─────┘ │
└─────────────────────────────────┘
```

### Measurements
- Chat area: Flex height, 16px padding
- Bot bubble: Left-aligned, gray background (#F3F4F6), 12px radius
- User bubble: Right-aligned, primary blue background, 12px radius, white text
- Bubble max width: 70% of container
- Bubble padding: 12px
- Input bar: 56px height, border top, 16px padding

### Interactions
- **Nav:** "Dash" → Links back to Screen 3 (Dashboard)
- **Nav:** "History" → Links to Screen 5
- **Hotspot:** "Send" button → (Prototype: No action, just visual)

---

## Screen 5: Glucose History (375x812 mobile, scrollable)

### Layout
```
┌─────────────────────────────────┐
│ GDM Care  [Dash][Chat][History] │  ← Nav bar
├─────────────────────────────────┤
│                                 │
│ Glucose History   [+ Log]       │  ← H1 + button
│                                 │
│ ┌─────────────────────────────┐│
│ │ Feb 2, 7:00 AM              ││
│ │ Fasting: 92 mg/dL           ││
│ │ Status: Normal         [🟢] ││  ← Green badge
│ ├─────────────────────────────┤│
│ │ Feb 2, 10:00 AM             ││
│ │ Post-Breakfast: 118 mg/dL   ││
│ │ Meal: 2 idlis + sambar      ││
│ │ Status: Normal         [🟢] ││
│ ├─────────────────────────────┤│
│ │ Feb 2, 3:00 PM              ││
│ │ Post-Lunch: 135 mg/dL       ││
│ │ Meal: Rice + fish curry     ││
│ │ Status: Above Target   [🟡] ││  ← Yellow badge
│ ├─────────────────────────────┤│
│ │ Feb 1, 7:00 AM              ││
│ │ Fasting: 88 mg/dL           ││
│ │ Status: Normal         [🟢] ││
│ └─────────────────────────────┘│
│                                 │
│ Showing last 50 readings        │  ← Footer note
│                                 │
└─────────────────────────────────┘
```

### Measurements
- Page header: 56px height, space-between
- Table rows: 80px height each, border bottom 1px
- Badge: 80x24px, 12px radius, colored background
- Footer: 16px padding, gray text

### Interactions
- **Nav:** "Dash" → Links to Screen 3
- **Nav:** "Chat" → Links to Screen 4
- **Hotspot:** "+ Log" button → (Prototype: No action)

---

## Prototyping Connections Summary

Create these clickable hotspots:

1. **Login** → Register (link)
2. **Login** → Dashboard (button)
3. **Register** → Login (link)
4. **Register** → Dashboard (button)
5. **Dashboard** → Chat (nav + action card)
6. **Dashboard** → History (nav + link)
7. **Chat** → Dashboard (nav)
8. **Chat** → History (nav)
9. **History** → Dashboard (nav)
10. **History** → Chat (nav)

---

## Figma Tips

### Create Components
1. Create frame for each screen (375x812)
2. Build reusable components:
   - Button Primary
   - Button Secondary
   - Input Field
   - Stat Card
   - Nav Bar
3. Use Auto Layout for responsive spacing
4. Create color styles for consistency

### Prototype Mode
1. Click "Prototype" tab (top right)
2. Select hotspot area
3. Drag blue handle to target frame
4. Set interaction: "On Click" → "Navigate to"
5. Animation: "Instant" (or "Smart Animate" for smooth transitions)

### Present Mode
1. Click Play button (top right)
2. Test all interactions
3. Share link with class

---

## Deliverable Checklist

- [ ] All 5 screens created (375x812)
- [ ] Color system applied
- [ ] Typography consistent (Inter font)
- [ ] Navigation bar on authenticated screens
- [ ] All hotspots connected
- [ ] Prototype tested in Present mode
- [ ] Share link generated

**Time estimate:** 2 hours for someone familiar with Figma, 3 hours for beginners.

---

## Alternative: Use Provided Screenshots

If short on time, take screenshots of the running Flask app and annotate them in Figma to show user flows.