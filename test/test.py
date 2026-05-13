
def log(func):
    def t():
        print("1")
        func()
        print("2")
    return t

@log
def hello_world():
    print("hello world")
    
hello_world()