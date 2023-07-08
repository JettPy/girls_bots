def func():
    print("Привет из функции!")


func()


def bread(fanc):
    def wrapper():
        print("/---------\\")
        func()
        print("\\---------/")
    return wrapper

def ingredients(fanc):
    def wrapper():
        print("#помидоры#")
        func()
        print("----салат-----")
    return wrapper


@bread
@ingredients
def sandwich(food="~~ветчина~~"):
    print(food)

sandwich()

