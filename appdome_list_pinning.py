#!/usr/bin/env python3

# Start of the main script
#appdome_api_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjg3MzVjZjAtNWEzOC0xMWVkLWE1ZjYtYjU2YzViZmRmMTQ1Iiwic2FsdCI6IjBmNmJjYTNmLTJiODAtNGRkYi1hMzQ2LTE1ZGRiMjM1NTYyOSJ9.Tk-6BgMmil8le-JDryq7URa9-P2Cf3Q2w-bfVZ-7CyY"
#gcash_dev_team_id = "c0ac05a0-f873-11ed-9512-1fbbcdd276ac"
#gcash_uat_team_id = "c4c6ddd0-adb0-11ed-a11c-6df62dbb669a"

# https://fusion.appdome.com/api/app/30c28f50-1bbd-11ee-905f-c15935bc916e/2af97590-0351-11ee-b924-07b6275ac60d/builds?onlyLatest=true&currTeamId=c4c6ddd0-adb0-11ed-a11c-6df62dbb669a


#30c28f50-1bbd-11ee-905f-c15935bc916e
#fusion_set_id 2af97590-0351-11ee-b924-07b6275ac60d
#team_id = c4c6ddd0-adb0-11ed-a11c-6df62dbb669a

# Alpha

import argparse
import requests
import json

# Create argument parser
parser = argparse.ArgumentParser(description='Appdome API Script')
parser.add_argument('--team_id', required=True, help='Team ID')
parser.add_argument('--api_token', required=True, help='API Token')
parser.add_argument('--session_file', required=True, help='Session File')
args = parser.parse_args()

# Get command-line argument values
team_id = args.team_id
api_token = args.api_token
session_file = args.session_file

def get_app_data(app_id, session_file):
    url = f"https://fusion.appdome.com/api/app/{app_id}/active-template?currTeamId={team_id}"

    headers = {
        "accept": "application/json",
        "Authorization": api_token
    }

    session_data = get_session_data(session_file)

    response = requests.get(url, headers=headers, cookies=session_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data for App ID: {app_id}. Status code: {response.status_code}")
        return None

url = f"https://fusion.appdome.com/api/v1/my-library-apps?team_id={team_id}"

headers = {
    "accept": "application/json",
    "Authorization": api_token
}

response = requests.get(url, headers=headers)

def get_session_data(session_file):
    session_data = {}
    with open(session_file, 'r') as f:
        lines = f.read().split(';')
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                session_data[key.strip()] = value.strip()
    return session_data

# Check if the request was successful
if response.status_code == 200:
    # Get the JSON data from the response
    data = response.json()

    # Iterate over the apps and print details
    for app in data['apps']:
        print(json.dumps(app, indent=4))
        #print("App ID:", app['id'])
        #print("Creation Time:", app['creation_time'])
        #print("Pack Name:", app['pack_name'])
        #print("Pack Size:", app['pack_size'])
        #print("Pack Type:", app['pack_type'])
        #print("Bundle Identifier:", app['pack_bundle_identifier'])
        #print("Bundle Version:", app['pack_bundle_version'])
        #print("Bundle Display Name:", app['pack_bundle_display_name'])
        #print("Bundle Build Number:", app['pack_bundle_build_number'])
        #print("App Store Description:", app['pack_app_store_description'])
        #print("Status:", app['status'])
        #print("---------------------------\n")

        # Get JSON data for the App ID
        app_id = app['id']
        app_data = get_app_data(app_id, session_file)

        mitm_host_server_pinned_certs_list = app_data["overrideOrSandbox"]["policy"]["mitm_host_server_pinned_certs_list"]
        print("Finding Defined Pinning Schemes\n")
        for item in mitm_host_server_pinned_certs_list:
            value = item["value"]
            domain = value["mitm_host_server_pinned_certs_domain"]
            pinning_type = value["mitm_host_server_pinned_certs_type"]
            print(f"\tDomain: {domain}, Type: {pinning_type}")

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

