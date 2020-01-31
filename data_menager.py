def read_file(file_name):
    """
    Opens a file and transform its content into list of strings.
    Args: file_name (string)
    Returns: list
    """
    
    table=[]
    with open(file_name) as file:
        for line in file:
            table.append(line)
    return table