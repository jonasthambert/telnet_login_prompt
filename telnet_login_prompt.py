#!/usr/bin/env python
# 
# Simply prints the telnet banner/login prompt 
# Jonas Thambert
#

# libs
import sys
import telnetlib
import re
import argparse
import threading
from multiprocessing.pool import ThreadPool

# variables
print_lock = threading.Lock()
MAX_THREADS = 25

# scan function
def scan(HOST,TIMEOUT):

# connect
 try:
  tn = telnetlib.Telnet(HOST, 23, TIMEOUT)
 except:
  with print_lock:
   print "Unable to connect to " + HOST + ":23"
   exit(1)

# read until login-regex and print
 try:
  response = tn.expect([re.compile(b"login:"),], timeout=TIMEOUT)
  with print_lock:
   print (HOST, response[2].decode())
 except: 
  with print_lock:
   print "Unable to talk telnet with " + HOST + ":23"
 tn.close()

# main
def main():

 if len(sys.argv) == 1:
  print "\n[+] Please give at least one argument. -h for help\n"
  exit(1)

# argparse
 parser = argparse.ArgumentParser(description='Simply prints the telnet banner/login prompt')
 parser.add_argument('-t','--target', help='IP or hostname')
 parser.add_argument('-f','--file', help='File with IP or hostnames. One on each line.', type=argparse.FileType('r'))
 args = parser.parse_args()

# variables
 HOST = args.target
 TIMEOUT = 1

# Threading
 pool = ThreadPool(processes=MAX_THREADS)
 results = []

# Thread or not ?
 if args.target:
  scan (HOST,TIMEOUT)
  exit(1)
 else:
  for LINE in args.file:
    LINE = LINE.strip()
    results.append(pool.apply_async(scan, (LINE,TIMEOUT)))
  while not(all(a_thread.ready() for a_thread in results)):
        pass  

if __name__=='__main__':
	main()
