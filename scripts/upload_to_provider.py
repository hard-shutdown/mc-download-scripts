import typing
import requests
import json
import re
import sys

def main():
    print(get_cdn_url(upload_to_provider('https://api.openload.cc/upload', sys.argv[1])))

def upload_to_provider(url: str, file: str) -> typing.Any:
    with open(file, 'rb') as f:
        r = requests.post(url, files={'file': f}, timeout=10)
        if r.status_code != 200:
            raise Exception("Failed to upload to provider")
        return r.json()

def get_cdn_url(upload_response: typing.Any) -> str:
    regex = r"\"http(|s):\/\/cdn-.+\/.+\/.+\""
    matches = re.search(regex, requests.get(upload_response['data']['file']['url']['full']).text)
    return matches.group(0).replace('\"', '') # type: ignore

if __name__ == '__main__':
    main()