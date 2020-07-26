#!/usr/bin/python3

""" 
Short description of this Python module.
Longer description of this module.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

"""

__author__ = "Pratik"
__authors__ = ["Pratik", "Saurabh", "Priyanka" , "Vivi" , "Eva"]
__contact__ = "pdhage@asu.edu"
__copyright__ = "Copyright 2020, home_9935"
__credits__ = ["Pratik", "Saurabh", "Priyanka", "Vivi" , "Eva"]
__date__ = "2020/07/25"
__deprecated__ = False
__email__ =  "pdhage@asu.edu"
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.0.1"

import time
import RPi.GPIO as GPIO
import sys
import os
import getopt
import sys
#import inspect
#import glob
#import subprocess
#import re
import logging
import shutil
import smtplib
#from email.mime.text import MIMEText
from datetime import datetime, date, timedelta
from cryptography.fernet import Fernet

"""
Rasberry pi GPIO name mapping
"""
GPIO__21__VALVE_CTRL = 21
GPIO__20__LED_CTRL   = 20
"""
Solenoid valve control
param@ GPIO pin setup, time delay
"""
def ctrl_valve_control(logging, pin, delay_sec):
    logging.info("Setting GPIO Pin {0} ON  for {1} sec".format(pin, delay_sec))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(delay_sec)
    GPIO.output(pin,GPIO.LOW)        
    logging.info("Setting GPIO Pin {0} OFF".format(pin))    
"""
Main function
"""

def main():
    argv = sys.argv[1:]
    now = datetime.now()
    currentdate = now.strftime("%Y-%m-%d")
    currenttime = now.strftime("%Y%m%d%H%M%S")
    currenttime_fmt = now.strftime("%Y-%m-%d %H:%M:%S")
    script_name=os.path.basename(__file__)
    """
    Put logs on output and also in file
    Create two seperate handler for logging 
    """
    logfile_name = script_name.split(".")[0] + "_" + currenttime + ".log"
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    output_file_handler = logging.FileHandler(logfile_name)
    stdout_handler      = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y-%m-%d %H-%M-%S')
    stdout_handler.setFormatter(formatter)
    output_file_handler.setFormatter(formatter)
    root.addHandler(stdout_handler)
    root.addHandler(output_file_handler)
    """
    Input arg parsing
    """
    try:
      opts, args = getopt.getopt(argv,"hsr", ["help", "status", "run"])
    except getopt.GetoptError:
        logging.error("Input argument exception errror")
        sys.exit(2)
    status_arg = 0
    run_arg = 0
    for opt, arg in opts:
      if opt in ("-h", "--help"):
        logging.info("{0} --status --help --run ".format(script_name))
        logging.info("{0} --run : Will run default program to turn on the valve for certain period and exit".format(script_name))
        logging.info("{0} --status : Status TBD".format(script_name))
        sys.exit(0)
      elif opt in ("-s", "--status"):
        status_arg = 1
      elif opt in ("-r", "--run"):
        run_arg = 1
    if (status_arg == 1) and (run_arg == 1):
        logging.error("Invalid argument passed. You can either do --status or --run and not both")
        sys.exit(1)
    if (run_arg == 0) and (status_arg == 0):
        logging.error("No valid argument passed. You can either do --status or --run")
        sys.exit(1)
    script_mode = ""
    if run_arg == 1:
        logging.info("Script in run mode")
        script_mode = "Run Mode"
    if status_arg == 1:
        logging.info("Script in status mode")
        script_mode = "Status Mode"
    if "HOME_GARDEN_IRRIGATION_9935_TEST" in os.environ:
        env = "TEST"
    else:
        env = "PRODUCTION"
    logging.info("Program version            :{0}".format(__version__))
    logging.info("Script environment set     :{0}".format(env))
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    if env == "TEST":
        delay_sec = 10;
        ctrl_valve_control(logging,GPIO__21__VALVE_CTRL, delay_sec)
        ctrl_valve_control(logging,GPIO__20__LED_CTRL, delay_sec)

    else:
        minutes = 5
        delay_sec = minutes*60
        ctrl_valve_control(logging,GPIO__21__VALVE_CTRL, delay_sec)
        ctrl_valve_control(logging,GPIO__20__LED_CTRL, delay_sec)        

    email_text="""
    Home backyard ran successfully at : {0}
    Water was on for                  : {1} sec ( or {2} minutes)
    Environment mode                  : {3}
    Mode                              : {4}
    Version                           : {5}
    """.format(currenttime_fmt, delay_sec,delay_sec/60, env, script_mode, __version__)
    with open ("../email/encrypted_pass.txt", "rb") as fp_r:
        for line in fp_r:
            encrypted_pwd = line
    key = b'lHwEPPG06WDsWCGC1HjgqtQzOuvvn2c5K1iUok7qiKs='
    cipher_suite = Fernet(key)
    uncipher_text = (cipher_suite.decrypt(encrypted_pwd))
    plain_text_encrypted_password = bytes(uncipher_text).decode("utf-8")                    
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login("homeirrigation9935@gmail.com", plain_text_encrypted_password)
    msg=email_text
    server.sendmail("homeirrigation9935@gmail.com","pratikpdhage@gmail.com", msg)
    server.quit()

if __name__ == '__main__':
    main()