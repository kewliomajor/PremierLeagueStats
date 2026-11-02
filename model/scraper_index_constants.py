
def get_fixed_index_table(current_year ):
    if current_year:
        return [2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:
        return [1, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def get_variable_index_table(table_size, current_year):
    indicies = []
    if current_year:
        indicies.append(table_size - 5)
        indicies.append(table_size - 4)
        indicies.append(table_size - 3)
        indicies.append(table_size - 2)
        indicies.append(table_size - 1)
    else:
        indicies.append(table_size - 4)
        indicies.append(table_size - 3)
        indicies.append(table_size - 2)
        indicies.append(table_size - 1)
    return indicies
