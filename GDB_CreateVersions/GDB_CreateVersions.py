# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# GDB_RecAndPost.py
# Created on: 2015-08-19

# Description: 
# Reconciles and Posts a list of versions found in one of two files:
#       todolist.txt (all processed by the same user)
#       todolist.lst (all processed by different users ... as described in the file)
#   It uses connection.txt to find the server and instance.
#   It uses the recnpost.cred to make it's initial connection and, depending on which
#       list is used, process all of the versions.
#   It writes out a log file containing a summary of all the attempted work, whether
#       each attempt succeeds or fails, and why.  A new log file is generated on each
#       day that it is run.
#   All files are in the installation directory.
#   The idea is that you configure this application to run with the Windows Task Scheduler
#       or an RDBMS Job ... so that it runs on a regular interval.

# Command Line Example: 
# GDB_RecAndPost.py -d "Database Connections/geobase.sde" -i "GeodatabaseVersions.lst" -l "logfile.log"
# Command Line Arguments
# -d: Database connection
# -i: To Do List
# -l: Log file


#---------------------------------------------------------------------------

# Set the necessary product code
import arceditor

# Import arcpy module
import arcpy
import logging
import sys, getopt
import csv
from time import  strftime, localtime

def main(argv):
    print 'start'
    
    try:
      opts, args = getopt.getopt(argv,"d:i:l:e:",["gdbconn=","inputlist=","logfile="])
    except getopt.GetoptError:
      print 'test.py -d <gdbconn> -i <inputlist> -l <logfile>'
      sys.exit(2)

    print 'parse options'

    for o, a in opts:
        if o in ("-d", "--gdbconn"):
            GDBConn = a
        elif o in ("-i", "--inputlist"):
            InputList = a
        elif o in ("-l", "--logfile"):
            LOG_FILENAME = a
        else:
            assert False, "unhandled option"
            
    ## Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=  LOG_FILENAME,
                        filemode='a')
    # Local variables:
    try:
        todo = csv.DictReader(open(InputList, 'r'),  delimiter=',')
    except:
        logging.info('Failed to read input list!')
        sys.exit(2)

    for row in todo:
        print row
        NewVersion = row.get('VersionName')
        ParentVersion = row.get('ParentVersion')
        #Generate Rec and Post Log file name
        try:
            arcpy.CreateVersion_management(in_workspace=GDBConn, 
                                           parent_version=ParentVersion, 
                                           version_name=NewVersion, 
                                           access_permission="PUBLIC")
        except:
            print arcpy.GetMessages(2)
            logging.info("ERROR: Creating " + NewVersion + " under " + ParentVersion + ": " + arcpy.GetMessages(2))

    logging.info("GDB_CreateVersions complete!")
    logging.info("****************************")
       

if __name__ == "__main__":
   main(sys.argv[1:])