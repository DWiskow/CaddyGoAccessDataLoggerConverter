#!/usr/bin/python3

""" ***********************************************************************************

Takes Caddy log data (in JSON format) as input (provided in the form of either an 
existing Caddy log file, or alternatively streamed over a network using TCP/IP sockets)
and converts it into a format suitable for analysis by goAccess (https://goaccess.io/).

To use the output file, goaccess must be run with the log-format specified as shown
below

    goaccess access.goaccess.log --log-format="%d %t %v %h %m %U %H %s %b %T %R %u" \
                                 --date-format=%F --time-format=%H:%M:%S -o access.html

    Note: when running Caddy the Caddyfile must specify "format json" and set the 
          output as either a file name or a network address as shown in one of
          the two examples detailed below

          Caddyfile - file output                  Caddtfile - network socket stream
          -----------------------                  ---------------------------------

          localhost {                              localhost {
                file_server                            file_server
                log {                                  log {
                    output file access.log {               output net localhost:55555
                        roll_local_time true               format json
                    }                                  }
                    format json                    }
                }
          }

*********************************************************************************** """

import sys, signal, getopt, socket, json
from datetime import datetime
from time import sleep

networkAddress = ''
inputJSONfilename = ''
timeInterval = 0
outputGoAccessFilename = ''
outputJSONfilename = ''

def shortHelp():
    print()
    print('   ./caddyLog.py -h -n <networkAddress> -i <inputJSONfilename> -t <timeInterval>')
    print('                    -g <outputGoAccessFilename> -j <outputJSONfilename>')
    print()
    print('   use ./caddyLog.py --help to obtain more comprehensive help')
    print()

def longHelp():
    print()
    print('   ./caddyLog.py -h -n <networkAddress> -j <inputJSONfilename> -i <timeInterval>')
    print('                    -g <outputGoAccessFilename> -o <outputJSONfilename>')
    print()
    print('   Example(s)')
    print('   __________')
    print()
    print('   ./caddyLog.py -n localhost:55555 -g access.goaccess.log -j access.json ')
    print()
    print('                 set up a TCP/IP network socket server on IP address localhost:55555')
    print('                 and output any log data streamed to it by Caddy over the network to')
    print('                 a file named "access.goaccess.log" (containing Caddy log data converted')
    print('                 into a format compatible with goAccess - https://goaccess.io/) AND ALSO')
    print('                 to an output file named "access.json" (containing the complete Caddy log')
    print('                 data in JSON format)')
    print()
    print('                 optionally select only the -g [--outputGoAccessFilename] OR the -o')
    print('                 [--outputJSONfilename] to output a single file of the required')
    print('                 format')
    print()
    print('   ./caddyLog.py -i access.log -g access.goaccess.log')
    print()
    print('                 read in the data from the file "access.log" (in JSON format) and write')
    print('                 out a file named "access.goaccess.log" (containing the Caddy log data')
    print('                 converted into a format compatible with goAccess).')
    print()
    print('   ./caddyLog.py -i access.log -i 600 -g access.goaccess.log')
    print()
    print('                 read in the data from the file "access.log" (in JSON format) and write')
    print('                 out a file named "access.goaccess.log" (containing the Caddy log data')
    print('                 converted into a format compatible with goAccess), then repeatedly')
    print('                 sleep for 10 minutes (600 seconds) before checking to see if any')
    print('                 additional Caddy log data has been written to "access.log". If')
    print('                 additional data has been added to "access.log", then convert it and')
    print('                 append it to "access.goaccess.log" before again sleeping.')
    print()
    print('   Options and arguments')
    print('   _____________________')
    print()
    print('   -h --help')
    print()
    print('      output comprehensive help for users of caddyLog.py')
    print()
    print('   -n --networkAddress <nnn.nnn.nnn.nnn:ppppp>')
    print()
    print('      Set the IP 4 address and PORT to be used by the caddyLog.py TCP/IP network')
    print('      socket server. This should be the same <IP address> and <port> as specified')
    print('      in the Caddyfile used when Caddy is run/started.')
    print()
    print('      If this option is specified caddyLog.py will run indefinitely. To terminate')
    print('      caddyLog.py use ctrl-c or stop the task/service')
    print()
    print('   -j --inputJSONfilename <filename>')
    print()
    print('      The filename of an existing Caddy log file to be converted and output.')
    print()
    print('   -i --timeInterval <seconds>')
    print()
    print('      The time, in seconds for which caddyLog.py will sleep, after converting the')
    print('      current content of the <inputJSONfilename>, before checking to see if any')
    print('      additional Caddy log data has been appended to the <inputJSONfilename> by Caddy.')
    print('      To terminate caddyLog.py use ctrl-c or stop the task/service')
    print()
    print('      This option may only be selected when optipon -i [--inputJSONfilename]')
    print('      has also been specified. If this option is set to zero or omitted, caddyLog.py')
    print('      will simply convert and output the existing Caddy log data and then terminate')
    print('      when it detects the input file EOF.')
    print()
    print('   -g --outputGoAccessFilename <filename>')
    print()
    print('      convert the Caddy log data from either the <inputJSONfilename> OR the TCP network')
    print('      socket stream into a format suitable for input to goAccess and write it into the')
    print('      file <filename> specified')
    print()
    print('   -o --outputJSONfilename <filename>')
    print()
    print('      output the complete Caddy log data from the TCP network socket stream into the file')
    print('       <filename> specified. This will be an exact copy of a standard Caddy JSON log file,')
    print('      but by replicating it over a TCP/IP network socket it can be captured on an')
    print('      alternate server.')
    print()
    print('      This option may ony be selected when option -n [--networkAddress] is specified.')
    print()
    print('   Using caddyLog.py output with goAccess')
    print('   _______________________________________')
    print()
    print('   To process the output file from caddyLog.py with goaccess, use the following command')
    print()
    print('      goaccess access.goaccess.log --log-format="%d %t %v %h %m %U %H %s %b %T %R %u" \\') 
    print('                                   --date-format=%F --time-format=%H:%M:%S -o filename.html')
    print()
    print('   This maximises the data provided to goAccess and optimises the analysis available.')
    print()

