def read_file(file_name):
    table=[]
    with open(file_name) as file:
        for line in file:
            table.append(line)
    return table