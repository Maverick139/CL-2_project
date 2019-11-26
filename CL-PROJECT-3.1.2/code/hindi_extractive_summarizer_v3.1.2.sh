# !/bin/bash

# Input Argument: file_path
if [ $# -ne 1 ]
then
	echo Please enter exactly one argument: filepath
else
	cat $1 > ../hindi-part-of-speech-tagger/hindi.input.txt
	cd ../hindi-part-of-speech-tagger/
    make -f Makefile tag
    cd ../code
	cat ../hindi-part-of-speech-tagger/hindi.output > pos_output.txt
	python3 hindi_summarizer_3.1.1.py > pyout.txt
    gedit pyout.txt
fi
