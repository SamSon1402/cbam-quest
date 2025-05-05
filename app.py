import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="CBAM Quest: Aluminum Decarbonization Planner",
    page_icon="🎮",
    layout="wide",
)

# Add custom CSS directly
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');

:root {
    --coral-main: #FF6F61;
    --coral-dark: #E05A4F;
    --coral-light: #FF8577;
    --pixel-black: #0D1117;
    --pixel-blue: #2F3E75;
}

/* Global Styles */
.stApp {
    background-color: var(--pixel-black);
}

h1, h2, h3 {
    font-family: 'VT323', monospace !important;
    color: var(--coral-main) !important;
    text-shadow: 2px 2px 0px var(--coral-dark);
    letter-spacing: 1px;
}

p, li, .stMarkdown {
    font-family: 'Space Mono', monospace !important;
    color: #FFFFFF;
}

/* Button Styling */
.stButton>button {
    font-family: 'VT323', monospace !important;
    background-color: var(--coral-main);
    color: white;
    border: 4px solid var(--coral-dark);
    box-shadow: 4px 4px 0px var(--coral-dark);
    transition: all 0.1s ease;
}

.stButton>button:hover {
    box-shadow: 2px 2px 0px var(--coral-dark);
    transform: translate(2px, 2px);
}

/* Widget Styling */
.stSlider, .stSelectbox {
    border: 2px solid var(--coral-dark);
    padding: 4px;
}

.stSlider .stSlider>div>div {
    background-color: var(--coral-main) !important;
}

/* Metric Card */
.metric-container {
    background-color: var(--pixel-blue);
    border: 4px solid var(--coral-main);
    padding: 20px;
    border-radius: 0px;
    box-shadow: 8px 8px 0px var(--coral-dark);
    margin-bottom: 20px;
}

/* Progress Bar */
.stProgress > div > div {
    background-color: var(--coral-main) !important;
}

/* Divider */
hr {
    border-top: 4px dashed var(--coral-light);
}

/* Data tables */
.dataframe {
    font-family: 'Space Mono', monospace !important;
    border: 2px solid var(--coral-dark);
}

/* Sidebar */
.css-1d391kg {
    background-color: var(--pixel-blue);
}

/* Inputs */
.stTextInput>div>div>input {
    background-color: var(--pixel-black);
    color: white;
    border: 2px solid var(--coral-dark);
    font-family: 'Space Mono', monospace !important;
}

/* Multiselect */
.stMultiSelect>div>div>div:first-child {
    background-color: var(--pixel-black);
    border: 2px solid var(--coral-dark);
}

.stMultiSelect>div>div>div:first-child>div:first-child {
    font-family: 'Space Mono', monospace !important;
    color: white;
}

/* Achievement badges */
.achievement-badge {
    background-color: #38761d;
    border: 2px solid var(--coral-light);
    padding: 10px;
    font-family: 'VT323', monospace !important;
    margin-top: 10px;
}

/* Tooltips */
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted var(--coral-main);
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 120px;
    background-color: var(--pixel-blue);
    color: #fff;
    text-align: center;
    border: 2px solid var(--coral-main);
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -60px;
    opacity: 0;
    transition: opacity 0.3s;
    font-family: 'Space Mono', monospace !important;
    font-size: 12px;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

/* Animation for achievements */
@keyframes achievement-unlock {
    0% { transform: scale(0.5); opacity: 0; }
    70% { transform: scale(1.2); }
    100% { transform: scale(1); opacity: 1; }
}

.achievement-unlocked {
    animation: achievement-unlock 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; font-size: 52px;'>🎮 CBAM QUEST: ALUMINUM DECARBONIZATION PLANNER 🎮</h1>", unsafe_allow_html=True)

# UI Components Functions
def pixel_card(title, content_function):
    """Create a pixel-art styled card with title and content"""
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
    content_function()
    st.markdown('</div>', unsafe_allow_html=True)

def achievement_badge(title, condition, threshold):
    """Display an achievement badge if condition meets threshold"""
    if condition >= threshold:
        st.markdown(
            f'<div class="achievement-badge achievement-unlocked">'
            f'🏆 ACHIEVEMENT UNLOCKED: {title}'
            f'</div>',
            unsafe_allow_html=True
        )
        return True
    else:
        next_level = ""
        if condition > threshold * 0.5:
            next_level = f"You're {round((condition/threshold)*100)}% of the way there!"
        st.info(f"🔒 Next Achievement: {title} ({next_level})")
        return False

def retro_slider(label, min_val, max_val, default_val, key):
    """Create a slider with retro styling"""
    st.markdown(f"<p>{label}</p>", unsafe_allow_html=True)
    return st.slider(
        label, 
        min_value=min_val, 
        max_value=max_val, 
        value=default_val,
        key=key,
        label_visibility="collapsed"
    )

def retro_progress_bar(label, value, max_value):
    """Create a retro-styled progress bar"""
    st.markdown(f"<p>{label}</p>", unsafe_allow_html=True)
    st.progress(min(value / max_value, 1.0))

def control_panel_section(title):
    """Create a section header for the control panel"""
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)

