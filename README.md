<div align="center">
  <h1>Advent of Code</h1> 
</div>

## File Structure

This repo contains all my advent of code solutions.

- Solutions are stored as `./solutions/YYYY/DD.py`.
- Puzzle input, test inputs and test answers are stored in `./data/YYYY/DD/`.

The `./utils` folder contains my python template, and the classes used to create new folders and files, read the puzzle inputs, and the base class solution implementation. It also contains `helper_functions.py`, which (as the name suggests), contains helper functions.

Solutions in other languages may be found in `./solutions/YYYY/language/`.

## Solution Class

Each solution implementation has 4 main components:

- The field `raw_input` determines whether the input is read as a raw string or is split into a list by line.
- The method `parse()` determines how the input is parsed. By default, it will return the input as is, but can be modified to fit your use case.
- The method `part1()` is your solution to part 1, which returns the solution.
- The method `part2()` is your solution to part 2, which returns the solution.

## Usage

```
pip install -r requirements.txt
```

```
usage: run.py [-h] [-y year_num] [-d day_num] [-p part_num] [-c] [-a] [-t]
              [--skip] [--create] [-ti] [-pr]

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

```
