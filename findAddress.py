import requests
import sys
import csv

# gather inputs
try:
    input = sys.argv[1]
    output = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <csv-file> <output-file>")


# Define the endpoint URL for the geocoding API
# url = 'https://services.nconemap.gov/secure/rest/services/Geocoding/GeocodeServer/findAddressCandidates'
url = 'https://services.nconemap.gov/secure/rest/services/AddressNC/AddressNC_geocoder/GeocodeServer/findAddressCandidates'

# Define the parameters for the geocoding request
params = {
    'f': 'json',                # Response format
    'outFields': '*',           # Return all fields in the response
    'maxLocations': 5,          # Maximum number of results to return
    # 'SingleLine': '101 Rose Hill dr, Holly Springs',  # Address to geocode
    'outSR': '4326'            # Spatial reference for the output
    #'apiKey': 'YOUR_API_KEY'    # Your API key (replace with actual API key)
}


with open(input) as inputCSV:
    with open(output, 'w') as outputCSV:
        csv_reader = csv.reader(inputCSV, delimiter=',')
        writer = csv.writer(outputCSV, lineterminator='\n')
        line_count = 0

        for row in csv_reader:
            # set new x and y headers for the output csv
            if line_count == 0:
                writer.writerow(row+['x']+['y'])

            if row and line_count > 0:
                # params['SingleLine'] = row[0] + ' ' + row[2] + ' ' + row[3];
                params['SingleLine'] = row[11] + ' ' + row[9] + ' ' + row[10];

                # Send the request to the API and get the response
                response = requests.get(url, params=params)

                # Check if the request was successful (HTTP status code 200)
                if response.status_code == 200:
                    # Parse the JSON response
                    data = response.json()
                    
                    # Save results to output CSV
                    if data['candidates']:
                        for candidate in data['candidates']:
                            print(str(line_count) + ' ' + candidate['address'], candidate['location']['x'], candidate['location']['y'])
                            writer.writerow(row+[candidate['location']['x']]+[candidate['location']['y']])
                    else:
                        print(str(line_count) + ' ' + row[0] + ' *** No geo code found ***')
                        writer.writerow(row)

                else:
                    print('Error:', response.status_code)
            line_count += 1
    print(f'Complete. {line_count} lines processed')