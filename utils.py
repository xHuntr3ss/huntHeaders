# huntHeaders/utils.py

import json
import urllib3
import requests
import datetime

from typing import Optional, Tuple, Any, Dict
from requests.structures import CaseInsensitiveDict
from huntHeaders.constants import COLORS, SECURITY_HEADERS, SUMMARY_TRUNCATE, DEFAULT_TIMEOUT


def print_banner() -> None:
    print(COLORS["banner"])
    print("························································································································")
    print(":                                                                                                                      :") 
    print(":                         ▄▄ ▄▄ ▄▄ ▄▄ ▄▄  ▄▄ ▄▄▄▄▄▄ ██  ██ ▄▄▄▄▄  ▄▄▄  ▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄   ▄▄▄▄                         :")
    print(":                       ▚▘██▄██ ██ ██ ███▄██   ██   ██████ ██▄▄  ██▀██ ██▀██ ██▄▄  ██▄█▄ ███▄▄                         :")
    print(":                       ▞▖██ ██ ▀███▀ ██ ▀██   ██   ██  ██ ██▄▄▄ ██▀██ ████▀ ██▄▄▄ ██ ██ ▄▄██▀                         :")
    print(":                created by @xHuntr3ss                                                       version:2.1               :")
    print("························································································································") 
    print(COLORS["reset"])


def print_target_info(url: str) -> None:
    exec_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 120)
    print(f"{COLORS['green']}[INFO]{COLORS['reset']} TARGET:    {url}")
    print(f"{COLORS['green']}[INFO]{COLORS['reset']} EXEC DATE: {exec_date}")
    print("-" * 120)


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    if url.endswith("/"):
        url = url[:-1]
    return url


def get_headers(
    url: str,
    custom_headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    verify_ssl: bool = True,
    timeout: int = DEFAULT_TIMEOUT,
    proxies: Optional[Dict[str, str]] = None
) -> Tuple[Optional[CaseInsensitiveDict], Optional[int], Optional[str]]:
    if not verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        headers = custom_headers if custom_headers else {}
        headers.setdefault("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            verify=verify_ssl,
            allow_redirects=True,
            timeout=timeout,
            proxies=proxies
        )
        return response.headers, response.status_code, response.url
    except requests.exceptions.RequestException as e:
        print(f"{COLORS['red']}[ERROR]{COLORS['reset']} Unable to fetch headers: {e}")
        return None, None, None


def analyze_headers(headers: CaseInsensitiveDict) -> Dict[str, Dict[str, Any]]:
    results: Dict[str, Dict[str, Any]] = {}

    for header, info in SECURITY_HEADERS.items():
        current_value = headers.get(header, "not present").lower()
        status = COLORS["red"] + "●" + COLORS["reset"]

        if current_value != "not present":
            if info["category"] in ["recommended", "optional"]:
                if info["recommended_values"] is None:
                    status = COLORS["green"] + "●" + COLORS["reset"]
                elif current_value in [v.lower() for v in info["recommended_values"]]:
                    status = COLORS["green"] + "●" + COLORS["reset"]
                else:
                    status = COLORS["yellow"] + "●" + COLORS["reset"]
            elif info["category"] == "deprecated":
                if info["recommended_values"] and current_value in [v.lower() for v in info["recommended_values"]]:
                    status = COLORS["yellow"] + "●" + COLORS["reset"]
                else:
                    status = COLORS["red"] + "●" + COLORS["reset"]

        if info["category"] != "deprecated" or current_value != "not present":
            results[header] = {
                "category": info["category"],
                "value": current_value,
                "recommended_values": info["recommended_values"],
                "reference": info["reference"],
                "status": status
            }

    return results


def print_summary(results: Dict[str, Dict[str, Any]]) -> None:
    col_header = 35
    col_cat = 13
    col_val = SUMMARY_TRUNCATE + 3

    print(f"{'HEADER':<{col_header}} {'CATEGORY':<{col_cat}} {'ST'} {'VALUE'}")
    print("-" * 120)

    for header, info in results.items():
        value = info["value"] if info["value"] and info["value"] != "not present" else "---"
        if len(value) > SUMMARY_TRUNCATE:
            value = value[:SUMMARY_TRUNCATE] + "..."
        print(f"{header:<{col_header}} {info['category']:<{col_cat}} {info['status']} {value}")


