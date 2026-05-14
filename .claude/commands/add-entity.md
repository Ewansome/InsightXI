# Add Entity: $ARGUMENTS

Scaffold a new entity across the **sportmonks-service** and **database-service**.

## Naming Conventions

Derive all names from `$ARGUMENTS` (provided as singular lowercase, e.g. "player"):

- **singular**: `$ARGUMENTS` (e.g. `player`)
- **plural**: `${singular}s` (e.g. `players`) - handle irregular plurals if needed (e.g. `country` -> `countries`)
- **PascalCase**: capitalised singular (e.g. `Player`)
- **PascalCasePlural**: capitalised plural (e.g. `Players`)

## Pre-flight Checks

1. Verify the entity does not already exist by checking for `services/sportmonks-service/app/models/{singular}.py` and `services/database-service/app/models/{singular}.py`. If either exists, abort and inform the user.
2. Look up the SportMonks Football API documentation or ask the user for the entity's field names and types. Confirm the field list with the user before proceeding.

## File Creation Order

Create files in this exact order. Use the existing **league** files as the template for every file - match the structure, imports, patterns, and style exactly.

### Template Reference Files

Read ALL of these before generating any code:

- `services/sportmonks-service/app/models/league.py`
- `services/sportmonks-service/app/services/league_service.py`
- `services/sportmonks-service/app/controllers/league_controller.py`
- `services/sportmonks-service/app/main.py`
- `services/sportmonks-service/tests/conftest.py`
- `services/sportmonks-service/tests/test_league_service.py`
- `services/sportmonks-service/tests/test_league_controller.py`
- `services/database-service/app/models/league.py`
- `services/database-service/app/schemas/league.py`
- `services/database-service/app/repositories/league_repository.py`
- `services/database-service/app/services/league_service.py`
- `services/database-service/app/controllers/league_controller.py`
- `services/database-service/app/main.py`
- `services/database-service/tests/conftest.py`
- `services/database-service/tests/test_league_controller.py`

### Step 1: SportMonks Service - Pydantic Model

Create `services/sportmonks-service/app/models/{singular}.py`

Following the pattern in `league.py`:
- Define a `{PascalCase}` Pydantic `BaseModel` with the confirmed fields
- Define a `{PascalCase}Response` model with `data: list[{PascalCase}]`

### Step 2: SportMonks Service - Service

Create `services/sportmonks-service/app/services/{singular}_service.py`

Following the pattern in `league_service.py`:
- Class `{PascalCase}Service` with `url_suffix = "football/{plural}"`
- Method `get_all_{plural}()` using `sportmonks_client.get_all_pages()` with structured logging
- Method `get_{singular}_by_id({singular}_id: int)` using `sportmonks_client.get()`
- Module-level singleton: `{singular}_service = {PascalCase}Service()`

### Step 3: SportMonks Service - Controller

Create `services/sportmonks-service/app/controllers/{singular}_controller.py`

Following the pattern in `league_controller.py`:
- `router = APIRouter(prefix="/{plural}", tags=["{plural}"])`
- GET `""` -> `get_{plural}()` returning `list[{PascalCase}]`
- GET `"/{{{singular}_id}}"` -> `get_{singular}({singular}_id: int)` returning `{PascalCase}`

### Step 4: SportMonks Service - Register Router

Modify `services/sportmonks-service/app/main.py`:
- Add `{singular}_controller` to the import from `app.controllers`
- Add `app.include_router({singular}_controller.router)` (maintain alphabetical order)

### Step 5: Database Service - SQLAlchemy Model

Create `services/database-service/app/models/{singular}.py`

Following the pattern in `league.py`:
- Class `{PascalCase}DB(Base)` with `__tablename__ = "{plural}"`
- Use `mapped_column` with appropriate SQLAlchemy types (`Integer`, `String(n)`, `Boolean`, etc.)
- Match the fields from the Pydantic model, using appropriate column types and nullable settings

### Step 6: Database Service - Pydantic Schemas

Create `services/database-service/app/schemas/{singular}.py`

Following the pattern in `league.py`:
- `{PascalCase}Base(BaseModel)` - all fields with defaults for optional ones
- `{PascalCase}Create({PascalCase}Base)` - pass
- `{PascalCase}Response({PascalCase}Base)` - with `model_config = {"from_attributes": True}`
- `BulkCreateResponse(BaseModel)` - with `created: int` and `updated: int`

