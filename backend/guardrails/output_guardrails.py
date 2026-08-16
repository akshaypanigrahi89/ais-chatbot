import re
from typing import Dict, Any, List


SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key\s*[=:]\s*["\']?)([a-zA-Z0-9_\-]{20,})', 'API Key'),
    (r'(?i)(aws[_-]?access[_-]?key[_-]?id\s*[=:]\s*["\']?)([A-Z0-9]{20})', 'AWS Key'),
    (r'(?i)(aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']?)([a-zA-Z0-9/+=]{40})', 'AWS Secret'),
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', 'Private Key'),
    (r'(?i)(password\s*[=:]\s*["\']?)([^\s"\']{8,})', 'Password'),
]

INSTRUCTION_LEAK_PATTERNS = [
    r"system\s+prompt",
    r"my\s+instructions?\s+(?:are|is|tell)",
    r"i\s+(?:am|was)\s+(?:told|instructed)\s+to",
    r"my\s+rules?\s+(?:are|is|say)",
    r"i\s+(?:can't|cannot|won't)\s+(?:share|reveal|tell)",
]

SENSITIVE_INFO_PATTERNS = [
    (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN'),
    (r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', 'Credit Card'),
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'Email'),
]

DANGEROUS_CONTENT_PATTERNS = [
    r"bypass\s+security",
    r"ignore\s+security",
    r"disable\s+guardrails",
    r"turn\s+off\s+safety",
    r"god\s+mode",
]


class OutputGuardrails:
    def __init__(self):
        pass

    def check(self, output: str, context: str = "") -> Dict[str, Any]:
        threats = []

        for pattern, threat_type in SECRET_PATTERNS:
            if re.search(pattern, output):
                threats.append({
                    "type": "secret_leak",
                    "threat": threat_type,
                    "severity": "CRITICAL"
                })

        for pattern in INSTRUCTION_LEAK_PATTERNS:
            if re.search(pattern, output, re.IGNORECASE):
                threats.append({
                    "type": "instruction_leak",
                    "threat": "System Prompt Leak",
                    "severity": "HIGH"
                })

        for pattern, info_type in SENSITIVE_INFO_PATTERNS:
            if re.search(pattern, output):
                threats.append({
                    "type": "sensitive_info",
                    "threat": info_type,
                    "severity": "MEDIUM"
                })

        for pattern in DANGEROUS_CONTENT_PATTERNS:
            if re.search(pattern, output, re.IGNORECASE):
                threats.append({
                    "type": "dangerous_content",
                    "threat": "Security Bypass",
                    "severity": "HIGH"
                })

        if context:
            citation_check = self._check_citations(output, context)
            if not citation_check["valid"]:
                threats.append({
                    "type": "fabricated_citation",
                    "threat": "Fabricated Citation",
                    "severity": "MEDIUM"
                })

        return {
            "passed": len(threats) == 0,
            "threats": threats,
            "sanitized_output": self._sanitize(output) if threats else output
        }

    def _check_citations(self, output: str, context: str) -> Dict[str, Any]:
        file_pattern = r'(?:Source \d+: )([^\s--]+)'
        cited_files = re.findall(file_pattern, output)

        context_files = set()
        for line in context.split('\n'):
            if line.startswith('[Source'):
                match = re.search(r'Source \d+: ([^\s--]+)', line)
                if match:
                    context_files.add(match.group(1))

        valid = all(file in context_files for file in cited_files)
        return {"valid": valid, "cited": cited_files, "available": list(context_files)}

    def _sanitize(self, text: str) -> str:
        for pattern, _ in SECRET_PATTERNS:
            text = re.sub(pattern, '[REDACTED]', text)
        return text


output_guardrails = OutputGuardrails()
