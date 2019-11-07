def is_new_version(current, new):
    current_list = current.split('.')
    new_list = new.split('.')

    if int(new_list[0]) > int(current_list[0]):
        return True
    elif int(new_list[0]) == int(current_list[0]):
        if int(new_list[1]) > int(current_list[1]):
            return True

    return False
