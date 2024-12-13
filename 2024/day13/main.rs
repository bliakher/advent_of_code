use num;
use std::{
    fs::File,
    io::{BufRead, BufReader},
};

struct Equation {
    a: i64,
    b: i64,
    res: i64,
}

fn solve_eq_system(eq1: Equation, eq2: Equation) -> Option<[i64; 2]> {
    let lcm = num::integer::lcm(eq1.a, eq2.a);
    let lcm1 = lcm / eq1.a;
    let lcm2 = lcm / eq2.a;
    let y_coeff = eq1.b * lcm1 - eq2.b * lcm2;
    let res = eq1.res * lcm1 - eq2.res * lcm2;
    let y = res / y_coeff;
    if res % y_coeff != 0 || y < 0 {
        return None;
    }
    let x_res = eq1.res - eq1.b * y;
    let x = x_res / eq1.a;
    if x_res % eq1.a != 0 || x < 0 {
        return None;
    }
    return Some([x, y]);
}

fn solve(filename: &str, conversion_error: bool) {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);
    let mut vec = Vec::new();
    let mut sum = 0;
    for line_result in reader.lines() {
        let line = line_result.unwrap();
        if line.is_empty() {
            assert!(vec.len() == 6);
            // println!("{} {}", vec[0], vec[1]);
            let mut eq1 = Equation {
                a: vec[0],
                b: vec[2],
                res: vec[4],
            };
            let mut eq2 = Equation {
                a: vec[1],
                b: vec[3],
                res: vec[5],
            };
            if conversion_error {
                eq1.res += 10000000000000;
                eq2.res += 10000000000000;
            }
            let res = solve_eq_system(eq1, eq2);
            match res {
                Some([a, b]) => {
                    // assert!(a <= 100 && b <= 100);
                    sum += a * 3 + b;
                }
                None => {}
            }
            vec = Vec::new();
            continue;
        }
        let parts: Vec<i64> = line
            .split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
        vec.extend(parts);
    }
    println!("{sum}");
}

fn main() {
    // part 1
    solve("day13/input.txt", false);
    // part 2
    solve("day13/input.txt", true);
}
