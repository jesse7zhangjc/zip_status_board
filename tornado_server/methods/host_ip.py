"""
Get Host IP Address
"""

from socket import gethostbyname, gethostname

HOST_IP = gethostbyname(gethostname())
