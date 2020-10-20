import subprocess
import sys

"""
	target:get sensor data through mesh and store in a file.
"""

def setup_mesh():
	proc = subprocess.run(["meshctl", "help"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	print(proc.stdout.decode("utf8"))


print(sys.argv)


