# **EcoFly Maintenance Planning**
In this repository, the source code for EcoFly's five-year Maintenacnce plan is visible.

## Python Dependancies:
The following Python packages are required for the main file to run:
- Numpy
- Pandas
- Openpyxl
- RE (Regex)

## How to Create a five-year Maintenance Plan:
Before you can run this program, you requre the Fokker 70/100 MPD (.xlsx). It is recommended to place this somewhere within this codebase. The raw MPD can already be found in `.Files/MPD.xlsx`

Run main.py in your python enviroment, with an argument to the (relative) directory of your MPD file. This generates a .csv file with a five-year maintenance plan.

**Main.py Syntax:**
> $`<your_python_enviroment> <path_to_main.py> <path_to_MPD.csv>`

## WIP:
- Smarter Maintenance Plan
- Maintenance Planning Chart