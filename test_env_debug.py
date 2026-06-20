#!/usr/bin/env python3
"""Debug environment variable loading"""
import os
from pathlib import Path
from dotenv import load_dotenv

print(f"Current working directory: {os.getcwd()}")
print(f"Python script location: {Path(__file__).parent}")

# Test 1: Load from current dir
env_path = Path('.') / '.env'
print(f"\nTest 1 - Relative path:")
print(f"  Env path: {env_path}")
print(f"  Absolute: {env_path.resolve()}")
print(f"  Exists: {env_path.exists()}")

# Test 2: Load from absolute path
env_path_abs = Path(__file__).parent / '.env'
print(f"\nTest 2 - Absolute path:")
print(f"  Env path: {env_path_abs}")
print(f"  Exists: {env_path_abs.exists()}")

# Try loading and check
load_dotenv(env_path_abs, override=True)
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

print(f"\nAfter load_dotenv:")
print(f"  SUPABASE_URL: {url}")
print(f"  SUPABASE_ANON_KEY: {key if key else 'NOT SET'}")
