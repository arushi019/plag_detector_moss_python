#!/bin/python3
import subprocess
import sys
import urllib.request
import mosspy
import os

userid = "80676590" # <==== Enter your MOSS user id here.
pathprefix = os.path.abspath(__file__)[:-len(__file__)] # This will point to the directory containing this file. The script assumes the SIM and JPlag files are relative to this

def check_language(language):
    #checks if the language input is valid. If invalid,program quits
    accepted=["java17", "java15", "java15dm", "java12", "java11", "python3", "c", "c++", "text",]
    if language not in accepted:
        print("language not accepted")
        quit()

def nStrip(s):
    if (s.rfind("/")!=-1):
        return s[s.rfind("/")+1:]
    return s

################
#Take user input
################
if __name__=='__main__':

    ####
    # Use command line arguments  to execute this script
    #   Example command : python3 jplagRunner.py java17 ./Codes/Case1v5/
    # The languages accepted are checked in the check_language() function
    # Invalid invocation results in a usage message being displayed.
    ####

    dynamic_denom = 0
    moss_d={}
    sim_d={}
    jplag_d={}

    if(len(sys.argv) != 3):
        print("Usage: python3 jplagRunner.py <language> <directory_location>")
        print("\t<language> : ","java17", "java15", "java15dm", "java12", "java11", "python3", "c", "c++", "text")
        print("\t<directory_location> : The location where all code files are present, relative to this python file. Subdirectories are not scanned.")
        print("NOTE: Ensure that you have JAVA >= 1.7 installed and configured correctly in order for JPlag to work !")
        quit()

    lang=sys.argv[1]
    files=sys.argv[2]
    jplag_files=sys.argv[2]
    check_language(lang)
    moss_lang=lang
    sim_lang=lang
    if files[-1]!='/':
        files=files+'/'
    files=files+"*."
    if lang=="java17" or lang=="java15" or lang=="java15dm" or lang=="java12" or lang=="java11":
        files=files+"java"
        moss_lang="java"
        sim_lang="java"
    elif lang=="python3":
        files=files+"py"
        moss_lang="python"
        sim_lang="disable"
    elif lang=="c":
        files=files+"c"
        moss_lang="c"
        sim_lang="c"
    elif lang=="c++":
        files=files+"cpp"
        moss_lang="cc"
        sim_lang="c++"
    else:
        files=files+"txt"
        moss_lang="ascii"
        sim_lang="text"


    #######
    #MOSS
    #######
    m = mosspy.Moss(userid, moss_lang)    
    # Submission Files
    m.addFilesByWildcard(files+"*")

    if(userid == ""):
        print("Cannot Run Moss Script without user id ! Enter the id in the automation file.")
        quit()
    else:
        l = m.send() 
        #print(l)
        try:
            fp=urllib.request.urlopen(l)
            mb=fp.read()
            web_string=mb.decode("utf-8")
            fp.close()
            l2=web_string.split()
            #print(l2)
            pos_start=l2.index('<TABLE>')
            pos_end=l2.index('</TABLE>')
            file_ptr=pos_start+6
            per_ptr=pos_start+7
            # print("\nMOSS Results")
            while per_ptr<pos_end:
                temp_file_name1=nStrip(l2[file_ptr].split('>')[1])
                temp_file_name2=nStrip(l2[file_ptr+3].split('>')[1])
                file_ptr=file_ptr+8
                temp_per1=l2[per_ptr].split('<')[0]
                temp_per2=l2[per_ptr+3].split('<')[0]
                per_ptr=per_ptr+8
                #moss_list.append([temp_file_name1.split('\\')[-1],temp_file_name2.split('\\')[-1],temp_per1])
                key=temp_file_name1.split('\\')[-1]+" "+temp_file_name2.split('\\')[-1]
                key2=temp_file_name2.split('\\')[-1]+" "+temp_file_name1.split('\\')[-1]
                value=float(temp_per1[1])*10+int(temp_per1[2])
                moss_d[key]=value
                moss_d[key2]=value
                # print(temp_file_name1,temp_per1,temp_file_name2,temp_per2)
                dynamic_denom+=1
        except Exception as e:
            pass
        
    # print(moss_d)
    # print("--------------------------------------------------------------------------------")
    
    ######
    #SIM
    ######
    if sim_lang!="disable":
        sim_string=pathprefix+"SIM/sim_"+sim_lang+".exe"
        temp=subprocess.check_output([sim_string,"-pe",files])
        string=temp.decode("utf-8").split()
        sim_ptr=len(string)-1
        k=0
        sim_results=[]
        while string[sim_ptr]!='tokens':
            key=''
            key2=''
            value=0
            if string[sim_ptr]!='material':
                if string[sim_ptr] not in ['consists','of','for','%']:
                    sim_results.append(string[sim_ptr])
            sim_ptr=sim_ptr-1
        key=''
        for i in range(0,len(sim_results),3):
            # if i%3==0:
            #     key=key+sim_results[i].split('/')[-1]
            #     key2=sim_results[i].split('/')[-1]+key2
            # elif i%3==2:
            #     key=key+sim_results[i].split('/')[-1]
            #     key2=sim_results[i].split('/')[-1]+key2
            # else:
            #     value=float(sim_results[i])
            #     sim_d[key]=value
            #     sim_d[key2]=value
            #     key=''
            #     key2=''
            key = nStrip(sim_results[i])+" "+nStrip(sim_results[i+2])
            key2 = nStrip(sim_results[i+2])+" "+nStrip(sim_results[i])
            value = float(sim_results[i+1])
            sim_d[key2] = value
            sim_d[key] = value
            # print(sim_results[i])
        dynamic_denom+=1
        # print("\nSIM Results")
        #print(sim_results)
        # print(sim_d)
    else:
        print("\nSIM results not available for Python")
        quit()
    # print("-------------------------------------------------------------------------------")


    ########
    #JPLAG
    ########
    jplag_string=pathprefix+"JPlag/jplag-2.11.9-SNAPSHOT-jar-with-dependencies.jar"
    temp=subprocess.check_output(["java","-jar",jplag_string,"-vq","-l",lang,jplag_files])
    output = temp.decode("UTF-8")
    i = output.find("submissions")
    jplag_results = output[i+12:-1]
    jplag_list=jplag_results.split()
    key=''
    key2=''
    #print(jplag_list)
    for i in range(len(jplag_list)):
        if i%3==1:
            temp=jplag_list[i].split('-')
            #print(temp)
            key=temp[0]+" "+temp[1][:-1]
            key2=temp[1][:-1]+" "+temp[0]
        if i%3==2:
            value=float(jplag_list[i])
            jplag_d[key]=value;
            jplag_d[key2]=value;
            key=''
            key2=''
    dynamic_denom+=1
    # print("JPlag Results")
    # print (jplag_d)


    #####
    # Printing results
    #####
    li = []
    for i in sorted(jplag_d.keys()):
        x = i.split(' ')
        if(((x[0]+" " +x[1]) in li) or ((x[1]+" " +x[0]) in li)):
            continue
        else:
            li.append(x[0]+" "+x[1])

    print("Results : (All values in %ages) - \n")
    print(("{0:<"+str(len(sorted(jplag_d.keys())[0]))+"} {1:>10} {2:>10} {3:>10} {4:>10}").format("Code Files:","MOSS","JPlag","SIM","Average"))
    # for i in sorted(jplag_d.keys()):
    for i in li:
        print(("{0:<"+str(len(sorted(jplag_d.keys())[0]))+"} {1:>10} {2:>10} {3:>10} {4:>10.2f}").format(i,jplag_d[i],sim_d[i],moss_d[i],(jplag_d[i]+sim_d[i]+moss_d[i])/3))
        # print(i,jplag_d[i],sim_d[i],moss_d[i])
