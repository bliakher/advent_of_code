use std::fs;

fn read_input(filename: &str) -> String {
    let contents = fs::read_to_string(filename).unwrap();
    return contents;
}

enum ParsingState {
    Default,
    mUl,
    muL,
    OpenBracket,
    FirstNumber,
    SecondNumber,
}

fn part1(filename: &str) {
    let contents = read_input(filename);
    let mut sum = 0;
    let mut state = ParsingState::Default;
    let mut first_number = String::new();
    let mut second_number = String::new();
    for char in contents.chars() {
        state = match state {
            ParsingState::Default => match char {
                'm' => ParsingState::mUl,
                _ => ParsingState::Default,
            },
            ParsingState::mUl => match char {
                'u' => ParsingState::muL,
                _ => ParsingState::Default,
            },
            ParsingState::muL => match char {
                'l' => ParsingState::OpenBracket,
                _ => ParsingState::Default,
            },
            ParsingState::OpenBracket => match char {
                '(' => ParsingState::FirstNumber,
                _ => ParsingState::Default,
            },
            ParsingState::FirstNumber => match char {
                ',' => ParsingState::SecondNumber,
                c => {
                    if c.is_numeric() {
                        first_number.push(c);
                        ParsingState::FirstNumber
                    } else {
                        first_number = String::new();
                        ParsingState::Default
                    }
                }
            },
            ParsingState::SecondNumber => match char {
                ')' => {
                    let num1: i32 = first_number.parse().unwrap();
                    let num2: i32 = second_number.parse().unwrap();
                    let mul = num1 * num2;
                    sum += mul;
                    first_number = String::new();
                    second_number = String::new();
                    ParsingState::Default
                }
                c => {
                    if c.is_numeric() {
                        second_number.push(c);
                        ParsingState::SecondNumber
                    } else {
                        first_number = String::new();
                        second_number = String::new();
                        ParsingState::Default
                    }
                }
            },
        }
    }
    println!("{sum}");
}

enum ParsingState2 {
    MulEnabled,
    MulDisabled,
    Mul,
    Do,
    Dont,
    FirstNumber,
    SecondNumber,
}

fn part2(filename: &str) {
    let contents = read_input(filename);
    let mut sum = 0;
    let mut state = ParsingState2::MulEnabled;
    let mut first_number = String::new();
    let mut second_number = String::new();
    let mut mul_counter = 0;
    let mut do_counter = 0;
    for char in contents.chars() {
        state = match state {
            ParsingState2::MulDisabled => match char {
                'd' => ParsingState2::Do,
                _ => ParsingState2::MulDisabled,
            },
            ParsingState2::MulEnabled => match char {
                'm' => ParsingState2::Mul,
                'd' => ParsingState2::Dont,
                _ => ParsingState2::MulEnabled,
            },
            ParsingState2::Do => match do_counter {
                0 => match char {
                    'o' => {
                        do_counter += 1;
                        ParsingState2::Do
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulDisabled
                    }
                },
                1 => match char {
                    '(' => {
                        do_counter += 1;
                        ParsingState2::Do
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulDisabled
                    }
                },
                2 => match char {
                    ')' => {
                        do_counter = 0;
                        ParsingState2::MulEnabled
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulDisabled
                    }
                },
                _ => {
                    do_counter = 0;
                    ParsingState2::MulDisabled
                }
            },
            ParsingState2::Dont => match do_counter {
                0 => match char {
                    'o' => {
                        do_counter += 1;
                        ParsingState2::Dont
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                1 => match char {
                    'n' => {
                        do_counter += 1;
                        ParsingState2::Dont
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                2 => match char {
                    '\'' => {
                        do_counter += 1;
                        ParsingState2::Dont
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                3 => match char {
                    't' => {
                        do_counter += 1;
                        ParsingState2::Dont
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                4 => match char {
                    '(' => {
                        do_counter += 1;
                        ParsingState2::Dont
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                5 => match char {
                    ')' => {
                        do_counter = 0;
                        ParsingState2::MulDisabled
                    }
                    _ => {
                        do_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                _ => {
                    do_counter = 0;
                    ParsingState2::MulEnabled
                }
            },
            ParsingState2::Mul => match mul_counter {
                0 => match char {
                    'u' => {
                        mul_counter += 1;
                        ParsingState2::Mul
                    }
                    _ => {
                        mul_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                1 => match char {
                    'l' => {
                        mul_counter += 1;
                        ParsingState2::Mul
                    }
                    _ => {
                        mul_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                2 => match char {
                    '(' => {
                        mul_counter = 0;
                        ParsingState2::FirstNumber
                    }
                    _ => {
                        mul_counter = 0;
                        ParsingState2::MulEnabled
                    }
                },
                _ => {
                    mul_counter = 0;
                    ParsingState2::MulEnabled
                }
            },
            ParsingState2::FirstNumber => match char {
                ',' => ParsingState2::SecondNumber,
                c => {
                    if c.is_numeric() {
                        first_number.push(c);
                        ParsingState2::FirstNumber
                    } else {
                        first_number = String::new();
                        ParsingState2::MulEnabled
                    }
                }
            },
            ParsingState2::SecondNumber => match char {
                ')' => {
                    let num1: i32 = first_number.parse().unwrap();
                    let num2: i32 = second_number.parse().unwrap();
                    let mul = num1 * num2;
                    sum += mul;
                    first_number = String::new();
                    second_number = String::new();
                    ParsingState2::MulEnabled
                }
                c => {
                    if c.is_numeric() {
                        second_number.push(c);
                        ParsingState2::SecondNumber
                    } else {
                        first_number = String::new();
                        second_number = String::new();
                        ParsingState2::MulEnabled
                    }
                }
            },
        }
    }
    println!("{sum}");
}

fn main() {
    part1("day03/input.txt");
    part2("day03/input.txt");
}
