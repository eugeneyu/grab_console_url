# Deploy to GCP Cloud Functions
# requirements.txt
# google-cloud-logging
# Runtime environment variables
# BITLY_ACCESS_TOKEN
import os
import logging
from google.cloud import logging as g_logging
import requests
from flask import abort
from urllib.parse import urlparse

BITLY_ACCESS_TOKEN = os.environ['BITLY_ACCESS_TOKEN']

logging_client = g_logging.Client()
logger = logging_client.logger('URL-Grabber-Log')

def exit_abort():
    return abort(500)


def process_request(request):

    request_json = request.get_json(silent=True)

    url_long = ''
    user_email = ''

    if request_json and 'url_long' in request_json:
        url_long = request_json['url_long']
    else:
        url_long = 'NA'

    if request_json and 'user_email' in request_json:
        user_email = request_json['user_email']
    else:
        user_email = 'NA'

    ua = request.headers['User-Agent']
    if "X-Forwarded-For" in request.headers:
    	ip = request.headers['X-Forwarded-For']
    elif "x-forwarded-for" in request.headers:
    	ip = request.headers['x-forwarded-for']
    else:
    	ip = request.remote_addr

    # Fence out abuse by allowing only URL with this domain
    domain = urlparse(url_long).netloc
    if not "console.cloud.google.com" in domain:
        data = {
            "link" : "Invalid"
        }
        log_message = "Rejected Request -- User: {}, IP: {}, UA: {}, URL: {}, Short URL: NA".format(user_email, ip, ua, url_long)
        print(log_message)
        logger.log_text(log_message, severity="NOTICE")
        return data

    api_url = "https://api-ssl.bitly.com/v4/shorten"

    headers = {
        "Authorization": "Bearer {}".format(BITLY_ACCESS_TOKEN),
        "Content-Type": "application/json"
    }

    data = {
    	"long_url" : "{}".format(url_long)
    }

    req = requests.Request('POST',api_url,headers=headers,json=data)
    prepared = req.prepare()

    response = requests.post(url = api_url, headers=headers, json = data)

    if not response.ok or "error" in response.text:
    	# this error will not be reported to Stackdriver but to Cloud Functions Log only
        logging.error(RuntimeError(response.text))
        exit_abort()

    response_json = response.json()
    log_message = "Processed Request -- User: {}, IP: {}, UA: {}, URL: {}, Short URL: {}".format(user_email, ip, ua, url_long, response_json['link'])
    print(log_message)
    # Log this to Stackdriver
    logger.log_text(log_message, severity="NOTICE")

    return response_json

