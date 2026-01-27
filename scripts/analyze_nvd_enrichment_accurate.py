#!/usr/bin/env python3
"""
Analyze NVD enrichment delays using the CVE History API.

This script uses the NVD CVE History API to accurately determine when
CVSS scores were first added to CVE records, providing true enrichment delays.

Metrics calculated:
- Median enrichment delay
- 90th percentile delay
- By year: 2021, 2022, 2023, 2024

Usage:
    export NVD_API_KEY=your_api_key_here
    python analyze_nvd_enrichment_accurate.py [sample_size]

Arguments:
    sample_size: Number of CVEs to randomly sample per year (recommended: 500-1000)
                 If not provided, defaults to 1000 for reasonable runtime

Examples:
    python analyze_nvd_enrichment_accurate.py                    # Sample 1000 CVEs (default)
    python analyze_nvd_enrichment_accurate.py 500                # Sample 500 CVEs per year
    python analyze_nvd_enrichment_accurate.py YOUR_API_KEY 1000  # With API key + sample
"""

import requests
import json
import sys
import os
import time
from datetime import datetime
from collections import defaultdict
import statistics

def fetch_cve_history(cve_id, api_key=None):
    """
    Fetch the change history for a specific CVE.

    Returns the first timestamp when CVSS data was added, or None.
    """
    base_url = "https://services.nvd.nist.gov/rest/json/cvehistory/2.0"

    headers = {
        'User-Agent': 'NVD-Analysis-Script/1.0'
    }

    if api_key:
        headers['apiKey'] = api_key

    params = {
        'cveId': cve_id
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Look through change history for when CVSS was first added
        changes = data.get('cveChanges', [])

        for change_wrapper in changes:
            change = change_wrapper.get('change', {})
            change_date = change.get('created')
            details = change.get('details', [])

            # Check if this change added CVSS data
            for detail in details:
                action = detail.get('action', '')
                detail_type = detail.get('type', '')

                # Look for "Added" action with CVSS type
                if action == 'Added' and 'CVSS' in detail_type:
                    return change_date

        return None

    except requests.exceptions.RequestException as e:
        print(f"    Error fetching history for {cve_id}: {e}", file=sys.stderr)
        return None

def fetch_nvd_data(year, api_key=None):
    """
    Fetch ALL NVD data for a specific year using pagination and date chunking.
    Note: NVD API 2.0 has a 120-day maximum range limit, so we chunk by quarters.
    """
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    headers = {
        'User-Agent': 'NVD-Analysis-Script/1.0'
    }

    if api_key:
        headers['apiKey'] = api_key

    all_vulnerabilities = []

    # NVD API has 120-day max range, so split year into quarters
    quarters = [
        (f'{year}-01-01T00:00:00.000Z', f'{year}-03-31T23:59:59.999Z'),
        (f'{year}-04-01T00:00:00.000Z', f'{year}-06-30T23:59:59.999Z'),
        (f'{year}-07-01T00:00:00.000Z', f'{year}-09-30T23:59:59.999Z'),
        (f'{year}-10-01T00:00:00.000Z', f'{year}-12-31T23:59:59.999Z'),
    ]

    print(f"Fetching CVEs from {year}...", file=sys.stderr)

    for quarter_num, (start_date, end_date) in enumerate(quarters, 1):
        print(f"  Quarter {quarter_num}/4...", file=sys.stderr)

        start_index = 0
        results_per_page = 2000  # Max allowed

        while True:
            params = {
                'pubStartDate': start_date,
                'pubEndDate': end_date,
                'resultsPerPage': results_per_page,
                'startIndex': start_index
            }

            try:
                response = requests.get(base_url, params=params, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()

                vulnerabilities = data.get('vulnerabilities', [])
                if not vulnerabilities:
                    break

                all_vulnerabilities.extend(vulnerabilities)

                total_results = data.get('totalResults', 0)
                print(f"    Fetched {len(vulnerabilities)} CVEs (total: {len(all_vulnerabilities)})...", file=sys.stderr)

                # Check if we've got all results for this quarter
                results_fetched = start_index + len(vulnerabilities)
                if results_fetched >= total_results:
                    break

                start_index += results_per_page

                # Rate limiting: with API key = 50 requests per 30 seconds
                # To be safe, wait 0.7 seconds between requests (allows ~43 requests per 30s)
                if api_key:
                    time.sleep(0.7)
                else:
                    # Without API key = 5 requests per 30 seconds
                    time.sleep(6)

            except requests.exceptions.RequestException as e:
                print(f"    Error fetching data for {year} Q{quarter_num} at index {start_index}: {e}", file=sys.stderr)
                break

        # Small delay between quarters
        if api_key:
            time.sleep(0.5)
        else:
            time.sleep(2)

    print(f"  Total CVEs fetched for {year}: {len(all_vulnerabilities)}", file=sys.stderr)
    return all_vulnerabilities

def calculate_enrichment_delay_accurate(cve_item, api_key=None):
    """
    Calculate accurate enrichment delay using CVE History API.

    IMPORTANT: Filters out CVEs enriched on day 0 (CNA-provided CVSS),
    only measuring true NVD enrichment delays.

    Returns delay in days, or None if data is missing or was CNA-enriched.
    """
    try:
        cve_id = cve_item.get('id')
        published = cve_item.get('published')

        # Check if CVSS scores exist
        metrics = cve_item.get('metrics', {})
        has_cvss = any(metrics.get(f'cvssMetricV{v}') for v in ['2', '3', '30', '31', '40'])

        if not has_cvss or not published or not cve_id:
            return None

        # Fetch when CVSS was first added from history API
        enrichment_date = fetch_cve_history(cve_id, api_key)

        if not enrichment_date:
            return None

        # Parse dates
        pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
        enrich_date = datetime.fromisoformat(enrichment_date.replace('Z', '+00:00'))

        # Calculate delay in days
        delay = (enrich_date - pub_date).days

        # Sanity check
        if delay < 0:
            return None

        # FILTER: Skip CVEs enriched on day 0 (CNA-provided CVSS, not NVD enrichment)
        if delay == 0:
            return None

        return delay

    except (KeyError, ValueError, AttributeError) as e:
        return None

def analyze_year(year, api_key=None, sample_size=None):
    """
    Analyze enrichment delays for a specific year.

    WARNING: This makes one API call per CVE to fetch history, which is slow!
    Use sample_size to limit to a random sample for testing.
    """
    cves = fetch_nvd_data(year, api_key)

    if not cves:
        print(f"No data available for {year}", file=sys.stderr)
        return None

    # Optionally sample for faster testing
    if sample_size and len(cves) > sample_size:
        import random
        cves = random.sample(cves, sample_size)
        print(f"  Analyzing sample of {sample_size} CVEs (out of {len(cves)} total)...", file=sys.stderr)

    delays = []
    total_cves = len(cves)
    processed = 0

    print(f"  Analyzing enrichment history for {total_cves} CVEs...", file=sys.stderr)

    for vuln in cves:
        cve_item = vuln.get('cve', {})
        cve_id = cve_item.get('id')

        delay = calculate_enrichment_delay_accurate(cve_item, api_key)

        if delay is not None:
            delays.append(delay)

        processed += 1
        if processed % 100 == 0:
            print(f"    Processed {processed}/{total_cves} CVEs...", file=sys.stderr)

        # Rate limiting for history API calls
        if api_key:
            time.sleep(0.7)
        else:
            time.sleep(6)

    if not delays:
        print(f"No enrichment data found for {year}", file=sys.stderr)
        return None

    # Calculate statistics
    delays.sort()
    median = statistics.median(delays)
    percentile_90_idx = int(len(delays) * 0.9)
    percentile_90 = delays[percentile_90_idx] if percentile_90_idx < len(delays) else delays[-1]

    result = {
        'year': year,
        'total_cves': total_cves,
        'enriched_cves': len(delays),
        'enrichment_rate': f"{(len(delays)/total_cves*100):.1f}%",
        'median_delay_days': median,
        'percentile_90_days': percentile_90,
        'max_delay_days': max(delays),
        'min_delay_days': min(delays)
    }

    return result

def main():
    """Main analysis function."""
    # Parse command line arguments
    api_key = os.environ.get('NVD_API_KEY')
    sample_size = 1000  # Default sample size

    # Parse args: can be either [sample_size] or [api_key, sample_size]
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        # If it's a number, it's sample_size
        if arg1.isdigit():
            sample_size = int(arg1)
        else:
            # Otherwise it's an API key
            api_key = arg1

    if len(sys.argv) > 2:
        # Second arg is sample_size
        if sys.argv[2].isdigit():
            sample_size = int(sys.argv[2])

    if not api_key:
        print("WARNING: No API key provided. Analysis will be VERY slow due to rate limiting.", file=sys.stderr)
        print("Provide API key via:", file=sys.stderr)
        print("  - Environment variable: export NVD_API_KEY=your_key", file=sys.stderr)
        print("  - Command line argument: python script.py [sample_size]", file=sys.stderr)
        print()
    else:
        print(f"Using API key: {api_key[:8]}...", file=sys.stderr)

    print(f"Sampling mode: analyzing {sample_size} CVEs per year", file=sys.stderr)
    print()
    print("NVD Enrichment Delay Analysis (Accurate Method)")
    print("=" * 60)
    print("This method uses CVE History API for accurate enrichment timestamps.")
    print("Note: Makes one history API call per CVE analyzed.")
    print("=" * 60)
    print()

    # Focus on 2024 for most accurate data
    years = [2021, 2022, 2023, 2025]
    results = {}

    for year in years:
        result = analyze_year(year, api_key, sample_size=sample_size)
        if result:
            results[year] = result
            print(f"\n{year} Analysis:")
            print(f"  Total CVEs: {result['total_cves']}")
            print(f"  Enriched CVEs: {result['enriched_cves']} ({result['enrichment_rate']})")
            print(f"  Median delay: {result['median_delay_days']} days")
            print(f"  90th percentile: {result['percentile_90_days']} days")
            print(f"  Range: {result['min_delay_days']}-{result['max_delay_days']} days")

    # Print summary table
    print("\n" + "=" * 60)
    print("SUMMARY TABLE")
    print("=" * 60)
    print()
    print("| Year | Median Enrichment Delay | 90th Percentile |")
    print("|------|------------------------|-----------------|")
    for year in years:
        if year in results:
            r = results[year]
            print(f"| {year} | {r['median_delay_days']} days | {r['percentile_90_days']} days |")
        else:
            print(f"| {year} | No data | No data |")

    # Save results to JSON file
    output_file = "nvd_enrichment_analysis_accurate.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n\nResults saved to: {output_file}")

if __name__ == '__main__':
    main()
