from todoo_project.models import users, todos

session = {}


def signinreqd(fn):
    def wrapper(*args, **kwargs):
        if "user" in session:
            return fn(*args, **kwargs)
        else:
            print("you must login")

    return wrapper


def authenticate(**kwargs):
    username = kwargs.get("username")
    password = kwargs.get("password")
    user = [user for user in users if user["username"] == username and user["password"] == password]
    return user


class SignInView:
    def post(self, *args, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        user = authenticate(username=username, password=password)
        if user:
            session["user"] = user[0]
            print("login successfull")
        else:
            print("invalid credentials", "try again")


class Todoview:
    @signinreqd
    def get(self, *args, **kwargs):
        return todos

    def todo(self, *args, **kwargs):
        userId = session["user"]["id"]
        kwargs["user"] = userId
        todos.append(kwargs)
        print(todos)


class MyTodoListView:
    @signinreqd
    def get(self, *args, **kwargs):
        print(session)
        userId = session["user"]["id"]
        print(userId)
        my_todo = [todo for todo in todos if todo["userId"] == userId]
        return my_todo


class TodoDetailsView:

    def get_object(self, id):
        todo = [todo for todo in todos if todo["todoId"] == id]
        return todo

    @signinreqd
    def get(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        todo = self.get_object(todo_id)

        return todo

    @signinreqd
    def delete(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        data = self.get_object(todo_id)
        if data:
            todo = data[0]
            todos.remove(todo)
            print("todo removed")
            print(len(todos))

    def put(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        instance = self.get_object(todo_id)
        data = kwargs.get("data")
        if instance:
            todo_obj = instance[0]
            todo_obj.update(data)
            return todo_obj


# log = SignInView()
# log.post(username="anu", password="Password@123")
#
# my_todo = MyTodoListView()
# print(my_todo.get())
#
# todo_details=TodoDetailsView()
# todo_details.delete(todo_id=6)
# print(todo_details.get(todo_id=4))

