import re
from typing import Dict, Any, Tuple, List
from enum import Enum


class ThreatType(str, Enum):
    PROMPT_INJECTION = "PROMPT_INJECTION"
    SYSTEM_PROMPT_EXTRACTION = "SYSTEM_PROMPT_EXTRACTION"
    CREDENTIAL_REQUEST = "CREDENTIAL_REQUEST"
    ROLE_MANIPULATION = "ROLE_MANIPULATION"
    CODE_INJECTION = "CODE_INJECTION"
    EXCESSIVE_LENGTH = "EXCESSIVE_LENGTH"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?above\s+instructions",
    r"disregard\s+(all\s+)?previous",
    r"forget\s+(all\s+)?previous",
    r"new\s+instructions?\s*:",
    r"system\s*prompt\s*:",
    r"you\s+are\s+now\s+",
    r"act\s+as\s+if\s+",
    r"pretend\s+you\s+are\s+",
    r"override\s+",
]

SYSTEM_PROMPT_EXTRACTION_PATTERNS = [
    r"show\s+me\s+your\s+system\s+prompt",
    r"what\s+is\s+your\s+system\s+prompt",
    r"reveal\s+your\s+system\s+prompt",
    r"print\s+your\s+instructions",
    r"output\s+your\s+instructions",
    r"tell\s+me\s+your\s+instructions",
    r"what\s+are\s+your\s+rules",
    r"repeat\s+(all\s+)?your\s+instructions",
]

CREDENTIAL_PATTERNS = [
    r"what\s+is\s+the\s+admin\s+password",
    r"what\s+is\s+the\s+password",
    r"give\s+me\s+(the\s+)?password",
    r"send\s+me\s+credentials",
]

ROLE_MANIPULATION_PATTERNS = [
    r"you\s+are\s+now\s+an?\s+admin",
    r"i\s+am\s+the\s+admin",
    r"i\s+have\s+admin\s+access",
    r"promote\s+me\s+to\s+admin",
    r"change\s+my\s+role\s+to",
    r"i\s+am\s+a\s+developer",
    r"i\s+work\s+for\s+the\s+company",
]

CODE_INJECTION_PATTERNS = [
    r"exec\s*\(",
    r"eval\s*\(",
    r"import\s+os",
    r"__import__",
    r"subprocess",
    r"DROP\s+TABLE",
    r"DELETE\s+FROM",
]

SANITIZE_PATTERN = re.compile(r'[\u200b\u200c\u200d\ufeff\x00-\x08\x0b\x0c\x0e-\x1f]')


class InputGuardrails:
    def __init__(self):
        self.max_length = 10000

    def check(self, user_input: str) -> Tuple[bool, Dict[str, Any]]:
        sanitized = self.sanitize(user_input)

        if len(sanitized) > self.max_length:
            return False, {
                "blocked": True,
                "threat_type": ThreatType.EXCESSIVE_LENGTH,
                "severity": Severity.HIGH,
                "message": "Input exceeds maximum length"
            }

        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                return False, {
                    "blocked": True,
                    "threat_type": ThreatType.PROMPT_INJECTION,
                    "severity": Severity.HIGH,
                    "message": "Potential prompt injection detected"
                }

        for pattern in SYSTEM_PROMPT_EXTRACTION_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                return False, {
                    "blocked": True,
                    "threat_type": ThreatType.SYSTEM_PROMPT_EXTRACTION,
                    "severity": Severity.HIGH,
                    "message": "System prompt extraction attempt detected"
                }

        for pattern in CREDENTIAL_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                return False, {
                    "blocked": True,
                    "threat_type": ThreatType.CREDENTIAL_REQUEST,
                    "severity": Severity.CRITICAL,
                    "message": "Credential request detected"
                }

        for pattern in ROLE_MANIPULATION_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                return False, {
                    "blocked": True,
                    "threat_type": ThreatType.ROLE_MANIPULATION,
                    "severity": Severity.MEDIUM,
                    "message": "Role manipulation attempt detected"
                }

        return True, {"blocked": False}

    def sanitize(self, text: str) -> str:
        text = SANITIZE_PATTERN.sub('', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text


input_guardrails = InputGuardrails()
