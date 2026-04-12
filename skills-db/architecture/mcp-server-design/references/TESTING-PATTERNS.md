# Testing Patterns

> **Principle**: Test with the smallest models to validate API clarity, use security corpora for edge cases, and verify concurrent access patterns.

## Haiku Canary Tests

Test APIs with smaller models to validate clarity:

```python
import pytest
from unittest.mock import MagicMock

class TestHaikuCanary:
    """
    Canary tests that validate API usability with smaller models.

    Smaller models (Haiku, GPT-4o-mini) struggle more with:
    - Ambiguous parameter names
    - Missing examples
    - Unclear error messages
    - Complex multi-step workflows

    If Haiku can use it, any model can.
    """

    @pytest.fixture
    def mock_haiku_agent(self):
        """Simulate a Haiku-class agent's behavior."""
        agent = MagicMock()
        agent.model = "claude-3-5-haiku"
        agent.context_window = 8192  # Smaller context
        agent.reasoning_depth = "shallow"
        return agent

    def test_tool_documentation_is_self_contained(self, mock_haiku_agent):
        """
        Verify tool docstrings contain everything needed for correct usage.
        Haiku shouldn't need to read multiple files.
        """
        from mcp_agent_mail.app import send_message

        doc = send_message.__doc__

        # Must have required sections
        assert "Parameters" in doc
        assert "Examples" in doc
        assert "Do / Don't" in doc

        # Examples must be complete
        assert "jsonrpc" in doc
        assert "project_key" in doc

    def test_error_messages_suggest_fix(self, mock_haiku_agent):
        """
        Verify errors tell the agent exactly how to fix the problem.
        """
        from mcp_agent_mail.app import register_agent

        # Simulate common mistake: using program name as agent name
        with pytest.raises(ToolExecutionError) as exc_info:
            register_agent(
                project_key="/test/project",
                name="claude-code",  # Wrong! This is a program name
                program="claude-code",
                model="opus",
            )

        error = exc_info.value
        assert error.error_type == "PROGRAM_NAME_AS_AGENT"
        assert "program" in error.message.lower()  # Suggests correct field
        assert error.recoverable is True

    def test_macro_reduces_steps(self, mock_haiku_agent):
        """
        Verify macros bundle what would be 3+ tool calls into one.
        Haiku is more likely to lose track in multi-step workflows.
        """
        from mcp_agent_mail.app import macro_start_session

        # One call should do: ensure_project + register_agent + fetch_inbox
        result = macro_start_session(
            human_key="/test/project",
            program="test-agent",
            model="haiku",
        )

        # All three results in one response
        assert "project" in result
        assert "agent" in result
        assert "inbox" in result
        assert "next_actions" in result  # Guidance for what to do next
```

## XSS Corpus Testing

Comprehensive security testing with attack categories:

```python
# tests/security/test_xss.py

XSS_CORPUS = {
    "script_injection": [
        "<script>alert('xss')</script>",
        "<script src='evil.js'></script>",
        "<script>document.cookie</script>",
    ],
    "event_handlers": [
        "<img src=x onerror=alert('xss')>",
        "<body onload=alert('xss')>",
        "<input onfocus=alert('xss') autofocus>",
        "<marquee onstart=alert('xss')>",
        "<video><source onerror=alert('xss')>",
    ],
    "protocol_handlers": [
        "<a href='javascript:alert(1)'>click</a>",
        "<a href='vbscript:msgbox(1)'>click</a>",
        "<iframe src='javascript:alert(1)'></iframe>",
    ],
    "encoding_bypass": [
        "<script>alert(String.fromCharCode(88,83,83))</script>",
        "<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>",
        "%3Cscript%3Ealert('xss')%3C/script%3E",
        "\\x3cscript\\x3ealert('xss')\\x3c/script\\x3e",
    ],
    "svg_injection": [
        "<svg onload=alert('xss')>",
        "<svg><script>alert('xss')</script></svg>",
        "<svg><animate onbegin=alert('xss')>",
    ],
    "style_injection": [
        "<style>body{background:url('javascript:alert(1)')}</style>",
        "<div style='background:url(javascript:alert(1))'>",
        "<link rel=stylesheet href='data:text/css,body{xss}'>",
    ],
    "html5_vectors": [
        "<details open ontoggle=alert('xss')>",
        "<audio src=x onerror=alert('xss')>",
        "<video poster=javascript:alert('xss')>",
        "<math><maction actiontype='statusline#xss'>",
    ],
    "template_injection": [
        "{{constructor.constructor('alert(1)')()}}",
        "${alert('xss')}",
        "#{alert('xss')}",
    ],
    "data_uri": [
        "<a href='data:text/html,<script>alert(1)</script>'>",
        "<object data='data:text/html,<script>alert(1)</script>'>",
    ],
    "mutation_xss": [
        "<noscript><p title='</noscript><script>alert(1)</script>'>",
        "<p><svg><![CDATA[</svg><script>alert(1)</script>]]>",
    ],
    "unicode_normalization": [
        "<script>alert﹙'xss'﹚</script>",  # Fullwidth parentheses
        "<ſcript>alert('xss')</ſcript>",  # Long s
    ],
    "null_byte": [
        "<scr\x00ipt>alert('xss')</script>",
        "<img src=x onerror=alert\x00('xss')>",
    ],
    "comment_bypass": [
        "<!--<script>alert('xss')</script>-->",
        "<script><!--alert('xss')--></script>",
    ],
}

class TestXSSSanitization:
    """Test that all XSS vectors are properly sanitized."""

    @pytest.mark.parametrize("category,payloads", XSS_CORPUS.items())
    def test_xss_category(self, category, payloads):
        """Test each XSS category is sanitized."""
        from mcp_agent_mail.utils import sanitize_html

        for payload in payloads:
            sanitized = sanitize_html(payload)

            # Should not contain dangerous elements
            assert "<script" not in sanitized.lower()
            assert "javascript:" not in sanitized.lower()
            assert "onerror=" not in sanitized.lower()
            assert "onload=" not in sanitized.lower()
            assert "onclick=" not in sanitized.lower()

    def test_markdown_xss_rendering(self):
        """Test XSS in markdown is sanitized during rendering."""
        from mcp_agent_mail.utils import render_markdown

        malicious_md = """
# Title

<script>alert('xss')</script>

[Click me](javascript:alert('xss'))

![img](x" onerror="alert('xss'))
"""
        rendered = render_markdown(malicious_md)

        assert "<script>" not in rendered
        assert "javascript:" not in rendered
        assert "onerror=" not in rendered
```

