def print_func_name(fn):
    def wrapper(self):
        name = fn.__name__ + '()'
        print '{}\n{}\n{}'.format( '_'*125, name, fn(self))
    return wrapper

class someclass():
    def __init__(self,value):
        self.value = value
        pass

    @print_func_name
    def print_stuff(self):
        if self.value == 1:
            return 1
        else:
            return 'it is not 1'


class someclass2():
    def __init__(self,value):
        self.value = value
        pass

    def print_stuff(self):
        if self.value == 1:
            return 1
        else:
            return 'it is not 1'