def processArgs(argv):

    global networkAddress
    global inputJSONfilename
    global timeInterval
    global outputGoAccessFilename
    global outputJSONfilename

    try:
        opts, args = getopt.getopt(argv,"hn:i:t:g:j:", ["help", "networkAddress=", "inputJSONfilename=", "timeInterval=", "outputGoAccessFilename=", "outputJSONfilename="])
    except getopt.GetoptError:
        shortHelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h'):
            shortHelp()
            sys.exit(0)
        elif opt in ("--help"):
            longHelp()
            sys.exit(0)
        elif opt in ("-n", "--networkAddress"):
            networkAddress = arg
        elif opt in ("-i", "--inputJSONfilename"):
            inputJSONfilename = arg
        elif opt in ("-g", "--outputGoAccessFilename"):
            outputGoAccessFilename = arg
        elif opt in ("-j", "--outputJSONfilename"):
            outputJSONfilename = arg
        elif opt in ("-t", "--timeInterval"):
            try:
                timeInterval = int(arg)
            except:
                print()
                print('{} - ERROR: Interval must be a whole number of seconds'.format(datetime.now()))
                shortHelp()
                sys.exit(2)

    if (len(args) > 0):
        print()
        print('{} - ERROR: superfluous trailing arguments on command line'.format(datetime.now()))
        shortHelp()
        sys.exit(2)
    
    if (networkAddress and inputJSONfilename):
        print()
        print('{} - ERROR: Input can not be both TCP/IP network socket AND JSON input file'.format(datetime.now()))
        shortHelp()
        sys.exit(2)

    if (networkAddress and (timeInterval > 0)):
        print()
        print('{} - ERROR: Interval time must be omitted (or zero) when TCP/IP network socket is selected as input'.format(datetime.now()))
        shortHelp()
        sys.exit(2)

    if (inputJSONfilename and outputJSONfilename):
        print()
        print('{} - ERROR: Output can not be JSON file when JSON input file is also selected'.format(datetime.now()))
        shortHelp()
        sys.exit(2)
        
    if ( (not outputGoAccessFilename) and (not outputJSONfilename) ):
        print()
        print('{} - ERROR: No output fie name specified'.format(datetime.now()))
        shortHelp()
        sys.exit(2)

def convertJSONtoGoAccess (JSONdata):
    ts = str(datetime.fromtimestamp(JSONdata['ts']))
    date = ts[0:10]                                                             #d
    time = ts[11:19]                                                            #t
    virtualHost = JSONdata['request']['host']                                   #v

    host = (JSONdata['request']['remote_addr'])                                 #h
    host = host[0:host.rindex(':')]
    if (host[0] == '['):
        host = host[1:host.rindex(']')]

    method = JSONdata['request']['method']                                      #m
    uri = JSONdata['request']['uri']                                            #U
    proto = JSONdata['request']['proto']                                        #H

    status = str( JSONdata['status'] )                                          #s
    size = str( JSONdata['size'] )                                              #b
    latency = str( JSONdata['duration'] )                                       #T

    if "Referer" in JSONdata['request']['headers'].keys():                      #R
        referer = JSONdata['request']['headers']['Referer'][0]
    else:
        referer = 'unknown'
    
    if "User-Agent" in JSONdata['request']['headers'].keys():                   #u
        user_agent = '"'+JSONdata['request']['headers']['User-Agent'][0]+'"'
    else:
        user_agent = '""'

    goAccessData = date+' '+time+' '+virtualHost+' '+host+' '+method+' '+uri+' '+proto+' '+status+' '+size+' '+latency+' '+referer+' '+user_agent
    return goAccessData

