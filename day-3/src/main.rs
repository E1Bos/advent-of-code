use regex::Regex;
use std::{env, fs};

fn solve(input: String) {
    let mut part_1 = 0;
    let mut part_2 = 0;
    let mut is_do = true;

    let nums = Regex::new(r"\(\d{1,3},\d{1,3}\)").unwrap();

    for index in 0..input.len() {
        
        if input[index..].starts_with("do()") {
            is_do = true;
        } else if input[index..].starts_with("don't()") {
            is_do = false;
        }

        if input[index..].starts_with("mul(") {
            // Max length `mul(XXX,YYY)` is 12 hence the magic number
            // not happy with this implementation
            if let Some(nums) = nums.find(&input[index..index + 12]) {
                // Remove the parenthesis
                let nums_str = &nums.as_str()[1..nums.as_str().len() - 1];
                
                // Split the numbers and parse
                let nums_str_split = nums_str.split_once(',');
                let (x, y) = match nums_str_split {
                    Some((a, b)) => (
                        a.parse::<i32>().expect("Expected a number"),
                        b.parse::<i32>().expect("Expected a number"),
                    ),
                    None => {
                        eprintln!("Expected comma separated numbers in string '{}'", nums_str);
                        continue;
                    }
                };

                part_1 += x * y;

                if is_do {
                    part_2 += x * y;
                }
            }
        }
    }

    println!("Part 1: {}", part_1);
    println!("Part 2: {}", part_2);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = args.get(1).map_or("input.txt", String::as_str);

    let input = fs::read_to_string(file_name).expect("Unable to read file.");

    solve(input);
}
