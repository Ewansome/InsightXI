# Add Entity E2E: $ARGUMENTS

Scaffold a new entity across all three services, wire up sync, then ship it — all in one go.

## Step 1: Create Feature Branch

1. Run `git branch` to check the current branch.
2. If already on a branch named `feature/$ARGUMENTS-entity-and-sync`, continue to Step 2.
3. If on any other branch, run `git checkout -b feature/$ARGUMENTS-entity-and-sync`.

## Step 2: Add Entity

Read `.claude/commands/add-entity.md` and follow every instruction in it, using `$ARGUMENTS` as the entity name.

## Step 3: Add Sync

Read `.claude/commands/add-sync.md` and follow every instruction in it, using `$ARGUMENTS` as the entity name.

## Step 4: Ship

Read `.claude/commands/ship.md` and follow every instruction in it.
