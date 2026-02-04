"""
Timezone utilities for handling UTC storage and local display.

Database stores all timestamps in UTC.
Client displays timestamps in user's local timezone.
User input is converted from local timezone to UTC before storage.
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Optional


# Default timezone for the application (Europe/Kiev for Ukraine)
DEFAULT_TIMEZONE = "Europe/Kiev"


def get_local_timezone() -> ZoneInfo:
    """
    Get the local timezone for the application.

    Returns:
        ZoneInfo object for the local timezone
    """
    return ZoneInfo(DEFAULT_TIMEZONE)


def local_to_utc(dt: datetime) -> datetime:
    """
    Convert a naive datetime from local timezone to UTC.

    Args:
        dt: Naive datetime in local timezone

    Returns:
        Timezone-aware datetime in UTC
    """
    # Make the naive datetime timezone-aware (assume it's in local timezone)
    local_tz = get_local_timezone()
    dt_local = dt.replace(tzinfo=local_tz)

    # Convert to UTC
    dt_utc = dt_local.astimezone(timezone.utc)

    return dt_utc


def utc_to_local(dt: datetime) -> datetime:
    """
    Convert a UTC datetime to local timezone.

    Args:
        dt: Datetime in UTC (can be naive or aware)

    Returns:
        Timezone-aware datetime in local timezone
    """
    # If datetime is naive, assume it's UTC
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)

    # Convert to local timezone
    local_tz = get_local_timezone()
    dt_local = dt_utc.astimezone(local_tz)

    return dt_local


def format_local_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime in local timezone for display.

    Args:
        dt: Datetime to format (will be converted to local if needed)
        fmt: Format string (default: ISO-like format)

    Returns:
        Formatted datetime string in local timezone
    """
    dt_local = utc_to_local(dt)
    return dt_local.strftime(fmt)


def now_utc() -> datetime:
    """
    Get current time in UTC.

    Returns:
        Current datetime in UTC
    """
    return datetime.now(timezone.utc)


def now_local() -> datetime:
    """
    Get current time in local timezone.

    Returns:
        Current datetime in local timezone
    """
    local_tz = get_local_timezone()
    return datetime.now(local_tz)
