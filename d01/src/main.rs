use std::{collections::HashMap, fs};

fn parse_input(input: &String) -> (Vec<i32>, Vec<i32>) {
    let mut left_side: Vec<i32> = Vec::new();
    let mut right_side: Vec<i32> = Vec::new();

    for line in input.lines() {
        let split: Vec<&str> = line.split(" ").filter(|x| x != &"".to_string()).collect();

        left_side.push(split[0].parse().unwrap());
        right_side.push(split[1].parse().unwrap());
    }

    return (left_side, right_side);
}

fn calc_value(left: i32, right: i32) -> i32 {
    return (left - right).abs();
}

fn part1(mut left_side: Vec<i32>, mut right_side: Vec<i32>) -> i32 {
    left_side.sort();
    right_side.sort();

    let mut result = 0;
    for i in 0..left_side.len() {
        result += calc_value(left_side[i], right_side[i]);
    }

    result
}

fn part2(left_side: Vec<i32>, right_side: Vec<i32>) -> i32 {
    let mut score_map: HashMap<i32, i32> = HashMap::new();
    for num in right_side.iter() {
        *score_map.entry(*num).or_insert(0) += 1;
    }

    let mut result = 0;
    for number in left_side.iter() {
        if score_map.contains_key(number) {
            result += number * score_map[number];
        }
    }

    result
}

fn main() {
    let input = fs::read_to_string("input.txt").expect("Unable to read file.");

    let (left_side, right_side) = parse_input(&input);

    let part1_output = part1(left_side.clone(), right_side.clone());
    println!("Part 1: {}", part1_output);

    let part2_output = part2(left_side, right_side);
    println!("Part 2: {}", part2_output);
}
