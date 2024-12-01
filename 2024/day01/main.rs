use std::{
    fs::File,
    io::{BufRead, BufReader},
};

fn read_input(filename: &str) -> (Vec<i32>, Vec<i32>) {
    // let lines = fs::read_to_string(filename).unwrap().lines();
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);
    let mut list1 = Vec::new();
    let mut list2 = Vec::new();
    for line_result in reader.lines() {
        let line = line_result.unwrap();
        let parts: Vec<_> = line.split_whitespace().collect();
        let first: i32 = parts[0].parse().unwrap();
        let second: i32 = parts[1].parse().unwrap();
        list1.push(first);
        list2.push(second);
    }
    return (list1, list2);
}

fn part1() {
    println!("Hello AoC");
    let (mut list1, mut list2) = read_input("day01/input.txt");
    list1.sort_unstable();
    list2.sort_unstable();
    let mut sum = 0;
    for i in 0..list1.len() {
        let diff = (list1[i] - list2[i]).abs();
        sum += diff;
    }
    println!("{sum}");
}

fn part2() {
    let (mut list1, mut list2) = read_input("day01/input.txt");
    list1.sort_unstable();
    list2.sort_unstable();
    let mut sum = 0;
    let mut pointer = 0;
    let mut prev = 0;
    let mut prev_count = 0;
    for i in 0..list1.len() {
        let item = list1[i];
        if item == prev {
            sum += item * prev_count;
            continue;
        }
        while list2[pointer] < item {
            pointer += 1;
        }
        let mut count = 0;
        while list2[pointer] == item {
            count += 1;
            pointer += 1;
        }
        sum += item * count;
        prev = item;
        prev_count = count;
    }
    println!("{sum}");
}

fn main() {
    part2();
}
