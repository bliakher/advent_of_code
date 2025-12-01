use std::{
    collections::{HashSet, VecDeque},
    fs::File,
    io::{BufRead, BufReader},
};

use delay::Delay;
use glam::IVec2;

const WIDTH: i64 = 101;
const HEIGHT: i64 = 103;
const CENTER_FRAME: i64 = 10;

struct Robot {
    pos: IVec2,
    vel: IVec2,
}
impl Robot {
    fn is_in_middle(&self, t: i64) -> bool {
        let x = ((self.pos.x as i64 + self.vel.x as i64 * t) % WIDTH + WIDTH) % WIDTH;
        let y = ((self.pos.y as i64 + self.vel.y as i64 * t) % HEIGHT + HEIGHT) % HEIGHT;

        let dx = (x - WIDTH / 2).abs();
        let dy = (y - HEIGHT / 2).abs();

        return dx < CENTER_FRAME && dy < CENTER_FRAME;
    }
}

fn read_input(filename: &str) -> Vec<Robot> {
    // I removed all non numeric elements from the input
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);
    let mut list: Vec<Robot> = Vec::new();
    for line_result in reader.lines() {
        let line = line_result.unwrap();
        let parts: Vec<i32> = line
            .split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
        let robot = Robot {
            pos: (parts[0], parts[1]).into(),
            vel: (parts[2], parts[3]).into(),
        };
        list.push(robot);
    }
    return list;
}

fn simulate_robots(robots: &mut Vec<Robot>, area: &mut Vec<Vec<i32>>, seconds: i32) {
    let width = area[0].len() as i32;
    let height = area.len() as i32;
    for robot in robots {
        let x = ((robot.pos.x + robot.vel.x * seconds) % width + width) % width;
        let y = ((robot.pos.y + robot.vel.y * seconds) % height + height) % height;
        area[y as usize][x as usize] += 1;
        robot.pos.x = x;
        robot.pos.y = y;
    }
}

fn simulate_robots2(robots: &mut [Robot], seconds: i32, width: i32, height: i32) {
    for robot in robots {
        let x = ((robot.pos.x + robot.vel.x * seconds) % width + width) % width;
        let y = ((robot.pos.y + robot.vel.y * seconds) % height + height) % height;
        robot.pos.x = x;
        robot.pos.y = y;
    }
}

fn part1(filename: &str) {
    let width = 101;
    let height = 103;
    let mut area = Vec::new();
    for _ in 0..height {
        let mut row = Vec::new();
        for _ in 0..width {
            row.push(0);
        }
        area.push(row);
    }
    let seconds = 1713;
    let mut robots = read_input(filename);
    let half_x = (width / 2) + 1;
    let half_y = (height / 2) + 1;
    let mut quadrants = vec![0, 0, 0, 0];
    simulate_robots(&mut robots, &mut area, seconds);
    for robot in robots {
        // skip robots in the middle
        let x = robot.pos.x;
        let y = robot.pos.y;
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
    print_area(&area);
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
    println!();
}

// stopped at: 97500000
fn search_for_tree1(robots: &mut [Robot]) {
    let mut area = vec![0; (WIDTH * HEIGHT) as usize];
    let mut elapsed = 0;
    loop {
        for r in robots.iter() {
            area[(r.pos.y * WIDTH as i32 + r.pos.x) as usize] -= 1;
        }
        simulate_robots2(robots, 1, WIDTH as _, HEIGHT as _);

        for r in robots.iter() {
            area[(r.pos.y * WIDTH as i32 + r.pos.x) as usize] += 1;
        }

        let center_size = search_for_tree_in_middle(&area, WIDTH as i32, HEIGHT as i32);
        if center_size > 15 {
            println!("Second: {elapsed}, size: {center_size}");
        }
        if elapsed % 100_000 == 0 {
            println!("Elapsed: {elapsed}");
        }
        elapsed += 1;
    }
}

fn search_for_tree_in_middle(area: &Vec<i32>, width: i32, height: i32) -> i32 {
    let mut queue = VecDeque::from([IVec2::new(width / 2, height / 2)]);
    let mut visited: HashSet<IVec2> = HashSet::new();
    let mut size = 0;
    while let Some(next) = queue.pop_front() {
        if visited.contains(&next) {
            continue;
        }
        visited.insert(next);
        let robot_count = area[(next.y * width + next.x) as usize];
        if robot_count == 0 {
            continue;
        }
        size += 1;
        let dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]];
        for dir in dirs {
            let new_x = next.x as i32 + dir[0];
            let new_y = next.y as i32 + dir[1];
            if new_x >= 0 && new_x < width && new_y >= 0 && new_y < height {
                queue.push_back(IVec2::new(new_x, new_y));
            }
        }
    }
    size
}

fn search_for_tree2(robots: &[Robot]) {
    let mut time: i64 = 0;
    loop {
        let middle = robots_in_middle(time, robots);
        time += 1;

        if middle > 95 {
            println!("Found {middle} robots in middle, t={time}");
        }
        if time % 100_000 == 0 {
            println!("Elapsed: {time}");
        }
    }
}

fn robots_in_middle(time: i64, robots: &[Robot]) -> i64 {
    robots.iter().filter(|r| r.is_in_middle(time)).count() as i64
}

fn part2(filename: &str) {
    let width: i32 = 101;
    let height: i32 = 103;

    let mut robots: Vec<Robot> = read_input(filename);
    search_for_tree2(&robots);
}

fn part2old(filename: &str) {
    let width = 101;
    let height = 103;
    let delay = Delay::builder();

    let mut robots: Vec<Robot> = read_input(filename);
    for i in 1..100 {
        let mut area = Vec::new();
        for _ in 0..height {
            let mut row = Vec::new();
            for _ in 0..width {
                row.push(0);
            }
            area.push(row);
        }
        simulate_robots(&mut robots, &mut area, 1);
        print!("\x1b[H\x1b[0J");
        println!("seconds: {i}");
        print_area(&area);
    }
}

fn main() {
    // part1("day14/input.txt");
    part2("day14/input.txt");
}