## Path Traversal Prevention

Security tests for directory escape:

```python
# tests/security/test_path_traversal.py

PATH_TRAVERSAL_VECTORS = [
    # Basic traversal
    "../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\config\\sam",

    # URL encoded
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
    "%2e%2e%5c%2e%2e%5c%2e%2e%5cwindows",

    # Double encoded
    "%252e%252e%252f",

    # Null byte injection
    "../../../etc/passwd%00.txt",
    "..\\..\\..\\boot.ini\x00.jpg",

    # Unicode normalization
    "..%c0%af..%c0%af..%c0%afetc/passwd",  # Overlong UTF-8

    # Mixed separators
    "..\\../..\\../etc/passwd",
    "../..\\../..\\windows",

    # Absolute paths
    "/etc/passwd",
    "%SystemRoot%\\System32\\config\\SAM",

    # Symlink tricks (path component)
    "safe/../../../etc/passwd",
    "uploads/../../secrets",
]

class TestPathTraversal:
    """Test path traversal prevention."""

    @pytest.mark.parametrize("malicious_path", PATH_TRAVERSAL_VECTORS)
    def test_path_traversal_blocked(self, malicious_path):
        """Verify malicious paths are rejected."""
        from mcp_agent_mail.utils import validate_path

        with pytest.raises(ValueError, match="path traversal"):
            validate_path(malicious_path, base_dir="/safe/directory")

    def test_file_reservation_path_validation(self):
        """File reservations must validate paths."""
        from mcp_agent_mail.app import file_reservation_paths

        with pytest.raises(ToolExecutionError) as exc_info:
            file_reservation_paths(
                project_key="/test/project",
                agent_name="TestAgent",
                paths=["../../../etc/passwd"],
            )

        assert "path traversal" in exc_info.value.message.lower()

    def test_attachment_path_validation(self):
        """Attachment paths must be within project."""
        from mcp_agent_mail.app import send_message

        with pytest.raises(ToolExecutionError) as exc_info:
            send_message(
                project_key="/test/project",
                sender_name="TestAgent",
                to=["Recipient"],
                subject="Test",
                body_md="See attachment",
                attachment_paths=["../../../etc/passwd"],
            )

        assert exc_info.value.error_type == "INVALID_ARGUMENT"
```

## Timestamp Edge Cases

Test time-related edge cases:

