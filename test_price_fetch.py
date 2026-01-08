#!/usr/bin/env python3
"""
Quick test of price fetcher
"""

import sys
import subprocess

if __name__ == "__main__":
    print("Testing price fetcher...")
    print("This will fetch live data from multiple sources...")
    
    # Run the fetcher script
    result = subprocess.run(
        ['python', 'scripts/fetch_latest_prices.py'],
        capture_output=True,
        text=True
    )
    
    # Print output
    print(result.stdout)
    
    if result.returncode == 0:
        print("\n✅ Test passed! Script executed successfully.")
    else:
        print(f"\n❌ Test failed with exit code {result.returncode}")
        if result.stderr:
            print("Error output:")
            print(result.stderr)
        sys.exit(1)
