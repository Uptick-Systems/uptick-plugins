# Uptick Scope Check

Turn a new client request into a clear scope decision, a proposed change order, and a reply you can review before sending.

## Install

Codex:

```sh
codex plugin marketplace add Uptick-Systems/uptick-plugins
codex plugin marketplace upgrade uptick-systems
codex plugin add uptick-scope-check@uptick-systems
```

Claude Code:

```sh
claude plugin marketplace add Uptick-Systems/uptick-plugins
claude plugin marketplace update uptick-systems
claude plugin install uptick-scope-check@uptick-systems
```

If the marketplace is already configured, skip the add command. Start a new session after installation. In Claude Code, invoke `/uptick-scope-check:scope-change-check`; in Codex, ask to use Scope Change Check.

## Try it

Provide the agreed statement of work, any approved amendments, and the new request. Include a rate card or effort estimate only when you want pricing.

> Compare this client request with our agreed scope. Show what is included, what needs correcting, what changes, and what needs clarification. Draft a change order and a client reply. Do not send anything.

For example, a client might request another revision round, a translated landing page, and a fix to a form that does not meet acceptance criteria. The plugin checks each separately instead of treating the whole request as extra work. An approved amendment controls over an unapproved newer draft.

The output includes source references, unresolved questions, and separate internal analysis and client-facing drafts. Missing rates, quantities, approvals, and dates stay unresolved. A bundled Python calculator verifies additional-work pricing when your AI tool supports execution. It excludes taxes, discounts, and credits.

## Access and limitations

The plugin has no service, account, API key, or telemetry. It reads material you provide through your AI tool. Your AI provider processes that material under its own settings and policies. No documents are sent to Uptick by the plugin. Do not include unnecessary sensitive information.

It does not monitor your inbox, send messages, approve charges, change agreements, or update project systems. It offers operational analysis, not a legal opinion or a guarantee of the interpretation. Review proposed terms, amounts, and delivery commitments before using them.

## Verification and publication

Run `python3 scripts/check.py` and `python3 scripts/test_scope_pricing.py` from the repository root. Skill behavior is also evaluated against a fictional project with approved and unapproved amendments, defects, extra revisions, ambiguous requirements, and an embedded malicious instruction.

This release is distributed through GitHub for Codex and Claude Code. It has not been submitted to OpenAI's directory. The website's existing terms describe a different product; Scope Check needs applicable published terms before directory submission. The local legacy manifest validator also lacks the currently documented `supportURL` field.

Get help through [GitHub issues](https://github.com/Uptick-Systems/uptick-plugins/issues). Avoid posting private client documents in a public issue.
