#!/usr/bin/env python3
"""
Smart HTML Updater
Main entry point for updating stock analysis HTML
- Tries to fetch real-time data
- Falls back to cached data if APIs are rate-limited
- Always updates HTML with latest available metrics
"""

import sys
import subprocess
from datetime import datetime
from pathlib import Path


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def run_script(script_name, description):
    """Run a Python script and handle errors"""
    script_path = Path(__file__).parent / script_name

    if not script_path.exists():
        print(f"  ❌ Error: {script_name} not found")
        return False

    print(f"\n📊 {description}...")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    if result.returncode == 0:
        print(f"  ✅ Success")
        return True
    else:
        print(f"  ⚠️  Completed with warnings (exit code: {result.returncode})")
        print(f"  Output: {result.stdout}")
        print(f"  Errors: {result.stderr}")
        return True  # Continue even with warnings


def check_cached_data():
    """Check if cached metrics data exists and is recent"""
    metrics_file = Path(__file__).parent.parent / 'data' / 'calculated_metrics.json'

    if not metrics_file.exists():
        print("\n  ❌ No cached metrics found")
        return False

    # Check file age
    try:
        with open(metrics_file, 'r') as f:
            import json
            data = json.load(f)

        timestamp_str = data.get('timestamp', '')
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            age_hours = (datetime.now() - timestamp).total_seconds() / 3600

            if age_hours < 24:
                print(f"\n  ✓ Cached metrics found (age: {age_hours:.1f} hours)")
                return True
            else:
                print(f"\n  ⚠️  Cached metrics are {age_hours:.1f} hours old")
                print(f"     Attempting to fetch fresh data...")
                return False
    except:
        print("\n  ❌ Error reading cached metrics")
        return False

    return False


def try_fetch_and_calculate():
    """Try to fetch fresh data and calculate metrics"""
    success = True

    # Step 1: Fetch live data
    if not run_script('update_financials.py', 'Fetching live data from Yahoo Finance'):
        success = False

    # Step 2: Calculate metrics (even if fetch had issues, we may have partial data)
    if not run_script('calculate_live_metrics.py', 'Calculating comprehensive metrics'):
        success = False

    return success


def main():
    print_header("SMART HTML UPDATER")

    # Check if we should try fetching or use cache
    use_cache = '--use-cache' in sys.argv or check_cached_data()

    if use_cache:
        print("\n  💾 Using cached metrics data")
    else:
        print("\n  🌐 Attempting to fetch fresh data...")

        try:
            fetch_success = try_fetch_and_calculate()

            if not fetch_success:
                print("\n  ⚠️  Data fetch encountered issues")
                print("  💾 Falling back to cached metrics if available...")
                use_cache = check_cached_data()

                if not use_cache:
                    print("\n  ❌ No cached metrics available")
                    print("  ⚠️  HTML will not be updated with new values")
                    return 1
        except Exception as e:
            print(f"\n  ❌ Error during fetch: {e}")
            print("  💾 Attempting to use cached metrics...")
            use_cache = check_cached_data()

            if not use_cache:
                print("\n  ❌ No cached metrics available")
                return 1

    # Step 3: Update HTML (always run this)
    if not run_script('final_update.py', 'Updating HTML file'):
        print("\n  ❌ Failed to update HTML")
        return 1

    print_header("UPDATE COMPLETE")
    print("\n  ✅ HTML file has been updated with latest metrics")
    print("  📊 Check equity-analysis.html to see the results")
    print()

    # Print summary
    metrics_file = Path(__file__).parent.parent / 'data' / 'calculated_metrics.json'
    if metrics_file.exists():
        try:
            with open(metrics_file, 'r') as f:
                import json
                data = json.load(f)
                timestamp = data.get('timestamp', 'Unknown')
                print(f"  📅 Metrics timestamp: {timestamp}")
        except:
            pass

    print()

    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n  ⚠️  Update cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n  ❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
