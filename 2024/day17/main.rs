use num::Integer;

struct Computer {
    regA: i64,
    regB: i64,
    regC: i64,
    instr_pointer: usize,
    program: Vec<usize>,
    output: Vec<i64>,
}

impl Computer {
    fn resolve_combo_op(&self, op: usize) -> i64 {
        match op {
            0..=3 => op as i64,
            4 => self.regA,
            5 => self.regB,
            6 => self.regC,
            7.. => unreachable!(),
        }
    }
    fn execute_instr(&mut self, opcode: usize, op: usize) {
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
    }
    fn adv(&mut self, op: usize) {
        let op_value = self.resolve_combo_op(op);
        self.regA = self.regA >> op_value;
        self.instr_pointer += 2;
    }
    fn bxl(&mut self, op: usize) {
        self.regB = self.regB ^ op as i64;
        self.instr_pointer += 2;
    }
    fn bst(&mut self, op: usize) {
        let op_value = self.resolve_combo_op(op);
        self.regB = op_value % 8;
        self.instr_pointer += 2;
    }
    fn jnz(&mut self, op: usize) {
        // assert!(op >= 0);
        if self.regA != 0 {
            self.instr_pointer = op;
        } else {
            self.instr_pointer += 2;
        }
    }
    fn bxc(&mut self, _: usize) {
        self.regB = self.regB ^ self.regC;
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
        self.regB = self.regA >> op_value;
        self.instr_pointer += 2;
    }
    fn cdv(&mut self, op: usize) {
        let op_value = self.resolve_combo_op(op);
        self.regC = self.regA >> op_value;
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
    fn reset(&mut self) {
        self.output = Vec::new();
        self.instr_pointer = 0;
        self.regA = 0;
        self.regB = 0;
        self.regC = 0;
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

fn part2(computer: &mut Computer) {
    let program = get_output_string(&computer.program);
    let mut a = 582945529;
    while a < 1_000_000_000_000 {
        println!("A: {a}");
        computer.reset();
        computer.regA = a;
        computer.execute_program();
        let output = get_output_string(&computer.output);
        if output == program {
            println!("MATCH!");
            break;
        }
        a += 1;
    }
}

fn main() {
    let mut test1 = Computer {
        regA: 2024,
        regB: 0,
        regC: 0,
        instr_pointer: 0,
        program: vec![0, 3, 5, 4, 3, 0],
        output: Vec::new(),
    };

    let mut example_computer = Computer {
        regA: 729,
        regB: 0,
        regC: 0,
        instr_pointer: 0,
        program: vec![0, 1, 5, 4, 3, 0],
        output: Vec::new(),
    };

    let mut computer = Computer {
        regA: 28066687,
        regB: 0,
        regC: 0,
        instr_pointer: 0,
        program: vec![2, 4, 1, 1, 7, 5, 4, 6, 0, 3, 1, 4, 5, 5, 3, 0],
        output: Vec::new(),
    };

    // part1(&mut example_computer);
    // part1(&mut computer);

    // part2(&mut test1);
    part2(&mut computer);
}
