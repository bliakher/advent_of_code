use std::{
    fs::File,
    io::{BufRead, BufReader},
};

fn read_input(filename: &str) -> Vec<Vec<i32>> {
    // I removed all non numeric elements from the input
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

fn part1(filename: &str) {
    let width = 101;
    let height = 103;
    // let mut area = Vec::new();
    // for _ in 0..height {
    //     let mut row = Vec::new();
    //     for _ in 0..width {
    //         row.push(0);
    //     }
    //     area.push(row);
    // }
    let seconds = 100;
    let robots = read_input(filename);
    let half_x = (width / 2) + 1;
    let half_y = (height / 2) + 1;
    let mut quadrants = vec![0, 0, 0, 0];
    for robot in robots {
        assert!(robot.len() == 4);
        let x = ((robot[0] + robot[2] * seconds) % width + width) % width;
        let y = ((robot[1] + robot[3] * seconds) % height + height) % height;
        // area[y as usize][x as usize] += 1;
        // skip robots in the middle
        if x + 1 == half_x || y + 1 == half_y {
            continue;
        }
        let quad_x = (x + 1) / half_x;
        let quad_y = (y + 1) / half_y;
        // println!("{} {} {} {}", x, y, quad_x, quad_y);
        let quad = (quad_x + 2 * quad_y) as usize;
        quadrants[quad] += 1;
    }
    println!("{:?}", quadrants);
    // print_area(&area);
    let res = quadrants.iter().fold(1, |acc, x| acc * x);
    println!("{res}");
}

fn print_area(area: &Vec<Vec<i32>>) {
    for i in 0..area.len() {
        for j in 0..area[0].len() {
            let s = match area[i][j] {
                0 => ".".to_string(),
                i => i.to_string(),
            };
            print!("{}", s)
        }
        println!();
    }
}

fn part2(filename: &str) {}

fn main() {
    part1("day14/input.txt");
    part2("day14/small_input.txt");
}
