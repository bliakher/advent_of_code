
class FileEntry:
    def __init__(self, name, parent, is_dir, size = 0):
        self.name = name
        self.parent = parent
        self.children = []
        self.is_dir = is_dir
        self.size = size

    def compute_size(self):
        for child in self.children:
            self.size += child.compute_size()
        return self.size

    def print(self, offset = ''):
        file_data = 'dir ' + str(self.size) if self.is_dir else str(self.size) 
        print(offset + '- ' + self.name, file_data)
        for child in self.children:
            child.print(offset + '  ')

    def find_dirs_less_than(self, limit, total = 0):
        if self.size <= limit:
            total += self.size
        for child in self.children:
            if child.is_dir:
                total = child.find_dirs_less_than(limit, total)
        return total

    def find_smallest_with_limit(self, limit, smallest):
        new_smallest = smallest
        if self.size > limit and self.size < smallest.size:
            new_smallest = self
        for child in self.children:
            if child.is_dir:
                new_smallest = child.find_smallest_with_limit(limit, new_smallest)
        return new_smallest






def read_input_to_list(file_name):
    res = []
    with open(file_name) as f:
        for line in f.readlines():
            command = line.strip()
            res.append(command)
    return res

def create_file(comand, parent):
    parts = comand.split(' ')
    identifier = parts[0] # size or dir
    name = parts[1]
    if (identifier.isdigit()):
        size = int(identifier)
        return FileEntry(name, parent, False, size)
    return FileEntry(name, parent, True)

def find_destination_dir(name, files):
    for file in files:
        if file.name == name:
            return file


def create_filesystem(comands):
    root = FileEntry('/', None, True)
    cur_dir = root
    for i in range(1, len(comands)):
        comand = comands[i]
        if comand[0] == '$':
            if comand == '$ ls':
                continue
            parts = comand.split(' ')
            if parts[1] != 'cd':
                print('ERROR')
            destination = parts[2]
            if destination == '..':
                cur_dir = cur_dir.parent
            else:
                cur_dir = find_destination_dir(destination, cur_dir.children)
        else:
            file_entry = create_file(comand, cur_dir)
            cur_dir.children.append(file_entry)
        
    return root

comands = read_input_to_list('input.txt')
filesystem = create_filesystem(comands)
filesystem.compute_size()
# filesystem.print()
print(filesystem.find_dirs_less_than(100000))

total_space = 70000000
space_for_update = 30000000
used_space = filesystem.size
free_space = total_space - used_space
space_needed = space_for_update - free_space

print(used_space, free_space, space_needed)
to_delete = filesystem.find_smallest_with_limit(space_needed, filesystem)
print(to_delete.name, to_delete.size)