def display_achievements(achievements):
    """Display a list of achievements"""
    if not achievements:
        st.info("No achievements unlocked yet. Keep exploring!")
        return
    
    st.markdown("<h3>ACHIEVEMENTS UNLOCKED</h3>", unsafe_allow_html=True)
    
    for i, achievement in enumerate(achievements):
        st.markdown(
            f'<div class="achievement-badge achievement-unlocked" style="animation-delay: {i*0.2}s">'
            f'{achievement.get("icon", "🏆")} {achievement.get("title", "Unknown")}'
            f'</div>',
            unsafe_allow_html=True
        )
        if "description" in achievement:
            st.markdown(f"<p><small>{achievement['description']}</small></p>", unsafe_allow_html=True)

# Data Processing Functions
def calculate_carbon_footprint(recycled_content, renewable_energy, process_efficiency):
    """Calculate carbon footprint based on parameters"""
    baseline = 2.1  # kg CO2e
    
    recycled_impact = (recycled_content - 40) * 0.01  # 40% is baseline
    energy_impact = renewable_energy * 0.005
    efficiency_impact = process_efficiency * 0.003
    
    footprint = baseline - recycled_impact - energy_impact - efficiency_impact
    return max(0.5, min(3.0, footprint))  # Constrain between 0.5-3.0

def calculate_implementation_costs(recycled_content, renewable_energy, process_efficiency):
    """Calculate implementation costs based on parameters"""
    recycled_cost = (recycled_content - 40) * 0.02 if recycled_content > 40 else 0
    energy_cost = renewable_energy * 0.03
    efficiency_cost = process_efficiency * 0.02
    
    total_cost = recycled_cost + energy_cost + efficiency_cost
    return max(0.5, min(5.0, total_cost))  # Constrain between 0.5-5.0

def generate_roadmap_phases(recycled_content, renewable_energy, process_efficiency):
    """Generate roadmap phases based on parameters"""
    phases = {
        "PHASE 1 (2025-2027)": [
            f"Increase recycled content to {min(recycled_content + 15, 100)}%",
            f"Transition {min(renewable_energy + 20, 100)}% energy to renewable sources",
            "Optimize transportation logistics (-15% emissions)"
        ],
        "PHASE 2 (2027-2029)": [
            f"Implement AI-driven process efficiency (+{min(process_efficiency + 15, 100)}%)",
            "Develop supplier certification program",
            "Convert 75% of facilities to low-carbon operations"
        ],
        "PHASE 3 (2029-2031)": [
            "Deploy advanced metal recovery technologies",
            "Achieve carbon neutrality at flagship plants",
            "Implement circular economy business model"
        ],
        "TARGET (2031-2033)": [
            "Achieve 90% recycled content across product lines",
            "100% renewable energy for all operations",
            "Full carbon neutrality across value chain"
        ]
    }
    
    return phases

# Visualization Functions
def create_cbam_heatmap(target_regions, carbon_price):
    """Create a heatmap of CBAM impacts"""
    regions = ["Europe", "UK", "Middle East", "Asia", "North America"]
    years = [2026, 2027, 2028, 2029, 2030]
    
    # Create sample data
    z = []
    for i, region in enumerate(regions):
        row = []
        for year in years:
            # Higher impact for earlier years and European regions
            impact = 5 - i * 0.8 - (year - 2026) * 0.3
            impact = max(0, min(5, impact))  # Constrain between 0-5
            row.append(impact)
        z.append(row)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=years,
        y=regions,
        colorscale=[
            [0, "#FFE1DE"], [0.2, "#FFCCC2"], 
            [0.4, "#FFA799"], [0.6, "#FF8577"], 
            [0.8, "#FF6F61"], [1, "#C8412E"]
        ],
        showscale=False
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    return fig

