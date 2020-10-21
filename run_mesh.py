import subprocess
import sys
from joblib import Parallel, delayed
"""
    Target:
        Get sensor data through mesh-cfgclient and store in a file by python.

        1. Need to implement parallel processes to deal with data log and file storage
    
    procedure: discover-unprovisioned on: search the unprovision node. 
"""

def setup_mesh():
    proc = subprocess.run(["meshctl","discover-unprovisioned","on"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(proc.stdout.decode("utf8"))

if __name__ == '__main__':
    setup_mesh()
