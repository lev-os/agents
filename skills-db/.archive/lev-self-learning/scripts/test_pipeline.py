#!/usr/bin/env python3
"""
Integration test for the passive scanning pipeline.

Creates mock session data and validates that all scanner types detect patterns correctly.

Usage:
    python test_pipeline.py
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List


# Mock session messages with patterns for each scanner type
MOCK_MESSAGES = [
    # Message 1: Synth declaration
    {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I've completed the analysis task.\n\n---\n🆔 **Session:** test-123 | 📋 executing | 🏷️ [test]\n\n**Queued:** [ ] None\n**Confirmed:** [x] Analysis complete\n\n🪄 **Next:**\n1. Review results\n\nsynths: [\"test-synth\"]\n---\n🧙🏽‍♂️ **[ROOT@KINGLY]** test-project | ⚡ COMPLETE\n---"
                }
            ]
        },
        "type": "message"
    },

    # Message 2: First tool call in workflow sequence
    {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "tool_1",
                    "name": "Read",
                    "input": {"file_path": "/test/file.py"}
                }
            ]
        },
        "type": "message"
    },

    # Message 3: Second tool call in workflow sequence
    {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "tool_2",
                    "name": "Edit",
                    "input": {"file_path": "/test/file.py", "old_string": "old", "new_string": "new"}
                }
            ]
        },
        "type": "message"
    },

    # Message 4: Third tool call in workflow sequence
    {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "tool_3",
                    "name": "Bash",
                    "input": {"command": "pytest /test/file.py"}
                }
            ]
        },
        "type": "message"
    },

    # Message 5: Skill indicator (needs 2+ indicators from different pattern groups)
    {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "This pattern is reusable for testing. Every time we make changes, we should always do these steps. Let's create a skill called 'test-automation' to capture this abstraction."
                }
            ]
        },
        "type": "message"
    },

    # Message 6: Documentation issue
    {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I noticed the README.md has outdated documentation about the setup process. The current steps don't match the actual requirements."
                }
            ]
        },
        "type": "message"
    },

    # Message 7: Memory candidate
    {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I learned that the test suite requires the virtual environment to be activated before running pytest. This is an important procedural step that should be remembered for future test executions."
                }
            ]
        },
        "type": "message"
    }
]


def create_mock_session(session_dir: Path) -> Path:
    """Create a mock session JSONL file with test messages."""
    session_file = session_dir / "test_session_001.jsonl"

    with open(session_file, 'w') as f:
        for msg in MOCK_MESSAGES:
            f.write(json.dumps(msg) + '\n')

    print(f"✓ Created mock session: {session_file}")
    return session_file


def run_scanner(session_dir: Path) -> List[Dict]:
    """Run scanner_framework.py and collect results."""
    script_path = Path(__file__).parent / "scanner_framework.py"

    cmd = [
        sys.executable,
        str(script_path),
        "--type", "all",
        "--session-dir", str(session_dir),
        "--output", "jsonl"
    ]

    print(f"✓ Running scanner: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"✗ Scanner failed with return code {result.returncode}")
        print(f"STDERR: {result.stderr}")
        return []

    # Parse JSONL output
    results = []
    for line in result.stdout.strip().split('\n'):
        if line:
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    print(f"✓ Scanner produced {len(results)} results")
    return results


def validate_results(results: List[Dict]) -> Dict[str, bool]:
    """Validate that expected patterns were detected."""
    validation = {
        "synth": False,
        "workflow": False,
        "skill": False,
        "doc": False,
        "memory": False
    }

    for result in results:
        scanner_type = result.get("scanner_type")
        if scanner_type in validation:
            validation[scanner_type] = True

    return validation


def print_summary(validation: Dict[str, bool], results: List[Dict]) -> bool:
    """Print test summary and return overall pass/fail."""
    print("\n" + "="*60)
    print("INTEGRATION TEST SUMMARY")
    print("="*60 + "\n")

    all_passed = True

    for scanner_type, passed in validation.items():
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {scanner_type.upper()}: {status}")

        if passed:
            # Show detected entities
            matching = [r for r in results if r.get("scanner_type") == scanner_type]
            for r in matching:
                print(f"    → {r.get('name')} (confidence: {r.get('confidence'):.2f})")
        else:
            all_passed = False

    print("\n" + "="*60)
    print(f"Overall: {'PASS ✓' if all_passed else 'FAIL ✗'}")
    print(f"Total detections: {len(results)}")
    print("="*60 + "\n")

    return all_passed


def main():
    """Run integration test pipeline."""
    print("\n🧪 PASSIVE SCANNING PIPELINE INTEGRATION TEST\n")

    # Create temporary directory for test session
    with tempfile.TemporaryDirectory() as tmpdir:
        session_dir = Path(tmpdir)

        # Step 1: Create mock session
        print("Step 1: Creating mock session data...")
        session_file = create_mock_session(session_dir)

        # Step 2: Run scanner
        print("\nStep 2: Running scanner framework...")
        results = run_scanner(session_dir)

        if not results:
            print("\n✗ FAIL: No results produced by scanner")
            return 1

        # Step 3: Validate results
        print("\nStep 3: Validating scanner output...")
        validation = validate_results(results)

        # Step 4: Print summary
        all_passed = print_summary(validation, results)

        return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
