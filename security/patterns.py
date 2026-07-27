"""
Known prompt injection and security patterns.

These are deterministic checks that run before invoking
the LLM-based Security Reviewer.
"""

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "forget previous instructions",
    "forget everything",
    "you are chatgpt",
    "system prompt",
    "developer instructions",
    "developer message",
    "assistant instructions",
    "override the system",
    "act as",
    "approve immediately",
    "always approve",
    "ignore ngo policy",
]

POLICY_BYPASS_PATTERNS = [
    "skip registration",
    "skip eligibility",
    "skip budget",
    "do not verify",
    "don't verify",
    "ignore registration",
    "ignore eligibility",
    "ignore budget",
    "ignore funding limits",
    "bypass policy",
    "bypass verification",
]

SUSPICIOUS_PATTERNS = [
    "only read this page",
    "ignore the rest",
    "hidden instruction",
    "secret instruction",
    "confidential instruction",
    "do not tell the reviewer",
]