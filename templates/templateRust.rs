use std::{env, fs};

fn parse_input(input: String) -> X {}

fn part1(input) -> X {}

fn part2(input) -> X {}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = args.get(1).map_or("input.txt", String::as_str);

    let input = fs::read_to_string(file_name).expect("Unable to read file.");

    let parsed_input = parse_input(input);

    part1(parsed_input);
    part2(parsed_input);
}
