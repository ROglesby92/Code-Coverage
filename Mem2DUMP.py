"""
Code to parse Mem files
Scans memory file for content dumps, stores them in a Dictionary with the keys being the name of the content dumps
and the values being lists of all lines of data in between those dumps.

Once the content has been sorted into a dictionary, the user can create a file of their choice using a key value from
the dictionary, or optionally they can create every content file in the dictionary into its own file.

Author: Ryan Oglesby


Use generateAllContentFiles() function to make every content key from the dictionary into its own file so it is
 able to be read with functions



"""
import os # Used to check files.
import argparse

def begine_file_parse(mFile, dFileName, dump_all, content_section):

    print 'begine_file_parse was passed %s for the dump file name' % dFileName

    if dump_all == True:
        print 'Dump all the content sections'
    else:
        print('Dump nothing')

    if content_section == "NO_FILE":
        print 'No specific section is asked for'
    else:
        print 'Dump section %s' % content_section



    STATE_addLine = False

    # dumpList = []  # List of all of our dump's
    _tempDump = []  # Each list temporarily goes here
    _dumpDict = {}  # Dictionary of of memory file values.

    for line in mFile:  # Go through the mem file
        line = line.split()

        if line:

            if line[0] == "Content":  # Encounter the first dump file

                if STATE_addLine:  # If we are already appending a dump file

                    # dumpList.append(_tempDump)  # Then append it to the total and start over
                    # noinspection PyUnboundLocalVariable
                    _dumpDict[_Name] = _tempDump
                    _tempDump = []

                _Name = line[3][1:]
                print("Content Dump found: %s" % _Name)  # See what content we are looking at

                _dumpDict.setdefault(_Name, [])

                STATE_addLine = True  # If its our first time seeing content, dont add a empty list
                continue  # Don't add the "content of" line

            if STATE_addLine:  # Append the line
                _tempDump.append(line)

        else:
            continue

    # End of the file, append the last dump file?
    # dumpList.append(_tempDump)

    _dumpDict[_Name] = _tempDump

    # Dictionary to present the names of the content file with the amount of lines in the content file.
    # A close representation to how many function values are in the file
    _nameCountDict = {}

    for key, value in _dumpDict.items():
        _nameCountDict.setdefault(key, len(value))

    print("Total Content Files: " + str(len(_dumpDict)))
    print("Names / lines of data in each content section")
    print(_nameCountDict)

    if dump_all == True:
        generateAllContentFiles(_dumpDict)

    # Form the Output File Name, if none given on CMD line then name it based on Content Section Name
    #  if a name was provided on command line then use that name for the dump
    if content_section != 'NO_FILE':
        if dFileName == 'NO_FILE':
            print 'No Output file name was given, defaulting to %s.DUMP' % _Name
            OutputFileName = content_section + '.DUMP'
        else:
            OutputFileName = dFileName

        singleContentFile( OutputFileName, _dumpDict, content_section)  # Example to create a single dict file.




# If the file is empty, this returns true.
def is_file_empty(filename):
    return os.stat(filename).st_size == 0


# Creates a file with unique filename, and closes it. Later reopened to populate with data from content file.
def create_file(filename, mode='w'):
    new_file = open(filename, mode)
    new_file.close()



# Populate a file with the contents of the content file,
def populate_file(filename, _dumpDict, contentSection):
    with open(filename, 'w') as output:
        outputList = _dumpDict[contentSection]
        for line in outputList:
            #output.write(str(line) + '\n')
            #output.write(str(line).replace('[','').replace(']','') + '\n')
            # no WORKIE! output.write(line.replace('[', '').replace(']', '') + '\n')
            #output.write(str(line).replace('[',''))
            output.write(' '.join(map(str,line)))
            output.write('\n')
        print(filename + " File generated")
        output.close()


def singleContentFile(fileName, _dumpDict,  contentName):
    fName = fileName
    cName = contentName
    create_file(fileName)
    print('\n' + "Generating file...." + fileName)
    if is_file_empty(fileName):
        populate_file(fileName, _dumpDict, contentName)

        print("...File created")
    else:
        print("File already populated with data,create new file name or delete file")


# Generate all content dumps into personal files appended with contentDumpFile

def generateAllContentFiles(_dumpDict):
    for x in _dumpDict:
        file_Name = x + "_DUMP.txt"
        create_file(file_Name)
        if is_file_empty(file_Name):
            populate_file(file_Name, _dumpDict, x)

""""
Un # these functions to run them, the singleContentFile function you just replace the "contentName" with a key from the
dictionary if you want to make a single list.

Or alternately you can use generateAllContentsFiles() which will just make a individual file of each content dump

"""
#if content_
#singleContentFile("roDataFileSingle", '.rodata')  # Example to create a single dict file.

#generateAllContentFiles()

def main():
    """
    Main program gets start, argparse requies starter file, end file and -v optional verbose 
    """
    dFileName = "NO_FILE"
    content_section = "NO_FILE"


    parser = argparse.ArgumentParser(
        description="Parses .MEM file, produces .DUMP file used by VP and Coverage tool")

    parser.add_argument('mem_file', type=argparse.FileType('r'),
                        help=".MEM file, INPUT - produced with FW Build")

    parser.add_argument('-o', action='store', dest='dFileName', default='NO_FILE',
                        help='File name of output file')

    parser.add_argument('-a', '-all',  action='store_true', default=False,
                        help='Dump all Content Sections into individual files')

    parser.add_argument('-n', action='store', dest='content_section', default='NO_FILE',
                        help='Dumps a specific content section based on name. (Example: -n SplitRom )')

    #parser.add_argument("--verbose", help="Show more data, good nodes , bad nodes", action="store_true")

    #parser.add_argument("-f", "--function", help="Optional func to search explicitly", type=str, default="UNSELECTED")

    #parser.add_argument("-csv", "--commaSeperatedValue", help="Option to write data into a CSV file of given file name", type=str, default="UNSELECTED")

    args = parser.parse_args()

    #dFileName = args.dumpFileName
    mFile = args.mem_file
    print dFileName
    print args.dFileName
    if args.dFileName != 'NO_FILE':
        dFileName = args.dFileName
    print 'dFileName is now %s' % dFileName
    print 'Done!'

    #selNode = args.function
    #isCSV = args.commaSeperatedValue
    #isVerb = False
    if args.a:
        dump_all=True
    else:
        dump_all=False


    begine_file_parse(args.mem_file, dFileName, dump_all, args.content_section)


if __name__ == '__main__':
    main()
