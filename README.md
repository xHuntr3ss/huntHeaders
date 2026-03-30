# huntHeaders

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-GPLv3-green?style=flat-square)

> CLI tool to analyze HTTP security headers of a target URL.  
> Detects missing, misconfigured, and deprecated headers based on OWASP recommendations.

---

## Installation

Install dependencies:

```bash
pip install requests urllib3
```

Clone the repo into your tools folder:

```bash
git clone https://github.com/xHuntr3ss/huntHeaders.git
```

Add the alias to your `.bashrc` / `.zshrc`:

```bash
alias huntHeaders='PYTHONPATH=/path/to/Tools python -m huntHeaders.cli'
```

Reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

> Replace `/path/to/Tools` with the folder **containing** the `huntHeaders/` directory.

---

## Usage / Examples

```
huntHeaders -u <URL> [options]
```

| Flag | Description |
|------|-------------|
| `-u`, `--url` | Target URL *(required)* |
| `-H`, `--header` | Custom HTTP header, e.g. `"Authorization: Bearer token"` |
| `--cookie` | Cookies, e.g. `"sessionid=abc; csrftoken=xyz"` |
| `--no-verify` | Disable SSL certificate verification |
| `--timeout` | Request timeout in seconds *(default: 10)* |
| `--proxy` | Proxy URL, e.g. `http://127.0.0.1:8080` |
| `--full` | Show all headers with full values and references |
| `--detail HEADER` | Show full detail for a single header |
| `--output FILE` | Save output to a plain text file |
| `--json FILE` | Export results to JSON |

**Basic scan:**
```bash
huntHeaders -u https://target.com
```

**Through Burp Suite:**
```bash
huntHeaders -u https://target.com --proxy http://127.0.0.1:8080 --no-verify
```

**With custom headers and cookie:**
```bash
huntHeaders -u https://target.com -H "Authorization: Bearer token" --cookie "sessionid=abc"
```

**Export results:**
```bash
huntHeaders -u https://target.com --json results.json --output results.txt
```

---

## Output Modes

### Default Mode
Compact table, values truncated. Clean for screenshots.

![default mode](https://raw.githubusercontent.com/xHuntr3ss/xHuntr3ss-assets/refs/heads/main/huntHeaders/huntHeaders-default-mode.png)

### Full Mode
Every header with its full value, recommended values, and OWASP reference link.

![full mode](https://raw.githubusercontent.com/xHuntr3ss/xHuntr3ss-assets/refs/heads/main/huntHeaders/huntHeaders-full-mode.png)

### Detailed Mode
Deep dive into a single header — full value, recommended values, and reference.

![detailed mode](https://raw.githubusercontent.com/xHuntr3ss/xHuntr3ss-assets/refs/heads/main/huntHeaders/huntHeaders-detailed-mode.png)
---

## Contributing

Got a new header to track? Found a bug? PRs are welcome.

1. Fork the repo
2. Create your branch: `git checkout -b feature/my-thing`
3. Commit your changes: `git commit -m 'add: my thing'`
4. Push and open a PR

---

*created by [@xHuntr3ss](https://github.com/xHuntr3ss)*