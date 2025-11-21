import re

# Patterns that indicate SQL injection
INJECTION_PATTERNS = [
    r"(--|#)",                     # Comment attempts
    r"(/\*.*?\*/)",                # Block comment
    r"\bOR\b\s+1=1",               # OR 1=1
    r"\bOR\b\s+'1'='1'",           # OR '1'='1'
    r"\bUNION\b\s+SELECT\b",       # UNION SELECT
    r";\s*DROP\s+TABLE",           # DROP TABLE
    r";\s*DELETE\s+FROM",          # DELETE FROM
    r";\s*ALTER\s+TABLE",          # ALTER TABLE
    r"SLEEP\s*\(",                 # SLEEP() for blind SQLi
    r"WAITFOR\s+DELAY",            # MSSQL delay injection
]

def is_sql_safe(query: str) -> bool:
    """
    Returns True if query is safe.
    Returns False if query contains SQL injection patterns.
    """

    q = query.lower().strip()

    # Allow normal safe patterns
    SAFE_PATTERNS = [
        r"^select\b",
        r"^update\b",
        r"^delete\b",
        r"^insert\b",
    ]

    # If query starts normally, we treat it as safe unless dangerous patterns appear
    if any(re.match(p, q) for p in SAFE_PATTERNS):
        # Check if any dangerous pattern exists
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, q, re.IGNORECASE):
                return False
        return True

    # If query does NOT start with valid SQL, treat as unsafe
    return False
