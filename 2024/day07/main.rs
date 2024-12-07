use std::{
    fs::File,
    io::{BufRead, BufReader},
};

struct Equation {
    test_value: i64,
    equation: Vec<i64>,
}

enum Operator {
    Add,
    Multiply,
}

fn parse_input(filename: &str) -> Vec<Equation> {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);
    let mut list = Vec::new();
    for line_result in reader.lines() {
        let line = line_result.unwrap();
        let parts: Vec<&str> = line.split(":").collect();
        let test_value: i64 = parts[0].parse().unwrap();
        let equation: Vec<i64> = parts[1]
            .split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
        list.push(Equation {
            test_value,
            equation,
        });
    }
    return list;
}

fn test_equation(eq: &Equation) -> bool {
    let first_add = try_operator(
        Operator::Add,
        &eq.equation,
        1,
        eq.test_value,
        eq.equation[0],
    );
    if first_add == eq.test_value {
        return true;
    }
    let first_mul = try_operator(
        Operator::Multiply,
        &eq.equation,
        1,
        eq.test_value,
        eq.equation[0],
    );
    return first_mul == eq.test_value;
}

fn try_operator(
    op: Operator,
    values: &Vec<i64>,
    from_idx: usize,
    target: i64,
    cur_value: i64,
) -> i64 {
    if from_idx >= values.len() {
        return cur_value;
    }
    if cur_value > target {
        return cur_value;
    }
    let mut new_result = cur_value;
    match op {
        Operator::Add => new_result += values[from_idx],
        Operator::Multiply => new_result *= values[from_idx],
    }
    let try_add = try_operator(Operator::Add, values, from_idx + 1, target, new_result);
    if try_add == target {
        return try_add;
    }
    let try_mul = try_operator(Operator::Multiply, values, from_idx + 1, target, new_result);
    return try_mul;
}

fn part1(filename: &str) {
    // let res = try_operator(Operator::Add, &vec![81, 40, 27], 1, 3267, 81);
    let equations = parse_input(filename);
    let res: i64 = equations
        .iter()
        .map(|eq| match test_equation(&eq) {
            true => eq.test_value,
            false => 0,
        })
        .sum();

    // let mut res = 0;
    println!("{res}")
}

fn part2(filename: &str) {}

fn main() {
    part1("day07/input.txt");
    part2("day07/small_input.txt");
}
