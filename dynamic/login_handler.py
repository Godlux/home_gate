def auth_user(login, password):
    if login == "admin" and password == "password":
        return True
    else:
        return False
