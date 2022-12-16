import requests
import sys

def main():
    payload = '{ "input" : "https://amazon.com/very-long-url" }'
    r = requests.get('https://api.shrtco.de/v2/shorten?url=' + sys.argv[1], timeout=10)
    if r.status_code != 201:
        raise Exception("Failed to shorten URL, status code: " + r.status_code.__str__())
    print(r.json()['result']['full_short_link2'])

if __name__ == '__main__':
    main()