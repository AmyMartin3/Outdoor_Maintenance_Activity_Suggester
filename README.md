# 🏡 Outdoor Maintenance Activity Suggester

A weather-aware dashboard that suggests outdoor home maintenance activities based on real-time weather conditions. Built with Dash and powered by Supabase.

## Features

- 🌤️ Real-time weather data from Open-Meteo API
- ✅ Intelligent activity recommendations based on weather conditions
- 📊 Interactive dashboard with weather charts and trends
- 🔄 Auto-refreshing data every 5 minutes
- 🗄️ Supabase backend for data persistence
- 📱 Responsive web interface

## Project Structure

```
├── dash_app/
│   ├── app.py                 # Main Dash application
│   ├── supabase_client.py     # Supabase connection & data retrieval
│   ├── components/            # Reusable Dash components (future)
│   └── __init__.py
├── sql/                       # SQL setup scripts
├── data/                      # Sample data
├── notebooks/                 # Jupyter notebooks for analysis
├── etl/                       # ETL scripts
├── docs/                      # Documentation
├── images/                    # Screenshots and diagrams
├── .env                       # Environment variables (DO NOT COMMIT)
├── .env.example               # Template for environment variables
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── run_dashboard.py           # Script to run the dashboard
└── README.md                  # This file
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Supabase account with project setup
- Git (for version control)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AmyMartin3/Outdoor_Maintenance_Activity_Suggester.git
cd Outdoor_Maintenance_Activity_Suggester
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Supabase project details:

```
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
DASH_DEBUG=True
DASH_PORT=8050
DASH_HOST=127.0.0.1
```

**Getting your Supabase credentials:**
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Navigate to Settings → API
4. Copy your **Project URL** and **Anon Public Key**

### 5. Setup Supabase Database

Run the SQL setup script in your Supabase SQL editor:

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Create a new query
4. Copy and run the contents of the SQL setup file

The SQL creates:
- Weather reference tables (`dim_weather_codes`, `hourly_weather_data`)
- Maintenance activity definitions (`dim_maintenance_activities`)
- Automated weather data refresh procedure
- PostgreSQL cron job for hourly updates
- Power BI integration view

### 6. Run the Dashboard

```bash
python run_dashboard.py
```

Or alternatively:

```bash
cd dash_app
python app.py
```

The dashboard will be available at: `http://127.0.0.1:8050`

## Dashboard Features

### Recommended Activities
- Displays maintenance tasks suitable for current weather conditions
- Shows temperature, precipitation, and wind speed constraints
- Updates in real-time

### Weather Display
- Current temperature (actual and "feels like")
- Humidity percentage
- Wind speed
- Precipitation probability

### Charts & Analytics
- **Temperature & Precipitation**: Shows temperature trends and rainfall probability
- **Wind Speed**: Hourly wind speed forecast
- **Activity Timeline**: Recommendations by hour

## How It Works

1. **Weather Data Collection**: The Supabase backend fetches real-time weather data from Open-Meteo API every hour
2. **Activity Matching**: The system matches current weather conditions against predefined maintenance activity requirements
3. **Recommendation Generation**: Activities that fit weather conditions are recommended to the user
4. **Dashboard Display**: Dash visualizes all data with interactive charts and cards

### Supported Activities

- Lawn Mowing (50-95°F, <20% precipitation, <15.5 mph wind)
- Exterior Painting (59-86°F, <10% precipitation, <9.3 mph wind)
- Gutter Cleaning (41-95°F, <30% precipitation, <12.4 mph wind)
- Tree Trimming (32-95°F, <40% precipitation, <9.3 mph wind)
- Pressure Washing (50-104°F, <50% precipitation, <18.6 mph wind)

## Database Schema

### Tables

- **dim_weather_codes**: Weather condition codes and descriptions
- **hourly_weather_data**: Hourly weather measurements (auto-updated)
- **dim_maintenance_activities**: Activity definitions with weather constraints

### Views

- **v_powerbi_maintenance_schedule**: Aggregated view of recommendations for the next 8 hours

## Deployment

### Local Development
Already covered above with `python run_dashboard.py`

### Production Deployment

For production, consider:

1. **Railway, Render, or Heroku**: Simple hosting for Dash apps
2. **Docker**: Containerize the app for consistent deployment
3. **Environment Variables**: Use secure secrets management

Example Railway deployment:
```yaml
# railway.toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python run_dashboard.py"
```

## Troubleshooting

### "No module named 'supabase'"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Connection refused to Supabase
- Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` are correct
- Check internet connection
- Ensure Supabase project is active

### No data displaying
- Verify the SQL setup script was run successfully
- Check that weather data procedure is running: `SELECT * FROM cron.job;`
- Try clicking "Refresh Data" button in the dashboard

### Port 8050 already in use
Change `DASH_PORT` in `.env` to another port (e.g., 8051)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Notes

- **Never commit `.env` file** to version control (it's in `.gitignore`)
- Use the **Anon Public Key** for client-side connections
- Consider RLS (Row Level Security) policies for production
- Regenerate keys periodically
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`

## Future Enhancements

- [ ] User accounts and saved preferences
- [ ] Push notifications for optimal activity windows
- [ ] Mobile app
- [ ] Activity history and completion tracking
- [ ] Integration with weather alerts
- [ ] Customizable activity criteria
- [ ] Multi-location support

## License

This project is available under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please open an issue on GitHub.

---

**Happy maintaining! 🔨**