def create_decarbonization_roadmap(recycled_content, renewable_energy, process_efficiency):
    """Create a roadmap chart"""
    years = [2025, 2027, 2029, 2031, 2033]
    
    # Calculate reduction trajectory based on sliders
    avg_improvement = (recycled_content + renewable_energy + process_efficiency) / 300
    reductions = [
        100,  # Start at baseline
        max(10, 100 - avg_improvement * 25),  # Phase 1
        max(10, 100 - avg_improvement * 50),  # Phase 2
        max(10, 100 - avg_improvement * 75),  # Phase 3
        max(10, 100 - avg_improvement * 100)  # Target
    ]
    
    fig = go.Figure()
    
    # Add timeline base
    fig.add_shape(
        type="line",
        x0=years[0], y0=50,
        x1=years[-1], y1=50,
        line=dict(color="#FF6F61", width=4)
    )
    
    # Add milestone points
    for i, year in enumerate(years):
        fig.add_trace(go.Scatter(
            x=[year],
            y=[50],
            mode="markers",
            marker=dict(size=15, color=["#FF6F61", "#FF8577", "#FFA799", "#FFCCC2", "#FFE1DE"][i]),
            showlegend=False
        ))
    
    # Add reduction line
    fig.add_trace(go.Scatter(
        x=years,
        y=[55 - r * 0.4 for r in reductions],  # Position above timeline
        mode="lines+markers",
        line=dict(color="white", width=3, dash="dash"),
        marker=dict(size=10, color="white"),
        showlegend=False
    ))
    
    # Add year labels
    for i, year in enumerate(years):
        fig.add_annotation(
            x=year,
            y=35,  # Position below timeline
            text=str(year),
            showarrow=False,
            font=dict(family="Space Mono", size=12, color="white")
        )
    
    # Add milestone flags
    for i, year in enumerate(years):
        height = 20 - reductions[i] * 0.15  # Higher flag for better reduction
        flag_color = ["#FF6F61", "#FF8577", "#FFA799", "#FFCCC2", "#FFE1DE"][i]
        
        # Flag pole
        fig.add_shape(
            type="rect",
            x0=year-2, y0=50,
            x1=year+2, y1=50+height,
            fillcolor=flag_color,
            line=dict(color=flag_color)
        )
        
        # Flag triangle
        fig.add_shape(
            type="path",
            path=f"M {year-2} {50+height} L {year+2} {50+height} L {year} {50+height+10} Z",
            fillcolor=flag_color,
            line=dict(color=flag_color)
        )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[2024, 2034]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, 100]
        )
    )
    
    return fig

def create_benchmark_radar(recycled_content, renewable_energy, process_efficiency):
    """Create a radar chart comparing to industry benchmarks"""
    categories = ["Recycled %", "Energy", "Transport", "Process", "Materials"]
    
    # Calculate our performance based on sliders
    # Scale from 0-100 to 0-5 for radar chart
    our_values = [
        recycled_content / 20,  # Recycled content (0-5)
        renewable_energy / 20,   # Energy (0-5)
        3.5,  # Transport (fixed value for demo)
        process_efficiency / 20,  # Process (0-5)
        4.2   # Materials (fixed value for demo)
    ]
    
    # Industry average (placeholder)
    industry_values = [3.0, 2.5, 2.2, 2.8, 2.3]
    
    fig = go.Figure()
    
    # Add industry average
    fig.add_trace(go.Scatterpolar(
        r=industry_values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255,133,119,0.2)',
        line=dict(color="#FF8577", width=2, dash="dash"),
        name="Industry Average"
    ))
    
    # Add our performance
    fig.add_trace(go.Scatterpolar(
        r=our_values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255,111,97,0.5)',
        line=dict(color="#FF6F61", width=3),
        name="Crown"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['1', '2', '3', '4', '5'],
                tickangle=0,
                gridcolor='rgba(255, 255, 255, 0.2)',
                linecolor='rgba(255, 255, 255, 0.2)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)',
                linecolor='rgba(255, 255, 255, 0.2)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            x=0.5,
            y=1.2,
            xanchor="center",
            orientation="h",
            font=dict(family="Space Mono", size=12, color="white")
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=40, b=40),
    )
    
    return fig

