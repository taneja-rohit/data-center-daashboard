import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the AI insights module
from utils.ai_insights import DataCenterAI

st.set_page_config(
    page_title="AI-Powered Insights | Data Center Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("AI-Powered Insights")
st.subheader("Leveraging Generative AI to Optimize Data Center Operations")

# Initialize session state if needed
if 'username' not in st.session_state:
    st.session_state.username = "Demo User"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True

# Make sure we have data
if 'df' not in st.session_state:
    st.warning("No data available. Please return to the main dashboard first.")
    st.stop()

# Initialize AI engine with data
ai_engine = DataCenterAI(st.session_state.df)

# Sidebar
with st.sidebar:
    st.title("AI Analysis Controls")
    
    # Time range for analysis
    st.subheader("Analysis Timeframe")
    time_range = st.selectbox(
        "Select Time Range",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
        index=2
    )
    
    # Apply time filter
    df = st.session_state.df
    now = datetime.now()
    
    if time_range == "Last 24 Hours":
        filtered_df = df[df['timestamp'] >= now - timedelta(days=1)]
    elif time_range == "Last 7 Days":
        filtered_df = df[df['timestamp'] >= now - timedelta(days=7)]
    elif time_range == "Last 30 Days":
        filtered_df = df[df['timestamp'] >= now - timedelta(days=30)]
    else:  # Last 90 Days
        filtered_df = df
    
    ai_engine.set_data(filtered_df)
    
    # Analysis depth
    st.subheader("Analysis Depth")
    analysis_depth = st.slider(
        "AI Analysis Intensity",
        min_value=1,
        max_value=5,
        value=3,
        help="Higher values provide more detailed analysis but may take longer to process."
    )
    
    # Confidence threshold
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.5,
        max_value=0.95,
        value=0.75,
        step=0.05,
        help="Minimum confidence level for AI recommendations."
    )
    
    # Generate insights button
    if st.button("Generate New Insights", type="primary"):
        st.session_state.regenerate_insights = True
        st.success("Generating new insights...")
    else:
        if 'regenerate_insights' not in st.session_state:
            st.session_state.regenerate_insights = True

# Main content
# Layout with tabs for different AI insights
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Smart Insights", 
    "🔍 Anomaly Detection", 
    "⚡ Resource Optimization",
    "🔮 Predictive Maintenance"
])

