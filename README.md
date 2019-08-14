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

## Scoring and Gradescope configuration
Project test cases and point values are specified in a file named `spec/cases.<project>`, one test case per line.
Note that the number of columns varies from project to project due to the differing nature of the tools and test cases.

Project tests add up to a variable number of points. 
With the exception of Project 0, which is a practice project, each project is intended to be worth a total of 75 points, with the difference being made up through style or interactive tests.
In making adjustments, I would lean towards increasing points from the autograder and reducing points from style.
  
| Project | Type | Points | Notes |
| ------: | :----------- | -----: | :-----|
|      00 | HDL          |      4 | Practice assignment - do not transfer to gradebook.
|      01 | HDL          |     60 |
|      02 | HDL          |     50 | 
|      03 | HDL          |     60 | Memory intensive - configure Gradescope to use a full CPU.
|      04 | ASM          |     50 | `Fill.asm` must be tested interactively. Export all submissions from "Review Grades."
|      05 | HDL          |     56 | Detailed scoring of the CPU is performed by the `score_cpu` script.
|      06 | Assembler    |     66 | 
|      07 | VM translator|     63 |
|      08 | VM translator|     75 | 
|      09 | Jack         |      - | Student-designed program. Automated testing not possible. Do not recommend Gradescope submission.
|      10 | Syntax analyzer |  75 |
|     11a | Compiler     |     75 |
|     11b | Compiler     |     75 |
|      12 | Jack OS      |      - | Not yet assigned.

Gradescope programming assignments should be configured to ignore certain files when uploaded by students.
The files named `spec/ignore.<project>` specify which files to ignore for teach project.
The contents can be copied and pasted to the corresponding Gradescope assignment settings page.

The autograder provides feedback on errors and test failures to the extent feasible. 
The autograder does not replace interactive testing in the development environment.

## Architecture
* A Makefile is provided. All source code is in the `spec` directory. 
* Tools and test cases are provided in the `spec\nand2tetris` directory.
  * The Nand2Tetris tools are treated as a black box. They are exactly the same tools used by students for their own testing.
  * Project 4 includes an additional program, `fillStatic`. This program can be tested automatically, unlike the `fill` program provided with Nand2Tetris which must be tested interactively.
  * There are additional test cases for projects 6-8 and 11.
  * Project 11 is divided in two parts, 11a and 11b.
  * Otherwise, assignments and test cases are as in the textbook Nand2Tetris distribution.   
* `spec/run_autograder` runs all test cases for a project, as required by Gradescope. It obtains the project name from a command-line parameter or from the `spec/project` file, which is created automatically when building a zipfile to upload to Gradescope.
* Projects using different tools require different scripts to evaluate test cases. These scripts are named `test_*`.
