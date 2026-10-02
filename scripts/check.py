"""Check both catalogs, manifest parity, and the packaged skill's provenance."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
plugin = root / "plugins/uptick"
def read(path):
    return json.loads(path.read_text())

codex = read(plugin / ".codex-plugin/plugin.json")
claude = read(plugin / ".claude-plugin/plugin.json")
assert {k: v for k, v in codex.items() if k != "interface"} == claude
assert codex["name"] == plugin.name
for catalog in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
    market = read(root / catalog)
    assert market["name"] == "uptick-systems"
    entry, = market["plugins"]
    assert entry["name"] == plugin.name
    source = entry["source"]
    assert root / (source["path"] if isinstance(source, dict) else source) == plugin
skill = (plugin / "skills/uptick-workspace-audit/SKILL.md").read_bytes()
assert hashlib.sha256(skill).hexdigest() == read(plugin / "source.json")["sha256"]
assert skill.startswith(b"---\nname: uptick-workspace-audit\n")
listing = codex["interface"]
assert listing["privacyPolicyURL"] == "https://www.uptick.systems/privacy"
for key, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80)):
    assert 0 < len(listing[key]) <= limit, key
for key in ("logo", "composerIcon"):
    asset = (plugin / listing[key]).resolve()
    assert asset.is_relative_to(plugin.resolve()), key
    assert asset.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), key
assert len(listing["defaultPrompt"]) <= 3
assert all(0 < len(prompt) <= 128 for prompt in listing["defaultPrompt"])
print("Catalogs, manifests, source checksum, listing limits, and icons passed.")
