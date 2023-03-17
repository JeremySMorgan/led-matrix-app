import requests
import time
import json
import datetime

def now_str() -> str:
    now = datetime.datetime.now()
    return now.strftime("%a %I:%M:%S %p")

def send_json_post(url: str, json_data: dict, verbose=False):
    """ Send a POST request with json data
    """
    req = requests.post(url, json=json_data)

    # 503: Service Unavailable
    if req.status_code == 503:
        print(f"Error: 'Service Unavailable' (at url: '{url}')")
        return False
    try:
        if verbose:
            print("response:", req)
            print("Send successful")
        _json = req.json()
        return _json
    except requests.exceptions.ConnectionError:
        print(f"Connection error sending POST message to '{url}'")
    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"  url:           {url}")
        print(f"  json fields:   {[f for f in json_data]}")
        print(f"  req:           {req}")
    return False

def wait_for_internet():
    """ Function blocks until the device is connected
    """
    print("Waiting for internet ...", flush=True)
    url = "http://www.google.com"
    while True:
        try:
            req = requests.get(url)
            if req.status_code == 200:
                print("Internet detected", flush=True)
                return
            return
        except requests.exceptions.ConnectionError:
            print("...", flush=True)
            time.sleep(0.1)


if __name__ == "__main__":
    print("calling wait_for_internet()")
    wait_for_internet()
    print("done")
