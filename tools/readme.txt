
the first tool is data_ticker_extract.py

this is a utility that skims the big data file and pulls out all lines with the ticker symbol specified
for now the ticker name is the first field ( row[ 0 ] ).
data gets output into cutting_board/

to run it, just:

python data_ticker_extract.py

(the ticker ysmbol is currently in the top of code, no command line args supported yet)


note: reference/ directory is just code examples that have useful snippets

