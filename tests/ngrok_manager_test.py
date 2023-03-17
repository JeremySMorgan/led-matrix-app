import unittest
import os
import sys
sys.path.append(os.getcwd())

from ngrok_manager import NgrokManager, ngrok_process_is_running

from tqdm import tqdm

class TestNgrokManager(unittest.TestCase):
    
    def setUp(self):
        self.ng_manager = NgrokManager(5000)

    def test_startup_shutdown(self):
        """ Test that ngrok starts up and shutsdown cleanly
        """
        # Create NgrokManager, start process
        self.ng_manager.start_tunnel()
        self.assertTrue(ngrok_process_is_running())
        hostname = self.ng_manager.get_public_hostname()
        self.assertTrue(hostname is not None)
        self.assertTrue(isinstance(hostname, str))
        self.assertGreater(len(hostname), 15) # http://_____.com
        
        self.ng_manager.stop_tunnel()
        hostname = self.ng_manager.get_public_hostname()
        self.assertTrue(hostname is None)


    def test_different_hostnames(self):
        """ Test that ngrok starts up and shutsdown cleanly
        """

        public_hostnames = []

        for _ in tqdm(range(5)):

            # Create NgrokManager, start process
            self.ng_manager.start_tunnel()
            self.assertTrue(ngrok_process_is_running())
            
            hostname = self.ng_manager.get_public_hostname()
            assert isinstance(hostname, str)
            self.assertTrue(hostname is not None)
            self.assertTrue(isinstance(hostname, str))
            self.assertGreater(len(hostname), 15) # http://_____.com
            assert hostname not in public_hostnames
            public_hostnames.append(hostname)

            self.ng_manager.stop_tunnel()
            hostname = self.ng_manager.get_public_hostname()
            self.assertTrue(hostname is None)

if __name__ == '__main__':
    unittest.main()
