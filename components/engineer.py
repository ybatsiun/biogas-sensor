"""
Engineer interface component for sensor and record CRUD operations.
"""

import streamlit as st
from datetime import datetime
from typing import Optional
from database import queries
from utils.validation import validate_numeric_value, validate_timestamp, validate_required_field, parse_timestamp
from utils.i18n import t
from utils.timezone import local_to_utc, utc_to_local, format_local_datetime


def render_engineer_interface():
    """Render the complete Engineer interface with sensor and record management."""
    # Mobile-first: Show content in optimal order for mobile (records first)
    render_record_management()  # Mobile-first: Add Record appears first
    render_sensor_management()  # Then sensor management


# ============================================================================
# SENSOR MANAGEMENT
# ============================================================================

def render_sensor_management():
    """Render sensor creation, editing, and deletion."""
    st.subheader(t('engineer.sensor_management'))

    # Create new sensor form - COLLAPSED by default (records are priority on mobile)
    with st.expander(f"➕ {t('engineer.create_sensor')}", expanded=False):
        render_create_sensor_form()

    # Display existing sensors - COLLAPSED by default for mobile
    with st.expander(f"📋 {t('engineer.existing_sensors')}", expanded=False):
        render_sensor_list()


def render_create_sensor_form():
    """Render form for creating a new sensor."""
    with st.form("create_sensor_form", clear_on_submit=True):
        name = st.text_input("Sensor Name*", placeholder="e.g., Temperature Sensor A")
        unit = st.text_input("Unit", placeholder="e.g., °C, bar, pH")
        comment = st.text_area("Comment", placeholder="Optional description")

        submitted = st.form_submit_button("Create Sensor", use_container_width=True)

        if submitted:
            # Validate required fields
            is_valid, error_msg = validate_required_field(name, "Sensor Name")
            if not is_valid:
                st.error(error_msg)
                return

            try:
                with st.spinner("Loading..."):
                    sensor = queries.create_sensor(
                        name=name.strip(),
                        unit=unit.strip() if unit else None,
                        comment=comment.strip() if comment else None
                    )
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to create sensor: {str(e)}")


def render_sensor_list():
    """Render list of all sensors with edit and delete options."""
    try:
        with st.spinner("Loading..."):
            sensors = queries.get_all_sensors()

        if not sensors:
            st.info("No sensors found. Create one above!")
            return

        for sensor in sensors:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.markdown(f"**{sensor['name']}**")
                    unit_text = f"Unit: {sensor['unit']}" if sensor['unit'] else "No unit"
                    comment_text = f" | {sensor['comment']}" if sensor['comment'] else ""
                    st.caption(f"{unit_text}{comment_text}")

                with col2:
                    if st.button("✏️ Edit", key=f"edit_sensor_{sensor['id']}", use_container_width=True):
                        st.session_state[f"editing_sensor_{sensor['id']}"] = True
                        st.rerun()

                with col3:
                    if st.button("🗑️ Delete", key=f"delete_sensor_{sensor['id']}", use_container_width=True):
                        st.session_state[f"deleting_sensor_{sensor['id']}"] = True
                        st.rerun()

                # Show edit form if editing
                if st.session_state.get(f"editing_sensor_{sensor['id']}", False):
                    render_edit_sensor_form(sensor)

                # Show delete confirmation if deleting
                if st.session_state.get(f"deleting_sensor_{sensor['id']}", False):
                    render_delete_sensor_confirmation(sensor)

                st.divider()

    except Exception as e:
        st.error(f"❌ Failed to load sensors: {str(e)}")


def render_edit_sensor_form(sensor: dict):
    """Render form for editing an existing sensor."""
    with st.form(f"edit_sensor_form_{sensor['id']}"):
        st.markdown(f"**Editing: {sensor['name']}**")

        name = st.text_input("Sensor Name*", value=sensor['name'])
        unit = st.text_input("Unit", value=sensor['unit'] if sensor['unit'] else "")
        comment = st.text_area("Comment", value=sensor['comment'] if sensor['comment'] else "")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Save", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)

        if submitted:
            # Validate required fields
            is_valid, error_msg = validate_required_field(name, "Sensor Name")
            if not is_valid:
                st.error(error_msg)
                return

            try:
                with st.spinner("Loading..."):
                    queries.update_sensor(
                        sensor_id=sensor['id'],
                        name=name.strip(),
                        unit=unit.strip() if unit else None,
                        comment=comment.strip() if comment else None
                    )
                del st.session_state[f"editing_sensor_{sensor['id']}"]
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to update sensor: {str(e)}")

        if cancelled:
            del st.session_state[f"editing_sensor_{sensor['id']}"]
            st.rerun()


