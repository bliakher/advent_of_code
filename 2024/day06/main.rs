use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
};

enum Direction {
    Up,
    Right,
    Down,
    Left,
}

impl Direction {
    fn get_right_rotation(&self) -> Direction {
        match self {
            Direction::Up => Direction::Right,
            Direction::Right => Direction::Down,
            Direction::Down => Direction::Left,
            Direction::Left => Direction::Up,
        }
    }
    fn get_vector(&self) -> [i32; 2] {
        match self {
            Direction::Up => [-1, 0],
            Direction::Right => [0, 1],
            Direction::Down => [1, 0],
            Direction::Left => [0, -1],
        }
    }
    fn from_char(c: char) -> Direction {
        match c {
            '^' => Direction::Up,
            '>' => Direction::Right,
            'v' => Direction::Down,
            '<' => Direction::Left,
            _ => unreachable!(),
        }
    }
}

struct Guard {
    pos: [i32; 2],
    direction: Direction,
}

struct Lab {
    floor_plan: Vec<Vec<char>>,
    guard: Guard,
    visited_pos: HashSet<String>,
}

impl Guard {
    fn rotate_right(&mut self) {
        self.direction = self.direction.get_right_rotation();
    }
    fn set_pos(&mut self, new_pos: [i32; 2]) {
        self.pos = new_pos
    }
    fn get_pos_in_dir(&self) -> [i32; 2] {
        let dir = self.direction.get_vector();
        [self.pos[0] + dir[0], self.pos[1] + dir[1]]
    }
}

impl Lab {
    fn patrol(&mut self) {
        loop {
            let guard_exited = self.move_guard();
            if guard_exited {
                break;
            }
        }
    }
    // return true if guard exits the lab
    fn move_guard(&mut self) -> bool {
        let [i, j] = self.guard.get_pos_in_dir();
        let height = self.floor_plan.len() as i32;
        let width = self.floor_plan[0].len() as i32;
        if i < 0 || i >= height || j < 0 || j >= width {
            return true;
        }
        if self.has_obstacle(i as usize, j as usize) {
            self.guard.rotate_right();
        } else {
            self.guard.set_pos([i, j]);
            self.mark_visited(i, j);
        }
        return false;
    }
    fn mark_visited(&mut self, i: i32, j: i32) {
        let pos_marker = format!("{i}-{j}");
        self.visited_pos.insert(pos_marker);
        self.floor_plan[i as usize][j as usize] = 'X';
    }
    fn has_obstacle(&self, i: usize, j: usize) -> bool {
        return self.floor_plan[i][j] == '#';
    }
    fn count_visited(&self) -> usize {
        return self.visited_pos.len();
    }
    fn print(&self) {
        for row in self.floor_plan.iter() {
            let mut row_str = String::new();
            for c in row.iter() {
                row_str.push(*c);
            }
            println!("{}", row_str);
        }
    }
}

fn read_input(filename: &str) -> Lab {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);
    let mut table = Vec::new();
    let mut i = 0;
    let mut pos = [0, 0];
    let mut dir = Direction::Up;
    for line_result in reader.lines() {
        let line = line_result.unwrap();
        let mut row = Vec::new();
        let mut j = 0;
        for c in line.chars() {
            if c == '^' || c == '>' || c == 'v' || c == '<' {
                row.push('.');
                pos = [i, j];
                dir = Direction::from_char(c);
            } else {
                row.push(c);
            }
            j += 1;
        }
        table.push(row);
        i += 1;
    }
    let guard = Guard {
        pos,
        direction: dir,
    };
    let lab = Lab {
        floor_plan: table,
        guard,
        visited_pos: HashSet::new(),
    };
    return lab;
}

fn part1(filename: &str) {
    let mut lab = read_input(filename);
    lab.patrol();
    let count = lab.count_visited();
    println!("{count}");
    // println!("{:?}", lab.visited_pos);
    // lab.print();
}

fn part2(filename: &str) {}

fn main() {
    part1("day06/input.txt");
    part2("day06/small_input.txt");
}
