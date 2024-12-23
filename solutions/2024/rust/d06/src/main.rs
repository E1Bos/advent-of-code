use std::{collections::HashSet, env, fs};

fn parse_input(input: String) -> Vec<Vec<char>> {
    input
        .lines()
        .map(|line| line.chars().collect())
        .collect()
}

fn get_guard_pos(input: &Vec<Vec<char>>, guard_char: &char) -> (i32, i32) {
    for row in 0..input.len() {
        for col in 0..input[row].len() {
            if input[row][col] == *guard_char {
                return (row as i32, col as i32);
            }
        }
    }
    panic!("Guard not found");
}

fn is_outside(pos: &(i32, i32), grid_size: &(i32, i32)) -> bool {
    pos.0 < 0 || pos.0 >= grid_size.0 || pos.1 < 0 || pos.1 >= grid_size.1
}

struct Part1Result {
    grid: Vec<Vec<char>>,
    visited: HashSet<(i32, i32)>,
    is_loop: bool,
}

fn part1(input: &Vec<Vec<char>>, stop_if_same_direction: bool) -> Part1Result {
    let mut seen_positions = HashSet::new();
    let grid_size = (input.len() as i32, input.first().map_or(0, |row| row.len()) as i32);

    let mut guard_char: char = '^';
    let mut guard_pos = get_guard_pos(input, &guard_char);

    let mut grid = input.to_vec();
    grid[guard_pos.0 as usize][guard_pos.1 as usize] = 'X';

    let mut barrier_positions: HashSet<String> = HashSet::new();
    let mut is_loop = false;

    loop {
        seen_positions.insert(guard_pos);

        let delta_x = match guard_char {
            '<' => -1,
            '>' => 1,
            _ => 0,
        };
        
        let delta_y = match guard_char {
            '^' => -1,
            'v' => 1,
            _ => 0,
        };

        let new_pos = (guard_pos.0 + delta_x, guard_pos.1 + delta_y);

        if is_outside(&new_pos, &grid_size) {
            break;
        }

        if grid[new_pos.0 as usize][new_pos.1 as usize] == '#' {
            guard_char = match guard_char {
                '^' => '>',
                '>' => 'v',
                'v' => '<',
                '<' => '^',
                _ => panic!("Unknown direction"),
            };
            let dict_key = format!("{},{},{}", guard_pos.0, guard_pos.1, guard_char);

            if stop_if_same_direction && barrier_positions.contains(&dict_key) {
                is_loop = true;
                break;
            } else {
                barrier_positions.insert(dict_key);
            }
        } else {
            guard_pos = new_pos;
        }
    }

    Part1Result {
        grid,
        visited: seen_positions,
        is_loop,
    }
}

// fn part2(input: &Vec<String>) {
//     println!("Part 2");
// }

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = args.get(1).map_or("testinput.txt", String::as_str);

    let input = fs::read_to_string(file_name).expect("Unable to read file.");

    let parsed_input = parse_input(input);

    let result = part1(&parsed_input, false);
    println!("Part 1: {}", result.visited.len());
    // part2(&parsed_input);
}
