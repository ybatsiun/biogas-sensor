"""
Validation utilities for user inputs.
"""

from datetime import datetime
from typing import Tuple, Optional
import re


def validate_numeric_value(value_str: str) -> Tuple[bool, Optional[float], Optional[str]]:
    """
    Validate that a string can be converted to a float.

    Args:
        value_str: String to validate

    Returns:
        Tuple of (is_valid, value, error_message)
        - is_valid: True if value is a valid number
        - value: Parsed float value or None if invalid
        - error_message: Error message or None if valid
    """
    if not value_str or value_str.strip() == "":
        return False, None, "Value cannot be empty"

    try:
        value = float(value_str)
        return True, value, None
    except ValueError:
        return False, None, f"'{value_str}' is not a valid number"


def validate_timestamp(timestamp: datetime) -> Tuple[bool, Optional[str]]:
    """
    Validate that a timestamp is not in the future.

    Args:
        timestamp: Datetime to validate

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if timestamp is valid
        - error_message: Error message or None if valid
    """
    now = datetime.now(timestamp.tzinfo)

    if timestamp > now:
        return False, "Cannot record future timestamps"

    return True, None


def validate_required_field(value: str, field_name: str = "Field") -> Tuple[bool, Optional[str]]:
    """
    Validate that a required field is not empty.

    Args:
        value: String value to validate
        field_name: Name of the field for error message

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if field is not empty
        - error_message: Error message or None if valid
    """
    if not value or value.strip() == "":
        return False, f"{field_name} is required"

    return True, None


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse timestamp string from Supabase, handling various formats.

    Args:
        timestamp_str: Timestamp string from database

    Returns:
        datetime object

    Raises:
        ValueError: If timestamp cannot be parsed
    """
    if not timestamp_str:
        raise ValueError("Timestamp string is empty")

    # Remove 'Z' suffix and replace with '+00:00' for UTC
    timestamp_str = timestamp_str.replace('Z', '+00:00')

    # Try parsing with different formats
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",  # With microseconds and timezone
        "%Y-%m-%dT%H:%M:%S%z",      # Without microseconds but with timezone
        "%Y-%m-%dT%H:%M:%S.%f",     # With microseconds, no timezone
        "%Y-%m-%dT%H:%M:%S",        # Without microseconds or timezone
    ]

    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue

    # If all formats fail, try using fromisoformat (Python 3.7+)
    try:
        return datetime.fromisoformat(timestamp_str)
    except ValueError:
        raise ValueError(f"Unable to parse timestamp: {timestamp_str}")
