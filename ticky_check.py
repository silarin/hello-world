#!/usr/bin/env python3

import os
import sys
import re
import operator
import csv

def main():
	syslog_file = "syslog.log"
	udt = {}
	edt = {}
	
	with open(syslog_file) as fp:
		for line in fp.readlines():
			if re.search(r"ticky: INFO [\w ]* ", line):
				a = re.search(r"\w.* ticky: INFO (\w.*) \((\w.*)\)$",line)
				udt[a.group(2)] = udt.get(a.group(2), 0) + 1
			elif re.search(r"ticky: ERROR [\w ]* ", line):
				a = re.search(r"\w.* ticky: ERROR (\w.*) \((\w.*)\)$",line)
				udt[a.group(2)] = udt.get(a.group(2), 0) + 1
				edt[a.group(1)] = edt.get(a.group(1), 0) + 1
			else:
				continue
	print(udt)

	with open('error_message.csv', 'w', encoding='UTF8', newline='') as fp:
		cw = csv.writer(fp)
		cw.writerow(["Error","Count"])
		for k, v in sorted(edt.items(), key=operator.itemgetter(1), reverse=True):
			cw.writerow([k,v])
		
	with open('user_statistics.csv', 'w', encoding='UTF8', newline='') as fp:
		cw = csv.writer(fp)
		cw.writerow(["Username","INFO"])
		for k, v in sorted(udt.items(), key=operator.itemgetter(0)):
			cw.writerow([k,v])

if __name__ == "__main__":
    main()
