# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:22:01 2022

@author: mad
"""

import os


def execute(cmd:str,sudo=True):
    """
    Execute shell cmd wit sudo or not
    """
    if sudo:
        os.system('sudo '+cmd)
    else:
        os.system(cmd)


try:
    execute("apt-get install iptables")
except Exception:
    print("Cannot use aptitude or iptables package does not exist.")