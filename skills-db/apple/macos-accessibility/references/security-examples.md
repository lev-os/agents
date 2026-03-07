# macOS Accessibility - Security Examples

## 5.1 Vulnerability Landscape (2022-2025)

### CVE-2023-32364 - TCC Bypass via Symlinks
**Severity**: CRITICAL (CVSS 9.1)
**Mitigation**: Resolve symbolic links before path validation

### CVE-2023-28206 - IOSurfaceAccelerator Privilege Escalation
**Severity**: HIGH (CVSS 8.6)
**Mitigation**: Keep macOS updated, validate process tokens

### CVE-2022-42796 - Hardened Runtime Bypass
**Severity**: MEDIUM (CVSS 5.5)
**Mitigation**: Verify target app hardened runtime status

## Input Validation

```python
import re

def validate_bundle_id(bundle_id: str) -> bool:
    """Validate bundle identifier format."""
    pattern = r'^[a-zA-Z][a-zA-Z0-9-]*(\.[a-zA-Z][a-zA-Z0-9-]*)+$'
    return bool(re.match(pattern, bundle_id)) and len(bundle_id) <= 255

def sanitize_ax_value(value: str) -> str:
    """Sanitize accessibility attribute value."""
    if not value:
        return ''
    return value[:10000].replace('\x00', '')
```

## Audit Logging

```python
import json
import logging

class AXAuditLogger:
    """Audit logging for accessibility operations."""

    def log_operation(self, operation: str, bundle_id: str, element: str, success: bool):
        record = {
            'timestamp': datetime.utcnow().isoformat(),
            'event': 'ax_operation',
            'operation': operation,
            'bundle_id': bundle_id,
            'element': element,
            'success': success
        }
        logging.getLogger('ax.audit').info(json.dumps(record))

    def log_tcc_check(self, granted: bool):
        record = {
            'timestamp': datetime.utcnow().isoformat(),
            'event': 'tcc_check',
            'permission': 'kTCCServiceAccessibility',
            'granted': granted
        }
        logging.getLogger('ax.audit').info(json.dumps(record))
```

## Code Signature Verification

```python
import subprocess

def verify_code_signature(app_path: str) -> dict:
    """Verify macOS code signature."""
    result = subprocess.run(
        ['codesign', '-dv', '--verbose=4', app_path],
        capture_output=True,
        text=True
    )

    info = {
        'valid': result.returncode == 0,
        'path': app_path,
    }

    if result.returncode == 0:
        # Parse signature info
        for line in result.stderr.split('\n'):
            if 'TeamIdentifier=' in line:
                info['team_id'] = line.split('=')[1]
            elif 'Authority=' in line:
                info['authority'] = line.split('=')[1]

    return info
```

## TCC Database Query (Diagnostic Only)

```python
import sqlite3

def query_tcc_permissions(bundle_id: str) -> list:
    """Query TCC database for diagnostic purposes.
    Note: Requires Full Disk Access or SIP disabled.
    """
    tcc_db = '/Library/Application Support/com.apple.TCC/TCC.db'

    try:
        conn = sqlite3.connect(tcc_db)
        cursor = conn.execute('''
            SELECT service, client, auth_value
            FROM access
            WHERE client = ?
        ''', (bundle_id,))

        return [
            {'service': row[0], 'client': row[1], 'granted': row[2] == 2}
            for row in cursor.fetchall()
        ]
    except Exception as e:
        return []
```
