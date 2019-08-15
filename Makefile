PACKAGE_FILES = spec/run_autograder spec/test_* spec/score_* spec/*.sh spec/nand2tetris/tools/*

%.test: spec/cases.% $(PACKAGE_FILES) 
	export GRADESCOPE_DEV=true; cd spec; ./run_autograder $*
	cat spec/results/results.json    

%.zip: spec/cases.% spec/nand2tetris/projects/% $(PACKAGE_FILES)
	echo $* > spec/project
	cd spec; zip -r ../$@ * --exclude results/\* submission/\*

clean:
	rm -f spec/project
	rm -rf spec/results/*
	
realclean: clean
	rm -f *.zip
	rm -rf spec/submission/*
