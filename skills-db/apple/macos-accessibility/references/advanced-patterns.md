# macOS Accessibility - Advanced Patterns

## Pattern: AXObserver for Event Monitoring

```python
from ApplicationServices import (
    AXObserverCreate,
    AXObserverAddNotification,
    AXObserverGetRunLoopSource,
)
from Quartz import CFRunLoopAddSource, kCFRunLoopDefaultMode

class SecureAXObserver:
    """Monitor accessibility events with security controls."""

    def __init__(self, pid: int, callback):
        if not ApplicationMonitor().validate_application(pid):
            raise SecurityError("Invalid application")

        self.observer = AXObserverCreate(pid, callback)
        self.pid = pid

    def add_notification(self, element, notification: str):
        """Add notification with security check."""
        allowed = ['AXFocusedUIElementChanged', 'AXWindowCreated']
        if notification not in allowed:
            raise SecurityError(f"Notification {notification} not allowed")

        AXObserverAddNotification(self.observer, element, notification, None)

    def start(self):
        """Start observing events."""
        source = AXObserverGetRunLoopSource(self.observer)
        CFRunLoopAddSource(CFRunLoopGetCurrent(), source, kCFRunLoopDefaultMode)
```

## Pattern: Element Tree Traversal

```python
class SafeElementTraversal:
    """Traverse AX element tree with security."""

    def __init__(self, automation: SecureAXAutomation):
        self.automation = automation
        self.max_depth = 10
        self.visited = set()

    def traverse(self, element, depth: int = 0):
        """Recursively traverse element tree."""
        if depth > self.max_depth:
            return

        element_id = id(element)
        if element_id in self.visited:
            return
        self.visited.add(element_id)

        # Process element
        yield element

        # Get children
        children = self.automation.get_attribute(element, 'AXChildren')
        if children:
            for child in children:
                yield from self.traverse(child, depth + 1)
```

## Pattern: Retry with Backoff

```python
import time

class AXRetryHandler:
    """Handle transient AX errors with retry."""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def with_retry(self, operation, *args, **kwargs):
        """Execute operation with exponential backoff."""
        for attempt in range(self.max_retries):
            try:
                return operation(*args, **kwargs)
            except (AXError, TimeoutError) as e:
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
```

## Pattern: Element Caching

```python
from functools import lru_cache
import time

class ElementCache:
    """Cache AX elements with TTL."""

    def __init__(self, ttl: int = 5):
        self.ttl = ttl
        self.cache = {}

    def get_element(self, key: str, factory):
        """Get cached element or create new."""
        if key in self.cache:
            element, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return element

        element = factory()
        self.cache[key] = (element, time.time())
        return element

    def invalidate(self, key: str = None):
        """Invalidate cache entries."""
        if key:
            self.cache.pop(key, None)
        else:
            self.cache.clear()
```
