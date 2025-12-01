use std::{
    fs::File,
    io::{BufRead, BufReader},
};

fn read_input(filename: &str) -> Vec<Vec<char>> {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);
    let mut table = Vec::new();
    for line_result in reader.lines() {
        let line = line_result.unwrap();
        let row: Vec<char> = line.chars().collect();
        table.push(row);
    }
    return table;
}

fn part1(filename: &str) {
    let word_search = read_input(filename);
    let mut counts = 0;
    let rows: i32 = word_search.len().try_into().unwrap();
    let cols: i32 = word_search[0].len().try_into().unwrap();
    for i in 0..word_search.len() {
        for j in 0..word_search[0].len() {
            counts += count_xmas(i, j, &word_search, rows, cols);
        }
    }
    println!("{counts}");
}

fn part2(filename: &str) {
    let word_search = read_input(filename);
    let mut counts = 0;
    let rows: i32 = word_search.len().try_into().unwrap();
    let cols: i32 = word_search[0].len().try_into().unwrap();
    for i in 0..word_search.len() {
        for j in 0..word_search[0].len() {
            counts += count_xmas_cross(i, j, &word_search, rows, cols);
        }
    }
    println!("{counts}");
}

fn solve(filename: &str) {
    let word_search = read_input(filename);
    let mut counts = 0;
    let rows: i32 = word_search.len().try_into().unwrap();
    let cols: i32 = word_search[0].len().try_into().unwrap();
    for i in 0..word_search.len() {
        for j in 0..word_search[0].len() {
            counts += count_xmas_cross(i, j, &word_search, rows, cols);
        }
    }
    println!("{counts}");
}

fn get_symbol(
    i: &mut usize,
    j: &mut usize,
    direction: [i32; 2],
    word_search: &Vec<Vec<char>>,
    rows: i32,
    cols: i32,
    update: bool,
) -> Option<char> {
    let new_i_d = TryInto::<i32>::try_into(*i).unwrap() + direction[0];
    let new_j_d = TryInto::<i32>::try_into(*j).unwrap() + direction[1];
    if new_i_d >= 0 && new_i_d < rows && new_j_d >= 0 && new_j_d < cols {
        let i_d: usize = new_i_d.try_into().unwrap();
        let j_d: usize = new_j_d.try_into().unwrap();
        if update {
            *i = i_d;
            *j = j_d;
        }
        return Some(word_search[i_d][j_d]);
    }
    return None;
}

fn count_xmas_cross(i: usize, j: usize, word_search: &Vec<Vec<char>>, rows: i32, cols: i32) -> i32 {
    if word_search[i][j] != 'A' {
        return 0;
    }
    let mut i_d = i;
    let mut j_d = j;
    let left_diag = [[-1, -1], [1, 1]];
    let right_diag = [[-1, 1], [1, -1]];
    let mut left_symbols: [char; 2] = left_diag
        .map(|dir| get_symbol(&mut i_d, &mut j_d, dir, word_search, rows, cols, false))
        .map(|op_s| match op_s {
            Some(s) => s,
            None => '.',
        });
    left_symbols.sort();
    let mut right_symbols = right_diag
        .map(|dir| get_symbol(&mut i_d, &mut j_d, dir, word_search, rows, cols, false))
        .map(|op_s| match op_s {
            Some(s) => s,
            None => '.',
        });
    right_symbols.sort();
    match left_symbols {
        ['M', 'S'] => match right_symbols {
            ['M', 'S'] => 1,
            _ => 0,
        },
        _ => 0,
    }
}

fn count_xmas(i: usize, j: usize, word_search: &Vec<Vec<char>>, rows: i32, cols: i32) -> i32 {
    if word_search[i][j] != 'X' {
        return 0;
    }
    let directions: [[i32; 2]; 8] = [
        [-1, -1],
        [-1, 0],
        [-1, 1],
        [0, -1],
        [0, 1],
        [1, -1],
        [1, 0],
        [1, 1],
    ];
    let mut counts = 0;
    let x_mas = ['M', 'A', 'S'];
    for direction in directions {
        let mut i_d = i;
        let mut j_d = j;
        let mut found = true;
        for letter in x_mas {
            if let Some(symbol) =
                get_symbol(&mut i_d, &mut j_d, direction, word_search, rows, cols, true)
            {
                if symbol != letter {
                    found = false;
                    break;
                }
            }
        }
        if found {
            counts += 1;
        }
    }
    return counts;
}

fn main() {
    part1("day04/input.txt");
    part2("day04/input.txt");
}
