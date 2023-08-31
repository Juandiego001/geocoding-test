import requests
from urllib.parse import quote


ADDRESS = '1300 SE Stark Street, Portland, OR 97214'
'''Things done with gmaps.
    import googlemaps
    from dotenv import load_dotenv
    import os

    load_dotenv()

    API_KEY = os.getenv('API_KEY')

    gmaps = googlemaps.Client(key=API_KEY)
    geocode_result = gmaps.geocode(ADDRESS)
'''
try:
    ADDRESS_ENCODED = quote(ADDRESS)
    address_found = requests.get(f'https://www.portlandmaps.com/arcgis/rest/services/Public/Address_Geocoding_PDX/GeocodeServer/findAddressCandidates?Street={ADDRESS_ENCODED}&City=&State=&ZIP=&Single+Line+Input=&outFields=&maxLocations=&matchOutOfRange=true&langCode=&locationType=&sourceCountry=&category=&location=&distance=&searchExtent=&outSR=&magicKey=&f=json')
    address_json = address_found.json()
    candidates = address_json['candidates']

    # Get location from first candidate
    location = candidates[0]['location']
    location_encoded = quote(f"{location['x']},{location['y']}")
    neighborhood_found = requests.get(f'https://www.portlandmaps.com/arcgis/rest/services/Public/COP_OpenData/MapServer/125/query?where=&text=&objectIds=&time=&timeRelation=esriTimeRelationOverlaps&geometry={location_encoded}&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&sqlFormat=none&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=json')
    neighborhood_json = neighborhood_found.json()
    the_neighborhood = neighborhood_json['features'][0]['attributes']['NAME']

    print(f'The neighborhood from the address is: { the_neighborhood }.')
except:
    print('There was an error while trying to make the requests. Re-launch app.py.')

INITIAL_STREET = 1400
def next_neighborhood(next_street):
    global the_neighborhood
    new_neighborhood = the_neighborhood
    try:
        NEW_ADDRESS = f'{next_street} SE Stark Street, Portland, OR 97214'
        ADDRESS_ENCODED = quote(NEW_ADDRESS)
        print(f'Making request with street number {next_street}...')
        address_found = requests.get(f'https://www.portlandmaps.com/arcgis/rest/services/Public/Address_Geocoding_PDX/GeocodeServer/findAddressCandidates?Street={ADDRESS_ENCODED}&City=&State=&ZIP=&Single+Line+Input=&outFields=&maxLocations=&matchOutOfRange=true&langCode=&locationType=&sourceCountry=&category=&location=&distance=&searchExtent=&outSR=&magicKey=&f=json')
        address_json = address_found.json()
        candidates = address_json['candidates']

        # Get location from first candidate
        if len(candidates):
            location = candidates[0]['location']
            location_encoded = quote(f"{location['x']},{location['y']}")
            neighborhood_found = requests.get(f'https://www.portlandmaps.com/arcgis/rest/services/Public/COP_OpenData/MapServer/125/query?where=&text=&objectIds=&time=&timeRelation=esriTimeRelationOverlaps&geometry={location_encoded}&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&sqlFormat=none&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=json')
            neighborhood_json = neighborhood_found.json()
            new_neighborhood = neighborhood_json['features'][0]['attributes']['NAME']

        if len(candidates) and new_neighborhood != the_neighborhood:
            print(f'The new neighborhood is {new_neighborhood} and his address is {NEW_ADDRESS}.')
        # I set a limit of 3000 to finish the program
        elif next_street > 3000:
            pass
        else:            
            next_neighborhood(next_street+100)

    except:
        print('There was an error while making the requests of the recursive function. Re-launch app.py.')

next_neighborhood(INITIAL_STREET)