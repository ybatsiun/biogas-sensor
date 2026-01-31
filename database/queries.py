"""
Database query functions for sensors and sensor_records tables.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from functools import wraps
from database.client import get_supabase

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# SENSOR OPERATIONS
# ============================================================================

def get_all_sensors() -> List[Dict[str, Any]]:
    """
    Fetch all sensors from the database.

    Returns:
        List of sensor dictionaries with keys: id, name, unit, comment
    """
    logger.info("📊 Fetching all sensors from database...")
    supabase = get_supabase()
    response = supabase.table("sensors").select("*").order("name").execute()
    logger.info(f"✅ Retrieved {len(response.data)} sensors")
    return response.data


def get_sensor_by_id(sensor_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a single sensor by ID.

    Args:
        sensor_id: UUID of the sensor

    Returns:
        Sensor dictionary or None if not found
    """
    supabase = get_supabase()
    response = supabase.table("sensors").select("*").eq("id", sensor_id).execute()
    return response.data[0] if response.data else None


def create_sensor(name: str, unit: Optional[str] = None, comment: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new sensor.

    Args:
        name: Sensor name (required)
        unit: Measurement unit (optional)
        comment: Description or notes (optional)

    Returns:
        Created sensor dictionary

    Raises:
        Exception: If database operation fails
    """
    logger.info(f"➕ Creating sensor: {name} ({unit})")
    supabase = get_supabase()
    data = {"name": name}
    if unit is not None:
        data["unit"] = unit
    if comment is not None:
        data["comment"] = comment

    response = supabase.table("sensors").insert(data).execute()
    logger.info(f"✅ Sensor created successfully: {name}")
    return response.data[0]


def update_sensor(sensor_id: str, name: Optional[str] = None,
                  unit: Optional[str] = None, comment: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing sensor.

    Args:
        sensor_id: UUID of the sensor to update
        name: New sensor name (optional)
        unit: New measurement unit (optional)
        comment: New description (optional)

    Returns:
        Updated sensor dictionary

    Raises:
        Exception: If database operation fails
    """
    supabase = get_supabase()
    data = {}
    if name is not None:
        data["name"] = name
    if unit is not None:
        data["unit"] = unit
    if comment is not None:
        data["comment"] = comment

    response = supabase.table("sensors").update(data).eq("id", sensor_id).execute()
    return response.data[0]


def delete_sensor(sensor_id: str) -> bool:
    """
    Delete a sensor and all associated records (CASCADE).

    Args:
        sensor_id: UUID of the sensor to delete

    Returns:
        True if deletion was successful

    Raises:
        Exception: If database operation fails
    """
    supabase = get_supabase()
    supabase.table("sensors").delete().eq("id", sensor_id).execute()
    return True


# ============================================================================
# SENSOR RECORD OPERATIONS
# ============================================================================

def get_recent_records(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Fetch recent sensor records with sensor information.

    Args:
        limit: Maximum number of records to return (default: 100)

    Returns:
        List of record dictionaries with sensor details
    """
    logger.info(f"📊 Fetching recent {limit} records from database...")
    supabase = get_supabase()
    response = (
        supabase.table("sensor_records")
        .select("*, sensors(name, unit)")
        .order("recorded_at", desc=True)
        .limit(limit)
        .execute()
    )
    logger.info(f"✅ Retrieved {len(response.data)} records")
    return response.data


def get_record_by_id(record_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a single sensor record by ID.

    Args:
        record_id: UUID of the record

    Returns:
        Record dictionary with sensor details or None if not found
    """
    supabase = get_supabase()
    response = (
        supabase.table("sensor_records")
        .select("*, sensors(name, unit)")
        .eq("id", record_id)
        .execute()
    )
    return response.data[0] if response.data else None


def create_record(sensor_id: str, recorded_at: datetime, value: float) -> Dict[str, Any]:
    """
    Create a new sensor record.

    Args:
        sensor_id: UUID of the sensor
        recorded_at: Timestamp of the recording
        value: Measured value

    Returns:
        Created record dictionary

    Raises:
        Exception: If database operation fails
    """
    supabase = get_supabase()
    data = {
        "sensor_id": sensor_id,
        "recorded_at": recorded_at.isoformat(),
        "value": value,
    }
    response = supabase.table("sensor_records").insert(data).execute()
    return response.data[0]


def update_record(record_id: str, sensor_id: Optional[str] = None,
                  recorded_at: Optional[datetime] = None, value: Optional[float] = None) -> Dict[str, Any]:
    """
    Update an existing sensor record.

    Args:
        record_id: UUID of the record to update
        sensor_id: New sensor ID (optional)
        recorded_at: New timestamp (optional)
        value: New value (optional)

    Returns:
        Updated record dictionary

    Raises:
        Exception: If database operation fails
    """
    supabase = get_supabase()
    data = {}
    if sensor_id is not None:
        data["sensor_id"] = sensor_id
    if recorded_at is not None:
        data["recorded_at"] = recorded_at.isoformat()
    if value is not None:
        data["value"] = value

    response = supabase.table("sensor_records").update(data).eq("id", record_id).execute()
    return response.data[0]


def delete_record(record_id: str) -> bool:
    """
    Delete a sensor record.

    Args:
        record_id: UUID of the record to delete

    Returns:
        True if deletion was successful

    Raises:
        Exception: If database operation fails
    """
    supabase = get_supabase()
    supabase.table("sensor_records").delete().eq("id", record_id).execute()
    return True


# ============================================================================
# ANALYST QUERY OPERATIONS
# ============================================================================

def get_records_for_chart(sensor_ids: Optional[List[str]] = None,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Fetch sensor records for charting with optional filters.

    Args:
        sensor_ids: List of sensor IDs to filter by (optional)
        start_date: Start of date range (optional)
        end_date: End of date range (optional)

    Returns:
        List of record dictionaries with sensor details
    """
    supabase = get_supabase()
    query = supabase.table("sensor_records").select("*, sensors(name, unit)")

    # Apply filters
    if sensor_ids:
        query = query.in_("sensor_id", sensor_ids)
    if start_date:
        query = query.gte("recorded_at", start_date.isoformat())
    if end_date:
        query = query.lte("recorded_at", end_date.isoformat())

    # Order by timestamp
    query = query.order("recorded_at", desc=False)

    response = query.execute()
    return response.data


def get_all_records_for_export() -> List[Dict[str, Any]]:
    """
    Fetch all sensor records with sensor information for CSV export.

    Returns:
        List of all records with sensor details
    """
    supabase = get_supabase()
    response = (
        supabase.table("sensor_records")
        .select("*, sensors(name, unit)")
        .order("recorded_at", desc=False)
        .execute()
    )
    return response.data
