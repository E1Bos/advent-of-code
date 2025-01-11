<div align="center">
  <h1>Advent of Code</h1> 
</div>

## 📁 File Structure

This repo contains all my advent of code solutions.

- Solutions are stored as `./solutions/YYYY/DD.py`.
- Puzzle input, test inputs and test answers are stored in `./data/YYYY/DD/`.

The `./utils` folder contains multiple helper classes.
  - `files.py` creates and manages the solution files and data
  - `puzzle_reader.py` reads the puzzle input
  - `output_handler.py` manages the output to stdout and to log file
  - `cli_args.py` is a data structure for the parsed args (so that the variables can have type definitions)
  - `solution_base.py` is the base class for all solutions
  - `helper_functions.py` is a list of helper functions that may be helpful in solving problems
  - `./templates/python_template.py` is the base python template copied when a new day is created

Solutions in other languages may be found in `./solutions/YYYY/language/`.

## 🏠 Solution Class

Each solution implementation has 5 main components:

- The field `raw_input` determines whether the input is read as a raw string or is split into a list by line.
- The field `skip_empty_tests`, which needs to be added manually, will skip empty tests instead of exiting.
- The method `parse()` determines how the input is parsed. By default, it will return the input as is, but can be modified to fit your use case.
- The method `part1()` is your solution to part 1, and returns the solution.
- The method `part2()` is your solution to part 2, and returns the solution.


The solution class also exposes several useful helper methods.
- `print()` prints to stdout and logs to the log file
- `debug()` prints to stdout and logs to the log file if the arg `--debug` is used

Additionally, the field `override_print` can be set to `True`, which will override the default `print()` (`builtins.print`) with the solution implementation of print, so that you don't need to call `self.print()`.  

During the execution of each part, the variables `is_test` and `is_part_1` are available so that the execution can change based on those parameters (e.g. grid size being different in the test case)


## 🚀 Usage

``` bash
pip install -r requirements.txt
```

``` console
usage: run.py [-h] [-y year_num] [-d day_num] [-p part_num] [-c] [-a] [-t]
              [--skip] [--create] [-ti] [-pr] [--debug]

Advent of Code CLI

options:
  -h, --help            show this help message and exit
  -y year_num, --year year_num
                        Optional, year of the AoC problem, defaults to the
                        current year
  -d day_num, --day day_num
                        Optional, day of the AoC problem, defaults to the
                        current day
  -p part_num, --part part_num
                        Optional, part number of the solution, defaults to
                        part 1
  -c, --copy            Optional, copy the results to the clipboard
  -a, --all             Optional, run all parts
  -t, --test            Optional, only run tests
  --skip, --skip-tests  Optional, skip running tests
  --create              Optional, create necessary files for specified year
                        and day
  -ti, --timeit         Optional, time the solution
  -pr, --profile        Optional, profile the solution and open the results in
                        a browser
  --debug               Optional, allow logging debug messages to stdout from
                        the solution
```

## 🐧 Linux

Change permissions so the scripts can be executed:
```bash
chmod +x run.py aoc
```

On Ubuntu, install xclip for clipboard support:
```bash
sudo apt-get install xclip
```
> I am running Linux Mint (Ubuntu). This is what I had to do, your mileage may vary.


You can then run the script with:
```bash
./run.py [args]
# or
./aoc [args] 
```