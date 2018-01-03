# Code-Coverage
Some work i did that involved evaluating "coverage" logs. Evaluating large sets of data and recording hit's or misses.

"Small_Dump_File" - Example of some data produced from a Mem2Dump function.
"ExCoverageLog"   - Shows how data is stored and represented in the coverage log
"ExMemFile"       - Shows how some data in memory is stored.

Mem2Dump.py
- Implemented to scan large memory files and grab only the information that we need under the "Content" dumps
- Once the program has found all the content dumps, it will show a list of found files, and 
 gives the user the ability to extract the data of specific content dumps or the entire list into seperate files.
- These files can be later used to ran against coverage files

CodeCoverage.py 
- Implemented functions to evaluate total amount of complete hits, partial hits and misses of the test data.
- Various functions such as "verbose" to show more individual node data, and options to forward the data into CSV files for later evaluation.

When dump_file.dump_short is ran against its coverage log file, we would get a result looking like 

-----------------------------------------

Total functions 111
Total functions covered = 73
Total functions missed  = 38
Total Time is 0.26514420826376645

-----------------------------------------
