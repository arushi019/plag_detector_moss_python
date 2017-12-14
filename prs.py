import subprocess
import sys
import urllib.request
lang=input("enter language ")
files=[]
print("Enter name of files or path")
files.append(input())
files.append(input())
#string=" -l "+lang+" "+files[0]+" "+files[1]
#print(string)
perl_script=subprocess.check_output(["C:\\cygwin64\\bin\\perl","C:\\Users\\Arushi Chauhan\\Documents\\moss_sub_script.pl",'-l',lang,files[0],files[1]])
#perl_script.communicate()
#print(perl_script.decode("utf-8"))
l=perl_script.decode("utf-8").split()
print(l)
fp=urllib.request.urlopen(l[-1])
mb=fp.read()
web_string=mb.decode("utf-8")
fp.close()
l2=web_string.split()
print(l2)
pos=l2.index('<TD')
print(l2[pos+1])
final_string=l2[pos+1]
pos=final_string.index('>')
final_string=final_string[pos+1]
num_lines=int(final_string)
print("number of lines matching ",num_lines)
