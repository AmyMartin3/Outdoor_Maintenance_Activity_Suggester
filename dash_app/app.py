"""
Outdoor Maintenance Activity Suggester Dashboard
A Dash app that recommends outdoor maintenance activities based on real-time weather data
"""
import os
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from supabase_client import (
    get_maintenance_schedule, 
    get_current_weather,
    get_maintenance_activities
)

# Load environment variables
load_dotenv()

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Outdoor Maintenance Activity Suggester"

# Define the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🏡 Outdoor Maintenance Activity Suggester", 
                style={'textAlign': 'center', 'marginBottom': 10}),
        html.P("Real-time weather-based recommendations for outdoor home maintenance tasks",
               style={'textAlign': 'center', 'color': '#666', 'marginBottom': 20})
    ], style={'backgroundColor': '#f8f9fa', 'padding': 20, 'borderRadius': 8}),
    
    # Refresh button and last updated timestamp
    html.Div([
        html.Button('🔄 Refresh Data', id='refresh-button', 
                   style={'padding': '10px 20px', 'fontSize': 16, 'cursor': 'pointer'}),
        html.Span(id='last-updated', style={'marginLeft': 20, 'color': '#666'})
    ], style={'marginBottom': 20, 'display': 'flex', 'alignItems': 'center'}),
    
    # Main content - two column layout
    html.Div([
        # Left column - Recommended activities
        html.Div([
            html.H2("✅ Recommended Activities (Next 8 Hours)", 
                   style={'fontSize': 20, 'marginBottom': 15}),
            html.Div(id='recommendations-container',
                    style={'minHeight': 300, 'borderRadius': 8, 'border': '1px solid #ddd', 
                          'padding': 15, 'backgroundColor': '#fff'})
        ], style={'flex': 1, 'marginRight': 15}),
        
        # Right column - Weather info
        html.Div([
            html.H2("🌤️ Current & Forecast Weather", 
                   style={'fontSize': 20, 'marginBottom': 15}),
            html.Div(id='weather-container',
                    style={'minHeight': 300, 'borderRadius': 8, 'border': '1px solid #ddd',
                          'padding': 15, 'backgroundColor': '#fff'})
        ], style={'flex': 1})
    ], style={'display': 'flex', 'marginBottom': 20}),
    
    # Charts section
    html.Div([
        html.H2("📊 Weather Forecast Trends", style={'fontSize': 20, 'marginBottom': 15}),
        dcc.Tabs([
            dcc.Tab(label='Temperature & Precipitation', children=[
                dcc.Graph(id='temp-precip-chart')
            ]),
            dcc.Tab(label='Wind Speed', children=[
                dcc.Graph(id='wind-chart')
            ]),
            dcc.Tab(label='Activity Recommendations Timeline', children=[
                dcc.Graph(id='activities-timeline-chart')
            ])
        ], style={'marginTop': 15})
    ], style={'marginBottom': 20, 'padding': 15, 'backgroundColor': '#fff', 
             'borderRadius': 8, 'border': '1px solid #ddd'}),
    
    # Hidden div to store the interval for auto-refresh
    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),  # 5 minutes
    
    # Store for caching data
    dcc.Store(id='maintenance-data-store'),
    dcc.Store(id='weather-data-store')
], style={'maxWidth': 1400, 'margin': 'auto', 'padding': 20, 'fontFamily': 'Arial, sans-serif'})


# Callbacks
@app.callback(
    [Output('maintenance-data-store', 'data'),
     Output('weather-data-store', 'data'),
     Output('last-updated', 'children')],
    [Input('refresh-button', 'n_clicks'),
     Input('interval-component', 'n_intervals')],
    prevent_initial_call=False
)
def update_data(n_clicks, n_intervals):
    """Fetch data from Supabase"""
    try:
        maintenance_df = get_maintenance_schedule()
        weather_df = get_current_weather()
        
        maintenance_data = maintenance_df.to_json(date_format='iso', orient='split') if not maintenance_df.empty else None
        weather_data = weather_df.to_json(date_format='iso', orient='split') if not weather_df.empty else None
        
        last_updated = datetime.now().strftime("%I:%M %p")
        
        return maintenance_data, weather_data, f"Last updated: {last_updated}"
    except Exception as e:
        print(f"Error updating data: {e}")
        return None, None, f"Error loading data: {str(e)}"


