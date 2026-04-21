#!/usr/bin/env python3
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main'))

def check_file_exists(path, description):
    """Check if a file exists"""
    exists = os.path.isfile(path)
    status = "✓" if exists else "✗"
    print(f"{status} {description}")
    return exists

def check_directory_exists(path, description):
    """Check if a directory exists"""
    exists = os.path.isdir(path)
    status = "✓" if exists else "✗"
    print(f"{status} {description}")
    return exists

print("=" * 70)
print("BSHunter ACTOR - VERIFICATION CHECKLIST")
print("=" * 70)

all_checks_pass = True

# Check root level files
print("\n[ROOT LEVEL FILES]")
all_checks_pass &= check_file_exists("requirements.txt", "requirements.txt")
all_checks_pass &= check_file_exists(".env", ".env file")
all_checks_pass &= check_file_exists("test_input.json", "test_input.json")

# Check directories
print("\n[DIRECTORIES]")
all_checks_pass &= check_directory_exists("main", "main/ directory")
all_checks_pass &= check_directory_exists("main/modules", "main/modules/ directory")

# Check module files
print("\n[MODULE FILES]")
all_checks_pass &= check_file_exists("main/modules/browser_module.py", "browser_module.py")
all_checks_pass &= check_file_exists("main/modules/post_scraper.py", "post_scraper.py")
all_checks_pass &= check_file_exists("main/modules/post_details.py", "post_details.py")
all_checks_pass &= check_file_exists("main/modules/data_parser.py", "data_parser.py")

# Check main actor file
print("\n[ACTOR MAIN]")
all_checks_pass &= check_file_exists("main/actor_main.py", "actor_main.py")

# Check test files
print("\n[TEST FILES]")
all_checks_pass &= check_file_exists("test_imports.py", "test_imports.py")
all_checks_pass &= check_file_exists("test_data_parser.py", "test_data_parser.py")

# Test imports
print("\n[IMPORT VALIDATION]")
try:
    from modules.browser_module import setup_driver, search_hashtag, wait_and_scroll, get_page_html, close_driver
    print("✓ browser_module imports OK")
except Exception as e:
    print(f"✗ browser_module import failed: {e}")
    all_checks_pass = False

try:
    from modules.post_scraper import scrape_feed_posts
    print("✓ post_scraper imports OK")
except Exception as e:
    print(f"✗ post_scraper import failed: {e}")
    all_checks_pass = False

try:
    from modules.post_details import get_post_details
    print("✓ post_details imports OK")
except Exception as e:
    print(f"✗ post_details import failed: {e}")
    all_checks_pass = False

try:
    from modules.data_parser import process_all_posts
    print("✓ data_parser imports OK")
except Exception as e:
    print(f"✗ data_parser import failed: {e}")
    all_checks_pass = False

# Check .env has token
print("\n[ENVIRONMENT SETUP]")
try:
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv('APIFY_API_TOKEN')
    if token and token != 'your_token_here':
        print("✓ APIFY_API_TOKEN configured")
    else:
        print("⚠ APIFY_API_TOKEN not set (set it before deploying to Apify)")
        all_checks_pass = False
except Exception as e:
    print(f"✗ Environment check failed: {e}")
    all_checks_pass = False

# Check test_input.json
print("\n[INPUT FILE]")
try:
    with open('test_input.json', 'r') as f:
        test_input = json.load(f)
    if 'hashtags' in test_input and isinstance(test_input['hashtags'], list):
        print(f"✓ test_input.json valid (hashtags: {test_input['hashtags']})")
    else:
        print("✗ test_input.json missing 'hashtags' field")
        all_checks_pass = False
except Exception as e:
    print(f"✗ test_input.json error: {e}")
    all_checks_pass = False

# Summary
print("\n" + "=" * 70)
if all_checks_pass:
    print("✅ ALL CHECKS PASSED - READY FOR TESTING!")
    print("\nNext steps:")
    print("  1. Update .env with your APIFY_API_TOKEN")
    print("  2. Run: python test_imports.py")
    print("  3. Run: python test_data_parser.py")
    print("  4. Review: README_ACTOR.md for full documentation")
    sys.exit(0)
else:
    print("❌ SOME CHECKS FAILED - PLEASE FIX THE ISSUES ABOVE")
    sys.exit(1)
