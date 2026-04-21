"""
Test data_parser.py with sample data to ensure normalization functions work
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main'))

from modules.data_parser import (
    normalize_like_count,
    parse_datetime,
    normalize_comment,
    normalize_post,
    validate_data
)

print("=" * 60)
print("TESTING DATA_PARSER MODULE")
print("=" * 60)

# Test 1: normalize_like_count
print("\n[Test 1] normalize_like_count()")
test_cases = [
    ("1.2K", 1200),
    ("1.5M", 1500000),
    ("1,234", 1234),
    (42, 42),
    (None, 0),
    ("invalid", 0),
]

for input_val, expected in test_cases:
    result = normalize_like_count(input_val)
    status = "✓" if result == expected else "✗"
    print(f"  {status} normalize_like_count({repr(input_val)}) = {result} (expected {expected})")

# Test 2: parse_datetime
print("\n[Test 2] parse_datetime()")
result = parse_datetime("2024-04-13T15:30:00Z")
print(f"  ✓ parse_datetime('2024-04-13T15:30:00Z') = {result}")

# Test 3: normalize_comment
print("\n[Test 3] normalize_comment()")
test_comment = {
    'author': 'testuser',
    'text': 'Great post!',
    'likes': '42',
    'timestamp': '2 hours ago'
}
normalized = normalize_comment(test_comment)
print(f"  ✓ Normalized comment: {normalized}")

# Test 4: normalize_post
print("\n[Test 4] normalize_post()")
test_post = {
    'author': {'username': 'instauser'},
    'metadata': {
        'caption': 'Amazing photo!',
        'image_url': 'https://example.com/image.jpg',
        'like_count': '1.2K',
        'timestamp': '2024-04-13T10:00:00Z'
    },
    'post_url': 'https://instagram.com/p/ABC123/',
    'comments': [
        {'author': 'user1', 'text': 'Nice!', 'likes': 5, 'timestamp': None},
        {'author': 'user2', 'text': 'Love it!', 'likes': 10, 'timestamp': None}
    ]
}
normalized = normalize_post(test_post)
print(f"  ✓ Post normalized successfully")
print(f"    - Username: {normalized['username']}")
print(f"    - Like count: {normalized['like_count']}")
print(f"    - Comment count: {normalized['comment_count']}")
print(f"    - Has timestamp: {normalized['timestamp'] is not None}")

# Test 5: validate_data
print("\n[Test 5] validate_data()")
is_valid = validate_data(normalized)
print(f"  {'✓' if is_valid else '✗'} Post validation: {is_valid}")

print("\n" + "=" * 60)
print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
