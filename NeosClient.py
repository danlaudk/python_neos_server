#!/usr/bin/env python
import sys
import xmlrpclib
import time

NEOS_HOST="www.neos-server.org"
NEOS_PORT=3332
CONTACT_EMAIL = 'youremail@email.com'
INTERFACE = 'XML-RPC'
neos=xmlrpclib.Server("http://%s:%d" % (NEOS_HOST, NEOS_PORT))

if len(sys.argv) < 2 or len(sys.argv) > 3:
  sys.stderr.write("Usage: NeosClient <xmlfilename | help | queue>\n")
  sys.exit(1)

# Verify the connection was successful
test = neos.ping()
if neos.ping() != "NeosServer is alive\n":
    sys.stderr.write("Could not make connection to the NEOS server")
    sys.exit(1)

if sys.argv[1] == "queue":
    # Print NEOS job queue
    msg = neos.printQueue()
    sys.stdout.write(msg)

else:
    xml = ""

    # Try to read the XML file
    try:
        xmlfile = open(sys.argv[1], "r")
        buffer = 1
        while buffer:
            buffer = xmlfile.read()
            xml += buffer
        xmlfile.close()
    except (FileNotFoundError, FileExistsError, IOError):
        sys.stderr.write("The file was not found or does not exist")
        sys.exit(1)

    # Submit the optimization problem to NEOS
    (jobNumber, password) = neos.submitJob(xml, CONTACT_EMAIL, INTERFACE)
    sys.stdout.write("JobNumber = %d \n" % jobNumber)

    # Check to make sure the queue is not full
    if jobNumber == 0:
        sys.stderr.write("NEOS error: %s" % password)
        sys.exit(1)
    else:
        offset = 0
        status = ""
        # Print out partial job output while job is running
        while status != "Done":
            (msg, offset) = neos.getIntermediateResults(jobNumber, password, offset)
            sys.stdout.write(msg.data.decode())
            status = neos.getJobStatus(jobNumber, password)

        # Print out the final result
        msg = neos.getFinalResults(jobNumber, password).data
        sys.stdout.write(msg.decode())