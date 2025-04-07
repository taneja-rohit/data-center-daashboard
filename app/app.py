import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page config
st.set_page_config(
    page_title="Data Center Dashboard",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Universal styling that works on both light and dark backgrounds
st.markdown("""
    <style>
        /* Universal text color that works on both light and dark backgrounds */
        .universal-text {
            color: #2DD4BF !important;  /* Sober teal color */
        }
        
        /* Ensure charts have transparent backgrounds to work with any theme */
        .js-plotly-plot .plotly {
            background: transparent !important;
        }
        
        /* Style adjustments for better visibility */
        [data-testid="stMetricValue"] {
            color: #2DD4BF !important;
        }
        
        [data-testid="stMetricDelta"] {
            color: #14B8A6 !important;
        }
        
        .stMarkdown {
            color: #2DD4BF !important;
        }
    </style>
""", unsafe_allow_html=True)

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("app/static/css/style.css")
except:
    st.write("CSS file not found. Using default styling.")

# Generate sample data for demonstration
def generate_sample_data():
    if 'data_generated' not in st.session_state:
        # Sample data center rack information
        racks = [f"Rack-{i:03d}" for i in range(1, 101)]
        
        # Sample location data
        locations = ["Row A", "Row B", "Row C", "Row D", "Row E"]
        
        # Generate 90 days of hourly data
        now = datetime.now()
        start_date = now - timedelta(days=90)
        dates = [start_date + timedelta(hours=i) for i in range(90*24)]
        
        # Create sample data for each metric
        data = []
        for rack in racks:
            row = np.random.choice(locations)
            for date in dates:
                # Temperature (°C)
                temp = np.random.normal(22, 3)
                # Power usage (kW)
                power = np.random.normal(5, 1.5)
                # CPU utilization (%)
                cpu = np.random.normal(60, 15)
                # Network traffic (Gbps)
                network = np.random.normal(8, 3)
                # Cooling efficiency
                cooling = np.random.normal(85, 10)
                
                # Add some anomalies
                if np.random.random() < 0.01:  # 1% chance of anomaly
                    temp += np.random.choice([-1, 1]) * np.random.uniform(5, 10)
                    power += np.random.choice([-1, 1]) * np.random.uniform(2, 4)
                
                data.append({
                    'timestamp': date,
                    'rack_id': rack,
                    'location': row,
                    'temperature': max(15, min(temp, 35)),  # Bound between 15-35
                    'power_usage': max(1, min(power, 10)),  # Bound between 1-10
                    'cpu_utilization': max(10, min(cpu, 100)),  # Bound between 10-100
                    'network_traffic': max(0.5, min(network, 20)),  # Bound between 0.5-20
                    'cooling_efficiency': max(50, min(cooling, 100))  # Bound between 50-100
                })
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Add calculated PUE (Power Usage Effectiveness)
        total_facility_power = df['power_usage'] * 1.2  # Simplified calculation
        df['pue'] = total_facility_power / df['power_usage']
        
        # Add uptime status (1 for up, 0 for down)
        df['uptime_status'] = np.where(np.random.random(len(df)) < 0.9995, 1, 0)  # 99.95% uptime
        
        # Add MTTR (Mean Time To Repair) in minutes
        df['mttr'] = np.random.normal(25, 10, len(df))
        df.loc[df['uptime_status'] == 1, 'mttr'] = 0
        
        # Calculate churn rate and CSAT
        df['churn_rate'] = np.random.normal(3, 1, len(df))
        df['csat_score'] = np.random.normal(87, 5, len(df))
        
        # Carbon footprint (metric tons CO2)
        df['carbon_footprint'] = df['power_usage'] * 0.5
        
        # Renewable energy percentage
        df['renewable_energy_pct'] = np.random.normal(35, 10, len(df))
        
        st.session_state.df = df
        st.session_state.racks = racks
        st.session_state.locations = locations
        st.session_state.data_generated = True
        st.session_state.authenticated = True

# Main dashboard layout
def main():
    # Set up session state
    if 'username' not in st.session_state:
        st.session_state.username = "Demo User"
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
    
    if 'active_persona' not in st.session_state:
        st.session_state.active_persona = "Data Center Operator"
    
    # Generate sample data
    generate_sample_data()
    
    # Persona tabs at the top
    persona = option_menu(
        menu_title=None,
        options=["Data Center Operator", "IT/Infra/DevOps Operator", "Contact Us"],
        icons=["building-gear", "pc-display", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#1E293B"},  # Darker background
            "icon": {"color": "#FFFFFF", "font-size": "18px"},  # White icons
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "color": "#FFFFFF",  # White text
                "background-color": "#1E293B",  # Same as container
                "--hover-color": "#334155",  # Slightly lighter on hover
                "transition": "background-color 0.3s ease"
            },
            "nav-link-selected": {
                "background-color": "#0EA5E9",  # Bright blue for selected tab
                "color": "#FFFFFF",  # White text for selected tab
                "font-weight": "600"  # Bold text for selected tab
            }
        }
    )
    
    st.session_state.active_persona = persona
    
    if persona == "IT/Infra/DevOps Operator":
        st.title("IT/Infra/DevOps Operator Dashboard")
        
        # Coming soon message
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 50px 0;">
                <h2>🚧 Coming Soon 🚧</h2>
                <p style="font-size: 18px;">
                    We're working on an exciting set of tools and dashboards for IT, Infrastructure, and DevOps teams.
                </p>
                <p style="font-size: 16px;">
                    This view will include compute, storage, network, and application performance metrics.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            features = [
                "🖥️ Compute Infrastructure Management",
                "💾 Storage Utilization and Performance",
                "🌐 Network Topology and Metrics",
                "📊 Application Performance Monitoring",
                "🚨 Alerts and Incident Management",
                "🔄 CI/CD Pipeline Monitoring"
            ]
            
            for feature in features:
                st.info(feature)
        
        return
    
    elif persona == "Contact Us":
        st.title("Contact Us")
        
        # Coming soon message
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 50px 0;">
                <h2>🚧 Coming Soon 🚧</h2>
                <p style="font-size: 18px;">
                    We're working on setting up our contact and support portal.
                </p>
                <p style="font-size: 16px;">
                    In the meantime, please check back soon for updates!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("✉️ Email: support@datacenter-dashboard.com")
            st.info("📞 Phone: +1 (555) 123-4567")
            st.info("💬 Live Chat: Coming soon")
        
        return
    
    # Data Center Operator view
    st.title("Data Center Operations")
    
    # Sidebar
    with st.sidebar:
        st.write(f"Welcome, {st.session_state.username}")
        st.divider()
        
        # Dashboard selection
        view = option_menu(
            "Select Dashboard View",
            ["Operational Metrics", "Resource Management"],
            icons=["speedometer", "hdd-stack"],
            menu_icon="list", 
            default_index=0
        )
        
        st.divider()
        
        # Filters
        st.subheader("Filters")
        
        # Time range filter
        time_range = st.selectbox(
            "Time Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days"]
        )
        
        # Location filter
        location = st.multiselect(
            "Location",
            options=st.session_state.locations,
            default=st.session_state.locations
        )
        
        # Rack filter
        rack_filter = st.multiselect(
            "Racks",
            options=st.session_state.racks,
            default=[]
        )
        
        # Apply filters
        df = st.session_state.df
        
        # Time filter
        now = datetime.now()
        if time_range == "Last 24 Hours":
            df = df[df['timestamp'] >= now - timedelta(days=1)]
        elif time_range == "Last 7 Days":
            df = df[df['timestamp'] >= now - timedelta(days=7)]
        elif time_range == "Last 30 Days":
            df = df[df['timestamp'] >= now - timedelta(days=30)]
        
        # Location filter
        if location:
            df = df[df['location'].isin(location)]
        
        # Rack filter
        if rack_filter:
            df = df[df['rack_id'].isin(rack_filter)]
        
        filtered_df = df
        st.session_state.filtered_df = filtered_df
    
    # Main content area
    if view == "Operational Metrics":
        render_operational_metrics()
    elif view == "Resource Management":
        render_resource_management()

