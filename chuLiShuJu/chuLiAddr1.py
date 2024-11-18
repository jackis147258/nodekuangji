# Read the input file
with open('./chuLiShuJu/data.py', 'r') as file:
    addresses = file.readlines()

# Clean up the addresses and format them
formatted_addresses = []
for index, address in enumerate(addresses, start=1):
    address = address.strip()
    if address:  # Ensure it's not an empty line
        formatted_addresses.append(f'{{"token": "{address}", "ApprovedBuy": {index}, "newToken": "newAddress"}}')

# Print the formatted output with a comma at the end
for item in formatted_addresses:
    print(item + ',')  # Add a comma after each item