def render_delete_sensor_confirmation(sensor: dict):
    """Render confirmation dialog for deleting a sensor."""
    st.warning(
        f"⚠️ **Delete '{sensor['name']}'?** This will also delete all associated records. This action cannot be undone."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm Delete", key=f"confirm_delete_sensor_{sensor['id']}", use_container_width=True):
            try:
                with st.spinner("Loading..."):
                    queries.delete_sensor(sensor['id'])
                del st.session_state[f"deleting_sensor_{sensor['id']}"]
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to delete sensor: {str(e)}")

    with col2:
        if st.button("❌ Cancel", key=f"cancel_delete_sensor_{sensor['id']}", use_container_width=True):
            del st.session_state[f"deleting_sensor_{sensor['id']}"]
            st.rerun()


# ============================================================================
# RECORD MANAGEMENT
# ============================================================================

def render_record_management():
    """Render record creation, editing, and deletion."""
    st.subheader(t('engineer.record_management'))

    # Create new record form - EXPANDED by default for mobile-first UX
    with st.expander(f"➕ {t('engineer.add_record')}", expanded=True):
        render_create_record_form()

    # Display recent records - COLLAPSED by default, show 10 records
    record_limit = 10  # Mobile-optimized: show only 10
    with st.expander(f"📋 {t('engineer.recent_records')} ({t('engineer.last_n_records', n=record_limit)})", expanded=False):
        render_record_list(limit=record_limit)


def render_create_record_form():
    """Render form for creating a new sensor record."""
    try:
        sensors = queries.get_all_sensors()

        if not sensors:
            st.warning("⚠️ Please create a sensor first before adding records.")
            return

        with st.form("create_record_form", clear_on_submit=True):
            # Sensor selection
            sensor_options = {s['id']: f"{s['name']} ({s['unit']})" if s['unit'] else s['name']
                              for s in sensors}
            selected_sensor_id = st.selectbox(
                "Sensor*",
                options=list(sensor_options.keys()),
                format_func=lambda x: sensor_options[x]
            )

            # Timestamp with current time as default
            col1, col2 = st.columns(2)
            with col1:
                recorded_date = st.date_input("Date*", value=datetime.now())
            with col2:
                recorded_time = st.time_input("Time*", value=datetime.now().time())

            # Value input
            value_str = st.text_input("Value*", placeholder="e.g., 37.5")

            submitted = st.form_submit_button("Add Record", use_container_width=True)

            if submitted:
                # Combine date and time (local timezone)
                recorded_at_local = datetime.combine(recorded_date, recorded_time)

                # Validate value
                is_valid_num, value, num_error = validate_numeric_value(value_str)
                if not is_valid_num:
                    st.error(num_error)
                    return

                # Validate timestamp
                is_valid_time, time_error = validate_timestamp(recorded_at_local)
                if not is_valid_time:
                    st.error(time_error)
                    return

                try:
                    with st.spinner("Loading..."):
                        # Convert local time to UTC for storage
                        recorded_at_utc = local_to_utc(recorded_at_local)
                        queries.create_record(
                            sensor_id=selected_sensor_id,
                            recorded_at=recorded_at_utc,
                            value=value
                        )
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to create record: {str(e)}")

    except Exception as e:
        st.error(f"❌ Failed to load sensors: {str(e)}")


def render_record_list(limit: int = 100):
    """Render list of recent records with edit and delete options."""
    try:
        with st.spinner("Loading..."):
            records = queries.get_recent_records(limit=limit)

        if not records:
            st.info("No records found. Add one above!")
            return

        for record in records:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])

                # Format the timestamp in local timezone
                recorded_at_utc = parse_timestamp(record['recorded_at'])
                formatted_time = format_local_datetime(recorded_at_utc)

                with col1:
                    sensor_name = record['sensors']['name']
                    sensor_unit = record['sensors']['unit']
                    unit_text = f" {sensor_unit}" if sensor_unit else ""
                    st.markdown(f"**{sensor_name}**: {record['value']}{unit_text}")
                    st.caption(f"Recorded: {formatted_time}")

                with col2:
                    if st.button("✏️ Edit", key=f"edit_record_{record['id']}", use_container_width=True):
                        st.session_state[f"editing_record_{record['id']}"] = True
                        st.rerun()

                with col3:
                    if st.button("🗑️ Delete", key=f"delete_record_{record['id']}", use_container_width=True):
                        st.session_state[f"deleting_record_{record['id']}"] = True
                        st.rerun()

                # Show edit form if editing
                if st.session_state.get(f"editing_record_{record['id']}", False):
                    render_edit_record_form(record)

                # Show delete confirmation if deleting
                if st.session_state.get(f"deleting_record_{record['id']}", False):
                    render_delete_record_confirmation(record)

                st.divider()

    except Exception as e:
        st.error(f"❌ Failed to load records: {str(e)}")


