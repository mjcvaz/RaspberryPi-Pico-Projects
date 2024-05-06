#!/usr/bin/python

import datetime
import os
import sys
import time

now = datetime.datetime.now()

filename = "%s_%.2i-%.2i-%i_%.2i-%.2i-%.2i" % ('ping',now.day,now.month,now.year,now.hour,now.minute,now.second)

print (filename)

data = datetime.datetime.now().strftime("%d-%m-%Y")
hora = datetime.datetime.now().strftime("%H:%M:%S")

registo = data + ":" + hora
print (registo)

#fim
