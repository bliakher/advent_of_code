use std::{
    collections::{HashSet, VecDeque},
    fs::File,
    io::{BufRead, BufReader},
};

#[derive(Copy, Clone, Hash)]
struct Pos {
    i: usize,
    j: usize,
}

impl PartialEq for Pos {
    fn eq(&self, other: &Self) -> bool {
        self.i == other.i && self.j == other.j
    }
}
impl Eq for Pos {}

struct Map<T: Copy> {
    map: Vec<Vec<T>>,
}

impl<T: Copy> Map<T> {
    fn get(&self, pos: &Pos) -> T {
        self.map[pos.i][pos.j]
    }
    fn set(&mut self, pos: &Pos, value: T) {
        self.map[pos.i][pos.j] = value;
    }
    fn rows(&self) -> usize {
        self.map.len()
    }

    fn cols(&self) -> usize {
        self.map[0].len()
    }

    /* Get positions of neighbors that satisfy the filter condition */
    fn filter_neighbors<F>(&self, pos: &Pos, condition: F) -> Vec<Pos>
    where
        F: Fn(T) -> bool,
    {
        let mut res = Vec::new();
        let dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]];
        for dir in dirs {
            let new_i = pos.i as i32 + dir[0];
            let new_j = pos.j as i32 + dir[1];
            if new_i >= 0
                && new_i < (self.rows() as i32)
                && new_j >= 0
                && new_j < (self.cols() as i32)
            {
                let neighbor = Pos {
                    i: new_i as usize,
                    j: new_j as usize,
                };
                if condition(self.get(&neighbor)) {
                    res.push(neighbor);
                }
            }
        }
        return res;
    }
}

fn read_input(filename: &str) -> Map<i32> {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);
    let mut list = Vec::new();
    for line_result in reader.lines() {
        let line = line_result.unwrap();
        let mut row = Vec::new();
        for c in line.chars() {
            let height: i32 = c.to_string().parse().unwrap();
            row.push(height);
        }
        list.push(row);
    }
    return Map { map: list };
}

fn find_trails(map: &Map<i32>, trail_head: Pos) -> i32 {
    // trails need to start at height 0
    if map.get(&trail_head) != 0 {
        return 0;
    }
    let mut queue = VecDeque::new();
    let mut visited = HashSet::<Pos>::new();
    let mut visited_peaks = HashSet::<Pos>::new();
    queue.push_back(trail_head);
    while queue.len() > 0 {
        let cur = queue.pop_front().unwrap();
        if visited.contains(&cur) {
            continue;
        }
        visited.insert(cur);
        let cur_height = map.get(&cur);
        // reaching the peak
        if cur_height == 9 {
            visited_peaks.insert(cur);
            continue;
        }
        let neighbors = map.filter_neighbors(&cur, |x| x == cur_height + 1);
        queue.extend(neighbors.iter());
    }
    return visited_peaks.len() as i32;
}

fn part1(filename: &str) {
    let map = read_input(filename);
    let mut sum = 0;
    // TODO: add iterator over positions
    for i in 0..map.rows() {
        for j in 0..map.cols() {
            let pos = Pos { i, j };
            let trails = find_trails(&map, pos);
            sum += trails;
        }
    }
    println!("{sum}");
}

fn part2(filename: &str) {}

fn main() {
    part1("day10/input.txt");
    part2("day10/small_input.txt");
}
