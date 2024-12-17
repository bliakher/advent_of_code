struct Computer {
    reg_a: i64,
    reg_b: i64,
    reg_c: i64,
    instr_pointer: usize,
    program: Vec<usize>,
    output: Vec<i64>,
}

impl Computer {
    fn resolve_combo_op(&self, op: usize) -> i64 {
        match op {
            0..=3 => op as i64,
            4 => self.reg_a,
            5 => self.reg_b,
            6 => self.reg_c,
            7.. => unreachable!(),
        }
    }
    fn execute_instr(&mut self, opcode: usize, op: usize) -> bool {
        match opcode {
            0 => self.adv(op),
            1 => self.bxl(op),
            2 => self.bst(op),
            3 => self.jnz(op),
            4 => self.bxc(op),
            5 => self.out(op),
            6 => self.bdv(op),
            7 => self.cdv(op),
            8.. => unreachable!(),
        };
        return opcode == 5;
    }
    fn adv(&mut self, op: usize) {
        let op_value = self.resolve_combo_op(op);
        self.reg_a = self.reg_a >> op_value;
        self.instr_pointer += 2;
    }
    fn bxl(&mut self, op: usize) {
        self.reg_b = self.reg_b ^ op as i64;
        self.instr_pointer += 2;
    }
    fn bst(&mut self, op: usize) {
        let op_value = self.resolve_combo_op(op);
        self.reg_b = op_value % 8;
        self.instr_pointer += 2;
    }
    fn jnz(&mut self, op: usize) {
        // assert!(op >= 0);
        if self.reg_a != 0 {
            self.instr_pointer = op;
        } else {
            self.instr_pointer += 2;
        }
    }
    fn bxc(&mut self, _: usize) {
        self.reg_b = self.reg_b ^ self.reg_c;
        self.instr_pointer += 2;
    }
    fn out(&mut self, op: usize) {
        let op_value = self.resolve_combo_op(op);
        self.output.push(op_value % 8);
        self.instr_pointer += 2;
        // println!("{:?}", self.output);
    }
    fn bdv(&mut self, op: usize) {
        let op_value = self.resolve_combo_op(op);
        self.reg_b = self.reg_a >> op_value;
        self.instr_pointer += 2;
    }
    fn cdv(&mut self, op: usize) {
        let op_value = self.resolve_combo_op(op);
        self.reg_c = self.reg_a >> op_value;
        self.instr_pointer += 2;
    }
    fn execute_program(&mut self) {
        assert!(self.program.len() % 2 == 0);
        while self.instr_pointer < self.program.len() - 1 {
            let instr_opcode = self.program[self.instr_pointer];
            let operand = self.program[self.instr_pointer + 1];
            self.execute_instr(instr_opcode, operand);
        }
    }
    fn execute_and_check(&mut self) -> bool {
        assert!(self.program.len() % 2 == 0);
        let mut check = true;
        while self.instr_pointer < self.program.len() - 1 {
            let instr_opcode = self.program[self.instr_pointer];
            let operand = self.program[self.instr_pointer + 1];
            let has_output = self.execute_instr(instr_opcode, operand);
            if has_output {
                let i = self.output.len() - 1;
                if self.program[i] as i64 != self.output[i] {
                    check = false;
                    // println!("{i}");
                    break;
                }
            }
        }
        return check;
    }
    fn reset(&mut self) {
        self.output = Vec::new();
        self.instr_pointer = 0;
        self.reg_a = 0;
        self.reg_b = 0;
        self.reg_c = 0;
    }
}

fn get_output_string<T>(list: &Vec<T>) -> String
where
    T: std::fmt::Display,
{
    let output_vec: Vec<String> = list.iter().map(|x| x.to_string()).collect();
    output_vec.join(",")
}

fn part1(computer: &mut Computer) {
    computer.execute_program();
    let output = get_output_string(&computer.output);
    println!("{}", output)
}

fn part2_bruteforce(computer: &mut Computer) {
    // let program = get_output_string(&computer.program);
    //  1_623_777_402_245_456
    let mut a = 35_187_900_000_000; // 35_187_900_000_000 35_184_000_000_000
    while a < 281_475_000_000_000 {
        // 140475000000000
        let b = (a % 8) ^ 1;
        if b == 0 || b == 1 {
            a += 1;
            continue;
        }
        let c = (a >> b) % 8;
        if (b == 2 && c != 4)
            || (b == 3 && c != 5)
            || (b == 4 && c != 2)
            || (b == 5 && c != 3)
            || (b == 6 && c != 0)
            || (b == 7 && c != 1)
        {
            a += 1;
            continue;
        }
        println!("A: {a}");
        computer.reset();
        computer.reg_a = a;
        let matched = computer.execute_and_check();
        // let output = get_output_string(&computer.output);
        if matched {
            println!("MATCH!");
            break;
        }
        a += 1;
    }
}

fn part2test(computer: &mut Computer) {
    let program = get_output_string(&computer.program);
    let mut a = 1;
    while a <= 1000 {
        // A: 1000000 - 5,1,5,5,6,3,6
        // A: 125000 -    1,5,5,6,3,6
        // 1_000_000_000_000
        computer.reset();
        computer.reg_a = a;
        computer.execute_program();
        let output = get_output_string(&computer.output);
        println!("A: {a} - {output}");
        if program == output {
            println!("MATCH!");
            println!("{:?}", computer.output);
            break;
        }
        a += 1;
    }
}

fn part2(computer: &mut Computer) {
    let mut a = 0;
    let program_len = computer.program.len();
    let mut bits: Vec<i64> = Vec::new();
    let mut i = 0;
    while i < program_len {
        if bits.len() <= i {
            bits.push(0);
        }
        let target = computer.program[program_len - i - 1];
        let mut found = false;
        let start_bits = bits[i];
        assert!(start_bits < 8);
        for last_bits in start_bits..8 {
            let a_new = a + last_bits;
            computer.reset();
            computer.reg_a = a_new;
            computer.execute_program();
            if computer.output[computer.output.len() - i - 1] == target as i64 {
                println!("{a_new} = {a} + {last_bits}: {:?}", computer.output);
                bits[i] = last_bits + 1;
                println!("{:?}", bits);
                found = true;
                a = a_new;
                break;
            }
        }
        if !found {
            i -= 1;
            a = a / 8;
            a = a - bits[i] + 1;
            bits.pop();
            continue;
        }
        a = a * 8;
        i += 1;
    }
    println!("Jupi: {}", a / 8);
}

fn main() {
    let mut test1 = Computer {
        reg_a: 2024,
        reg_b: 0,
        reg_c: 0,
        instr_pointer: 0,
        program: vec![0, 3, 5, 4, 3, 0],
        output: Vec::new(),
    };

    let mut example_computer = Computer {
        reg_a: 729,
        reg_b: 0,
        reg_c: 0,
        instr_pointer: 0,
        program: vec![0, 1, 5, 4, 3, 0],
        output: Vec::new(),
    };

    let mut computer = Computer {
        reg_a: 28066687,
        reg_b: 0,
        reg_c: 0,
        instr_pointer: 0,
        program: vec![2, 4, 1, 1, 7, 5, 4, 6, 0, 3, 1, 4, 5, 5, 3, 0],
        output: Vec::new(),
    };

    // part1(&mut example_computer);
    // part1(&mut computer);

    // part2(&mut test1);
    // part2test(&mut computer);
    // part2_bruteforce(&mut computer);

    part2(&mut computer);
}
