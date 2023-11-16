import requests
import json
import hashlib

base_url = "https://api.ethscriptions.com/api/ethscriptions/exists/"

# Function to generate the data string
def generate_data_string(token_id):
    data_string = f"data:,{{\"p\":\"erc-20\",\"op\":\"mint\",\"tick\":\"💯\",\"id\":\"{token_id}\",\"amt\":\"1\"}}"
    return data_string.encode('utf-8')

# Function to check existence and create JSON output
def check_ethscriptions():
    tokens_data = []

    for token_id in range(1, 101):
        encoded_data = generate_data_string(token_id)
        hashed_value = hashlib.sha256(encoded_data).hexdigest()
        url = base_url + hashed_value
        
        print(f"Checking for rock #{token_id} at URL {url}...", end='')

        response = requests.get(url)
        if response.status_code == 200:
            api_data = response.json()
            ethscription_id = api_data.get('ethscription', {}).get('transaction_hash')
            if ethscription_id:
                print("FOUND!")
            else:
                print("Not Found :(")

            token_data = {
                "ethscription_id": ethscription_id,
                "name": f"Rock #{token_id}",
                "description": "",
                "external_url": "",
                "background_color": "",
                "item_index": token_id - 1,
                "item_attributes": [
                    {
                        "trait_type": "ID",
                        "value": token_id
                    }
                ]
            }

            tokens_data.append(token_data)

    # Constructing the final JSON structure
    final_json = {
        "name": "Rocks",
        "description": "One hundred rock emojis as ERC-20 tokens on Ethscriptions",
        "total_supply": 100,
        "logo_image_uri": "",
        "banner_image_uri": "",
        "background_color": "#C4FF00",
        "twitter_link": "",
        "website_link": "",
        "discord_link": "",
        "collection_items": tokens_data
    }

    return final_json

# Function to save JSON to a specified location
def save_json_to_file(json_data, file_path):
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

# Specifying the file path
file_location = "file path to where you want to save the metadata JSON"

# Calling the function and saving the output to the specified location
result = check_ethscriptions()
save_json_to_file(result, file_location)
print(f"JSON data saved to: {file_location}")