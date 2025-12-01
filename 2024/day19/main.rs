use std::collections::HashMap;

type Pattern = Vec<char>;

fn try_towel(pattern: &Pattern, towel: &Pattern, start_idx: usize) -> bool {
    let mut same = true;
    for i in 0..towel.len() {
        if start_idx + i >= pattern.len() || pattern[start_idx + i] != towel[i] {
            same = false;
            break;
        }
    }
    return same;
}

fn check_pattern(
    pattern: &Pattern,
    available_towels: &HashMap<char, Vec<&Pattern>>,
    from: usize,
) -> bool {
    if from >= pattern.len() {
        return true;
    }
    let pattern_start: char = pattern[from];
    if !available_towels.contains_key(&pattern_start) {
        return false;
    }
    let towels = &available_towels[&pattern_start];
    for towel in towels {
        if try_towel(pattern, towel, from) {
            let fit_rest = check_pattern(pattern, available_towels, from + towel.len());
            if fit_rest {
                return true;
            }
        }
    }
    return false;
}

fn part1(filename: &str) {
    let pattern: Vec<char> = "brwrr".chars().collect();
    let towels: Vec<Pattern> = vec!["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]
        .iter()
        .map(|x| x.chars().collect())
        .collect();
    let mut available_towels: HashMap<char, Vec<&mut Pattern>> = HashMap::new();
    for towel in towels {
        let first = towel[0];
        if available_towels.contains_key(&first) {
            // available_towels[&first].push(&towel);
        }
    }
    // check_pattern(pattern, available_towels, 0);
}

fn main() {}
