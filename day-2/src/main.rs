use std::{env, fs};

fn parse_input(input: String) -> Vec<Vec<i32>> {
    input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|x| x.parse().unwrap())
                .collect()
        })
        .collect()
}

fn is_safe(input: &Vec<i32>) -> bool {
    let mut sorted_input = input.clone();
    sorted_input.sort_unstable();
    let is_sorted = *input == sorted_input || *input == sorted_input.iter().rev().cloned().collect::<Vec<_>>();

    let mut is_good = true;
    let mut prev = input[0];
    
    for &num in input.iter().skip(1) {
        let difference = (prev - num).abs();
        if !(1 <= difference && difference <= 3) {
            is_good = false;
            break;
        }
        prev = num;
    }

    is_good && is_sorted
}

fn solve(input: Vec<Vec<i32>>) {
    let mut part1 = 0;
    let mut part2 = 0;

    for line in input {
        // Part 1
        if is_safe(&line) {
            part1 += 1;
        }

        // Part 2
        let mut is_new_safe = false;
        for i in 0..line.len() {
            let new_line = {
                let mut v = line.clone();
                v.remove(i);
                v
            };
            if is_safe(&new_line) {
                is_new_safe = true;
                break;
            }
        }

        if is_new_safe {
            part2 += 1;
        }
    }

    println!("Part 1: {}", part1);
    println!("Part 2: {}", part2);

}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = args.get(1).map_or("input.txt", String::as_str);

    let input = fs::read_to_string(file_name).expect("Unable to read file.");

    let parsed_input = parse_input(input);

    solve(parsed_input);
}
