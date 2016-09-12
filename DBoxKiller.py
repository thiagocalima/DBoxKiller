#!/usr/bin/python
import sys
import subprocess
import datetime

def main():
	csvfile = "/home/thiago/Documents/git-repos/DBoxKiller/DBoxKiller.log"

	try:
		csvfile = open(csvfile, 'a')
	except IOError, e:
		print ("Failed to find file " + csvfile)
		sys.exit(1)

	out = subprocess.Popen(["ps", "-aux"], stdout=subprocess.PIPE).stdout.readlines()

	for line in out:
		if "dropbox" in line:
			mem = str(line.splitlines()).split()[3]
			pid = str(line.splitlines()).split()[1]
			if float(mem) > 10:
				csvfile.write("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()) + " (PID: " + pid + "; MEM: " + mem +"%) Memory consumption higher than 10%. Killing process...\n")
				subprocess.call(["kill", "-9", pid])
				csvfile.write("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()) + " Restarting process...\n")
				subprocess.call(["dropbox", "start", "-i"])
			
			csvfile.close()
			sys.exit(0)
			

	csvfile.write("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()) + " Dropbox isn't running. Starting...")
	subprocess.call(["dropbox", "start", "-i"])

	csvfile.close()

if __name__ == '__main__':
		sys.exit(main())