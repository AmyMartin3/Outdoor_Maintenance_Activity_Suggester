"""
Supabase connection and data retrieval module
"""
import os
from supabase import create_client, Client
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from root .env file (override existing env vars)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path, override=True)

# Initialize Supabase client
def get_supabase_client() -> Client:
    """Create and return a Supabase client"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env")
    
    return create_client(supabase_url, supabase_key)


def get_maintenance_schedule() -> pd.DataFrame:
    """
    Fetch the current maintenance activity recommendations from Supabase
    Returns a DataFrame with weather data and recommended activities
    """
    try:
        supabase = get_supabase_client()
        
        # Query the tables directly and join locally instead of using the view
        # (view may have permission issues with RLS)
        weather_response = supabase.table("hourly_weather_data")\
            .select("*")\
            .order("Time", desc=True)\
            .limit(24)\
            .execute()
        
        activities_response = supabase.table("dim_maintenance_activities")\
            .select("*")\
            .execute()
        
        if not weather_response.data or not activities_response.data:
            return pd.DataFrame()
        
        # Convert to DataFrames
        weather_df = pd.DataFrame(weather_response.data)
        activities_df = pd.DataFrame(activities_response.data)
        
        # Convert timestamp
        if 'Time' in weather_df.columns:
            weather_df['Time'] = pd.to_datetime(weather_df['Time'])
        
        # Match activities to weather conditions
        recommendations = []
        for _, weather in weather_df.iterrows():
            for _, activity in activities_df.iterrows():
                # Check if weather matches activity constraints
                temp = weather.get('temperature_2m_f', 0)
                precip = weather.get('precipitation_prob_pct', 0)
                wind = weather.get('wind_speed_10m_mph', 0)
                
                if (activity.get('min_temp_f', 0) <= temp <= activity.get('max_temp_f', 200) and
                    precip <= activity.get('max_precipitation_prob_pct', 100) and
                    wind <= activity.get('max_wind_speed_mph', 100)):
                    
                    recommendations.append({
                        'weather_time': weather.get('Time'),
                        'weather_date': pd.to_datetime(weather.get('Time')).date() if weather.get('Time') else None,
                        'hour_of_day': pd.to_datetime(weather.get('Time')).hour if weather.get('Time') else None,
                        'temperature_f': temp,
                        'precipitation_prob_pct': precip,
                        'wind_speed_mph': wind,
                        'weather_description': 'Good conditions',
                        'activity_name': activity.get('activity_name'),
                        'is_recommended': 1
                    })
        
        return pd.DataFrame(recommendations) if recommendations else pd.DataFrame()
            
    except Exception as e:
        err_text = str(e)
        if 'Unregistered API key' in err_text or '401' in err_text:
            raise RuntimeError(
                "Supabase authentication failed: your anon API key appears unregistered or invalid.\n"
                "Please regenerate the Anon Public Key in Supabase (Settings → API) and update the .env file with the new key."
            )
        print(f"Error fetching maintenance schedule: {e}")
        return pd.DataFrame()


def get_current_weather() -> pd.DataFrame:
    """
    Fetch the most recent hourly weather data
    """
    try:
        supabase = get_supabase_client()

        # Query hourly weather data, ordered by most recent first
        response = supabase.table("hourly_weather_data")\
            .select("*")\
            .order("Time", desc=True)\
            .limit(24)\
            .execute()

        if response.data:
            df = pd.DataFrame(response.data)
            df['Time'] = pd.to_datetime(df['Time'])
            df = df.sort_values('Time')
            return df
        else:
            return pd.DataFrame()

    except Exception as e:
        err_text = str(e)
        if 'Unregistered API key' in err_text or '401' in err_text:
            raise RuntimeError(
                "Supabase authentication failed: your anon API key appears unregistered or invalid.\n"
                "Please regenerate the Anon Public Key in Supabase (Settings → API) and update the .env file with the new key."
            )
        print(f"Error fetching weather data: {e}")
        return pd.DataFrame()


def get_maintenance_activities() -> pd.DataFrame:
    """
    Fetch all maintenance activities and their weather requirements
    """
    try:
        supabase = get_supabase_client()

        response = supabase.table("dim_maintenance_activities").select("*").execute()

        if response.data:
            return pd.DataFrame(response.data)
        else:
            return pd.DataFrame()

    except Exception as e:
        err_text = str(e)
        if 'Unregistered API key' in err_text or '401' in err_text:
            raise RuntimeError(
                "Supabase authentication failed: your anon API key appears unregistered or invalid.\n"
                "Please regenerate the Anon Public Key in Supabase (Settings → API) and update the .env file with the new key."
            )
        print(f"Error fetching maintenance activities: {e}")
        return pd.DataFrame()
