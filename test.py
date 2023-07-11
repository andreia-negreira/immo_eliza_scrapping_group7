import folium
import pandas as pd
dict_data = df.to_dict(orient='list')

data = {
    'City': ['Brussels', 'Antwerp', 'Ghent', 'Bruges'],
    'Latitude': [50.8503, 51.2194, 51.0543, 51.2093],
    'Longitude': [4.3517, 4.4025, 3.7174, 3.2247],
    'Price': [500000, 400000, 300000, 450000]
}
belgium_map = folium.Map(location=[50.5039, 4.4699], zoom_start=8)
df = pd.DataFrame(data)
for index, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['City']}, Price: {row['Price']}",
        icon=folium.Icon(color='blue', icon='home')
    ).add_to(belgium_map)

belgium_map.save("belgium_map.html")