from datetime import datetime

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def load_hurdat2(self):
        data = []
        current_storm_id = None

        try:
            file = open(self.filepath, 'r')

            for line in file:
                line = line.strip()
                parts = line.split(",")

                for i in range(len(parts)):
                    parts[i] = parts[i].strip()

                # HEADER
                if parts[0].startswith("AL") or parts[0].startswith("EP") or parts[0].startswith("CP"):
                    current_storm_id = parts[0]
                    continue

                # DATA
                try:
                    date_str = parts[0]
                    time_str = parts[1]

                    lat_str = parts[4]
                    lon_str = parts[5]
                    wind_str = parts[6]

                    lat = self.parse_lat(lat_str)
                    lon = self.parse_lon(lon_str)
                    wind = float(wind_str)

                    datetime_str = date_str + time_str
                    dt = datetime.strptime(datetime_str, "%Y%m%d%H%M")

                    row = {
                        'storm_id': current_storm_id,
                        'time': dt,
                        'lat': lat,
                        'lon': lon,
                        'wind': wind
                    }

                    self.validate_row(row)
                    data.append(row)

                except (ValueError, IndexError):
                    continue

            file.close()

        except FileNotFoundError:
            print("Error: file not found")

        return data
    
    def validate_data(self, row):
        if not (-90 <= row['lat'] <= 90):
            raise ValueError("Invalid latitude")
        
        if not (-90 <= row['lon'] <= 90):
            raise ValueError("Invalid longitude")
        
        if row['wind'] < 0:
            raise ValueError("Wind cannot be negative")
        
    def parse_lat(self, lat_str):
        lat = float(lat_str[:-1])
        if lat_str[-1] == 'S':
            lat *= -1
        return lat
    
    def parse_lon(self, lon_str):
        lon = float(lon_str[:-1])
        if lon_str[-1] == 'W':
            lon *= -1
        return lon