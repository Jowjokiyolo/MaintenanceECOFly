# **EcoFly Maintenance Planning**
In this repository, the source code for EcoFly's five-year Maintenance plan is available.

## Python Dependencies:
The following Python packages are required for the main file to run:
- Numpy
- Pandas
- Openpyxl
- RE (Regex)

## How to Create a Five-Year Maintenance Plan:
Before you can run this program, you require the Fokker 70/100 MPD (.xlsx). It is recommended to place this somewhere within this codebase. The raw MPD can already be found in `.Files/MPD.xlsx`.

Run main.py in your Python environment, with an argument to the (relative) directory of your MPD file. This generates a .csv file with a five-year maintenance plan.

**main.py Syntax:**
```bash 
<python> <path_to_main.py> <path_to_MPD.xlsx>
```

## WIP:
- Maintenance Planning Chart
