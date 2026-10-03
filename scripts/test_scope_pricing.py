"""Run with python3 scripts/test_scope_pricing.py."""
import copy
import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "plugins/uptick-scope-check/skills/scope-change-check/scripts/price_change.py"
spec = importlib.util.spec_from_file_location("price_change", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
quote = {"currency": "CAD", "decimal_places": 2, "items": [
    {"description": "Extra page", "quantity": "3.5", "unit_rate": "120.00"},
    {"description": "Additional review", "quantity": "1", "unit_rate": "10.005"},
    {"description": "Additional review", "quantity": "1", "unit_rate": "10.005"},
]}
original = copy.deepcopy(quote)
assert module.price_change(quote)["subtotal"] == "440.02"
assert quote == original
assert module.price_change({**quote, "currency": "JPY", "decimal_places": 0})["subtotal"] == "440"
assert module.price_change({"currency": "CAD", "decimal_places": 4, "items": [
    {"description": "Precision boundary", "quantity": "999999999.999999", "unit_rate": "999999999.999999"}
]})["subtotal"] == "999999999999998000.0000"
for invalid in ("NaN", "Infinity", "-1", "1e3", "1,000", "", 1.2, True, "1000000000"):
    bad = copy.deepcopy(quote)
    bad["items"][0]["quantity"] = invalid
    try:
        module.price_change(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"Accepted invalid quantity: {invalid!r}")
for bad in ({**quote, "decimal_places": True}, {**quote, "items": []}, {**quote, "tax": "5"}, {**quote, "currency": "$"}):
    try:
        module.price_change(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"Accepted malformed quote: {bad!r}")
print("Scope pricing: decimal rounding, input validation, and no mutation passed.")
