from functools import wraps


def qq(args):
    def wrapper(func):
        @wraps(func)
        def wrap():
            print("before")
            func(args)
            print("after")
            return
        return wrap
    return wrapper


@qq('user')
def hello(q):
    print("hello,", q)
    return


hello()
