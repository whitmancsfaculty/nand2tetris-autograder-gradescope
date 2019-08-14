# Nand2Tetris Gradescope Autograder

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
1. Complete configuration of the assignment by visiting the assignment settings page. Under `Ignored Files`, copy and paste the contents of `spec/ignore.00`.  

See the [Gradescope autograder documentation](https://gradescope-autograders.readthedocs.io/en/latest/) for more information.

## Architecture
* A Makefile is provided. All source code is in the `spec` directory. 
* Tools and test cases are provided in the `spec\nand2tetris` directory.
  * The Nand2Tetris tools are treated as a black box. They are exactly the same tools used by students for their own testing.
  * Project 4 includes an additional program, `fillStatic`. This program can be tested automatically, unlike the `fill` program provided with Nand2Tetris which must be tested interactively.
  * There are additional test cases for projects 6-8 and 11.
  * Project 11 is divided in two parts, 11a and 11b.
  * Otherwise, assignments and test cases are as in the textbook Nand2Tetris distribution.
  * If using [Python starter code](https://github.com/whitmancsfaculty/nand2tetris-startercode), the instructor may want to add Python files that students do not modify before building zip files, so that students do not have to include unmodified files in their Gradescope submissions. Those files are not provided in this public repository.
* The files `cases.<project>` specify test cases and point values for each project.
* The files `ignore.<project>` specify files that Gradescope should not upload from student submissions.
* `spec/run_autograder` runs all test cases for a project, as required by Gradescope. It obtains the project name from a command-line parameter or from the `spec/project` file, which is created automatically when building a zipfile to upload to Gradescope.
* Projects using different tools require different scripts to evaluate test cases. These scripts are named `test_*`.

## Scoring
Project test cases and point values are specified in a file named `spec/cases.<project>`, one test case per line.
Note that the number of columns varies from project to project due to the differing nature of the tools and test cases.

Project tests add up to a variable number of points. 
With the exception of Project 0, which is a practice project, each project is intended to be worth a total of 75 points. 
The difference is made up through style or interactive tests.
In making adjustments, I would lean towards increasing points from the autograder and reducing points from style.

Unless otherwise specified, automated scoring is binary with respect to each test case: full credit is awarded if the canonical output is produced, otherwise 0.

The autograder provides feedback on errors and test failures to the extent feasible. 
The autograder does not replace interactive testing in the development environment.
  
| Project | Type | Points | Notes |
| ------: | :----------- | -----: | :-----|
|      00 | HDL          |      4 | Practice assignment - do not transfer to gradebook.
|      01 | HDL          |     60 |
|      02 | HDL          |     50 | 
|      03 | HDL          |     60 | Memory intensive - configure Gradescope to use a full CPU.
|      04 | ASM          |     50 | Scoring is the fraction of tests passed times points possible. `Fill.asm` must be tested interactively. Export all submissions from "Review Grades."  
|      05 | HDL          |     56 | Detailed scoring of the CPU is performed by the `score_cpu` script.
|      06 | Assembler    |     66 | Additional unit tests in `symbols` and `instructions`. 
|      07 | VM translator|     63 |
|      08 | VM translator|     75 | Additional tests in `FunctionCalls/LocalsTest`, `FunctionCalls/MinMax`, and `ProgramFlow/BasicGoto`. 
|      09 | Jack         |      - | Student-designed program. Automated testing not possible. Gradescope submission not recommended.
|      10 | Syntax analyzer |  75 |
|     11a | Compiler     |     75 | Consists of the `seven` and `convertToBin` test cases. Automated scoring is the higher of two times the number of keywords found or the percent of the output identical to expected output times the point value.
|     11b | Compiler     |     75 | Consists of the remaining Project 11 test cases. Automated scoring is as for 11a.
|      12 | Jack OS      |      - | Not yet assigned.
