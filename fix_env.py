#!/usr/bin/env python3
"""Fix .env file by removing BOM"""

content = """SUPABASE_URL=https://snwmhtbgbwblvbhzwsnj.supabase.co
SUPABASE_ANON_KEY=sb_publishable_OfCgpNcMrhjBaVIbHT5-PQ_LuEvCbO2
DASH_DEBUG=True
DASH_PORT=8050
DASH_HOST=127.0.0.1
"""

# Write WITHOUT the BOM
with open('.env', 'w', encoding='utf-8') as f:
    f.write(content)

print("File written successfully with UTF-8 (no BOM)")

# Verify
from dotenv import dotenv_values
vals = dotenv_values('.env')
print(f"\nParsed values:")
print(f"  SUPABASE_URL: {vals.get('SUPABASE_URL')}")
print(f"  SUPABASE_ANON_KEY: {vals.get('SUPABASE_ANON_KEY')}")