def render_edit_record_form(record: dict):
    """Render form for editing an existing sensor record."""
    try:
        sensors = queries.get_all_sensors()

        with st.form(f"edit_record_form_{record['id']}"):
            st.markdown(f"**Editing Record**")

            # Sensor selection
            sensor_options = {s['id']: f"{s['name']} ({s['unit']})" if s['unit'] else s['name']
                              for s in sensors}
            selected_sensor_id = st.selectbox(
                "Sensor*",
                options=list(sensor_options.keys()),
                index=list(sensor_options.keys()).index(record['sensor_id']),
                format_func=lambda x: sensor_options[x]
            )

            # Parse existing timestamp (UTC) and convert to local
            recorded_at_utc = parse_timestamp(record['recorded_at'])
            recorded_at_local = utc_to_local(recorded_at_utc)

            # Timestamp inputs (in local timezone)
            col1, col2 = st.columns(2)
            with col1:
                recorded_date = st.date_input("Date*", value=recorded_at_local.date())
            with col2:
                recorded_time = st.time_input("Time*", value=recorded_at_local.time())

            # Value input
            value_str = st.text_input("Value*", value=str(record['value']))

            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("💾 Save", use_container_width=True)
            with col2:
                cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)

            if submitted:
                # Combine date and time (local timezone)
                new_recorded_at_local = datetime.combine(recorded_date, recorded_time)

                # Validate value
                is_valid_num, value, num_error = validate_numeric_value(value_str)
                if not is_valid_num:
                    st.error(num_error)
                    return

                # Validate timestamp
                is_valid_time, time_error = validate_timestamp(new_recorded_at_local)
                if not is_valid_time:
                    st.error(time_error)
                    return

                try:
                    with st.spinner("Loading..."):
                        # Convert local time to UTC for storage
                        new_recorded_at_utc = local_to_utc(new_recorded_at_local)
                        queries.update_record(
                            record_id=record['id'],
                            sensor_id=selected_sensor_id,
                            recorded_at=new_recorded_at_utc,
                            value=value
                        )
                    del st.session_state[f"editing_record_{record['id']}"]
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to update record: {str(e)}")

            if cancelled:
                del st.session_state[f"editing_record_{record['id']}"]
                st.rerun()

    except Exception as e:
        st.error(f"❌ Failed to load sensors: {str(e)}")


def render_delete_record_confirmation(record: dict):
    """Render confirmation dialog for deleting a record."""
    sensor_name = record['sensors']['name']
    st.warning(f"⚠️ **Delete this record from '{sensor_name}'?** This action cannot be undone.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm Delete", key=f"confirm_delete_record_{record['id']}", use_container_width=True):
            try:
                with st.spinner("Loading..."):
                    queries.delete_record(record['id'])
                del st.session_state[f"deleting_record_{record['id']}"]
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to delete record: {str(e)}")

    with col2:
        if st.button("❌ Cancel", key=f"cancel_delete_record_{record['id']}", use_container_width=True):
            del st.session_state[f"deleting_record_{record['id']}"]
            st.rerun()
