import requests
import pandas as pd

import sys
print(sys.version)

data = requests.get(
            f"http://data.mobility.brussels/traffic/api/counts/?request=devices&outputFormat=json&interval={15}")

columns = ['id', 'lat', 'lon']
df_out = pd.DataFrame(columns=columns)
all_data = data.json()['features']

#print(all_data)


# for sensor_dict in all_data:
#     coordinates = list(reversed(sensor_dict['geometry']['coordinates']))
#     sensor_name = sensor_dict['properties']['traverse_name']
#     if sensor_name == 'STE_TD3':
#         print('here')

#     if sensor_name in cls.unavailable_sensors or \
#             (not coordinates[0] or not coordinates[1]) or \
#             (not np.isfinite(coordinates[0]) or not np.isfinite(coordinates[1])):
#         continue
#     record = pd.DataFrame([{'id': sensor_name, 'lat': coordinates[0], 'lon': coordinates[1]}])
#     df_out = pd.concat([df_out, record], axis=0, ignore_index=True)
# df_out.to_csv(output_fname, mode='w', sep=';', index=False, header=True)