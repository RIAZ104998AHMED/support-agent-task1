import json
from pathlib import Path


def load_cancel_order_tsv(path: str) -> list[dict]:
    file_path = Path(path)
    lines = file_path.read_text(encoding="utf-8").splitlines()

    rows = []
    for line in lines[1:]:
        if not line.strip():
            continue

        parts = line.split("\t")
        if len(parts) < 5:
            continue

        rows.append(
            {
                "code": parts[0],
                "user_message": parts[1],
                "domain": parts[2],
                "intent": parts[3],
                "reference_response": parts[4],
            }
        )

    return rows


def load_extra_routes(path: str) -> list[dict]:
    file_path = Path(path)
    return json.loads(file_path.read_text(encoding="utf-8"))["tickets"]


def load_all_tickets() -> list[dict]:
    cancel_rows = load_cancel_order_tsv("data/cancel_order_dataset.tsv")
    extra_rows = load_extra_routes("data/extra_routes.json")
    return cancel_rows + extra_rows