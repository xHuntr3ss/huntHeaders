# huntHeaders/constants.py

# ANSI color codes
COLORS = {
    "yellow": "\033[33m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "red": "\033[31m",
    "pink": "\033[38;5;198m",
    'banner': "\033[38;2;0;178;169m",
    'turquoise': '\033[38;5;38m',
    "bold": "\033[1m",
    "underline": "\033[4m",
    "reset": "\033[0m"
}

# List of headers to analyze
SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "category": "recommended",
        "recommended_values": [
            "max-age=31536000",
            "max-age=31536000; includeSubDomains",
            "max-age=63072000; includeSubDomains; preload"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#strict-transport-security"
    },
    "Content-Security-Policy": {
        "category": "recommended",
        "recommended_values": None,
        "reference": "https://owasp.org/www-project-secure-headers/#content-security-policy"
    },
    "X-Frame-Options": {
        "category": "recommended",
        "recommended_values": [
            "deny",
            "sameorigin"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#x-frame-options"
    },
    "X-Content-Type-Options": {
        "category": "recommended",
        "recommended_values": [
            "nosniff"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#x-content-type-options"
    },
    "X-Permitted-Cross-Domain-Policies": {
        "category": "optional",
        "recommended_values": [
            "none",
            "master-only"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#x-permitted-cross-domain-policies"
    },
    "Referrer-Policy": {
        "category": "optional",
        "recommended_values": [
            "no-referrer",
            "strict-origin",
            "strict-origin-when-cross-origin"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#referrer-policy"
    },
    "Clear-Site-Data": {
        "category": "optional",
        "recommended_values": [
            "cookies",
            "cache",
            "storage",
            "*"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#clear-site-data"
    },
    "Cross-Origin-Resource-Policy": {
        "category": "optional",
        "recommended_values": [
            "same-site",
            "same-origin"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#cross-origin-resource-policy"
    },
    "Cross-Origin-Embedder-Policy": {
        "category": "optional",
        "recommended_values": [
            "require-corp"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#cross-origin-embedder-policy"
    },
    "Cross-Origin-Opener-Policy": {
        "category": "optional",
        "recommended_values": [
            "same-origin"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy"
    },
    "Cache-Control": {
        "category": "optional",
        "recommended_values": None,
        "reference": "https://owasp.org/www-community/OWASP_Secure_Headers_Project#Cache-Control"
    },
    "Feature-Policy": {
        "category": "deprecated",
        "recommended_values": None,
        "reference": "https://owasp.org/www-project-secure-headers/#feature-policy"
    },
    "Expect-CT": {
        "category": "deprecated",
        "recommended_values": None,
        "reference": "https://owasp.org/www-project-secure-headers/#expect-ct"
    },
    "Public-Key-Pins": {
        "category": "deprecated",
        "recommended_values": None,
        "reference": "https://owasp.org/www-project-secure-headers/#public-key-pins"
    },
    "X-XSS-Protection": {
        "category": "deprecated",
        "recommended_values": [
            "0"
        ],
        "reference": "https://owasp.org/www-project-secure-headers/#x-xss-protection"
    },
    "Pragma": {
        "category": "deprecated",
        "recommended_values": None,
        "reference": "https://owasp.org/www-project-secure-headers/#pragma"
    }
}

# Truncation limit for summary mode
SUMMARY_TRUNCATE = 60

# Default request timeout in seconds
DEFAULT_TIMEOUT = 10
