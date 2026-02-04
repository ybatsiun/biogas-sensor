"""
Analyst interface component for data visualization and export.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import queries
from utils.validation import parse_timestamp
from utils.i18n import t


def render_analyst_interface():
    """Render the complete Analyst interface with charts and data tables."""
    # Create tabs for different views
    tab1, tab2 = st.tabs([f"📈 {t('analyst.charts_tab')}", f"📊 {t('analyst.data_table_tab')}"])

    with tab1:
        render_charts_tab()

    with tab2:
        render_data_table_tab()


# ============================================================================
# CHARTS TAB
# ============================================================================

def render_charts_tab():
    """Render interactive charts with sensor selection and date filtering."""
    st.subheader("Interactive Multi-Sensor Chart")

    try:
        with st.spinner("Loading..."):
            sensors = queries.get_all_sensors()

        if not sensors:
            st.warning("⚠️ No sensors found. Please create sensors in the Engineer interface.")
            return

        # Sensor selection
        st.markdown("**Select Sensors to Display:**")
        col1, col2 = st.columns([4, 1])

        with col1:
            # Create checkboxes for each sensor
            selected_sensor_ids = []
            cols = st.columns(min(3, len(sensors)))  # Up to 3 columns

            for idx, sensor in enumerate(sensors):
                with cols[idx % 3]:
                    sensor_label = f"{sensor['name']}"
                    if sensor['unit']:
                        sensor_label += f" ({sensor['unit']})"

                    # Check if this sensor was previously selected (persist across reruns)
                    default_value = st.session_state.get(f"sensor_selected_{sensor['id']}", True)

                    if st.checkbox(sensor_label, value=default_value, key=f"sensor_checkbox_{sensor['id']}"):
                        selected_sensor_ids.append(sensor['id'])
                        st.session_state[f"sensor_selected_{sensor['id']}"] = True
                    else:
                        st.session_state[f"sensor_selected_{sensor['id']}"] = False

        with col2:
            if st.button("Clear All", use_container_width=True):
                for sensor in sensors:
                    st.session_state[f"sensor_selected_{sensor['id']}"] = False
                st.rerun()

        # Date range filter
        st.markdown("**Date Range Filter:**")
        col1, col2 = st.columns(2)

        with col1:
            # Default: 30 days ago
            default_start = datetime.now() - timedelta(days=30)
            start_date = st.date_input("Start Date", value=default_start)

        with col2:
            # Default: today
            end_date = st.date_input("End Date", value=datetime.now())

        # Convert dates to datetime
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        # Fetch and display chart
        if not selected_sensor_ids:
            st.info("ℹ️ Please select at least one sensor to display the chart.")
            return

        render_chart(selected_sensor_ids, start_datetime, end_datetime)

    except Exception as e:
        st.error(f"❌ Failed to render charts: {str(e)}")


def render_chart(sensor_ids: list, start_date: datetime, end_date: datetime):
    """Render Plotly line chart for selected sensors."""
    try:
        with st.spinner("Loading..."):
            records = queries.get_records_for_chart(
                sensor_ids=sensor_ids,
                start_date=start_date,
                end_date=end_date
            )

        if not records:
            st.warning("⚠️ No data found for the selected sensors and date range.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(records)

        # Extract sensor name and unit from nested structure
        df['sensor_name'] = df['sensors'].apply(lambda x: x['name'])
        df['sensor_unit'] = df['sensors'].apply(lambda x: x['unit'])

        # Parse timestamps safely
        df['recorded_at'] = df['recorded_at'].apply(lambda x: parse_timestamp(x) if isinstance(x, str) else x)
        df['recorded_at'] = pd.to_datetime(df['recorded_at'], utc=True)

        # Create Plotly figure
        fig = go.Figure()

        # Group by sensor and add traces
        for sensor_id in sensor_ids:
            sensor_df = df[df['sensor_id'] == sensor_id]

            if not sensor_df.empty:
                sensor_name = sensor_df.iloc[0]['sensor_name']
                sensor_unit = sensor_df.iloc[0]['sensor_unit']

                # Create hover text with unit
                hover_template = f"<b>{sensor_name}</b><br>"
                hover_template += "Time: %{x}<br>"
                hover_template += f"Value: %{{y}}"
                if sensor_unit:
                    hover_template += f" {sensor_unit}"
                hover_template += "<extra></extra>"

                fig.add_trace(go.Scatter(
                    x=sensor_df['recorded_at'],
                    y=sensor_df['value'],
                    mode='lines+markers',
                    name=sensor_name,
                    hovertemplate=hover_template,
                    line=dict(width=2),
                    marker=dict(size=6)
                ))

        # Update layout
        fig.update_layout(
            title="Sensor Data Over Time",
            xaxis_title="Timestamp",
            yaxis_title="Value",
            hovermode='closest',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="rgba(0, 0, 0, 0.2)",
                borderwidth=1
            ),
            height=600,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        # Enable interactive features
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')

        # Display chart
        st.plotly_chart(fig, use_container_width=True)

        # Display summary statistics
        st.markdown("### Summary Statistics")
        summary_data = []

        for sensor_id in sensor_ids:
            sensor_df = df[df['sensor_id'] == sensor_id]

            if not sensor_df.empty:
                sensor_name = sensor_df.iloc[0]['sensor_name']
                sensor_unit = sensor_df.iloc[0]['sensor_unit']
                unit_text = f" {sensor_unit}" if sensor_unit else ""

                summary_data.append({
                    "Sensor": sensor_name,
                    "Min": f"{sensor_df['value'].min():.2f}{unit_text}",
                    "Max": f"{sensor_df['value'].max():.2f}{unit_text}",
                    "Average": f"{sensor_df['value'].mean():.2f}{unit_text}",
                    "Count": len(sensor_df)
                })

        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"❌ Failed to render chart: {str(e)}")


# ============================================================================
# DATA TABLE TAB
# ============================================================================

def render_data_table_tab():
    """Render data table with filtering, sorting, and CSV export."""
    st.subheader("Data Table View")

    try:
        # Filter options
        st.markdown("**Filters:**")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            # Sensor filter
            sensors = queries.get_all_sensors()
            sensor_options = {"all": "All Sensors"}
            sensor_options.update({s['id']: f"{s['name']}" for s in sensors})

            selected_sensor = st.selectbox(
                "Sensor",
                options=list(sensor_options.keys()),
                format_func=lambda x: sensor_options[x]
            )

        with col2:
            # Date range quick filters
            date_range_option = st.selectbox(
                "Date Range",
                options=["Last 7 days", "Last 30 days", "Last 90 days", "All time", "Custom"],
                index=1
            )

        with col3:
            st.markdown("&nbsp;")  # Spacing
            apply_filter = st.button("Apply Filters", use_container_width=True)

        # Custom date range if selected
        start_date = None
        end_date = None

        if date_range_option == "Custom":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
            with col2:
                end_date = st.date_input("End Date", value=datetime.now())

            start_date = datetime.combine(start_date, datetime.min.time())
            end_date = datetime.combine(end_date, datetime.max.time())
        elif date_range_option == "Last 7 days":
            start_date = datetime.now() - timedelta(days=7)
        elif date_range_option == "Last 30 days":
            start_date = datetime.now() - timedelta(days=30)
        elif date_range_option == "Last 90 days":
            start_date = datetime.now() - timedelta(days=90)

        # Fetch data
        sensor_ids = None if selected_sensor == "all" else [selected_sensor]
        with st.spinner("Loading..."):
            records = queries.get_records_for_chart(
                sensor_ids=sensor_ids,
                start_date=start_date,
                end_date=end_date
            )

        if not records:
            st.warning("⚠️ No data found matching the selected filters.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(records)
        df['sensor_name'] = df['sensors'].apply(lambda x: x['name'])
        df['sensor_unit'] = df['sensors'].apply(lambda x: x['unit'] if x['unit'] else '')

        # Parse timestamps safely
        df['recorded_at'] = df['recorded_at'].apply(lambda x: parse_timestamp(x) if isinstance(x, str) else x)
        df['recorded_at'] = pd.to_datetime(df['recorded_at'], utc=True)

        # Select and rename columns for display
        display_df = df[['sensor_name', 'sensor_unit', 'recorded_at', 'value']].copy()
        display_df.columns = ['Sensor', 'Unit', 'Timestamp', 'Value']

        # Format timestamp
        display_df['Timestamp'] = display_df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Sort options
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**Showing {len(display_df)} records**")

        with col2:
            sort_order = st.selectbox(
                "Sort by Time",
                options=["Newest First", "Oldest First"],
                label_visibility="collapsed"
            )

        # Apply sorting
        if sort_order == "Newest First":
            display_df = display_df.sort_values('Timestamp', ascending=False)
        else:
            display_df = display_df.sort_values('Timestamp', ascending=True)

        # Display table with pagination
        render_paginated_table(display_df)

        # CSV Export
        st.markdown("### Export Data")
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown("Download the displayed data as CSV")

        with col2:
            csv_data = display_df.to_csv(index=False)
            filename = f"biogas_sensor_data_{datetime.now().strftime('%Y%m%d')}.csv"

            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"❌ Failed to render data table: {str(e)}")


def render_paginated_table(df: pd.DataFrame, rows_per_page: int = 50):
    """Render a paginated data table."""
    total_rows = len(df)
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page

    # Initialize page number in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    # Pagination controls
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

    with col1:
        if st.button("◀◀ First", disabled=st.session_state.current_page == 1, use_container_width=True):
            st.session_state.current_page = 1
            st.rerun()

    with col2:
        if st.button("◀ Previous", disabled=st.session_state.current_page == 1, use_container_width=True):
            st.session_state.current_page -= 1
            st.rerun()

    with col3:
        st.markdown(f"<div style='text-align: center; padding-top: 5px;'>Page {st.session_state.current_page} of {total_pages}</div>", unsafe_allow_html=True)

    with col4:
        if st.button("Next ▶", disabled=st.session_state.current_page == total_pages, use_container_width=True):
            st.session_state.current_page += 1
            st.rerun()

    with col5:
        if st.button("Last ▶▶", disabled=st.session_state.current_page == total_pages, use_container_width=True):
            st.session_state.current_page = total_pages
            st.rerun()

    # Calculate start and end indices
    start_idx = (st.session_state.current_page - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)

    # Display page data
    page_df = df.iloc[start_idx:end_idx]
    st.dataframe(page_df, use_container_width=True, hide_index=True)
