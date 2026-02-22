#!/usr/bin/env python3
"""
Saveweb Search CLI Tool

Search for blogs in the saveweb database.
"""
import argparse
import sys
from urllib.parse import quote
import json
try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


def search_saveweb(query: str) -> dict:
    """Search saveweb API for the given query."""
    url = f"https://search-api.saveweb.org/api/search?q={quote(query)}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Search saveweb database for blog information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by article title and domain
  %(prog)s "文章标题" example.com

  # Search by domain only
  %(prog)s --domain-only example.com

  # Get blog_id from any article in the blog
  %(prog)s "any keyword" example.com --get-blog-id
        """
    )

    parser.add_argument(
        "title",
        nargs="?",
        help="Article title or keyword to search"
    )

    parser.add_argument(
        "domain",
        nargs="?",
        help="Blog domain (e.g., example.com)"
    )

    parser.add_argument(
        "-d", "--domain-only",
        action="store_true",
        help="Search by domain only"
    )

    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output raw JSON result"
    )

    parser.add_argument(
        "-n", "--num-results",
        type=int,
        default=10,
        help="Number of results to display (default: 10)"
    )

    args = parser.parse_args()

    # Build search query
    if args.domain_only:
        if not args.domain:
            parser.error("--domain-only requires a domain argument")
        query = args.domain
    else:
        if not args.title or not args.domain:
            parser.error("Both title and domain are required unless using --domain-only")
        query = f"{args.title} {args.domain}"

    # Perform search
    try:
        result = search_saveweb(query)
    except requests.RequestException as e:
        print(f"Error: Failed to search saveweb: {e}", file=sys.stderr)
        sys.exit(1)

    # Handle results
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    total_hits = result.get("estimatedTotalHits", 0)

    if total_hits == 0:
        print(f"No results found for query: {query}")
        sys.exit(1)

    hits = result.get("hits", [])

    # Display search results
    print(f"Found {total_hits} results for: {query}")
    print(f"{'='*60}")

    for i, hit in enumerate(hits[:args.num_results], 1):
        print(f"\n[{i}] Blog ID: {hit.get('id_feed', 'N/A')}")
        print(f"    Title: {hit.get('title', 'N/A')}")
        print(f"    Link: {hit.get('link', 'N/A')}")
        print(f"    Date: {hit.get('date', 'N/A')}")

    if total_hits > args.num_results:
        print(f"\n... and {total_hits - args.num_results} more results")


if __name__ == "__main__":
    main()
