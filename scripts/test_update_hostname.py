from threading import Thread
import time

from utils import wait_for_internet, send_json_post

if __name__ == "__main__":
    wait_for_internet()


HEROKU_HOSTNAME = "http://jeremysmorgan.herokuapp.com"
UPDATE_HEROKU_HOSTNAME_URL = f"{HEROKU_HOSTNAME}/update_rpi_hypervisor_address"
UPDATE_HEROKU_HOSTNAME_INTERVAL = 5

exit_thread = False

def update_heroku_known_hostnames_thread():
    """ Update the heroku server with the known app & hypervisor public
    ngrok addresses
    """
    global exit_thread
    while True:
        data = {"HOSTNAME": "DNE"}
        res = send_json_post(UPDATE_HEROKU_HOSTNAME_URL, data, verbose=False)
        time.sleep(UPDATE_HEROKU_HOSTNAME_INTERVAL)
        if exit_thread:
            break
    

"""" Example usage

python test_update_hostname.py
"""

if __name__ == "__main__":
    thread = Thread(target=update_heroku_known_hostnames_thread)
    thread.start()
    
    time.sleep(100)
