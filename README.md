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

Version 1.0.2 packages the upgraded skill from PR #540 at revision `ae5afd1852dfbc7a601f45b11744e33d730695bd`. The skill is copied unchanged. `plugins/uptick/source.json` records its SHA-256 checksum. This plugin release is independent of the website release.

## Validate

```sh
python3 scripts/check.py
claude plugin validate .
```

For an update, replace the skill, update its source record, increment the version in both plugin manifests, and rerun validation and an installation check before publishing.

## OpenAI directory submission

Download `uptick-1.0.2.zip` from the GitHub release, then upload it at https://platform.openai.com/plugins using Uptick's verified developer identity. Use the release asset, not GitHub's automatic source-code ZIP, which contains the marketplace repository.

The package contains the listing copy, logo, composer icon, and skill. Resolve the portal's metadata and skill-scan findings, then submit for review. After approval, select Publish plugin. GitHub publication does not submit to the OpenAI directory.

The local checks validate packaging and listing limits. They do not replace OpenAI's scans or a full audit-quality evaluation.