def main():
    global networkAddress
    global inputJSONfilename
    global timeInterval
    global outputGoAccessFilename
    global outputJSONfilename

    print()
    print('{} - INITIALISING: caddyLog.py (Caddy/GoAccess data logger & converter - copyright 2020 Dorian Wiskow)'.format(datetime.now()))

    processArgs(sys.argv[1:])

    if (inputJSONfilename):
        try:
            with open(outputGoAccessFilename, 'w') as g:
                totalLogCount = 0
                try:
                    with open(inputJSONfilename) as j:
                        print('{} - processing JSON input file: {}'.format(datetime.now(), inputJSONfilename))
                        batchLogCount = 0
                        while True:
                            line = j.readline()
                            if (line != ""):
                                JSONdata = json.loads(line)
                                goAccessData = convertJSONtoGoAccess(JSONdata)
                                g.write(goAccessData+'\n')
                                totalLogCount += 1
                                batchLogCount += 1
                            elif (timeInterval > 0):
                                g.flush()
                                if (batchLogCount):
                                    print('{} - {} log entries written to {}'.format(datetime.now(), str(batchLogCount), outputGoAccessFilename))
                                    batchLogCount = 0
                                print('{} - sleeping for {} seconds before checking for additional log entries'.format(datetime.now(), str(timeInterval)))
                                sleep(timeInterval)
                            elif (timeInterval == 0):
                                print('{} - TOTAL: {} log entries written to {}'.format(datetime.now(), str(totalLogCount), outputGoAccessFilename))
                                print()
                                batchLogCount = 0
                                g.flush()
                                break
                except FileNotFoundError:
                    print()
                    print('{} - ERROR: Input file "{}" not found'.format(datetime.now(), inputJSONfilename))
                    shortHelp()
                    sys.exit(2)
        except IOError:
            print()
            print('{} - ERROR: Output file "{}" error'.format(datetime.now(), outputGoAccessFilename))
            shortHelp()
            sys.exit(2)

    if (networkAddress):
        host = networkAddress[0:networkAddress.rindex(':')]
        port = int(networkAddress[(networkAddress.rindex(':')+1):])
        print('{} - TCP/IP NETWORK socket server created @ {}:{}'.format(datetime.now(), host, port))
        with socket.socket(family=socket.AF_INET) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen()
            try:
                if (outputGoAccessFilename):
                    g = open(outputGoAccessFilename, 'w')
                if (outputJSONfilename):
                    j = open(outputJSONfilename, 'w')
                totalLogCount = 0
                while True:
                    print('{} - Caddy not connected: Waiting for connection'.format(datetime.now()))
                    connection, client_address = sock.accept()
                    print('{} - Caddy @ {}:{} connected'.format(datetime.now(), client_address[0], client_address[1]))
                    batchLogCount = 0
                    with connection:
                        while True:
                            data = connection.recv(4096)
                            if data:
                                JSONdata = json.loads(data.strip().decode())
                                if (outputJSONfilename):
                                    j.write(json.dumps(JSONdata)+'\n')
                                    j.flush()
                                if (outputGoAccessFilename):
                                    goAccessData = convertJSONtoGoAccess(JSONdata)
                                    g.write(goAccessData+'\n')
                                    g.flush()
                                totalLogCount += 1
                                batchLogCount += 1
                            else:
                                if (batchLogCount):
                                    print('{} - {} log entries written to {}'.format(datetime.now(), str(batchLogCount), outputGoAccessFilename))
                                    batchLogCount = 0
                                break
            except IOError:
                print()
                print('{} - ERROR: Output file "{}" error'.format(datetime.now(), outputGoAccessFilename))
                shortHelp()
                sys.exit(2)
            finally:
                print('{} - TOTAL: {} log entries written to {}'.format(datetime.now(), str(totalLogCount), outputGoAccessFilename))
                print()
                if (outputGoAccessFilename):
                    g.close()
                if (outputJSONfilename):
                    j.close()


def signal_handler(signal, frame):
    print()
    print('{} - Terminating . . . '.format(datetime.now()))
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