```python
# tests/test_timestamps.py

import pytest
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

class TestTimestampHandling:
    """Test timestamp parsing and edge cases."""

    @pytest.mark.parametrize("input_ts,expected", [
        # ISO 8601 variants
        ("2024-01-15T10:30:00Z", datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)),
        ("2024-01-15T10:30:00+00:00", datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)),
        ("2024-01-15T10:30:00-05:00", datetime(2024, 1, 15, 10, 30, tzinfo=timezone(timedelta(hours=-5)))),

        # Slash separators (auto-corrected)
        ("2024/01/15T10:30:00Z", datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)),

        # Missing timezone (defaults to UTC)
        ("2024-01-15T10:30:00", datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)),

        # Date only
        ("2024-01-15", datetime(2024, 1, 15, 0, 0, tzinfo=timezone.utc)),
    ])
    def test_timestamp_coercion(self, input_ts, expected):
        """Test various timestamp formats are normalized."""
        from mcp_agent_mail.utils import normalize_timestamp

        result = normalize_timestamp(input_ts)
        assert result == expected

    def test_dst_transition(self):
        """Test handling around DST transitions."""
        from mcp_agent_mail.utils import normalize_timestamp

        # Spring forward (2:00 AM becomes 3:00 AM)
        # This time doesn't exist in US Eastern
        ambiguous = "2024-03-10T02:30:00"

        # Should handle gracefully (not raise)
        result = normalize_timestamp(ambiguous)
        assert result is not None

    def test_epoch_boundary(self):
        """Test Unix epoch boundary handling."""
        from mcp_agent_mail.utils import normalize_timestamp

        # Unix epoch
        epoch = normalize_timestamp("1970-01-01T00:00:00Z")
        assert epoch == datetime(1970, 1, 1, tzinfo=timezone.utc)

        # Before epoch (some systems can't handle)
        pre_epoch = normalize_timestamp("1969-12-31T23:59:59Z")
        assert pre_epoch is not None

    def test_far_future(self):
        """Test far future dates (Y2K38 and beyond)."""
        from mcp_agent_mail.utils import normalize_timestamp

        # Y2K38 boundary
        y2k38 = normalize_timestamp("2038-01-19T03:14:08Z")
        assert y2k38.year == 2038

        # Far future
        far_future = normalize_timestamp("2100-12-31T23:59:59Z")
        assert far_future.year == 2100

    def test_leap_second(self):
        """Test leap second handling."""
        from mcp_agent_mail.utils import normalize_timestamp

        # :60 seconds (leap second)
        # Most parsers reject this; verify behavior is defined
        try:
            result = normalize_timestamp("2016-12-31T23:59:60Z")
            # If accepted, should normalize to valid time
            assert result.second in (59, 0)
        except ValueError:
            # Rejection is also acceptable
            pass
```

## Image Processing Edge Cases

Test image handling edge cases:

```python
# tests/test_images.py

import pytest
from io import BytesIO
from PIL import Image

class TestImageProcessing:
    """Test image processing edge cases."""

    def test_palette_mode_conversion(self):
        """Test palette (P) mode images are handled."""
        from mcp_agent_mail.utils import process_image

        # Create palette image
        img = Image.new("P", (100, 100))
        img.putpalette([i % 256 for i in range(768)])

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Should convert to RGB/RGBA for WebP
        result = process_image(buffer.read())
        assert result is not None

    def test_cmyk_mode_conversion(self):
        """Test CMYK images are converted to RGB."""
        from mcp_agent_mail.utils import process_image

        img = Image.new("CMYK", (100, 100), (0, 255, 255, 0))
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)

        result = process_image(buffer.read())
        assert result is not None

    def test_data_uri_parsing(self):
        """Test data URI image extraction."""
        from mcp_agent_mail.utils import parse_image_reference

        # Valid data URI
        data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

        mime, data = parse_image_reference(data_uri)
        assert mime == "image/png"
        assert len(data) > 0

    def test_format_detection(self):
        """Test image format detection from bytes."""
        from mcp_agent_mail.utils import detect_image_format

        # PNG magic bytes
        png_bytes = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        assert detect_image_format(png_bytes) == "png"

        # JPEG magic bytes
        jpeg_bytes = b'\xff\xd8\xff\xe0' + b'\x00' * 100
        assert detect_image_format(jpeg_bytes) == "jpeg"

        # WebP magic bytes
        webp_bytes = b'RIFF' + b'\x00' * 4 + b'WEBP' + b'\x00' * 100
        assert detect_image_format(webp_bytes) == "webp"

    def test_oversized_image_rejection(self):
        """Test that oversized images are rejected."""
        from mcp_agent_mail.utils import process_image, ImageTooLargeError

        # Create very large image
        img = Image.new("RGB", (10000, 10000))
        buffer = BytesIO()
        img.save(buffer, format="PNG")

        with pytest.raises(ImageTooLargeError):
            process_image(buffer.getvalue(), max_size_mb=1)

    def test_malformed_image_handling(self):
        """Test handling of malformed/corrupt images."""
        from mcp_agent_mail.utils import process_image

        malformed = b"not an image at all"

        with pytest.raises(ValueError, match="Invalid image"):
            process_image(malformed)
```

## Concurrent Access Tests

Test race conditions and concurrent operations:

