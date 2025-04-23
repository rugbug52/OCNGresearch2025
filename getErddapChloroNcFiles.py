import requests
from datetime import datetime, timedelta
import os

# === USER CONFIGURATION ===
start_date_str = "2018-01-01"  # Start date (inclusive)
end_date_str   = "2024-12-31"  # End date (inclusive)
output_dir     = "C:/Users/rugbug/Documents/OCNGresearch/chloro_erddap_files_all"  # Folder to save .nc files

# === BASE URL COMPONENTS ===
base_url = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/noaacwNPPN20S3ASCIDINEOF2kmDaily.nc"

# These parts stay fixed
params = (
    "?chlor_a%5B({date}T12:00:00Z)%5D%5B(0.0)%5D%5B(-29.98959):(-54.98959)%5D%5B(-69.98959):(-45.01041)%5D"
    "&.draw=surface"
    "&.vars=longitude%7Clatitude%7Cchlor_a"
    "&.colorBar=%7C%7C%7C%7C%7C"
    "&.bgColor=0xffccccff"
)

# === DATE SETUP ===
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date   = datetime.strptime(end_date_str, "%Y-%m-%d")

# === Ensure output directory exists ===
os.makedirs(output_dir, exist_ok=True)

# === Loop through dates and download ===
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    formatted_date = f"{date_str}"
    
    # Construct full URL for the given date
    full_url = base_url + params.format(date=formatted_date)

    # Define output filename
    output_filename = f"{output_dir}/chlor_a_{date_str}.nc"

    try:
        print(f"Downloading data for {date_str}...")
        response = requests.get(full_url, stream=True)

        if response.status_code == 200:
            with open(output_filename, 'wb') as f:
                f.write(response.content)
                        # Calculate file size
            file_size = os.path.getsize(output_filename)
            file_size_kb = file_size / 1024
            file_size_mb = file_size_kb / 1024

            print(f"✅ Saved: {output_filename}")
            print(f"🔗 URL used: {full_url}")
            print(f"📦 File size: {file_size_kb:.2f} KB ({file_size_mb:.2f} MB)")
        else:
            print(f"❌ Failed to download for {date_str}. Status code: {response.status_code}")

    except Exception as e:
        print(f"🚫 Error on {date_str}: {e}")

    # Move to next day
    current_date += timedelta(days=1)