use std::{
    collections::{HashMap, HashSet},
    fmt::Debug,
    fs::File,
    io::{BufRead, BufReader},
    str::FromStr,
};

#[derive(PartialEq, Eq, Copy, Clone, Hash)]
struct Pos {
    i: usize,
    j: usize,
}

struct Map<T: Copy> {
    map: Vec<Vec<T>>,
}

struct MapIterator {
    width: usize,
    height: usize,
    idx: usize,
}

impl Iterator for MapIterator {
    type Item = Pos;

    fn next(&mut self) -> Option<Self::Item> {
        if self.idx >= self.width * self.height {
            return None;
        }
        let i = self.idx / self.width;
        let j = self.idx % self.width;
        self.idx += 1;
        Some(Pos { i, j })
    }
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
    fn inside(&self, i: i32, j: i32) -> bool {
        i >= 0 && i < self.rows() as i32 && j >= 0 && j < self.cols() as i32
    }

    // fn iter_pos() -> impl Iterator<Item = Pos> {
    //     (0..100).map()
    // }

    fn iter_pos(&self) -> MapIterator {
        MapIterator {
            width: self.cols(),
            height: self.rows(),
            idx: 0,
        }
    }

    fn parse_from_file(filename: &str) -> Map<T>
    where
        T: FromStr,
        <T as FromStr>::Err: Debug,
    {
        let f = File::open(filename).unwrap();
        let reader = BufReader::new(f);
        let mut list = Vec::new();
        for line_result in reader.lines() {
            let line = line_result.unwrap();
            let mut row = Vec::new();
            for c in line.chars() {
                let height = c.to_string().parse().unwrap();
                row.push(height);
            }
            list.push(row);
        }
        return Map { map: list };
    }
}

impl<T: Copy> IntoIterator for Map<T> {
    type Item = Pos;

    type IntoIter = MapIterator;

    fn into_iter(self) -> Self::IntoIter {
        self.iter_pos()
    }
}

fn get_antinodes(pos1: Pos, pos2: Pos, map: &Map<char>) -> Vec<Pos> {
    let diff_i = pos1.i as i32 - pos2.i as i32;
    let diff_j: i32 = pos1.j as i32 - pos2.j as i32;
    let mut res = Vec::new();
    let a1_i = pos1.i as i32 + diff_i;
    let a1_j = pos1.j as i32 + diff_j;
    let a2_i = pos2.i as i32 - diff_i;
    let a2_j = pos2.j as i32 - diff_j;
    if map.inside(a1_i, a1_j) {
        res.push(Pos {
            i: a1_i as usize,
            j: a1_j as usize,
        });
    }
    if map.inside(a2_i, a2_j) {
        res.push(Pos {
            i: a2_i as usize,
            j: a2_j as usize,
        });
    }
    res
}

fn get_all_antinodes(antenna_positions: &Vec<Pos>, map: &Map<char>) -> HashSet<Pos> {
    let mut antinodes: HashSet<Pos> = HashSet::new();
    for i in 1..antenna_positions.len() {
        for j in 0..i {
            let res = get_antinodes(antenna_positions[i], antenna_positions[j], map);
            antinodes.extend(res);
        }
    }
    antinodes
}

fn part1(filename: &str) {
    let map = Map::<char>::parse_from_file(filename);
    let mut antennas: HashMap<char, Vec<Pos>> = HashMap::new();
    for pos in map.iter_pos() {
        let symbol = map.get(&pos);
        if symbol != '.' {
            if antennas.contains_key(&symbol) {
                antennas.get_mut(&symbol).unwrap().push(pos);
            } else {
                antennas.insert(symbol, vec![pos]);
            }
        }
    }
    let mut antinodes: HashSet<Pos> = HashSet::new();
    for (_, positions) in antennas {
        let res = get_all_antinodes(&positions, &map);
        antinodes.extend(res);
    }
    println!("{}", antinodes.len());
}

fn main() {
    part1("day08/small_input.txt");
    part1("day08/input.txt");
}
