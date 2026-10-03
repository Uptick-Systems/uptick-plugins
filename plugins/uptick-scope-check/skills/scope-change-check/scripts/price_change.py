"""Calculate additional-work line totals from explicit quantities and rates."""
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, localcontext


def price_change(data):
    if not isinstance(data, dict) or set(data) != {"currency", "decimal_places", "items"}:
        raise ValueError("Provide currency, decimal_places, and items only.")
    currency, places, items = data["currency"], data["decimal_places"], data["items"]
    if not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency):
        raise ValueError("Currency must be an explicit three-letter code.")
    if type(places) is not int or not 0 <= places <= 4:
        raise ValueError("decimal_places must be an integer from 0 to 4.")
    if not isinstance(items, list) or not 1 <= len(items) <= 100:
        raise ValueError("Provide between 1 and 100 line items.")
    quantum = Decimal(1).scaleb(-places)
    result = []
    for item in items:
        if not isinstance(item, dict) or set(item) != {"description", "quantity", "unit_rate"}:
            raise ValueError("Each item needs description, quantity, and unit_rate only.")
        if not isinstance(item["description"], str) or not item["description"].strip():
            raise ValueError("Each item needs a nonempty description.")
        values = []
        for key in ("quantity", "unit_rate"):
            value = item[key]
            if not isinstance(value, str) or not re.fullmatch(r"[0-9]{1,9}(?:\.[0-9]{1,6})?", value):
                raise ValueError(f"{key} must be a nonnegative decimal string (up to 9 integer and 6 decimal digits).")
            values.append(Decimal(value))
        with localcontext() as context:
            context.prec = 40
            amount = (values[0] * values[1]).quantize(quantum, rounding=ROUND_HALF_UP)
        result.append({**item, "amount": str(amount)})
    total = sum((Decimal(item["amount"]) for item in result), Decimal(0)).quantize(quantum)
    return {"currency": currency, "items": result, "subtotal": str(total),
            "basis": "Each line rounded half-up; excludes tax, discounts, and credits."}


if __name__ == "__main__":
    try:
        if len(sys.argv) > 2:
            raise ValueError("Usage: price_change.py [input.json]")
        if len(sys.argv) == 2:
            with open(sys.argv[1]) as source:
                data = json.load(source)
        else:
            data = json.load(sys.stdin)
        print(json.dumps(price_change(data), indent=2))
    except (ValueError, OSError) as error:
        print(f"Cannot price change: {error}", file=sys.stderr)
        sys.exit(1)
