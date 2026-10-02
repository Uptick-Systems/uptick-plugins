# Uptick plugins

Evidence-backed improvements for the way you work with AI.

## Install in Codex

```sh
codex plugin marketplace add Uptick-Systems/uptick-plugins
codex plugin add uptick@uptick-systems
```

Start a new Codex thread and ask: "Use the Uptick workspace audit skill. Do not edit files. Show evidence and proposed changes."

## Install in Claude Code

```sh
claude plugin marketplace add Uptick-Systems/uptick-plugins
claude plugin install uptick@uptick-systems
```

Start a new session and run `/uptick:uptick-workspace-audit`.

## What it does

The workspace audit inspects instructions, skills, workflows, and operating evidence. It returns ranked opportunities, confidence levels, proposed instruction diffs, a seven-day action plan, and ways to measure progress.

The audit is read-only. It does not change files or send workspace contents to Uptick. Your AI tool processes inspected content under that tool's own settings and terms. No Uptick account or API key is required.

## Release source

Version 1.0.0 packages the upgraded skill from PR #540 at revision `ae5afd1852dfbc7a601f45b11744e33d730695bd`. The skill is copied unchanged. `plugins/uptick/source.json` records its SHA-256 checksum. This plugin release is independent of the website release.

## Validate

```sh
python3 scripts/check.py
claude plugin validate .
```

For an update, replace the skill, update its source record, increment the version in both plugin manifests, and rerun validation and an installation check before publishing.
