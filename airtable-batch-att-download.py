import requests
import json
import os

#Python script to batch donwload attachments, preserving file name and extension
# Define your Airtable base ID, table ID, and URL
base_id = "<<YOUR BASE ID>>"
table_id = "<<YOUR TABLE ID>>"
url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

# Use your Personal Access Token (PAT) here
pat = "<<YOUR PERSONAL ACCESS TOKEN>>"
headers = {"Authorization": f"Bearer {pat}"}

# Initialize parameters for the API request
params = ()
airtable_records = []
run = True

while run:
    # Make a GET request to the Airtable API
    response = requests.get(url, params=params, headers=headers)
    airtable_response = response.json()

    # Collect records from the response
    airtable_records.extend(airtable_response['records'])

    # Process each record
    for record in airtable_response['records']:
        # Your attachment field name "Attachment-column-name"
        if child := record['fields'].get("AttachmentColumn"):
            for attachment in child:
                # Use the original filename from the attachment metadata
                filename = attachment['filename']
                attachment_url = attachment['url']
                print(f"Downloading {filename} from {attachment_url}")

                # Get the file extension from the URL
                file_extension = os.path.splitext(attachment_url)[1]
                if not file_extension:
                    file_extension = ".pdf"  # Default to .pdf if no extension found

                # Ensure filename has the correct extension
                if not filename.endswith(file_extension):
                    filename += file_extension

                # Download the attachment
                attachment_response = requests.get(attachment_url)
                with open(filename, "wb") as file:
                    file.write(attachment_response.content)

    # Handle pagination by checking for an offset in the response
    if 'offset' in airtable_response:
        run = True
        params = (('offset', airtable_response['offset']),)
    else:
        run = False

# Optional: print all collected records
#print(airtable_records)
