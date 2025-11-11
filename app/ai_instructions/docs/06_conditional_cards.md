# 🎯 CONDITIONAL CARDS IN LOVELACE DASHBOARDS

## Overview

Conditional cards allow you to show/hide cards dynamically based on entity state. This is especially powerful for monitoring dashboards where you only want to see active/relevant information.

---

## ✅ CORRECT PATTERN FOR CONDITIONAL CARDS

### Basic Structure

```yaml
type: conditional
conditions:
  - entity: sensor.example
    state: "on"
card:
  type: thermostat
  entity: climate.example_trv
```

**Key Points:**
- `conditions:` is an **array** (always use `-` for each condition)
- Each condition has `entity:` and `state:` keys
- The `card:` key contains the card to show when conditions are met
- Multiple conditions use AND logic (all must be true)

---

## 🔥 REAL-WORLD EXAMPLE: HEATING NOW DASHBOARD

**From Commit a16f9403** - Optimal pattern for TRVs in heating state:

### Problem
Show TRV thermostat cards **only** when they are actively heating, not when idle/off.

### Solution
Use `hvac_action` attribute with state `heating`:

```yaml
title: Heating Now
views:
  - title: Active Heating
    path: heating
    icon: mdi:fire
    cards:
      # Always visible status cards
      - type: entity
        entity: binary_sensor.boiler_status
        name: 🔥 Boiler
      
      - type: entity
        entity: sensor.cooldown_status
        name: ⏱️ Cooldown
      
      - type: sensor
        entity: sensor.active_heating_count
        name: 📊 Active Heating
      
      # CONDITIONAL CARDS - Only visible when heating!
      - type: conditional
        conditions:
          - entity: climate.office_trv
            state_not: "unavailable"
          - entity: climate.office_trv
            state: "heat"
        card:
          type: thermostat
          entity: climate.office_trv
          name: 🌡️ Office TRV
      
      - type: conditional
        conditions:
          - entity: climate.living_room_trv
            state_not: "unavailable"
          - entity: climate.living_room_trv
            state: "heat"
        card:
          type: thermostat
          entity: climate.living_room_trv
          name: 🌡️ Living Room TRV
      
      # Repeat for all TRVs...
```

### Result
- **No heating** → Shows 3 status cards only
- **1 TRV heating** → Shows 3 status + 1 thermostat
- **All 7 heating** → Shows 3 status + 7 thermostats
- **Dynamic, clean, focused interface!**

---

## 🎓 ADVANCED PATTERNS

### Pattern 1: Multiple Conditions (AND Logic)

```yaml
type: conditional
conditions:
  - entity: climate.bedroom_trv
    state_not: "unavailable"
  - entity: climate.bedroom_trv
    state: "heat"
card:
  type: thermostat
  entity: climate.bedroom_trv
```

This shows the card only when:
1. TRV is available (not offline)
2. AND TRV is in heat mode

### Pattern 2: Check Attribute Value

**IMPORTANT: For checking hvac_action attribute:**

```yaml
type: conditional
conditions:
  - entity: climate.office_trv
    state_not: "unavailable"
  # Check main state for mode
  - entity: climate.office_trv
    state: "heat"
card:
  type: thermostat
  entity: climate.office_trv
```

**Note:** To check `hvac_action` directly, you need a template sensor:

```yaml
# Create template sensor first
template:
  - sensor:
      - name: "Office TRV Heating"
        state: >
          {{ state_attr('climate.office_trv', 'hvac_action') == 'heating' }}
        
# Then use in conditional
type: conditional
conditions:
  - entity: sensor.office_trv_heating
    state: "True"
card:
  type: thermostat
  entity: climate.office_trv
```

### Pattern 3: State Not Equal (Excluding States)

```yaml
type: conditional
conditions:
  - entity: climate.bedroom_trv
    state_not: "unavailable"
  - entity: climate.bedroom_trv
    state_not: "off"
card:
  type: thermostat
  entity: climate.bedroom_trv
```

### Pattern 4: Numeric Threshold

```yaml
type: conditional
conditions:
  - entity: sensor.battery_level
    state_below: 20
card:
  type: entity
  entity: sensor.battery_level
  name: ⚠️ Low Battery!
```

### Pattern 5: Show When Above Threshold

```yaml
type: conditional
conditions:
  - entity: sensor.temperature
    state_above: 25
card:
  type: sensor
  entity: sensor.temperature
  name: 🔥 High Temperature!
```

---

## ❌ COMMON MISTAKES TO AVOID

### Mistake 1: Forgetting Array Syntax

```yaml
# ❌ WRONG - Missing dash before entity
type: conditional
conditions:
  entity: climate.office_trv
  state: "heat"
card:
  type: thermostat
  entity: climate.office_trv
```

```yaml
# ✅ CORRECT - Dash indicates array item
type: conditional
conditions:
  - entity: climate.office_trv
    state: "heat"
card:
  type: thermostat
  entity: climate.office_trv
```

