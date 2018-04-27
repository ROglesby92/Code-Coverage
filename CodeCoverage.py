# import csv
"""
Read functions addresses from dump py

Authors: Matthew Oglesby, Ryan Oglesby




"""

import argparse
import csv
from ColorSupport import *



import ctypes

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_color(color, handle=std_out_handle):
    """(color) -> BOOL

    Example: set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    """
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool

#from colorama import Fore, Back, Style, init
#import color_console as cons
#init(autoreset=True)  # This resets the prints back to normal after each print


def beginEvaluation(dFile, cFile, verbose=False, selfFunc='UNSELECTED', toCSV='UNSELECTED'):
    f = dFile
    format_line = "-----------------------------------------"

    ST_FIND_FUNC_NAME = 1
    ST_FIND_FUNC_START_ADDRESS = 2
    ST_FIND_FUNC_END_ADDRESS = 3
    state = ST_FIND_FUNC_NAME

    # Create FuNction / Address List of List
    fnAdr_ll = []

    function_counter = 0

    # Count the amount of adresses visited in each node

    # Count the amount of nodes that get a hit and the amount of nodes that miss
    total_good_nodes = 0
    total_bad_nodes = 0
    node_counter = 0

    for line in f:

        if state == ST_FIND_FUNC_START_ADDRESS:
            code_line = line.partition(':')
            start_address = int(code_line[0], 16)
            node_counter = 1
            state = ST_FIND_FUNC_END_ADDRESS

        elif state == ST_FIND_FUNC_END_ADDRESS:
            if line.endswith(':\n'):

                # We found a new function name so we need to store the data from the last function before proceeding




                # Check to see if only 1 address in our range
                if node_counter == 1:
                    end_address = start_address

                # load the list temp_l with func name, start & end address,total nodes, good nodes, hit status, and a list
                # of each individual node in each function
                total_good_nodes = 0
                function__status = ""
                individual_nodes = []

                temp_l = [func_name, start_address, end_address, node_counter, total_good_nodes, function__status,
                          individual_nodes]
                node_counter = 0
                # Append temp_l to the list of list
                fnAdr_ll.append(temp_l)

                function_counter += 1

                # Store new function name, getting rid of the ':' and '\n' from end of file name
                func_name = line[:-2]

                state = ST_FIND_FUNC_START_ADDRESS


            else:
                code_line = line.partition(':')
                end_address = int(code_line[0], 16)
                node_counter += 1

                state = ST_FIND_FUNC_END_ADDRESS

        # This state is only hit on the first line of the DUMP file so put it at the end to prevent checking
        # for this state constantly
        elif state == ST_FIND_FUNC_NAME:
            if line.endswith(':\n'):
                func_name = line[:-2]

                state = ST_FIND_FUNC_START_ADDRESS

    f.close()

    #####################################################################################################################
    # At this point we have a list of list (fnAdr_ll) that contains all the function names, starting & ending addresses
    # Now we want to read in the Coverage file which contains a list of all the address visited and not visited.
    ######################################################################################################################



    # Open Coverage file
    f2 = cFile

    ST_FIND_START_OF_COVERAGE_DATA = 0
    ST_GET_VISITED_ADDRESS = 1
    state = ST_FIND_START_OF_COVERAGE_DATA

    visited_address_counter = 0

    # Visited Address List of List
    va_ll = []

    for line in f2:

        if state == ST_GET_VISITED_ADDRESS:
            visited_address = int(line.split('[', 1)[1].split(']')[0], 16)
            visited_state = int(line[-2], 16)

            temp_l = [visited_address, visited_state]
            va_ll.append(temp_l)

            visited_address_counter += 1

        if state == ST_FIND_START_OF_COVERAGE_DATA:
            if line.startswith('[0x'):
                state = ST_GET_VISITED_ADDRESS
            else:
                print('Non-address header information')

    f2.close()

    #####################################################################################################################
    # We now have 2 ListOfLists,
    #  fnAdr_ll --> Functions names with start & end address
    #  va_ll    --> Address' that have been visited
    # We now need to run through the Visited list and create the functions names with address
    #####################################################################################################################

    tmp_visited_start      = 0
    functions_covered_cntr = 0
    functions_partial_cntr = 0
    functions_missed_cntr  = 0
    total_node_counter     = 0

    for x in range(0, function_counter):

        tmp_function_name      = fnAdr_ll[x][0]
        tmp_function_adr_start = fnAdr_ll[x][1]
        tmp_function_adr_end   = fnAdr_ll[x][2]
        tmp_total_nodes        = fnAdr_ll[x][3]

        func_was_visited = 0;  # Flag used to indicate if function range was visited
        # Using function start and end address, find the corresponding visited address

        good_nodes_single = 0

        temporary_individual_nodes = []
        for y in range(tmp_visited_start, visited_address_counter):
            tmp_visited_address = va_ll[y][0]
            address_results = tuple()
            if (tmp_visited_address >= tmp_function_adr_start) and (tmp_visited_address <= tmp_function_adr_end):
                if (va_ll[y][1] == 1):
                    address_results = (va_ll[y][0], va_ll[y][1])
                    temporary_individual_nodes.append(address_results)
                    func_was_visited    = 1
                    good_nodes_single  += 1
                    total_good_nodes   += 1
                    total_node_counter += 1


                else:
                    address_results = (va_ll[y][0], va_ll[y][1])
                    temporary_individual_nodes.append(address_results)
                    total_node_counter += 1
                    total_bad_nodes    += 1

            else:

                break

        # adjust the index into the visited list so we don't need to always start from zero
        tmp_visited_start = y
        if verbose:
            fnAdr_ll[x][6] = temporary_individual_nodes
        fnAdr_ll[x][4] = good_nodes_single

        if func_was_visited == 1:
            # If all nodes connected
            if fnAdr_ll[x][4] == fnAdr_ll[x][3]:
               
                fnAdr_ll[x][5] = 'All Hit'

               
                set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
               
                print ('COVERED'),
                print(' %30s : %X ~ %X  Total Nodes: %3d | Good Nodes: %3d' % (
                    tmp_function_name, int(str(tmp_function_adr_start), 16), int(str(tmp_function_adr_end), 16),
                    int(str(tmp_total_nodes), 16), int(str(good_nodes_single), 16)))

                functions_covered_cntr += 1
            else:
                # Partial nodes hit
                fnAdr_ll[x][5] = "Partial Coverage"
             
                print('PARTIAL'),  # The comma at the end prevents new line
                print(' %30s : %X ~ %X  Total Nodes: %3d | Good Nodes: %3d' % (
                    tmp_function_name, int(str(tmp_function_adr_start), 16), int(str(tmp_function_adr_end), 16),
                    int(str(tmp_total_nodes), 16), int(str(good_nodes_single), 16)))
                #functions_covered_cntr += 1
                functions_partial_cntr += 1


        else:
            fnAdr_ll[x][5] = 'Miss'
       
            print('MISSED '),
            print(' %30s : %X ~ %X  Total Nodes: %3d' % (
                tmp_function_name, int(str(tmp_function_adr_start), 16), int(str(tmp_function_adr_end), 16),
                int(str(tmp_total_nodes), 16)))
            functions_missed_cntr += 1

    print(format_line)
    print('Total functions         = ' + str(function_counter))
    print('Total functions covered = ' + str(functions_covered_cntr))
    print('Total functions partial = ' + str(functions_partial_cntr))
    print('Total functions missed  = ' + str(functions_missed_cntr))

    if verbose:
        print(format_line)
        print('Total Addresses      = ' + str(total_node_counter))
        print('Total ' + Fore.YELLOW + Back.RED + 'MISSED ' + Style.RESET_ALL + ' Addresses = %d%% ' % ((float(total_bad_nodes) / total_node_counter) * 100))
        print('Total ' + Fore.RED + Back.GREEN  + 'COVERED' + Style.RESET_ALL + ' Addresses = %d%%  ' % ((float(total_good_nodes) / total_node_counter) * 100))

    

    if selfFunc != 'UNSELECTED':
        for list in fnAdr_ll:

            if list[0] == selfFunc:
                print(format_line)
                print(Back.LIGHTBLUE_EX + list[0])
                print("Total Address Elements: %d" % list[3])
                print(Fore.GREEN + Back.BLACK + 'Address Elements Accessed' + Style.RESET_ALL + ' = %d' % list[4])
                print(Fore.RED + Back.BLACK   + 'Address Elements Missed  ' + Style.RESET_ALL + ' = %d' % (list[3] - list[4]))
                print('Percent Covered : %.2d' % ((float(list[4]) / list[3] * 100)) + "%")

                if verbose:
                    print("Address Elements - 1:Covered, 0:Missed ")
                    print(list[6])
                    print(format_line)

    if toCSV != 'UNSELECTED':
        with open(toCSV, 'wt') as f:
            writer = csv.writer(f)
            writer.writerow(('Function Name', 'Start Address', 'End Address', 'Total Individual nodes'
                             , 'Total Hit Individual Nodes', 'Status:'))

            for i in range(len(fnAdr_ll)):
                row = fnAdr_ll[i]
                writer.writerow(row)


def main():
    """
    Main program gets start, argparse requies starter file, end file and -v optional verbose 
    """
    parser = argparse.ArgumentParser(
        description="Analyze Code Coverage data")
    parser.add_argument('dump_file', type=argparse.FileType('r'),
                        help="The dump file")
    parser.add_argument('coverage_file', type=argparse.FileType('r'),
                        help="the coverage file")

    parser.add_argument("--verbose", help="Show more data, good nodes , bad nodes", action="store_true")

    parser.add_argument("-f", "--function", help="Optional func to search explicitly", type=str, default="UNSELECTED")

    parser.add_argument("-csv", "--commaSeperatedValue", help="Option to write data into a CSV file of given file name",
                        type=str, default="UNSELECTED")

    args = parser.parse_args()

    dFile = args.dump_file
    cFile = args.coverage_file
    selNode = args.function
    isCSV = args.commaSeperatedValue
    isVerb = False

    if args.verbose:
        isVerb = True

    beginEvaluation(dFile, cFile, isVerb, selNode, isCSV)


if __name__ == '__main__':
    main()
