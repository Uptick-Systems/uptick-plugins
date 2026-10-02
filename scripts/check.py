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
print("Catalogs, manifests, and source checksum passed.")