### Mistake 2: Wrong Indentation

```yaml
# ❌ WRONG - Incorrect indentation
type: conditional
conditions:
- entity: climate.office_trv
  state: "heat"
  card:
    type: thermostat
    entity: climate.office_trv
```

```yaml
# ✅ CORRECT - card at same level as conditions
type: conditional
conditions:
  - entity: climate.office_trv
    state: "heat"
card:
  type: thermostat
  entity: climate.office_trv
```

### Mistake 3: Using Attributes Directly in Conditions

```yaml
# ❌ WRONG - Cannot check attributes directly
type: conditional
conditions:
  - entity: climate.office_trv
    attribute: hvac_action
    state: "heating"
```

```yaml
# ✅ CORRECT - Create template sensor first or check main state
type: conditional
conditions:
  - entity: climate.office_trv
    state: "heat"
```

### Mistake 4: Multiple Cards Without Wrapping

```yaml
# ❌ WRONG - Cannot show multiple cards directly
type: conditional
conditions:
  - entity: climate.office_trv
    state: "heat"
card:
  - type: thermostat
    entity: climate.office_trv
  - type: sensor
    entity: sensor.temperature
```

```yaml
# ✅ CORRECT - Wrap in vertical-stack
type: conditional
conditions:
  - entity: climate.office_trv
    state: "heat"
card:
  type: vertical-stack
  cards:
    - type: thermostat
      entity: climate.office_trv
    - type: sensor
      entity: sensor.temperature
```

---

## 📋 CONDITION OPTIONS REFERENCE

| Option | Purpose | Example |
|--------|---------|---------|
| `state:` | Exact state match | `state: "on"` |
| `state_not:` | State not equal | `state_not: "unavailable"` |
| `state_above:` | Numeric above | `state_above: 20` |
| `state_below:` | Numeric below | `state_below: 50` |

**Important:** All state values should be **strings** (quoted), except for numeric comparisons.

---

## 🎯 WHEN TO USE CONDITIONAL CARDS

### ✅ Good Use Cases

1. **Heating Monitoring** - Show only TRVs that are actively heating
2. **Low Battery Alerts** - Display devices with battery below threshold
3. **Problem Alerts** - Show warnings only when issues exist
4. **Active Media** - Display media players only when playing
5. **Motion Detection** - Show cameras only when motion detected

### ❌ Not Recommended

1. **Static Content** - If card should always show, don't make it conditional
2. **Complex Logic** - If you need OR logic or complex conditions, use templates instead
3. **All Cards Conditional** - Keep some static cards for context

---

## 🔧 DEBUGGING TIPS

### Card Not Showing?

1. **Check entity state** - Use Developer Tools → States to verify actual state
2. **Check entity availability** - Add `state_not: "unavailable"` condition
3. **Check quotes** - States should be quoted: `state: "heat"` not `state: heat`
4. **Check indentation** - YAML is sensitive to indentation
5. **Check array syntax** - Don't forget the dash: `- entity:` not `entity:`

### Test Your Conditions

```yaml
# Add a test card to see when conditions are met
- type: conditional
  conditions:
    - entity: climate.office_trv
      state: "heat"
  card:
    type: markdown
    content: "✅ CONDITION MET - Office is heating!"
```

---

## 📝 TEMPLATE FOR TRV HEATING MONITORING

**Use this template for any TRV heating dashboard:**

```yaml
title: Heating Monitor
views:
  - title: Active Heating
    path: active-heating
    icon: mdi:fire
    cards:
      # Status cards (always visible)
      - type: entity
        entity: binary_sensor.boiler_status
        name: 🔥 Boiler Status
      
      # CONDITIONAL TRV CARDS
      # Copy this block for each TRV
      - type: conditional
        conditions:
          - entity: climate.ROOM_NAME_trv
            state_not: "unavailable"
          - entity: climate.ROOM_NAME_trv
            state: "heat"
        card:
          type: thermostat
          entity: climate.ROOM_NAME_trv
          name: 🌡️ ROOM_NAME TRV
```

**Replace:**
- `ROOM_NAME` with actual room name (office, bedroom, etc.)
- Add one conditional block per TRV
- Keep status cards at the top for context

---

## 🎓 SUMMARY: GOLDEN RULES

1. ✅ Always use array syntax: `conditions:` with `-` for each item
2. ✅ Always quote state values: `state: "heat"` not `state: heat`
3. ✅ Proper indentation: `card:` at same level as `conditions:`
4. ✅ Add availability check: `state_not: "unavailable"` to prevent errors
5. ✅ Test conditions in Developer Tools first
6. ✅ Keep some static cards for context (don't make everything conditional)
7. ✅ Use meaningful names and emojis for better UX

---

**Reference Commit:** `a16f9403` - "feat: Heating Now dashboard with conditional TRV controls"

This pattern was battle-tested and works perfectly for dynamic heating monitoring! 🔥

