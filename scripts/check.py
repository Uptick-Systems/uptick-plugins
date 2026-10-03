"""Check catalogs, manifest parity, listing limits, assets, and source provenance."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads(path.read_text())

plugins = {path.name: path for path in (root / "plugins").iterdir() if path.is_dir()}
for catalog in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
    market = read(root / catalog)
    assert market["name"] == "uptick-systems"
    assert len(market["plugins"]) == len(plugins)
    assert {entry["name"] for entry in market["plugins"]} == set(plugins)
    for entry in market["plugins"]:
        source = entry["source"]
        assert root / (source["path"] if isinstance(source, dict) else source) == plugins[entry["name"]]
for plugin in plugins.values():
    codex = read(plugin / ".codex-plugin/plugin.json")
    claude = read(plugin / ".claude-plugin/plugin.json")
    assert {k: v for k, v in codex.items() if k != "interface"} == claude
    assert codex["name"] == plugin.name
    skills = list((plugin / "skills").glob("*/SKILL.md"))
    assert skills
    for skill in skills:
        assert skill.read_text().startswith(f"---\nname: {skill.parent.name}\n")
    listing = codex["interface"]
    for key in ("websiteURL", "privacyPolicyURL", "supportURL"):
        assert listing[key].startswith("https://") and len(listing[key]) <= 1024, key
    if plugin.name == "uptick":
        for field, path in (("websiteURL", "skills/uptick-workspace-audit"), ("privacyPolicyURL", "privacy"), ("supportURL", "support"), ("termsOfServiceURL", "terms")):
            assert listing[field] == f"https://www.uptick.systems/{path}", field
        skill = (plugin / "skills/uptick-workspace-audit/SKILL.md").read_bytes()
        assert hashlib.sha256(skill).hexdigest() == read(plugin / "source.json")["sha256"]
    for key, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80)):
        assert 0 < len(listing[key]) <= limit, key
    for key in ("logo", "composerIcon"):
        asset = (plugin / listing[key]).resolve()
        assert asset.is_relative_to(plugin.resolve()), key
        assert asset.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), key
    assert len(listing["defaultPrompt"]) <= 3
    assert all(0 < len(prompt) <= 128 for prompt in listing["defaultPrompt"])
print("Catalogs, manifests, source checksum, listing limits, and icons passed.")
