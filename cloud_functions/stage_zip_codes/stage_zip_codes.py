import os

import requests
from google.cloud import pubsub_v1

GET_ZIP_CODES_URL = "https://www.zipcodeapi.com/rest/{ZIP_CODE_API_KEY}/city-zips.json/{city}/{state}"

requests.get(GET_ZIP_CODES_URL)


def stage_zip_codes(request):
    request_json = request.get_json()
    city = request_json["city"]
    state = request_json["state"]
    zip_codes = get_zip_codes_for_city(city, state)
    publish_zip_codes(zip_codes)


def get_zip_codes_for_city(city, state):
    url = GET_ZIP_CODES_URL.format(city=city, state=state)
    response = requests.get(url)
    response_json = response.get_json()
    return response_json["zip_codes"]


def publish_zip_codes(zip_codes):
    for zip_code in zip_codes:
        publisher = pubsub_v1.PublisherClient()
        topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
            topic='MY_TOPIC_NAME',
        )
        publisher.publish(topic_name, zip_code.encode())
