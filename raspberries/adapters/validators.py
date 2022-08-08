

def is_password_valid(value: str) -> None:
    if len(value) not in range(8, 17):
        raise ValueError("Wrong password length")