# Operational metrics dashboard
def render_operational_metrics():
    st.title("Operational Metrics Dashboard")
    
    df = st.session_state.filtered_df
    
    # Calculate key metrics
    uptime_pct = df['uptime_status'].mean() * 100
    avg_mttr = df[df['mttr'] > 0]['mttr'].mean()
    avg_pue = df['pue'].mean()
    utilization_rate = df['cpu_utilization'].mean()
    avg_csat = df['csat_score'].mean()
    avg_churn = df['churn_rate'].mean()
    
    # Row 1: KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Uptime",
            f"{uptime_pct:.3f}%",
            delta=f"{uptime_pct-99.95:.4f}%" if uptime_pct != 99.95 else None,
            delta_color="normal"
        )
        st.caption("Target: 99.999%")
    
    with col2:
        st.metric(
            "Avg MTTR",
            f"{avg_mttr:.1f} min",
            delta=f"{30-avg_mttr:.1f} min" if avg_mttr < 30 else f"-{avg_mttr-30:.1f} min",
            delta_color="inverse"
        )
        st.caption("Target: <30 minutes")
    
    with col3:
        st.metric(
            "Power Usage Effectiveness",
            f"{avg_pue:.2f}",
            delta=f"{1.2-avg_pue:.2f}" if avg_pue < 1.2 else f"+{avg_pue-1.2:.2f}",
            delta_color="inverse"
        )
        st.caption("Target: 1.2 or lower")
    
    with col4:
        st.metric(
            "Utilization Rate",
            f"{utilization_rate:.1f}%",
            delta=f"{utilization_rate-75:.1f}%" if utilization_rate != 75 else None,
            delta_color="off" if 70 <= utilization_rate <= 80 else "inverse"
        )
        st.caption("Optimal: 70-80%")
    
    st.divider()
    
    # Row 2: Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("PUE Trend Over Time")
        # Group by day
        pue_trend = df.groupby(df['timestamp'].dt.date)['pue'].mean().reset_index()
        fig = px.line(
            pue_trend, 
            x='timestamp', 
            y='pue',
            labels={'timestamp': 'Date', 'pue': 'PUE'}
        )
        fig.add_hline(y=1.2, line_dash="dash", line_color="green", annotation_text="Target PUE (1.2)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Uptime Status")
        # Calculate uptime per day
        uptime_daily = df.groupby(df['timestamp'].dt.date)['uptime_status'].mean().reset_index()
        uptime_daily['uptime_pct'] = uptime_daily['uptime_status'] * 100
        
        fig = px.bar(
            uptime_daily, 
            x='timestamp', 
            y='uptime_pct',
            labels={'timestamp': 'Date', 'uptime_pct': 'Uptime %'}
        )
        fig.add_hline(y=99.999, line_dash="dash", line_color="green", annotation_text="Target (99.999%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 3: Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Customer Satisfaction Score")
        # Group by day
        csat_data = df.groupby(df['timestamp'].dt.date)['csat_score'].mean().reset_index()
        
        fig = px.line(
            csat_data, 
            x='timestamp', 
            y='csat_score',
            labels={'timestamp': 'Date', 'csat_score': 'CSAT Score'}
        )
        fig.add_hline(y=85, line_dash="dash", line_color="green", annotation_text="Target (85%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Churn Rate")
        # Group by day
        churn_data = df.groupby(df['timestamp'].dt.date)['churn_rate'].mean().reset_index()
        
        fig = px.line(
            churn_data, 
            x='timestamp', 
            y='churn_rate',
            labels={'timestamp': 'Date', 'churn_rate': 'Churn Rate %'}
        )
        fig.add_hline(y=5, line_dash="dash", line_color="red", annotation_text="Target (<5%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 4: Sustainability metrics
    st.subheader("Sustainability Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Carbon Footprint")
        carbon_data = df.groupby(df['timestamp'].dt.date)['carbon_footprint'].sum().reset_index()
        
        fig = px.area(
            carbon_data, 
            x='timestamp', 
            y='carbon_footprint',
            labels={'timestamp': 'Date', 'carbon_footprint': 'Carbon Emissions (metric tons CO2)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Renewable Energy Usage")
        renewable_data = df.groupby(df['timestamp'].dt.date)['renewable_energy_pct'].mean().reset_index()
        
        fig = px.line(
            renewable_data, 
            x='timestamp', 
            y='renewable_energy_pct',
            labels={'timestamp': 'Date', 'renewable_energy_pct': 'Renewable Energy (%)'}
        )
        fig.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Target (50%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 5: Alerts and Thresholds
    st.subheader("Alert Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input("PUE Alert Threshold", min_value=1.0, max_value=2.0, value=1.4, step=0.1)
    
    with col2:
        st.number_input("Temperature Alert Threshold (°C)", min_value=20, max_value=35, value=28, step=1)
    
    with col3:
        st.number_input("Uptime Alert Threshold (%)", min_value=99.0, max_value=100.0, value=99.9, step=0.01)
    
    # Row 6: Report Generation
    st.subheader("Report Generation")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Daily Summary", "Weekly Overview", "Monthly Performance", "Quarterly Analysis"]
        )
    
    with col2:
        report_format = st.selectbox(
            "Format",
            ["PDF", "Excel", "CSV", "Interactive Dashboard"]
        )
    
    with col3:
        if st.button("Generate Report", type="primary"):
            st.success(f"{report_type} report requested in {report_format} format. It will be emailed when ready.")

# Resource management dashboard
def render_resource_management():
    st.title("Resource Management Dashboard")
    
    df = st.session_state.filtered_df
    
    # Row 1: Available capacity metrics
    st.subheader("Available Capacity")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        space_avail = 73.5  # sample percentage
        st.metric(
            "Space Availability",
            f"{space_avail}%",
            delta=f"{space_avail-70:.1f}%" if space_avail != 70 else None
        )
    
    with col2:
        power_avail = 62.8  # sample percentage
        st.metric(
            "Power Availability", 
            f"{power_avail}%",
            delta=f"{power_avail-65:.1f}%" if power_avail != 65 else None,
            delta_color="inverse"
        )
    
    with col3:
        cooling_avail = 58.3  # sample percentage
        st.metric(
            "Cooling Availability", 
            f"{cooling_avail}%",
            delta=f"{cooling_avail-60:.1f}%" if cooling_avail != 60 else None,
            delta_color="inverse"
        )
    
    with col4:
        network_avail = 77.2  # sample percentage
        st.metric(
            "Network Availability", 
            f"{network_avail}%",
            delta=f"{network_avail-75:.1f}%" if network_avail != 75 else None
        )
    
    st.divider()
    
    # Row 2: Heat map visualization
    st.subheader("Temperature Distribution Heatmap")
    
    try:
        # Create a pivot table for the heatmap
        latest_data = df.sort_values('timestamp').groupby('rack_id').tail(1)
        pivot_df = latest_data.pivot_table(
            index='location', 
            columns='rack_id', 
            values='temperature',
            aggfunc='mean'
        )
        
        # Sort columns alphabetically
        pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)
        
        # Create heatmap
        fig = px.imshow(
            pivot_df,
            labels=dict(x="Rack ID", y="Row", color="Temperature (°C)"),
            x=pivot_df.columns,
            y=pivot_df.index,
            color_continuous_scale="Thermal",
            aspect="auto"
        )
        
        fig.update_layout(
            height=500,
            margin=dict(l=60, r=50, t=30, b=50),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not create heatmap visualization: {str(e)}")
    
    # Row 3: Power and Cooling
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Peak Load Per Cabinet")
        
        try:
            # Group by rack and get max power
            peak_power = df.groupby('rack_id')['power_usage'].max().reset_index()
            peak_power = peak_power.sort_values('power_usage', ascending=False).head(15)
            
            fig = px.bar(
                peak_power,
                x='rack_id',
                y='power_usage',
                labels={'rack_id': 'Rack ID', 'power_usage': 'Peak Power (kW)'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not create peak load visualization: {str(e)}")
    
    with col2:
        st.subheader("Cooling Efficiency Trend")
        
        try:
            # Group by day
            cooling_trend = df.groupby(df['timestamp'].dt.date)['cooling_efficiency'].mean().reset_index()
            
            fig = px.line(
                cooling_trend,
                x='timestamp',
                y='cooling_efficiency',
                labels={'timestamp': 'Date', 'cooling_efficiency': 'Cooling Efficiency (%)'}
            )
            fig.add_hline(y=85, line_dash="dash", line_color="green", annotation_text="Target Efficiency (85%)")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not create cooling efficiency visualization: {str(e)}")
    
    # Row 4: Hot Spot Analysis
    st.subheader("Hot Spot Analysis")
    
    try:
        # Identify hot spots (temperature over 28°C)
        hot_spots = df[df['temperature'] > 28].groupby(['rack_id', 'location']).size().reset_index(name='occurrences')
        hot_spots = hot_spots.sort_values('occurrences', ascending=False).head(10)
        
        if not hot_spots.empty:
            fig = px.bar(
                hot_spots,
                x='rack_id',
                y='occurrences',
                color='location',
                labels={'rack_id': 'Rack ID', 'occurrences': 'Hot Spot Occurrences', 'location': 'Row'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hot spots detected in the selected time period.")
    except Exception as e:
        st.warning(f"Could not create hot spot analysis: {str(e)}")
    
    # Row 5: Predictive Analytics
    st.subheader("Resource Forecasting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Power Usage Forecast (Next 30 Days)")
        
        try:
            # Create a simple forecast
            last_date = df['timestamp'].max()
            forecast_dates = [last_date + timedelta(days=i) for i in range(1, 31)]
            
            # Simple forecast based on recent trend
            recent_data = df[df['timestamp'] >= last_date - timedelta(days=30)]
            power_avg = recent_data.groupby(recent_data['timestamp'].dt.date)['power_usage'].mean()
            
            if not power_avg.empty:
                # Create a simple trend (random walk with drift)
                np.random.seed(42)
                forecast_values = [power_avg.iloc[-1]]
                for i in range(1, 30):
                    forecast_values.append(max(0, forecast_values[-1] + np.random.normal(0.02, 0.1)))
                
                forecast_df = pd.DataFrame({
                    'date': forecast_dates,
                    'power_usage': forecast_values
                })
                
                # Historical data
                historical = df.groupby(df['timestamp'].dt.date)['power_usage'].mean().reset_index()
                historical.columns = ['date', 'power_usage']
                historical['type'] = 'Historical'
                forecast_df['type'] = 'Forecast'
                
                # Combine actual and forecast using concat
                combined_df = pd.concat([historical, forecast_df], axis=0)
                
                fig = px.line(
                    combined_df,
                    x='date',
                    y='power_usage',
                    color='type',
                    labels={'date': 'Date', 'power_usage': 'Average Power Usage (kW)', 'type': 'Data Type'},
                    color_discrete_map={'Historical': '#2E86C1', 'Forecast': '#FF7F50'}
                )
                
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Average Power Usage (kW)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#2C3E50')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data to generate forecast.")
        except Exception as e:
            st.warning(f"Could not create power usage forecast: {str(e)}")
    
    with col2:
        st.subheader("Capacity Planning")
        
        try:
            # Calculate future capacity needs
            current_utilization = df['cpu_utilization'].mean()
            projected_utilization = current_utilization * 1.15  # Assume 15% growth
            
            # Create a gauge chart with better color contrast
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=current_utilization,
                delta={'reference': 75, 'increasing': {'color': "#E74C3C"}, 'decreasing': {'color': "#27AE60"}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#2C3E50"},
                    'bar': {'color': "#2E86C1"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "#2C3E50",
                    'steps': [
                        {'range': [0, 50], 'color': '#A8E6CF'},  # Light green
                        {'range': [50, 70], 'color': '#FFD3B6'},  # Light orange
                        {'range': [70, 85], 'color': '#FFAAA5'},  # Darker orange
                        {'range': [85, 100], 'color': '#FF8B94'}  # Light red
                    ],
                    'threshold': {
                        'line': {'color': "#E74C3C", 'width': 4},
                        'thickness': 0.75,
                        'value': projected_utilization
                    }
                },
                title={'text': "Current CPU Utilization", 'font': {'color': "#2C3E50"}}
            ))
            
            fig.update_layout(
                paper_bgcolor='white',
                font={'color': "#2C3E50"},
                margin=dict(t=80, b=0)
            )
            
            fig.add_annotation(
                x=0.5,
                y=0.25,
                text=f"Projected: {projected_utilization:.1f}%",
                showarrow=False,
                font=dict(color="#2C3E50")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not create capacity planning visualization: {str(e)}")
    
    # Row 6: Network Topology
    st.subheader("Network Port Availability")
    
    # Sample data for network ports
    network_data = {
        'switch': ['Core-SW-01', 'Core-SW-02', 'Dist-SW-01', 'Dist-SW-02', 'Dist-SW-03', 'Dist-SW-04', 'Access-SW-01', 'Access-SW-02', 'Access-SW-03', 'Access-SW-04'],
        'total_ports': [48, 48, 24, 24, 24, 24, 48, 48, 48, 48],
        'used_ports': [45, 42, 20, 19, 22, 18, 35, 40, 32, 28]
    }
    
    network_df = pd.DataFrame(network_data)
    network_df['available_ports'] = network_df['total_ports'] - network_df['used_ports']
    network_df['utilization_pct'] = (network_df['used_ports'] / network_df['total_ports']) * 100
    
    fig = px.bar(
        network_df,
        x='switch',
        y=['used_ports', 'available_ports'],
        labels={'switch': 'Switch Name', 'value': 'Number of Ports', 'variable': 'Port Status'},
        title="Network Switch Port Utilization",
        color_discrete_map={'used_ports': 'blue', 'available_ports': 'green'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Recommendations
    st.subheader("AI-Powered Recommendations")
    
    recommendations = [
        "⚠️ Potential cooling issue detected in Row C, Rack-042. Schedule maintenance within 48 hours.",
        "💡 Redistribute workloads from Row A to Row E to balance power consumption and improve PUE.",
        "📊 Based on current growth patterns, additional capacity will be needed in approximately 45 days.",
        "🔋 Power consumption in Row B exceeds optimal thresholds during peak hours. Consider load balancing.",
        "🌡️ Three hot spots detected in the past week. Increasing cooling efficiency could reduce these by 85%."
    ]
    
    for i, rec in enumerate(recommendations):
        st.info(rec)

# Run the app
if __name__ == "__main__":
    main() 