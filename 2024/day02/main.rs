use std::{
    fs::File,
    io::{BufRead, BufReader},
};

fn read_input(filename: &str) -> Vec<Vec<i32>> {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);
    let mut list = Vec::new();
    for line_result in reader.lines() {
        let line = line_result.unwrap();
        let parts: Vec<i32> = line
            .split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
        list.push(parts);
    }
    return list;
}

fn check_report(report: &Vec<i32>) -> bool {
    let mut prev = report[0];
    let mut prev_diff = report[1] - report[0];
    for i in 1..report.len() {
        let level = report[i];
        let diff = level - prev;
        if diff.abs() >= 1 && diff.abs() <= 3 && diff * prev_diff > 0 {
            prev = level;
            prev_diff = diff;
            continue;
        }
        return false;
    }
    return true;
}

fn part1(filename: &str) {
    let reports = read_input(filename);
    let mut sum = 0;
    for report in reports {
        if check_report(&report) {
            sum += 1;
        }
    }

    println!("{:?}", sum);
}

fn part2(filename: &str) {
    let reports = read_input(filename);
    let mut sum = 0;
    for report in reports {
        if check_report(&report) {
            sum += 1;
            continue;
        }
        for i in 0..report.len() {
            let fixed_report: Vec<i32> = report
                .iter()
                .enumerate()
                .filter(|&(j, _)| i != j)
                .map(|(_, val)| *val)
                .collect();
            if check_report(&fixed_report) {
                sum += 1;
                break;
            }
        }
    }

    println!("{:?}", sum);
}

fn main() {
    part1("day02/input.txt");
    part2("day02/input.txt");
}
