use std::{
    fs::File,
    io::{BufRead, BufReader},
};

struct Equation {
    test_value: i64,
    equation: Vec<i64>,
}

#[derive(Clone, Copy)]
enum Operator {
    Add,
    Multiply,
    Concat,
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

fn test_equation(eq: &Equation, allowed_ops: &Vec<Operator>) -> bool {
    for next_op in allowed_ops {
        if try_operator(
            *next_op,
            allowed_ops,
            &eq.equation,
            1,
            eq.test_value,
            eq.equation[0],
        ) {
            return true;
        }
    }
    return false;
}

fn concat(n1: i64, n2: i64) -> i64 {
    let mut res = String::new();
    res.push_str(&n1.to_string());
    res.push_str(&n2.to_string());
    return res.parse().unwrap();
}

fn try_operator(
    op: Operator,
    allowed_ops: &Vec<Operator>,
    values: &Vec<i64>,
    from_idx: usize,
    target: i64,
    cur_value: i64,
) -> bool {
    if from_idx >= values.len() {
        return cur_value == target;
    }
    if cur_value > target {
        return false;
    }
    let mut new_result = cur_value;
    match op {
        Operator::Add => new_result += values[from_idx],
        Operator::Multiply => new_result *= values[from_idx],
        Operator::Concat => new_result = concat(cur_value, values[from_idx]),
    }
    for next_op in allowed_ops {
        if try_operator(
            *next_op,
            allowed_ops,
            values,
            from_idx + 1,
            target,
            new_result,
        ) {
            return true;
        }
    }
    return false;
}

fn solve(equations: &Vec<Equation>, allowed_ops: &Vec<Operator>) -> i64 {
    let res: i64 = equations
        .iter()
        .map(|eq| match test_equation(&eq, allowed_ops) {
            true => eq.test_value,
            false => 0,
        })
        .sum();
    return res;
}

fn part1(filename: &str) {
    let equations = parse_input(filename);
    let res: i64 = solve(&equations, &vec![Operator::Add, Operator::Multiply]);
    println!("{res}")
}

fn part2(filename: &str) {
    let equations = parse_input(filename);
    let res: i64 = solve(
        &equations,
        &vec![Operator::Add, Operator::Multiply, Operator::Concat],
    );
    println!("{res}")
}

fn main() {
    part1("day07/input.txt");
    part2("day07/input.txt");
}
