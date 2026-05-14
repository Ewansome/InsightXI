# Add Sync: $ARGUMENTS

Wire up a sync workflow in the **orchestrator-service** for an entity that already exists in the sportmonks-service and database-service.

## Naming Conventions

Derive all names from `$ARGUMENTS` (provided as singular lowercase, e.g. "player"):

- **singular**: `$ARGUMENTS` (e.g. `player`)
- **plural**: `${singular}s` (e.g. `players`) - handle irregular plurals if needed (e.g. `country` -> `countries`)
- **PascalCase**: capitalised singular (e.g. `Player`)

## Pre-flight Checks

1. Verify the entity **exists** in both sportmonks-service and database-service by checking for:
   - `services/sportmonks-service/app/controllers/{singular}_controller.py`
   - `services/database-service/app/controllers/{singular}_controller.py`
   If either is missing, abort and tell the user to run `/add-entity {singular}` first.

2. Verify the sync does **not** already exist by checking for `services/orchestrator-service/app/services/{singular}_sync_service.py`. If it exists, abort and inform the user.

## File Modification/Creation Order

Use the existing **league** sync files as the template for every file - match the structure, imports, patterns, and style exactly.

### Template Reference Files

Read ALL of these before generating any code:

- `services/orchestrator-service/app/clients/sportmonks_service_client.py`
- `services/orchestrator-service/app/clients/database_service_client.py`
- `services/orchestrator-service/app/services/league_sync_service.py`
- `services/orchestrator-service/app/controllers/sync_controller.py`
- `services/orchestrator-service/tests/conftest.py`
- `services/orchestrator-service/tests/test_league_sync_service.py`
- `services/orchestrator-service/tests/test_sync_controller.py`
- `Makefile`

### Step 1: SportMonks Service Client

Modify `services/orchestrator-service/app/clients/sportmonks_service_client.py`:

Add two methods to the `SportMonksServiceClient` class, following the exact pattern of the existing `get_leagues`/`get_league` methods:

- `get_{plural}()` - fetches all entities with structured logging (entity="{plural}")
- `get_{singular}({singular}_id: int)` - fetches single entity by ID

Place the new methods maintaining the existing ordering style (grouped by entity).

### Step 2: Database Service Client

Modify `services/orchestrator-service/app/clients/database_service_client.py`:

Add two methods to the `DatabaseServiceClient` class, following the exact pattern of the existing `bulk_upsert_leagues`/`get_leagues` methods:

- `bulk_upsert_{plural}({plural}: list[dict])` - bulk upsert with structured logging (entity="{plural}", operation="bulk_upsert")
- `get_{plural}()` - fetches all entities
- `get_{singular}({singular}_id: int)` - fetches single entity by ID

Place the new methods maintaining the existing ordering style (grouped by entity).

### Step 3: Sync Service

Create `services/orchestrator-service/app/services/{singular}_sync_service.py`

Following the exact pattern of `league_sync_service.py`:

- Import `database_service_client` and `sportmonks_service_client` from their respective client modules
- Import `SyncResult` from `app.models.sync`
- Class `{PascalCase}SyncService` with method `sync_{plural}() -> SyncResult`
- The method must:
  1. Log `sync_started` with entity="{plural}"
  2. Fetch from sportmonks with timing logs (`sportmonks_fetch_started`/`completed`)
  3. Bulk upsert to database with timing logs (`database_upsert_started`/`completed`)
  4. Log `sync_completed` with entity, created, updated, duration
  5. Return `SyncResult(entity="{plural}", created=..., updated=..., status="completed")`
- Module-level singleton: `{singular}_sync_service = {PascalCase}SyncService()`

### Step 4: Sync Controller

Modify `services/orchestrator-service/app/controllers/sync_controller.py`:

- Add import: `from app.services.{singular}_sync_service import {singular}_sync_service`
- Add endpoint following the existing pattern:
  ```python
  @router.post("/{plural}", response_model=SyncResult)
  async def sync_{plural}() -> SyncResult:
      return await {singular}_sync_service.sync_{plural}()
  ```
- Maintain alphabetical order of endpoints

### Step 5: Test Fixtures

Modify `services/orchestrator-service/tests/conftest.py`:

Add a `mock_{plural}` fixture returning a list of 2 dicts with realistic test data for the entity. Follow the exact same pattern as the existing `mock_leagues`/`mock_teams`/`mock_fixtures` fixtures.

### Step 6: Sync Service Tests

Create `services/orchestrator-service/tests/test_{singular}_sync_service.py`

Following the exact pattern of `test_league_sync_service.py`:

- Class `Test{PascalCase}SyncService`
- Fixture for `service` returning `{PascalCase}SyncService()`
- Test `sync_fetches_and_stores_{plural}` that:
  1. Patches `app.services.{singular}_sync_service.sportmonks_service_client`
  2. Patches `app.services.{singular}_sync_service.database_service_client`
  3. Sets up `AsyncMock` for `get_{plural}` and `bulk_upsert_{plural}`
  4. Asserts result entity, created, updated, and status
  5. Asserts both client methods were called correctly

### Step 7: Sync Controller Tests

Modify `services/orchestrator-service/tests/test_sync_controller.py`:

Add a new test class following the exact pattern of `TestSyncLeagues`/`TestSyncFixtures`:

- Class `TestSync{PascalCasePlural}` with three tests:
  1. `test_sync_{plural}_returns_result` - POST to `/sync/{plural}`, assert status 200 and response fields
  2. `test_sync_{plural}_calls_sportmonks_service` - assert `get_{plural}` called once
  3. `test_sync_{plural}_sends_data_to_database_service` - assert `bulk_upsert_{plural}` called with correct data
- All tests patch `app.services.{singular}_sync_service.sportmonks_service_client` and `app.services.{singular}_sync_service.database_service_client`

### Step 8: Makefile

Modify the root `Makefile`:

1. Add `sync-{plural}` to the `.PHONY` declaration (maintain alphabetical position among sync targets)
2. Add a new `sync-{plural}` target following the exact pattern of `sync-leagues`:
   ```makefile
   sync-{plural}:
   	@start=$$(date -u +%Y-%m-%dT%H:%M:%SZ) && \
   	curl -s -X POST $(SERVER_URL)/sync/{plural} | python3 -m json.tool && \
   	podman logs --since "$$start" orchestrator-service
   ```
3. Add `make sync-{plural}` to the `sync` target chain (maintain alphabetical order)

## Verification

After all modifications:

1. Run `cd services/orchestrator-service && make lint` - fix any issues
2. Run `cd services/orchestrator-service && make test` - fix any failures
3. Iterate on lint/test until both pass cleanly