### Step 7: Database Service - Repository

Create `services/database-service/app/repositories/{singular}_repository.py`

Following the pattern in `league_repository.py`:
- Class `{PascalCase}Repository` with `__init__(self, db: Session)`
- Methods: `get_all()`, `get_by_id({singular}_id)`, `create({singular})`, `bulk_upsert({plural})`, `delete({singular}_id)`
- `bulk_upsert` must include structured logging with entity name, timing, and created/updated counts

### Step 8: Database Service - Service

Create `services/database-service/app/services/{singular}_service.py`

Following the pattern in `league_service.py`:
- Class `{PascalCase}Service` taking `repository: {PascalCase}Repository`
- Methods: `get_all_{plural}()`, `get_{singular}_by_id()`, `create_{singular}()`, `bulk_upsert_{plural}()`, `delete_{singular}()`
- Raise `HTTPException(404)` for not found, `HTTPException(409)` for duplicate create

### Step 9: Database Service - Controller

Create `services/database-service/app/controllers/{singular}_controller.py`

Following the pattern in `league_controller.py`:
- `router = APIRouter(prefix="/{plural}", tags=["{plural}"])`
- Factory function `get_{singular}_service(db: Session = Depends(get_db))` with DI
- Endpoints: GET `""`, GET `"/{{{singular}_id}}"`, POST `""` (201), POST `"/bulk"`, DELETE `"/{{{singular}_id}}"` (204)

### Step 10: Database Service - Register Router & Model

Modify `services/database-service/app/main.py`:
- Add `{singular}_controller` to the import from `app.controllers`
- Add `from app.models import {singular}` inside the `lifespan` function (with `# noqa: F401` comment), maintaining alphabetical order
- Add `app.include_router({singular}_controller.router)` (maintain alphabetical order)

### Step 11: SportMonks Service - Test Fixtures

Modify `services/sportmonks-service/tests/conftest.py`:
- Add a `mock_{singular}_data` fixture returning a dict with realistic test data for the entity
- Add a `mock_{plural}_response` fixture returning `[mock_{singular}_data]`
- Add a `mock_{singular}_response` fixture returning `{"data": mock_{singular}_data}`
- Follow the exact same pattern as the existing league/team/fixture fixtures

### Step 12: SportMonks Service - Service Tests

Create `services/sportmonks-service/tests/test_{singular}_service.py`

Following the pattern in `test_league_service.py`:
- Class `Test{PascalCase}Service`
- Fixture for `service` returning `{PascalCase}Service()`
- Test `get_all_{plural}` with patched `sportmonks_client.get_all_pages`
- Test `get_{singular}_by_id` with patched `sportmonks_client.get`
- Both tests should assert on ID and name fields from mock data

### Step 13: SportMonks Service - Controller Tests

Create `services/sportmonks-service/tests/test_{singular}_controller.py`

Following the pattern in `test_league_controller.py`:
- Class `TestGet{PascalCasePlural}` - test list endpoint returns data, test correct endpoint called
- Class `TestGet{PascalCase}ById` - test single entity return, test correct endpoint called
- All tests patch `app.services.{singular}_service.sportmonks_client`

### Step 14: Database Service - Test Fixtures

Modify `services/database-service/tests/conftest.py`:
- Add a `mock_{singular}_data` fixture returning a dict with realistic test data
- Follow the exact same pattern as existing league/team/fixture fixtures

### Step 15: Database Service - Controller Tests

Create `services/database-service/tests/test_{singular}_controller.py`

Following the pattern in `test_league_controller.py`:
- Class `TestGet{PascalCasePlural}` - empty list and populated list tests
- Class `TestGet{PascalCase}ById` - found and 404 tests
- Class `TestCreate{PascalCase}` - create and 409 duplicate tests
- Class `TestBulkUpsert{PascalCasePlural}` - create multiple and update existing tests
- Class `TestDelete{PascalCase}` - delete existing and 404 tests
- All tests use the `client` and `mock_{singular}_data` fixtures from conftest

## Verification

After creating all files:

1. Run `cd services/sportmonks-service && make lint` - fix any issues
2. Run `cd services/sportmonks-service && make test` - fix any failures
3. Run `cd services/database-service && make lint` - fix any issues
4. Run `cd services/database-service && make test` - fix any failures
5. Iterate on lint/test until both pass cleanly
