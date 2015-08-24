# ---------------------------------------------------------------------------
# GDB_CreateVersionis.py
# Created on: 2015-08-19

# Description: 
# Creates geodatabase versions from a input file with listed name and parent version pairs

# Command Line Example: 
# GDB_CreateVersions.py -d "Database Connections/geobase.sde" -i "GeodatabaseVersions.lst" -l "logfile.log"

# Command Line Arguments
# -d: Database connection
# -i: To Do List
# -l: Log file

# Input file format (must have header row):
# VersionName,ParentVersion
# Editing,DBO.Default
# GIS Manager,DBO.Editing

#---------------------------------------------------------------------------

# Set the necessary product code
import arceditor

# Import arcpy module
import arcpy
import logging
import sys, getopt
import csv

def main(argv):
    try:
      opts, args = getopt.getopt(argv,"d:i:l:",["gdbconn=","inputlist=","logfile="])
    except getopt.GetoptError:
      print 'test.py -d <gdbconn> -i <inputlist> -l <logfile>'
      sys.exit(2)

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
  
    # Get input file
    try:
        todo = csv.DictReader(open(InputList, 'r'),  delimiter=',')
    except:
        logging.info('Failed to read input list!')
        sys.exit(2)

    # Read through input file
    for row in todo:
        print row
        NewVersion = row.get('VersionName')
        ParentVersion = row.get('ParentVersion')
        # Create version
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