@app.callback(
    Output('recommendations-container', 'children'),
    Input('maintenance-data-store', 'data')
)
def update_recommendations(data):
    """Display recommended maintenance activities"""
    if not data:
        return html.Div("Loading recommendations...", style={'color': '#999'})
    
    try:
        df = pd.read_json(data, orient='split')
        if df.empty:
            return html.Div("No recommendations available at this time.", 
                          style={'color': '#999', 'padding': 20, 'textAlign': 'center'})
        
        # Group by activity and get unique recommendations
        activities = df.groupby('activity_name').first().reset_index()
        
        if len(activities) == 0:
            return html.Div("No recommendations available at this time.",
                          style={'color': '#999', 'padding': 20, 'textAlign': 'center'})
        
        activity_cards = []
        for _, row in activities.iterrows():
            card = html.Div([
                html.H3(row['activity_name'], style={'marginTop': 0, 'color': '#2c3e50'}),
                html.P(f"🌡️ Temperature: {row.get('temperature_f', 'N/A')}°F", style={'margin': '5px 0'}),
                html.P(f"💧 Precipitation Prob: {row.get('precipitation_prob_pct', 'N/A')}%", style={'margin': '5px 0'}),
                html.P(f"💨 Wind Speed: {row.get('wind_speed_mph', 'N/A')} mph", style={'margin': '5px 0'}),
                html.P(f"☁️ Conditions: {row.get('weather_description', 'N/A')}", style={'margin': '5px 0', 'color': '#666'})
            ], style={'borderLeft': '4px solid #27ae60', 'paddingLeft': 12, 'marginBottom': 15, 'padding': 12})
            activity_cards.append(card)
        
        return html.Div(activity_cards)
    except Exception as e:
        return html.Div(f"Error displaying recommendations: {str(e)}", style={'color': 'red'})


@app.callback(
    Output('weather-container', 'children'),
    Input('weather-data-store', 'data')
)
def update_weather_display(data):
    """Display current weather information"""
    if not data:
        return html.Div("Loading weather data...", style={'color': '#999'})
    
    try:
        df = pd.read_json(data, orient='split')
        if df.empty:
            return html.Div("No weather data available.", 
                          style={'color': '#999', 'padding': 20, 'textAlign': 'center'})
        
        # Get the most recent weather data
        latest = df.iloc[-1]
        
        weather_info = html.Div([
            html.Div([
                html.Span("Temperature:", style={'fontWeight': 'bold'}),
                html.Span(f" {latest.get('temperature_2m_f', 'N/A')}°F", style={'marginLeft': 10, 'fontSize': 18})
            ], style={'marginBottom': 10}),
            html.Div([
                html.Span("Feels Like:", style={'fontWeight': 'bold'}),
                html.Span(f" {latest.get('feels_like_f', 'N/A')}°F", style={'marginLeft': 10})
            ], style={'marginBottom': 10}),
            html.Div([
                html.Span("Humidity:", style={'fontWeight': 'bold'}),
                html.Span(f" {latest.get('humidity_pct', 'N/A')}%", style={'marginLeft': 10})
            ], style={'marginBottom': 10}),
            html.Div([
                html.Span("Wind Speed:", style={'fontWeight': 'bold'}),
                html.Span(f" {latest.get('wind_speed_10m_mph', 'N/A')} mph", style={'marginLeft': 10})
            ], style={'marginBottom': 10}),
            html.Div([
                html.Span("Precipitation Probability:", style={'fontWeight': 'bold'}),
                html.Span(f" {latest.get('precipitation_prob_pct', 'N/A')}%", style={'marginLeft': 10})
            ])
        ], style={'lineHeight': 1.8})
        
        return weather_info
    except Exception as e:
        return html.Div(f"Error displaying weather: {str(e)}", style={'color': 'red'})