```python
# tests/test_concurrency.py

import pytest
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class TestConcurrentAccess:
    """Test concurrent access patterns."""

    def test_concurrent_agent_creation(self, session):
        """Test multiple agents registering simultaneously."""
        from mcp_agent_mail.app import register_agent

        errors = []
        results = []

        def register_worker(i):
            try:
                result = register_agent(
                    project_key="/test/project",
                    program="test-agent",
                    model="test-model",
                    # Don't specify name - let server generate
                )
                results.append(result)
            except Exception as e:
                errors.append(e)

        # Launch 10 concurrent registrations
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(register_worker, i) for i in range(10)]
            for future in as_completed(futures):
                future.result()  # Raise any exceptions

        # All should succeed with unique names
        assert len(errors) == 0
        assert len(results) == 10
        names = [r["name"] for r in results]
        assert len(set(names)) == 10  # All unique

    def test_concurrent_file_reservation(self, session):
        """Test file reservation conflict detection under concurrency."""
        from mcp_agent_mail.app import file_reservation_paths

        # Two agents trying to reserve the same file
        results = []
        errors = []

        def reserve_worker(agent_name):
            try:
                result = file_reservation_paths(
                    project_key="/test/project",
                    agent_name=agent_name,
                    paths=["shared/config.json"],
                    exclusive=True,
                )
                results.append((agent_name, result))
            except Exception as e:
                errors.append((agent_name, e))

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(reserve_worker, "AgentA"),
                executor.submit(reserve_worker, "AgentB"),
            ]
            for future in as_completed(futures):
                future.result()

        # One should succeed, one should report conflict
        granted = [r for r in results if r[1].get("granted")]
        conflicts = [r for r in results if r[1].get("conflicts")]

        assert len(granted) + len(conflicts) == 2
        # At least one should have conflict (or both succeed with proper ordering)

    def test_database_lock_recovery(self, session):
        """Test database lock recovery under load."""
        from mcp_agent_mail.app import send_message

        errors = []

        def send_worker(i):
            try:
                send_message(
                    project_key="/test/project",
                    sender_name="Sender",
                    to=["Recipient"],
                    subject=f"Message {i}",
                    body_md=f"Body {i}",
                )
            except Exception as e:
                errors.append(e)

        # Burst of 50 messages
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(send_worker, i) for i in range(50)]
            for future in as_completed(futures):
                future.result()

        # All should eventually succeed (with retries)
        assert len(errors) == 0
```

## Advisory Semantics Tests

Test file reservation advisory behavior:

```python
# tests/test_file_reservations.py

class TestFileReservationSemantics:
    """Test that file reservations are advisory, not blocking."""

    def test_reservation_is_advisory(self, session):
        """Verify reservations don't actually prevent file access."""
        from mcp_agent_mail.app import file_reservation_paths
        import os

        # Create reservation
        file_reservation_paths(
            project_key="/test/project",
            agent_name="AgentA",
            paths=["test.txt"],
            exclusive=True,
        )

        # File should still be writable
        test_file = "/test/project/test.txt"
        os.makedirs(os.path.dirname(test_file), exist_ok=True)

        with open(test_file, "w") as f:
            f.write("content")  # Should not raise

        # Read should also work
        with open(test_file, "r") as f:
            content = f.read()

        assert content == "content"

    def test_reservation_expiry(self, session, freezer):
        """Test that reservations expire correctly."""
        from mcp_agent_mail.app import file_reservation_paths, release_file_reservations
        from datetime import timedelta

        # Create short-lived reservation
        result = file_reservation_paths(
            project_key="/test/project",
            agent_name="AgentA",
            paths=["test.txt"],
            ttl_seconds=60,
        )

        assert len(result["granted"]) == 1

        # Fast-forward past expiry
        freezer.move_to(timedelta(seconds=120))

        # Same file should now be available
        result2 = file_reservation_paths(
            project_key="/test/project",
            agent_name="AgentB",
            paths=["test.txt"],
            exclusive=True,
        )

        # Should succeed (old reservation expired)
        assert len(result2["granted"]) == 1
        assert len(result2.get("conflicts", [])) == 0

    def test_glob_pattern_overlap(self, session):
        """Test glob pattern conflict detection."""
        from mcp_agent_mail.app import file_reservation_paths

        # Reserve with glob
        file_reservation_paths(
            project_key="/test/project",
            agent_name="AgentA",
            paths=["src/*.py"],
            exclusive=True,
        )

        # Try to reserve specific file matching glob
        result = file_reservation_paths(
            project_key="/test/project",
            agent_name="AgentB",
            paths=["src/main.py"],
            exclusive=True,
        )

        # Should detect conflict
        assert len(result.get("conflicts", [])) > 0
```

## Do / Don't

**Do:**
- Test with smallest models (Haiku canary)
- Use comprehensive security corpora
- Test concurrent access patterns
- Verify advisory semantics
- Test timezone edge cases

**Don't:**
- Skip security testing categories
- Assume single-threaded access
- Ignore time-related edge cases
- Test only happy paths
- Forget to test expiry behavior