def create_scenario_results_chart(baseline_emissions, projected_emissions):
    """Create a bar chart comparing baseline and projected emissions"""
    fig = go.Figure()
    
    # Add baseline bar
    fig.add_trace(go.Bar(
        x=["Baseline"],
        y=[baseline_emissions],
        name="Baseline",
        marker_color="#C8412E",
        text=[f"{baseline_emissions:,} tCO₂e"],
        textposition="outside",
        textfont=dict(family="Space Mono", size=12, color="white")
    ))
    
    # Add projected bar
    fig.add_trace(go.Bar(
        x=["Projected"],
        y=[projected_emissions],
        name="Projected",
        marker_color="#FF6F61",
        text=[f"{int(projected_emissions):,} tCO₂e"],
        textposition="outside",
        textfont=dict(family="Space Mono", size=12, color="white")
    ))
    
    # Calculate and display reduction arrow
    reduction = baseline_emissions - projected_emissions
    reduction_percent = (reduction / baseline_emissions) * 100
    
    fig.add_annotation(
        x=0.5,
        y=baseline_emissions + 5000,
        text=f"↓ {reduction:,.0f} tCO₂e ({reduction_percent:.1f}%)",
        showarrow=False,
        font=dict(family="VT323", size=18, color="#FF6F61")
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(
            title="",
            tickfont=dict(family="Space Mono", size=12, color="white")
        ),
        yaxis=dict(
            title="Emissions (tCO₂e)",
            titlefont=dict(family="Space Mono", size=12, color="white"),
            tickfont=dict(family="Space Mono", size=10, color="white"),
            gridcolor='rgba(255, 255, 255, 0.1)'
        )
    )
    
    return fig

# Card Content Functions
def cbam_heatmap_content():
    st.plotly_chart(
        create_cbam_heatmap(target_regions, carbon_price),
        use_container_width=True
    )

def carbon_intensity_content():
    st.markdown("<h3>Material Components</h3>", unsafe_allow_html=True)
    
    # Material breakdown chart
    component_data = {
        "Component": ["Aluminum", "Coatings", "Inks", "Other"],
        "Percentage": [68, 12, 8, 12],
        "Color": ["#FF6F61", "#FF8577", "#FFA799", "#FFCCC2"]
    }
    
    st.plotly_chart(
        px.bar(
            component_data,
            x="Percentage",
            y="Component",
            orientation='h',
            color="Component",
            color_discrete_map=dict(zip(component_data["Component"], component_data["Color"])),
            labels={"Percentage": "% of Total Weight"}
        ).update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='VT323', size=14),
            showlegend=False
        ),
        use_container_width=True
    )
    
    # Carbon footprint
    carbon_footprint = calculate_carbon_footprint(
        recycled_content=recycled_content,
        renewable_energy=renewable_energy,
        process_efficiency=process_efficiency
    )
    
    st.markdown(f"<h3 style='text-align: center; color: #FF6F61;'>CARBON FOOTPRINT: {carbon_footprint:.2f} kg CO₂e</h3>", unsafe_allow_html=True)
    
    # Recycled content slider display
    st.markdown("<p>Recycled Content:</p>", unsafe_allow_html=True)
    st.progress(recycled_content/100)

def decarbonization_roadmap_content():
    st.plotly_chart(
        create_decarbonization_roadmap(
            recycled_content=recycled_content,
            renewable_energy=renewable_energy,
            process_efficiency=process_efficiency
        ),
        use_container_width=True
    )
    
    # Phase details
    phases = generate_roadmap_phases(
        recycled_content=recycled_content,
        renewable_energy=renewable_energy,
        process_efficiency=process_efficiency
    )
    
    selected_phase = st.selectbox(
        "Select Phase for Details",
        options=list(phases.keys()),
        key="phase_selector"
    )
    
    st.markdown(f"<h3>{selected_phase}:</h3>", unsafe_allow_html=True)
    
    for action in phases[selected_phase]:
        st.markdown(f"• {action}", unsafe_allow_html=True)

def benchmarking_content():
    st.plotly_chart(
        create_benchmark_radar(
            recycled_content=recycled_content,
            renewable_energy=renewable_energy,
            process_efficiency=process_efficiency
        ),
        use_container_width=True
    )