@app.callback(
    Output('temp-precip-chart', 'figure'),
    Input('weather-data-store', 'data')
)
def update_temp_precip_chart(data):
    """Create temperature and precipitation chart"""
    if not data:
        return {'data': [], 'layout': go.Layout(title='Loading...')}
    
    try:
        df = pd.read_json(data, orient='split')
        if df.empty:
            return {'data': [], 'layout': go.Layout(title='No weather data available')}
        
        fig = go.Figure()
        
        # Add temperature trace
        fig.add_trace(go.Scatter(
            x=df['Time'], 
            y=df['temperature_2m_f'],
            name='Temperature (°F)',
            line=dict(color='#e74c3c', width=2),
            yaxis='y1'
        ))
        
        # Add precipitation probability trace
        fig.add_trace(go.Bar(
            x=df['Time'],
            y=df['precipitation_prob_pct'],
            name='Precipitation Probability (%)',
            marker=dict(color='#3498db'),
            opacity=0.6,
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Temperature & Precipitation Forecast',
            hovermode='x unified',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Temperature (°F)', side='left'),
            yaxis2=dict(title='Precipitation Probability (%)', side='right', overlaying='y'),
            template='plotly_white'
        )
        
        return fig
    except Exception as e:
        return {'data': [], 'layout': go.Layout(title=f'Error: {str(e)}')}


@app.callback(
    Output('wind-chart', 'figure'),
    Input('weather-data-store', 'data')
)
def update_wind_chart(data):
    """Create wind speed chart"""
    if not data:
        return {'data': [], 'layout': go.Layout(title='Loading...')}
    
    try:
        df = pd.read_json(data, orient='split')
        if df.empty:
            return {'data': [], 'layout': go.Layout(title='No weather data available')}
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['wind_speed_10m_mph'],
            mode='lines+markers',
            name='Wind Speed (mph)',
            line=dict(color='#f39c12', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Wind Speed Forecast',
            hovermode='x',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Wind Speed (mph)'),
            template='plotly_white'
        )
        
        return fig
    except Exception as e:
        return {'data': [], 'layout': go.Layout(title=f'Error: {str(e)}')}


@app.callback(
    Output('activities-timeline-chart', 'figure'),
    Input('maintenance-data-store', 'data')
)
def update_activities_timeline(data):
    """Create activities recommendation timeline chart"""
    if not data:
        return {'data': [], 'layout': go.Layout(title='Loading...')}
    
    try:
        df = pd.read_json(data, orient='split')
        if df.empty:
            return {'data': [], 'layout': go.Layout(title='No recommendations available')}
        
        # Count recommendations per hour
        if 'weather_time' in df.columns:
            df['hour'] = pd.to_datetime(df['weather_time']).dt.strftime('%I:%M %p')
            hourly_activities = df.groupby('hour').size()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=hourly_activities.index,
                y=hourly_activities.values,
                marker=dict(color='#27ae60')
            ))
            
            fig.update_layout(
                title='Recommended Activities by Hour',
                hovermode='x',
                xaxis=dict(title='Time'),
                yaxis=dict(title='Number of Recommended Activities'),
                template='plotly_white'
            )
            
            return fig
        else:
            return {'data': [], 'layout': go.Layout(title='No time data available')}
    except Exception as e:
        return {'data': [], 'layout': go.Layout(title=f'Error: {str(e)}')}


if __name__ == '__main__':
    debug = os.getenv('DASH_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('DASH_PORT', 8050))
    host = os.getenv('DASH_HOST', '127.0.0.1')
    
    app.run(debug=debug, host=host, port=port)
