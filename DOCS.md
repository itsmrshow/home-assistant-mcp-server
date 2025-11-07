# HA Cursor Agent - API Documentation

**Complete API reference for developers and AI agents**

---

## 🤖 For Cursor AI: Quick Start

### Connection Prompt (Copy This)

```
I have HA Cursor Agent running on my Home Assistant.

Token: YOUR_TOKEN_HERE
API URL: http://homeassistant.local:8099

Please read the Cursor AI instructions at:
https://github.com/Coolver/home-assistant-cursor-agent/blob/main/DOCS.md#cursor-ai-instructions

Confirm you understand the safety protocols and are ready to help.

My request: [describe what you want]
```

### Cursor AI Instructions {#cursor-ai-instructions}

**READ THESE BEFORE MAKING ANY CHANGES TO USER'S HOME ASSISTANT**

#### 1️⃣ Analysis First (MANDATORY)
- Read `configuration.yaml` to understand HA version and structure
- Check existing `automations.yaml`, `scripts.yaml` format
- Query `/api/entities/list` to understand user's devices
- **Never assume** - always verify current state

#### 2️⃣ Verify Compatibility
- Compare your knowledge with user's actual HA version
- Check if syntax matches current files format
- DO NOT use deprecated YAML syntax
- When uncertain, ASK user first

#### 3️⃣ Safety Protocols
- **ALWAYS** create backup: `POST /api/backup/commit`
- Show planned changes BEFORE applying
- Make changes incrementally (test each step)
- Provide verification links after changes

#### 4️⃣ After Changes
- Summary of what was modified
- Links: `http://homeassistant.local:8123/config/automation` (etc.)
- Testing instructions
- Rollback command if needed

#### 🚫 Never Do
- ❌ Skip reading current configuration
- ❌ Use outdated syntax from training data
- ❌ Make changes without backup
- ❌ Ignore configuration check errors

---

## 🔗 Base URL

```
http://homeassistant.local:8099
```

---

## 🔐 Authentication

All endpoints (except `/api/health` and `/`) require authentication.

**Header:**
```
Authorization: Bearer YOUR_LONG_LIVED_TOKEN
```

---

## 📁 Files API

### List Files

**GET** `/api/files/list`

**Query Parameters:**
- `directory` (optional): Directory to list (default: root)
- `pattern` (optional): File pattern (default: `*.yaml`)

**Response:**
```json
[
  {
    "path": "configuration.yaml",
    "name": "configuration.yaml",
    "size": 1234,
    "modified": 1699000000.0,
    "is_yaml": true
  }
]
```

---

### Read File

**GET** `/api/files/read`

**Query Parameters:**
- `path` (required): File path relative to `/config`

**Response:**
```json
{
  "success": true,
  "path": "configuration.yaml",
  "content": "# Home Assistant configuration...",
  "size": 1234
}
```

---

### Write File

**POST** `/api/files/write`

**Body:**
```json
{
  "path": "scripts.yaml",
  "content": "my_script:\n  alias: Test\n  sequence: []",
  "create_backup": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "File written: scripts.yaml",
  "data": {
    "success": true,
    "path": "scripts.yaml",
    "size": 123,
    "backup": "a1b2c3d4",
    "git_commit": "a1b2c3d4"
  }
}
```

---

## 🏠 Entities API

### List Entities

**GET** `/api/entities/list`

**Query Parameters:**
- `domain` (optional): Filter by domain
- `search` (optional): Search term

**Response:**
```json
{
  "success": true,
  "count": 192,
  "entities": [
    {
      "entity_id": "climate.bedroom_trv_thermostat",
      "state": "heat",
      "attributes": {
        "current_temperature": 20.5,
        "temperature": 21.0,
        "hvac_modes": ["off", "heat"]
      },
      "last_changed": "2025-11-03T10:00:00"
    }
  ]
}
```

---

### Get Entity State

**GET** `/api/entities/state/{entity_id}`

**Response:**
```json
{
  "success": true,
  "entity_id": "sensor.temperature",
  "state": {
    "entity_id": "sensor.temperature",
    "state": "20.5",
    "attributes": {...},
    "last_changed": "..."
  }
}
```

---

## 🤖 Automations API

### Create Automation

**POST** `/api/automations/create`

**Body:**
```json
{
  "id": "climate_control",
  "alias": "Climate Control",
  "description": "Smart climate control",
  "trigger": [
    {
      "platform": "state",
      "entity_id": "sensor.any_trv_heating",
      "to": "True"
    }
  ],
  "condition": [
    {
      "condition": "state",
      "entity_id": "input_boolean.system_enabled",
      "state": "on"
    }
  ],
  "action": [
    {
      "service": "script.start_heating",
      "data": {}
    }
  ],
  "mode": "single"
}
```

**Automatically:**
- ✅ Appends to automations.yaml
- ✅ Creates backup
- ✅ Reloads automations
- ✅ Commits to Git

---

## 💾 Backup API

### Create Backup

**POST** `/api/backup/commit`

**Body:**
```json
{
  "message": "Before major changes"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Backup created: a1b2c3d4",
  "data": {
    "commit_hash": "a1b2c3d4"
  }
}
```

---

### Rollback

**POST** `/api/backup/rollback`

**Body:**
```json
{
  "commit_hash": "a1b2c3d4"
}
```

**⚠️ Warning:** This overwrites current configuration!

---

## 📊 Complete Workflow Example

### Installing Climate Control System via AI

```python
import requests

url = "http://homeassistant.local:8099"
headers = {"Authorization": "Bearer TOKEN"}

# 1. Create backup
requests.post(f"{url}/api/backup/commit", 
              json={"message": "Before climate control"}, 
              headers=headers)

# 2. Get current entities
entities = requests.get(f"{url}/api/entities/list?domain=climate", 
                        headers=headers).json()

# 3. Create helpers
for helper in helpers_list:
    requests.post(f"{url}/api/helpers/create", json=helper, headers=headers)

# 4. Update configuration.yaml
config = requests.get(f"{url}/api/files/read?path=configuration.yaml", 
                      headers=headers).json()['content']
new_config = config + "\n" + template_sensors
requests.post(f"{url}/api/files/write", 
              json={"path": "configuration.yaml", "content": new_config},
              headers=headers)

# 5. Create automations
for automation in automations_list:
    requests.post(f"{url}/api/automations/create", json=automation, headers=headers)

# 6. Reload all
requests.post(f"{url}/api/system/reload?component=all", headers=headers)

# 7. Verify
requests.post(f"{url}/api/system/check_config", headers=headers)

print("✅ Climate control system installed!")
```

---

## 🚀 For Cursor AI

### Recommended Workflow

1. **Explore:** Use `/api/entities/list` to understand current setup
2. **Backup:** Create commit before changes
3. **Develop:** Create/modify components via API
4. **Validate:** Check config validity
5. **Apply:** Reload components
6. **Monitor:** Check logs for errors
7. **Rollback:** If issues, restore previous state

### Tips for AI

- Always create backup before modifications
- Use `/api/files/parse_yaml` to understand existing structure
- Check `/api/logs/` for operation results
- Use `/api/backup/diff` to see what changed
- Provide clear commit messages for tracking

---

**Full interactive documentation:** `http://homeassistant.local:8099/docs` 📚

