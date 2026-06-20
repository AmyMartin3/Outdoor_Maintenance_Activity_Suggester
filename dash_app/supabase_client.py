"""
Supabase connection and data retrieval module
"""
import os
from supabase import create_client, Client
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from root .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

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

        # Query the v_powerbi_maintenance_schedule view
        response = supabase.table("v_powerbi_maintenance_schedule").select("*").execute()

        if response.data:
            df = pd.DataFrame(response.data)
            # Convert timestamp columns
            if 'weather_time' in df.columns:
                df['weather_time'] = pd.to_datetime(df['weather_time'])
            if 'weather_date' in df.columns:
                df['weather_date'] = pd.to_datetime(df['weather_date'])
            return df
        else:
            return pd.DataFrame()

    except Exception as e:
        err_text = str(e)
        if 'Unregistered API key' in err_text or 'code':
            # Provide a clear actionable message for 401-like failures
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