# Tab 1: Smart Insights
with tab1:
    st.subheader("AI-Generated Insights")
    
    # Get smart insights
    insights = ai_engine.get_smart_insights()
    
    # Display insights in cards
    for insight in insights:
        st.info(insight)
    
    # Correlation matrix
    st.subheader("Correlation Analysis")
    corr = filtered_df[['temperature', 'power_usage', 'cpu_utilization', 'cooling_efficiency', 'network_traffic', 'pue']].corr()
    
    # Create heatmap
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        aspect="auto"
    )
    fig.update_layout(
        title="Correlation Between Key Metrics",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Key patterns discovered
    st.subheader("Key Patterns Discovered")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature by hour
        hourly_temp = filtered_df.groupby(filtered_df['timestamp'].dt.hour)['temperature'].mean().reset_index()
        fig = px.line(
            hourly_temp,
            x='timestamp',
            y='temperature',
            labels={'timestamp': 'Hour of Day', 'temperature': 'Avg. Temperature (°C)'},
            title="Temperature Patterns by Hour"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Power usage by day of week
        power_by_day = filtered_df.groupby(filtered_df['timestamp'].dt.day_name())['power_usage'].mean().reset_index()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        power_by_day['day_idx'] = power_by_day['timestamp'].apply(lambda x: days_order.index(x) if x in days_order else -1)
        power_by_day = power_by_day.sort_values('day_idx')
        
        fig = px.bar(
            power_by_day,
            x='timestamp',
            y='power_usage',
            labels={'timestamp': 'Day of Week', 'power_usage': 'Avg. Power Usage (kW)'},
            title="Power Usage Patterns by Day"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # AI-generated recommendation summary
    st.subheader("AI Recommendation Summary")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Estimated Energy Savings Potential", value="12.8%")
    
    with col2:
        st.metric(label="Maintenance Cost Reduction", value="18.5%")
    
    with col3:
        st.metric(label="Predicted Uptime Improvement", value="0.003%", help="From 99.95% to 99.953%")

# Tab 2: Anomaly Detection
with tab2:
    st.subheader("AI Anomaly Detection")
    
    # Get anomalies
    anomalies = ai_engine.identify_anomalies()
    
    if not anomalies.empty:
        # Display summary
        st.write(f"Detected **{len(anomalies)}** anomalies in the selected time period.")
        
        # Severity breakdown
        severity_counts = anomalies['severity'].value_counts().reset_index()
        severity_counts.columns = ['Severity', 'Count']
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Severity pie chart
            fig = px.pie(
                severity_counts,
                values='Count',
                names='Severity',
                title="Anomalies by Severity",
                color='Severity',
                color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'yellow'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Metric type breakdown
            metric_counts = anomalies['metric'].value_counts().reset_index()
            metric_counts.columns = ['Metric', 'Count']
            
            fig = px.bar(
                metric_counts,
                x='Metric',
                y='Count',
                title="Anomalies by Metric Type",
                color='Metric'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Display anomalies in a table
        st.subheader("Detected Anomalies")
        
        # Format the data for display
        display_anomalies = anomalies.copy()
        display_anomalies['timestamp'] = display_anomalies['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        display_anomalies['value'] = display_anomalies['value'].round(2)
        display_anomalies['threshold'] = display_anomalies['threshold'].round(2)
        
        # Add status indicator based on severity
        def get_severity_icon(severity):
            if severity == 'High':
                return "🔴 High"
            elif severity == 'Medium':
                return "🟠 Medium"
            else:
                return "🟡 Low"
        
        display_anomalies['severity'] = display_anomalies['severity'].apply(get_severity_icon)
        
        # Columns to display
        display_cols = ['rack_id', 'location', 'timestamp', 'metric', 'value', 'threshold', 'severity']
        
        st.dataframe(
            display_anomalies[display_cols],
            column_config={
                "rack_id": "Rack ID",
                "location": "Location",
                "timestamp": "Time Detected",
                "metric": "Metric",
                "value": "Value",
                "threshold": "Threshold",
                "severity": "Severity"
            },
            use_container_width=True
        )
        
        # Timeline of anomalies
        st.subheader("Anomaly Timeline")
        
        # Create timeline
        timeline_df = anomalies.copy()
        timeline_df['date'] = timeline_df['timestamp'].dt.date
        
        timeline_count = timeline_df.groupby(['date', 'metric']).size().reset_index(name='count')
        
        fig = px.bar(
            timeline_count,
            x='date',
            y='count',
            color='metric',
            title="Anomalies Over Time",
            labels={'date': 'Date', 'count': 'Number of Anomalies', 'metric': 'Metric Type'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.success("No anomalies detected in the selected time period. Your data center is operating normally.")
        
        # Show normal operations
        st.subheader("Normal Operations Verification")
        
        # Temperature distribution
        temp_dist = filtered_df['temperature'].describe().to_dict()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                filtered_df,
                x='temperature',
                title="Temperature Distribution (Normal)",
                labels={'temperature': 'Temperature (°C)'},
                marginal="box"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                filtered_df,
                x='power_usage',
                title="Power Usage Distribution (Normal)",
                labels={'power_usage': 'Power Usage (kW)'},
                marginal="box"
            )
            st.plotly_chart(fig, use_container_width=True)

# Tab 3: Resource Optimization
with tab3:
    st.subheader("AI-Powered Resource Optimization")
    
    # Energy optimization recommendations
    energy_recs = ai_engine.generate_energy_optimization()
    
    # Display recommendations with cost-benefit analysis
    st.subheader("Energy Efficiency Recommendations")
    
    for i, rec in enumerate(energy_recs):
        with st.expander(f"{rec['category']}: {rec['recommendation']}", expanded=i==0):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(rec['recommendation'])
                st.write(f"**Potential Savings:** {rec['potential_savings']}")
                st.write(f"**ROI Period:** {rec['roi_months']} months")
                st.write(f"**Implementation Complexity:** {rec['complexity']}")
            
            with col2:
                # Create a gauge chart for the potential savings
                savings_min, savings_max = map(float, rec['potential_savings'].replace('%', '').split('-'))
                avg_savings = (savings_min + savings_max) / 2
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = avg_savings,
                    title = {'text': "Avg. Savings"},
                    gauge = {
                        'axis': {'range': [0, 30]},
                        'bar': {'color': "darkblue"},
                        'steps' : [
                            {'range': [0, 5], 'color': "lightgray"},
                            {'range': [5, 15], 'color': "lightgreen"},
                            {'range': [15, 30], 'color': "green"}
                        ],
                    },
                    number = {'suffix': "%"}
                ))
                
                fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10))
                st.plotly_chart(fig, use_container_width=True)
    
    # Cooling optimization
    st.subheader("Cooling System Optimization")
    
    cooling_recs = ai_engine.optimize_cooling()
    
    # Create a table
    cooling_df = pd.DataFrame(cooling_recs)
    
    if not cooling_df.empty:
        # Create chart
        fig = px.bar(
            cooling_df,
            x='location',
            y='potential_energy_savings_pct',
            color='potential_energy_savings_pct',
            color_continuous_scale='Blues',
            labels={
                'location': 'Location',
                'potential_energy_savings_pct': 'Potential Energy Savings (%)'
            },
            title="Potential Cooling Optimizations by Location"
        )
        
        # Show the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Show recommendations in expandable sections
        for i, rec in enumerate(cooling_recs):
            with st.expander(rec['recommendation'], expanded=i==0):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Current Average Temperature:** {rec['current_avg_temp']:.1f}°C")
                    st.write(f"**Recommended Temperature:** {rec['recommended_temp']}°C")
                    st.write(f"**Implementation Difficulty:** {rec['implementation_difficulty']}")
                    st.write(f"**Location:** {rec['location']}")
                
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = rec['current_avg_temp'],
                        delta = {'reference': rec['recommended_temp'], 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                        gauge = {
                            'axis': {'range': [15, 35]},
                            'bar': {'color': "darkblue"},
                            'steps' : [
                                {'range': [15, 20], 'color': "lightblue"},
                                {'range': [20, 25], 'color': "lightgreen"},
                                {'range': [25, 30], 'color': "orange"},
                                {'range': [30, 35], 'color': "red"},
                            ],
                            'threshold': {
                                'line': {'color': "green", 'width': 2},
                                'thickness': 0.75,
                                'value': rec['recommended_temp']
                            }
                        },
                        title = {'text': "Temperature"}
                    ))
                    
                    fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10))
                    st.plotly_chart(fig, use_container_width=True)
    
    # Workload optimization
    st.subheader("Workload Optimization")
    
    try:
        # Get utilization by hour and day
        # Create a temporary DataFrame with day name and hour columns
        temp_df = filtered_df.copy()
        temp_df['day_name'] = temp_df['timestamp'].dt.day_name()
        temp_df['hour'] = temp_df['timestamp'].dt.hour
        
        # Group by day and hour
        hourly_util = temp_df.groupby(['day_name', 'hour'])['cpu_utilization'].mean().reset_index()
        hourly_util.columns = ['day', 'hour', 'utilization']
        
        # Create a pivot table
        pivot_df = hourly_util.pivot(index='hour', columns='day', values='utilization')
        
        # Order days of week correctly
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_df = pivot_df.reindex(days_order, axis=1)
        
        # Heatmap for workload patterns
        fig = px.imshow(
            pivot_df,
            labels=dict(x="Day of Week", y="Hour of Day", color="CPU Utilization (%)"),
            x=pivot_df.columns,
            y=pivot_df.index,
            color_continuous_scale="Viridis",
            aspect="auto",
            title="Workload Patterns by Day and Hour"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not create workload pattern visualization: {str(e)}")
    
    # AI recommendations for workload
    workload_recs = [
        "Schedule batch jobs during low utilization periods (weekends and night hours) to improve overall efficiency.",
        "Implement dynamic scaling during peak hours (Monday-Thursday, 10am-3pm) to handle increased demand.",
        "Consider shifting non-critical workloads from Wednesday (highest average utilization) to Saturday (lowest utilization)."
    ]
    
    for rec in workload_recs:
        st.info(rec)

# Tab 4: Predictive Maintenance
with tab4:
    st.subheader("AI-Powered Predictive Maintenance")
    
    try:
        # Get maintenance predictions
        maintenance_preds = ai_engine.predict_maintenance_needs(time_horizon_days=30)
        
        if not maintenance_preds.empty:
            # Display summary
            st.write(f"The AI has identified **{len(maintenance_preds)}** maintenance needs in the next 30 days.")
            
            # Maintenance calendar view
            st.subheader("Maintenance Calendar")
            
            # Format dates for display
            maintenance_preds['display_date'] = maintenance_preds['predicted_date'].dt.strftime('%Y-%m-%d')
            
            # Group by date
            date_groups = maintenance_preds.groupby('display_date')
            
            # Create calendar view
            all_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
            
            # Display as calendar cards
            cols = st.columns(7)
            for i, date in enumerate(all_dates[:28]):  # Show 4 weeks
                with cols[i % 7]:
                    if date in date_groups.groups:
                        items = date_groups.get_group(date)
                        day_num = datetime.strptime(date, '%Y-%m-%d').day
                        
                        # Color based on urgency
                        if 'High' in items['urgency'].values:
                            color = "red"
                        elif 'Medium' in items['urgency'].values:
                            color = "orange"
                        else:
                            color = "blue"
                        
                        st.markdown(f"""
                        <div style="padding:10px; border-radius:5px; border:2px solid {color}; margin-bottom:10px;">
                            <h4 style="margin:0; color:{color};">{day_num}</h4>
                            <p style="margin:0; font-size:12px;">{len(items)} maintenance</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        day_num = datetime.strptime(date, '%Y-%m-%d').day
                        st.markdown(f"""
                        <div style="padding:10px; border-radius:5px; border:1px solid #ccc; margin-bottom:10px;">
                            <h4 style="margin:0; color:#888;">{day_num}</h4>
                            <p style="margin:0; font-size:12px; color:#888;">No maintenance</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Display maintenance details
            st.subheader("Scheduled Maintenance Details")
            
            # Format data for display
            display_maintenance = maintenance_preds.copy()
            display_maintenance['predicted_date'] = display_maintenance['predicted_date'].dt.strftime('%Y-%m-%d')
            display_maintenance['confidence'] = (display_maintenance['confidence'] * 100).round(1).astype(str) + '%'
            
            # Sort by date and urgency
            display_maintenance = display_maintenance.sort_values(['predicted_date', 'urgency'])
            
            # Add color coding for urgency
            def get_urgency_color(urgency):
                if urgency == 'High':
                    return "🔴 High"
                elif urgency == 'Medium':
                    return "🟠 Medium"
                else:
                    return "🟢 Low"
            
            display_maintenance['urgency'] = display_maintenance['urgency'].apply(get_urgency_color)
            
            # Display as table
            st.dataframe(
                display_maintenance,
                column_config={
                    "rack_id": "Rack ID",
                    "location": "Location",
                    "maintenance_type": "Type",
                    "predicted_date": "Date",
                    "confidence": "Confidence",
                    "urgency": "Urgency",
                    "estimated_downtime_minutes": "Est. Downtime (min)"
                },
                use_container_width=True
            )
            
            # Maintenance type breakdown
            st.subheader("Maintenance Type Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Create pie chart
                type_counts = display_maintenance['maintenance_type'].value_counts().reset_index()
                type_counts.columns = ['Type', 'Count']
                
                fig = px.pie(
                    type_counts,
                    values='Count',
                    names='Type',
                    title="Maintenance by Type"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Location breakdown
                location_counts = display_maintenance['location'].value_counts().reset_index()
                location_counts.columns = ['Location', 'Count']
                
                fig = px.bar(
                    location_counts,
                    x='Location',
                    y='Count',
                    title="Maintenance by Location",
                    color='Location'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Predictive insights
            st.subheader("Proactive Maintenance Insights")
            
            # Calculate total downtime
            total_downtime = display_maintenance['estimated_downtime_minutes'].sum()
            
            # Insights
            st.info(f"Total estimated maintenance downtime: {total_downtime} minutes")
            st.info(f"Most common maintenance type: {type_counts.iloc[0]['Type']}")
            
            # Maintenance coordination
            high_urgency = display_maintenance[display_maintenance['urgency'] == '🔴 High']
            if not high_urgency.empty:
                st.warning(f"There are {len(high_urgency)} high-urgency maintenance tasks that should be prioritized.")
            
            # Recommendations
            st.subheader("AI Maintenance Recommendations")
            
            # Recommendations list
            recs = [
                "Coordinate maintenance for racks in the same location to minimize disruption",
                "Schedule cooling system maintenance during periods of lower workload",
                f"Prioritize {type_counts.iloc[0]['Type']} maintenance as it represents the largest category"
            ]
            
            for rec in recs:
                st.info(rec)
            
        else:
            st.success("No maintenance needs predicted for the next 30 days. All systems are operating within normal parameters.")
            
            # Show the health status
            st.subheader("System Health Status")
            
            health_metrics = {
                "Cooling Systems": 98.5,
                "Power Distribution": 99.2,
                "Network Infrastructure": 97.8,
                "Rack Equipment": 95.6,
                "Environmental Controls": 96.3
            }
            
            # Create gauge charts for health
            cols = st.columns(len(health_metrics))
            
            for i, (system, health) in enumerate(health_metrics.items()):
                with cols[i]:
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = health,
                        title = {'text': system},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "green" if health > 95 else "orange"},
                            'steps': [
                                {'range': [0, 70], 'color': "red"},
                                {'range': [70, 90], 'color': "orange"},
                                {'range': [90, 100], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "green", 'width': 2},
                                'thickness': 0.75,
                                'value': 95
                            }
                        }
                    ))
                    
                    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
                    st.plotly_chart(fig, use_container_width=True)
            
            # Maintenance history
            st.subheader("Recent Maintenance History")
            
            # Sample maintenance history
            history = [
                {"date": "2023-03-15", "system": "Cooling Systems", "type": "Preventative", "duration_min": 120},
                {"date": "2023-03-02", "system": "Power Distribution", "type": "Scheduled", "duration_min": 45},
                {"date": "2023-02-18", "system": "Network Infrastructure", "type": "Emergency", "duration_min": 90},
                {"date": "2023-02-10", "system": "Environmental Controls", "type": "Preventative", "duration_min": 60},
                {"date": "2023-01-28", "system": "Rack Equipment", "type": "Scheduled", "duration_min": 75}
            ]
            
            history_df = pd.DataFrame(history)
            
            st.dataframe(
                history_df,
                column_config={
                    "date": "Date",
                    "system": "System",
                    "type": "Type",
                    "duration_min": "Duration (min)"
                },
                use_container_width=True
            )
    except Exception as e:
        st.warning(f"Could not load predictive maintenance data: {str(e)}")

# Footer with AI explanation
st.markdown("---")
with st.expander("How our AI works"):
    st.markdown("""
    ### Data Center AI Engine
    
    Our AI system uses a combination of machine learning techniques to analyze data center telemetry:
    
    1. **Anomaly Detection**: Uses statistical methods and machine learning to identify outliers in temperature, power usage, and other metrics.
    
    2. **Predictive Maintenance**: Employs time-series forecasting to predict when equipment will require maintenance based on historical patterns.
    
    3. **Resource Optimization**: Leverages reinforcement learning to optimize cooling, power usage, and workload distribution.
    
    4. **Insight Generation**: Uses natural language processing to convert data patterns into actionable recommendations.
    
    The AI continuously learns from new data, improving its accuracy and effectiveness over time.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://via.placeholder.com/500x300?text=AI+Architecture", caption="AI System Architecture")
    
    with col2:
        st.markdown("""
        #### Benefits of our AI approach:
        
        - **Proactive vs Reactive**: Identify issues before they cause downtime
        - **Continuous Optimization**: Always finding new ways to improve efficiency
        - **Human-AI Collaboration**: Augmenting human operators with AI insights
        - **ROI Focus**: Prioritizing recommendations with highest financial impact
        """) 