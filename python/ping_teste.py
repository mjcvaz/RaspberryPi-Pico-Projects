#!/usr/bin/python

import datetime
import os
import sys
import time

now = datetime.datetime.now()

#path_prefix = "/usr/local/logs/scripts/python/cisco_cfg/"
path_prefix = "result/"
filename = "%s_%.2i-%.2i-%i_%.2i-%.2i-%.2i" % ('ping',now.day,now.month,now.year,now.hour,now.minute,now.second)
output_file = path_prefix + filename

hosts = "C:\Users\884103\github\mjcv-projects\python\hosts_imps.txt"
hostsFile = open(hosts, "r")
lines = hostsFile.readlines()
fp=open(output_file,"w")

os.system("clear")
mine = []

for linha in lines:
    #print (linha)
    ip = linha
    #ip, codigo, loja, xxxx = linha.split(":", 4)
    result = os.system("ping -c 1 " + ip)
    #os.system("clear")
    if result == 0:
        data = datetime.datetime.now().strftime("%Y-%m-%d")
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        #registo = ip + ":" + codigo + ":" + loja + ":1:" + data + ":" + hora
        registo = ip + ":" + data + ":" + hora
        print (registo)
        mine.append(registo)

        os.system("clear")
        for j in mine:
            #ip, codigo, loja, st, data, h, m, s = j.split(":", 8)
            ip, st, data, h, m, s = j.split(":", 6)
            out = "%s%s-%s%s%s %s:%s:%s%s" % ("O IP ", ip, " em ", data, h, m, s, " is up")
            #out = "%s%s%s" % ("O IP ", j.rstrip() , " is up")
            print (out)
fp.write(out + "\n")

fp.close()

#fim
