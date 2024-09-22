import requests

# Получите API ключи
opencage_api_key = 'e497b262c86c41ca884bcf02c8cf3792'
timezone_api_key = '3KW25Z8CFGVF'


def get_coordinates(city_name):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={opencage_api_key}'
    response = requests.get(url)
    data = response.json()

    if data['results']:
        coordinates = data['results'][0]['geometry']
        return coordinates['lat'], coordinates['lng']
    else:
        return None, None


def get_time_zone(lat, lng):
    url = f'http://api.timezonedb.com/v2.1/get-time-zone?key={timezone_api_key}&format=json&by=position&lat={lat}&lng={lng}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        return data['zoneName'], data['gmtOffset'], data['timestamp']
    else:
        return None, None, None


def main(city_name):
    lat, lng = get_coordinates(city_name)
    if lat is not None and lng is not None:
        timezone, gmt_offset, timestamp = get_time_zone(lat, lng)
    else:
        print('Не удалось получить координаты.')
    return round(lat,2), round(lng,2), int(gmt_offset/3600)