def scenario_results_content():
    col_chart, col_impact = st.columns([3, 2])
    
    # Calculate projected emissions based on sliders
    projected_emissions = baseline_emissions - (baseline_emissions * (recycled_content + renewable_energy + process_efficiency) / 300)
    
    # Financial impact
    baseline_cbam_fees = baseline_emissions * carbon_price / 1000000  # Convert to millions
    projected_cbam_fees = projected_emissions * carbon_price / 1000000  # Convert to millions
    implementation_cost = calculate_implementation_costs(
        recycled_content=recycled_content,
        renewable_energy=renewable_energy,
        process_efficiency=process_efficiency
    )
    net_savings = baseline_cbam_fees - projected_cbam_fees - implementation_cost/3  # Amortized over 3 years
    
    # Emissions chart
    with col_chart:
        st.plotly_chart(
            create_scenario_results_chart(
                baseline_emissions=baseline_emissions,
                projected_emissions=projected_emissions
            ),
            use_container_width=True
        )
    
    # Financial impact
    with col_impact:
        st.markdown("<h3>FINANCIAL IMPACT:</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>CBAM Fees: €{baseline_cbam_fees:.1f}M → €{projected_cbam_fees:.1f}M</p>", unsafe_allow_html=True)
        st.markdown(f"<p>Implementation Cost: €{implementation_cost:.1f}M</p>", unsafe_allow_html=True)
        st.markdown(f"<p>Net Savings: €{net_savings:.1f}M/year</p>", unsafe_allow_html=True)
        
        # Unlock achievement if significant savings
        if net_savings >= 1.0:
            achievement_badge(
                "CBAM COST OPTIMIZER",
                net_savings,
                1.0  # Threshold for achievement
            )

# Sidebar with game controller aesthetic
with st.sidebar:
    st.markdown("<h2>CONTROL PANEL</h2>", unsafe_allow_html=True)
    
    # CBAM Settings section
    control_panel_section("CBAM SETTINGS")
    
    carbon_price = st.slider(
        "Carbon Price (€/tCO₂e)",
        min_value=50,
        max_value=150,
        value=90,
        step=5
    )
    
    target_regions = st.multiselect(
        "Target Regions",
        options=["Europe", "UK", "Middle East", "Asia", "North America"],
        default=["Europe"]
    )
    
    # Roadmap Progress section
    control_panel_section("ROADMAP PROGRESS")
    
    # Calculate current progress
    current_progress = 30  # This would be calculated based on actual data in a real app
    
    retro_progress_bar("Decarbonization Progress", current_progress, 100)
    st.markdown(f"<p>Progress: {current_progress}% Complete</p>", unsafe_allow_html=True)
    
    # Achievement display
    achievements = []
    if current_progress >= 25:
        achievements.append({
            "title": "TIER 1 CBAM DEFENDER",
            "description": "Achieved 25% reduction in CBAM exposure",
            "icon": "🏆"
        })
    
    display_achievements(achievements)
    
    # Impact Simulator section
    control_panel_section("IMPACT SIMULATOR")
    
    recycled_content = retro_slider(
        "Recycled Content %",
        0,
        100,
        60,
        "recycled_slider"
    )
    
    renewable_energy = retro_slider(
        "Renewable Energy %",
        0,
        100,
        40,
        "energy_slider"
    )
    
    process_efficiency = retro_slider(
        "Process Efficiency %",
        0,
        100,
        50,
        "efficiency_slider"
    )
    
    # Calculate CBAM fee reduction based on sliders
    baseline_emissions = 125000  # tCO2e - would be calculated from data in real app
    recycled_impact = baseline_emissions * (recycled_content - 40) / 100 * 0.005  # Example formula
    energy_impact = baseline_emissions * renewable_energy / 100 * 0.003
    efficiency_impact = baseline_emissions * process_efficiency / 100 * 0.002
    
    total_reduction = recycled_impact + energy_impact + efficiency_impact
    cbam_reduction = total_reduction * carbon_price / 1000  # Convert to millions of euros
    
    st.markdown("<p>CBAM Fee Reduction:</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-family: VT323, monospace; font-size: 24px; color: #FF6F61;'>- €{cbam_reduction:.2f}M</p>", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns(2)

with col1:
    # CBAM Impact Heatmap
    pixel_card("CBAM IMPACT HEATMAP", cbam_heatmap_content)
    
    # Carbon Intensity Calculator
    pixel_card("CARBON INTENSITY CALCULATOR", carbon_intensity_content)

with col2:
    # Decarbonization Roadmap
    pixel_card("DECARBONIZATION ROADMAP", decarbonization_roadmap_content)
    
    # Industry Benchmarking
    pixel_card("INDUSTRY BENCHMARKING", benchmarking_content)

# Bottom section - Scenario Results
st.markdown("<h2>DECARBONIZATION SCENARIO RESULTS</h2>", unsafe_allow_html=True)

# Scenario results card
pixel_card("DECARBONIZATION SCENARIO RESULTS", scenario_results_content)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Created for Crown Holdings - Sustainability Data Analyst Internship</p>", 
    unsafe_allow_html=True
)