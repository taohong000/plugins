# Repository Instructions

This repository is a local fork of the official OpenAI plugins marketplace:

https://github.com/openai/plugins

The user's fork remote is expected to be `origin`. The official repository should
be configured as `upstream` when syncing official updates.

## Upstream Sync

Before syncing, check the working tree:

```bash
git status --short
```

If `upstream` is not configured, add it:

```bash
git remote add upstream https://github.com/openai/plugins.git
```

Fetch and merge official updates:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

After resolving any conflicts, push the updated fork:

```bash
git push origin main
```

## Local Marketplace Identity

The marketplace names are intentionally different from the official OpenAI
marketplace to avoid collisions in Codex. Preserve these local values during
upstream syncs, even if the official repository changes the same files.

- `.agents/plugins/marketplace.json`
  - `name`: `hongtao-curated`
  - `interface.displayName`: `Hongtao curated`
- `.agents/plugins/api_marketplace.json`
  - `name`: `hongtao-api-curated`
  - `interface.displayName`: `Hongtao API curated`

When merge conflicts occur in these marketplace files, prefer official changes
for plugin list updates, but keep the local `name` and `interface.displayName`
values above.

## Scheduled Sync

The repository includes `.github/workflows/sync-upstream.yml` to sync from
`https://github.com/openai/plugins` every day at 18:15 UTC, which is 02:15 in
Asia/Shanghai.

The workflow can also be started manually from GitHub Actions with
`workflow_dispatch`. It merges `upstream/main`, preserves the local marketplace
identity values listed above, commits any changes, and pushes them to `main`.

If conflicts occur outside `.agents/plugins/marketplace.json` or
`.agents/plugins/api_marketplace.json`, the workflow aborts and requires manual
resolution. For conflicts in those two marketplace files, it keeps the official
plugin list updates while restoring the local marketplace `name` and
`interface.displayName` values.
