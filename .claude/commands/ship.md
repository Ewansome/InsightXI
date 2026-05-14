# Ship

Stage, commit, push, and open a pull request for the current branch.

## Step 1: Pre-flight Checks

1. Run `git branch` to get the current branch name.
   - If on `main`, create a feature branch first using the `{branch-type}/{feature-summary}` format.
2. Run `git status` to check for changes.
   - If the working tree is clean and there are no staged changes and the local branch is up to date with the remote, abort and tell the user there is nothing to ship.
   - If there are changes, then read through the changes and check if any documentation needs to be updated in line with the changes.

## Step 2: Run Linter and Tests

1. Run `make lint` from the project root.
2. Run `make test` from the project root.
3. If either command fails, stop and fix the issues. Re-run both commands until they pass before continuing.

## Step 3: Stage and Commit

1. Run `git diff` and `git status` to understand all staged and unstaged changes.
2. Stage all relevant changed files using specific file paths (do NOT use `git add .` or `git add -A`).
3. Write a one-sentence commit message summarising the changes.
4. Commit the changes.

## Step 4: Push to Remote

1. Push the current branch to origin with the `-u` flag.

## Step 5: Create Pull Request

1. Check if a PR already exists for this branch using `gh pr view`. If one already exists, print the existing PR URL and stop.
2. Use `gh pr create` targeting `main` as the base branch.
3. Derive the PR title from the branch name and commit history (keep under 70 chars).
4. Format the PR body with exactly these sections (never credit claude):
   ```
   ## Overview
   <couple of sentences summarising the implemented functionality>

   ## Changes
   <bullet point list of changes>
   ```
