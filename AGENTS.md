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

If conflicts occur outside `.agents/plugins/marketplace.json`,
`.agents/plugins/api_marketplace.json`, or localized plugin manifests listed in
`.agents/plugins/local-overrides.zh-CN.json`, the workflow aborts and requires
manual resolution. For conflicts in those local override files, it keeps the
official plugin list or manifest updates while restoring local values afterward.

## Local Chinese Metadata

Do not directly edit upstream-owned plugin descriptions when localizing the
marketplace UI. Put local Chinese metadata in:

```text
.agents/plugins/local-overrides.zh-CN.json
```

Then apply it with:

```bash
python3 .agents/plugins/apply-local-overrides.py
```

The override file supports marketplace root metadata and per-plugin manifest
overrides. Per-plugin overrides are keyed by plugin name and merge into:

```text
plugins/<plugin-name>/.codex-plugin/plugin.json
```

Use this shape for Chinese marketplace descriptions:

```json
{
  "plugins": {
    "linear": {
      "description": "查找并引用 Linear 议题和项目。",
      "interface": {
        "shortDescription": "查找并引用 Linear 议题和项目。",
        "longDescription": "在 Codex 中管理 Linear 的议题、项目和团队工作流。"
      }
    }
  }
}
```

The scheduled sync workflow runs the override script after merging upstream, so
official plugin list changes can still be synced while local Chinese
descriptions are restored afterward.
