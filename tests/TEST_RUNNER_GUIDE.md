# 🚀 Test Runner Guide for AI Assistant

**Purpose:** Instructions for AI to execute HA Agent tests programmatically

---

## Commands

### Run Full Test Suite
```
"запусти тест Home Assistant Agent"
"run HA Agent test suite"
"test all HA Agent functions"
```

### Run Category Tests
```
"запусти тесты Files"
"test Entity operations"
"run Git/Backup tests"
```

### Run Single Test
```
"запусти тест test_read_configuration_yaml"
"run test_list_entities"
```

---

## Test Execution Flow

### 1. Initialize
- Verify MCP connection
- Check HA Agent status
- Note start time
- Create test report structure

### 2. Execute Tests
For each test:
1. Log test start
2. Call MCP function with parameters
3. Validate response
4. Record result (PASS/FAIL/SKIP)
5. Capture duration
6. Clean up if needed

### 3. Report Results
- Summary statistics
- Failed tests with errors
- Skipped tests with reasons
- Performance metrics
- Recommendations

---

## Test Execution Template

```markdown
## 🧪 Starting Test Suite: [Category Name]

### Test 1: [test_name]
**Function:** ha_xxx
**Status:** Running...

[Execute test]

**Result:** ✅ PASS (125ms)
**Response:** [brief summary]

---

### Test 2: [test_name]
**Function:** ha_xxx
**Status:** Running...

[Execute test]

**Result:** ❌ FAIL (50ms)
**Error:** [error message]
**Expected:** [what should happen]

---

[Continue for all tests]

## 📊 Summary
- **Total:** X tests
- **Passed:** X (XX%)
- **Failed:** X (XX%)
- **Skipped:** X (XX%)
- **Duration:** XX.X seconds
```

---

## Phase Execution Order

### Phase 1: Read-Only (Always Safe)
Execute first, should never fail in healthy system:
- test_list_files_root
- test_list_all_entities
- test_list_climate_entities
- test_get_entity_state
- test_list_helpers
- test_list_automations
- test_list_scripts
- test_git_history
- test_check_config
- test_get_logs
- test_hacs_status
- test_list_store_addons
- test_list_available_addons
- test_list_installed_addons
- test_analyze_entities_for_dashboard
- test_list_addon_repositories

### Phase 2: Non-Destructive Writes
Safe operations, can be rolled back:
- test_write_and_read_test_file
- test_git_commit
- test_git_diff_last_two_commits
- test_create_input_boolean_helper
- test_create_test_automation
- test_create_test_script
- test_apply_dashboard

### Phase 3: Cleanup Operations
Remove test artifacts:
- test_delete_test_file
- Delete test helper
- Delete test automation
- Delete test script
- test_delete_dashboard

### Phase 4: Advanced (Optional)
Skip in production, require confirmation:
- test_reload_config_core
- test_git_rollback_and_restore
- test_install_addon
- test_start_addon
- test_stop_addon
- HACS operations
- Add-on management

---

## Error Handling

### Network Errors
- Retry up to 3 times with 5s delay
- If persistent: SKIP test, note in report

### Validation Errors
- Mark as FAIL
- Include error details
- Continue to next test

### Timeout Errors
- Default timeout: 30 seconds
- Long operations: 5 minutes
- Mark as FAIL if timeout

### Expected Errors
Some tests expect errors (e.g., delete non-existent file):
- Verify error matches expected
- Mark as PASS if correct error

---

## Cleanup Strategy

### After Each Test
```
1. If test created files → delete them
2. If test created entities → remove them
3. If test modified config → restore or document
```

### After Full Suite
```
1. Git commit: "Test suite execution - cleanup"
2. Review created entities
3. Remove any test artifacts
4. Verify system state restored
```

### Emergency Cleanup
If tests interrupted:
```
1. Check for test_* files
2. Check for test_agent_* entities
3. Check for test-* dashboards
4. Remove all found test artifacts
5. Git status to see changes
```

---

## Response Validation

### For List Operations
```typescript
✅ Response is array
✅ Array length > 0 (or = 0 if expected empty)
✅ Each item has expected properties
```

### For Create Operations
```typescript
✅ Response contains success message or entity_id
✅ Created entity appears in subsequent list
✅ Entity has correct properties
```

### For Read Operations
```typescript
✅ Response is string or object
✅ Content matches expected format
✅ Required fields present
```

### For Delete Operations
```typescript
✅ Success message received
✅ Entity no longer in list
✅ Subsequent read returns 404/not found
```

---

## Safety Checks

### Before Starting
```
1. ✅ MCP connection active
2. ✅ HA Agent reachable
3. ✅ Not in production mode (or user confirmed)
4. ✅ Git repo clean (no uncommitted changes)
```

### During Execution
```
1. ⚠️ Stop if >50% tests fail (system issue)
2. ⚠️ Skip destructive tests in production
3. ⚠️ Confirm before HA restart
4. ⚠️ Backup before HACS uninstall
```

### After Completion
```
1. ✅ All test artifacts removed
2. ✅ System returned to pre-test state
3. ✅ Git commit with test results
4. ✅ Report generated
```

---

## Example Execution

```
User: "запусти тест Home Assistant Agent"

AI: "Starting comprehensive HA Agent test suite..."

🔄 Phase 1: Read-Only Tests (16 tests)
  ✅ test_list_files_root - PASS (85ms)
  ✅ test_list_all_entities - PASS (340ms)
  ✅ test_get_entity_state - PASS (65ms)
  ...
  
📊 Phase 1 Complete: 16/16 passed (2.3s)

🔄 Phase 2: Non-Destructive Writes (7 tests)
  ✅ test_write_and_read_test_file - PASS (145ms)
  ✅ test_git_commit - PASS (220ms)
  ...

📊 Phase 2 Complete: 7/7 passed (1.8s)

🔄 Phase 3: Cleanup (4 tests)
  ✅ test_delete_test_file - PASS (55ms)
  ...

📊 Phase 3 Complete: 4/4 passed (0.4s)

═══════════════════════════════════════
📊 FINAL RESULTS
═══════════════════════════════════════
Total Tests: 27
Passed: 27 (100%)
Failed: 0 (0%)
Skipped: 20 (advanced tests)
Duration: 4.5 seconds

✅ All critical functions working correctly!

Skipped Tests:
- Advanced add-on operations (safe in production)
- HACS operations (not needed)
- System restart tests (not needed)

Recommendation: System healthy, all core functions operational.
```

---

## Test Data

### Safe Test Values
```yaml
# Files
test_file: "test_agent.txt"
test_content: "Test from HA Agent"

# Entities
test_entity: "sun.sun"  # Always exists
climate_domain: "climate"

# Helpers
test_helper_name: "Test Agent Helper"
test_helper_icon: "mdi:test-tube"

# Dashboard
test_dashboard_file: "test-agent-dashboard.yaml"
test_dashboard_title: "Test Dashboard"
```

### Expected Response Patterns
```javascript
// List operations
["item1", "item2", ...]
[{entity_id: "...", state: "..."}, ...]

// Create operations  
{success: true, entity_id: "..."}
"Entity created successfully"

// Read operations
"file content here..."
{state: "on", attributes: {...}}

// Delete operations
{success: true}
"File deleted successfully"
```

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-11  
**Compatible with:** HA Cursor Agent v2.7.7+