def print_full(results: Dict[str, Dict[str, Any]]) -> None:
    separator = "-" * 120
    for header, info in results.items():
        recommended = ""
        if info["recommended_values"]:
            recommended = "; ".join(info["recommended_values"])

        value_display = info["value"] if info["value"] != "not present" else "---"

        print(f"{COLORS['bold']}{header}{COLORS['reset']} ({info['category']}) {info['status']}")
        print(f"  Value:       {value_display}")
        if recommended:
            print(f"  Recommended: {recommended}")
        print(f"  Reference:   {info['reference']}")
        print(separator)


def print_detail(results: Dict[str, Dict[str, Any]], header_name: str) -> None:
    match = None
    for header, info in results.items():
        if header.lower() == header_name.lower():
            match = (header, info)
            break

    if not match:
        print(f"{COLORS['red']}[!]{COLORS['reset']} Header '{header_name}' not found in analysis.")
        print(f"    Available: {', '.join(results.keys())}")
        return

    header, info = match
    recommended = "; ".join(info["recommended_values"]) if info["recommended_values"] else "No specific recommendation"
    value_display = info["value"] if info["value"] != "not present" else "--- (not present)"

    print("=" * 120)
    print(f"  {COLORS['bold']}{header}{COLORS['reset']}  {info['status']}")
    print("-" * 120)
    print(f"  Category:    {info['category']}")
    print(f"  Value:       {value_display}")
    print(f"  Recommended: {recommended}")
    print(f"  Reference:   {info['reference']}")
    print("=" * 120)


def get_summary(results: Dict[str, Dict[str, Any]]) -> Tuple[int, int, int, int]:
    green_bullet = COLORS["green"] + "●" + COLORS["reset"]
    yellow_bullet = COLORS["yellow"] + "●" + COLORS["reset"]
    red_bullet = COLORS["red"] + "●" + COLORS["reset"]

    total_security_headers = len([
        h for h, info in SECURITY_HEADERS.items()
        if info["category"] != "deprecated"
    ])

    implemented_count = 0
    misconfigured_count = 0
    deprecated_count = 0

    for header, info in results.items():
        if info["category"] == "deprecated":
            deprecated_count += 1
        elif info["status"] == green_bullet:
            implemented_count += 1
        elif info["status"] == yellow_bullet:
            misconfigured_count += 1

    missing_count = total_security_headers - implemented_count - misconfigured_count
    return implemented_count, misconfigured_count, deprecated_count, missing_count


def export_json(
    filepath: str,
    url: str,
    results: Dict[str, Dict[str, Any]],
    implemented: int,
    misconfigured: int,
    deprecated: int,
    missing: int
) -> None:
    clean_results = {}
    for header, info in results.items():
        clean_results[header] = {
            "category": info["category"],
            "value": info["value"],
            "recommended_values": info["recommended_values"],
            "reference": info["reference"],
        }

    output = {
        "target": url,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "implemented": implemented,
            "misconfigured": misconfigured,
            "deprecated": deprecated,
            "missing": missing,
        },
        "results": clean_results,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)


def export_txt(
    filepath: str,
    url: str,
    results: Dict[str, Dict[str, Any]],
    implemented: int,
    misconfigured: int,
    deprecated: int,
    missing: int
) -> None:
    col_header = 35
    col_cat = 13

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 120 + "\n")
        f.write(f"TARGET:    {url}\n")
        f.write(f"EXEC DATE: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 120 + "\n\n")
        f.write(f"{'HEADER':<{col_header}} {'CATEGORY':<{col_cat}} VALUE\n")
        f.write("-" * 120 + "\n")

        for header, info in results.items():
            value = info["value"] if info["value"] != "not present" else "---"
            if len(value) > SUMMARY_TRUNCATE:
                value = value[:SUMMARY_TRUNCATE] + "..."
            f.write(f"{header:<{col_header}} {info['category']:<{col_cat}} {value}\n")

        f.write("\n" + "=" * 120 + "\n")
        f.write(f"[RESULTS] {url}\n")
        f.write(f"  [+] {implemented} security headers implemented correctly\n")
        f.write(f"  [-] {misconfigured} headers present but misconfigured\n")
        f.write(f"  [-] {deprecated} deprecated headers detected\n")
        f.write(f"  [!] {missing} headers missing\n")


def parse_headers(header_list: list) -> dict:
    headers = {}
    for item in header_list:
        if ':' not in item:
            print(f"{COLORS['red']}[WARNING]{COLORS['reset']} Malformed header ignored: {item}")
            continue
        key, value = item.split(':', 1)
        headers[key.strip()] = value.strip()
    return headers


def parse_cookies(cookie_string: str) -> dict:
    cookies = {}
    for item in cookie_string.split(';'):
        if '=' not in item:
            continue
        key, value = item.split('=', 1)
        cookies[key.strip()] = value.strip()
    return cookies
