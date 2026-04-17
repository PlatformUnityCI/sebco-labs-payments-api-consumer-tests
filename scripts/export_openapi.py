import json
from pathlib import Path
from lib_core.utils.app.main import app

output_dir = Path("docs/swagger")
output_dir.mkdir(parents=True, exist_ok=True)

with open(output_dir / "openapi.json", "w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2)

print("OpenAPI exported to docs/swagger/openapi.json")