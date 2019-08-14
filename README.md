# nand2tetris_gradescope_autograder
Gradescope autograder specification for Nand2Tetris projects.

Nand2Tetris materials are copyright the authors and may be found at https://www.nand2tetris.org/

Gradescope can be found at https://www.gradescope.com. 
The autograder specification is documented at http://gradescope-autograders.readthedocs.io/en/latest/specs/.

## Testing the sample assignment
The sample assignment (`00`) is intended to be completed in class as an introduction to HDL and to the 
Gradescope autograder. It also serves as an example for the instructor.

To test the sample assignment on your own computer:
1. Create the `spec/submission` directory, if it does not already exist. 
1. Place a sample solution (e.g., `Xor.hdl`) in the `spec/submission` directory.
1. Run the autograder by typing `make 00.test`.
1. Review the results printed from `spec/results/results.json`.

## Releasing the sample assignment on Gradescope
To build a zipfile and upload it to a corresponding assignment on Gradescope:
1. To build the zipfile, `make 00.zip clean`.
1. On Gradescope, upgrade the course to **Gradescope Complete**. Go to the **Assignments** tab and create a new programming assignment worth 4 points.
1. Upload `00.zip`.
1. Click **Update Autograder**.
1. When the update is complete, click **Test Autograder** and upload your sample solution (e.g., `Xor.hdl`).

See the [Gradescope autograder documentation](https://gradescope-autograders.readthedocs.io/en/latest/) for more information.

## Architecture
* A Makefile is provided. All source code is in the `spec` directory. 
* Tools and test cases are provided in the `spec\nand2tetris` directory.
  * The Nand2Tetris tools are treated as a black box. They are exactly the same tools used by students for their own testing.
  * Project 4 includes an additional program, `fillStatic`. This program can be tested automatically, unlike the `fill` program provided with Nand2Tetris which must be tested interactively.
  * There are additional test cases for projects 6-8 and 11.
  * Project 11 is divided in two parts, 11a and 11b.
  * Otherwise, assignments and test cases are as in the textbook Nand2Tetris distribution.   
* Each `spec/cases.<project>` file lists the test cases and point values for a project assignment, one test case per line.
  * There are no cases files for projects 9, 12, and 13 because they cannot be tested automatically.
  * Note that file format varies from project to project due to the different nature of the test cases.
  * Additional scoring breakdown for the CPU constructed in Project 5 can be found in `spec/score_cpu`.
* `spec/run_autograder` runs all test cases for a project, as required by Gradescope. It obtains the project name from a command-line parameter or from the `spec/project` file, which is created automatically when building a zipfile to upload to Gradescope.
* Projects using different tools require different scripts to evaluate test cases. These scripts are named `test_*`.
