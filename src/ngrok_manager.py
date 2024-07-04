import requests
import json
import time

from pyngrok import ngrok


def ngrok_process_is_running() -> bool:
    """Returns true if an ngrok process is running"""
    url = "http://localhost:4040/api/tunnels/"
    try:
        res = requests.get(url)
        res_unicode = res.content.decode("utf-8")
        res_json = json.loads(res_unicode)
    except requests.exceptions.ConnectionError:
        return False
    return True


""" NgrokManager is a wrapper provides an api for starting and shutting down ngrok tunnels

"""


class NgrokManager:

    def __init__(self, port: int):
        """
        Args
            port: int. The port to spawn the ngrok process to forward to
        """
        self._port = port
        self.tunnel = None

    def start_tunnel(self):
        """Start a ngrok tunnel"""
        print("NgrokManager.start_tunnel(): starting tunnel")
        self.tunnel = ngrok.connect(addr=self._port)

    def stop_tunnel(self):
        """Kill the current running ngrok tunnels"""
        print("NgrokManager.stop_tunnel():  stopping tunnel")
        if self.tunnel is None:
            return
        for tunnel in ngrok.get_tunnels():
            ngrok.disconnect(tunnel.public_url)
        self.tunnel = None

    def get_public_hostname(self):
        """Return the public url of the ngrok process running with the
        port specified in the parameterized config. Returns none if no
        process is running.
        """
        if self.tunnel is None:
            return None
        return self.tunnel.public_url


if __name__ == "__main__":
    nm = NgrokManager(5000)
    nm.start_tunnel()
    while True:
        time.sleep(10)
        print("\nUpdating ngrok url")
        print("current hostname:", nm.get_public_hostname())
        nm.stop_tunnel()
        nm.start_tunnel()
        print("new hostname:    ", nm.get_public_hostname())
