#!/usr/bin/env python3
"""
Quick test to demonstrate database logging.
Run this to see database requests in the terminal.
"""

from database import queries

print("\n" + "="*60)
print("🔬 TESTING DATABASE REQUESTS")
print("="*60 + "\n")

# Test 1: Fetch all sensors
print("TEST 1: Fetching all sensors...")
sensors = queries.get_all_sensors()
print(f"Result: Found {len(sensors)} sensors\n")

# Test 2: Fetch recent records
print("TEST 2: Fetching recent records...")
records = queries.get_recent_records(limit=5)
print(f"Result: Found {len(records)} records\n")

print("="*60)
print("✅ DATABASE REQUESTS COMPLETED")
print("="*60)
print("\nNotice the log messages above showing:")
print("  🔌 Connection to Supabase")
print("  📊 Data fetching operations")
print("  ✅ Successful responses")
print("\nThese same requests happen when you use the Streamlit UI,")
print("but they occur on the Python server side, not in the browser!")
print()
