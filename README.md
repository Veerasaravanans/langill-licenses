# Langill Licenses

Private license database for Langill Agent Kernel distribution.

## Structure

- `licenses.json` — License key database (keys, device bindings, status)
- `versions.json` — Version metadata for update checks
- `admin/cli.py` — Admin CLI for key management
- `admin/web/index.html` — Admin web dashboard

## Usage

### Admin CLI
```bash
python admin/cli.py generate-key --label "user-name"
python admin/cli.py list-keys
python admin/cli.py revoke-key LGL-XXXX-XXXX-XXXX
python admin/cli.py unbind-key LGL-XXXX-XXXX-XXXX
```

### Web Dashboard
Open `admin/web/index.html` in a browser. Requires a GitHub PAT with repo scope.
