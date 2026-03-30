# huntHeaders/cli.py

import argparse
from huntHeaders.utils import (
    print_banner, print_target_info, get_headers,
    analyze_headers, print_summary, print_full, print_detail,
    get_summary, parse_headers, parse_cookies, normalize_url,
    export_json, export_txt
)
from huntHeaders.constants import COLORS, DEFAULT_TIMEOUT


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze security headers of a URL.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-u', '--url', required=True, help='URL to analyze')
    parser.add_argument('-H', '--header', action='append', default=[],
                        help='Custom HTTP header, e.g., "Authorization: Bearer token"')
    parser.add_argument('--cookie', help='Cookies, e.g., "sessionid=abc; csrftoken=xyz"')
    parser.add_argument('--no-verify', action='store_false', dest='verify_ssl',
                        help='Disable SSL certificate verification')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, metavar='SECONDS',
                        help=f'Request timeout in seconds (default: {DEFAULT_TIMEOUT})')
    parser.add_argument('--proxy', metavar='URL',
                        help='Proxy URL, e.g., http://127.0.0.1:8080')
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--full', action='store_true',
                            help='Show all headers with full values and references')
    mode_group.add_argument('--detail', metavar='HEADER',
                            help='Show full detail for a single header, e.g., --detail Content-Security-Policy')
    # Export options
    parser.add_argument('--output', metavar='FILE',
                        help='Save output to a plain text file, e.g., --output results.txt')
    parser.add_argument('--json', metavar='FILE',
                        help='Export results to JSON file, e.g., --json results.json')

    args = parser.parse_args()

    custom_headers = parse_headers(args.header)
    cookies = parse_cookies(args.cookie) if args.cookie else None
    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else None
    url = normalize_url(args.url)

    print_banner()
    print_target_info(url)

    headers, status_code, final_url = get_headers(
        url, custom_headers, cookies,
        verify_ssl=args.verify_ssl,
        timeout=args.timeout,
        proxies=proxies
    )
    if headers is None:
        return

    print(f"{COLORS['green']}[INFO]{COLORS['reset']} Effective URL: {final_url}")
    print(f"{COLORS['green']}[INFO]{COLORS['reset']} Status Code:   {status_code}")
    print("=" * 120)
    print()

    results = analyze_headers(headers)

    if args.full:
        print_full(results)
    elif args.detail:
        print_detail(results, args.detail)
    else:
        print_summary(results)

    print()
    print("=" * 120)
    implemented_count, misconfigured_count, deprecated_count, missing_count = get_summary(results)
    print(f"\n{COLORS['bold']}[RESULTS]{COLORS['reset']} {url}")
    print(f"  {COLORS['green']}[+]{COLORS['reset']} {implemented_count} security headers implemented correctly")
    print(f"  {COLORS['yellow']}[-]{COLORS['reset']} {misconfigured_count} headers present but misconfigured")
    print(f"  {COLORS['yellow']}[-]{COLORS['reset']} {deprecated_count} deprecated headers detected")
    print(f"  {COLORS['red']}[!]{COLORS['reset']} {missing_count} headers missing\n")

    if args.output:
        export_txt(args.output, url, results, implemented_count, misconfigured_count, deprecated_count, missing_count)
        print(f"{COLORS['green']}[INFO]{COLORS['reset']} Output saved to {args.output}")

    if args.json:
        export_json(args.json, url, results, implemented_count, misconfigured_count, deprecated_count, missing_count)
        print(f"{COLORS['green']}[INFO]{COLORS['reset']} JSON saved to {args.json}")


if __name__ == "__main__":
    main()
