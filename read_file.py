def read_every_second_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    every_second_line = []
    for index in range(1, len(lines), 2):
        every_second_line.append(lines[index])
    
    return every_second_line
