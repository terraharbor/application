from user import User
import json
import os
import time

# Get the data directory from environment variable, fallback to 'data' for local development
DATA_DIR = os.getenv('STATE_DATA_DIR', 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json') 

def decode_token(token: str) -> User | None:
    """
    Decode the token and return the user information.
    This function assumes the token is valid and contains user information.
    """
    try:
        with open(USERS_FILE, "r") as f:
            users_dict = json.load(f)
            for user in users_dict.values():
                if user.get("token") == token:
                    return User(
                        username=user["username"],
                        email=user["email"],
                        full_name=user.get("full_name"),
                        disabled=user.get("disabled", False),
                        sha512_hash=user["sha512_hash"],
                        token=token,
                        token_validity=user.get("token_validity")
                    )
    except Exception as e:
        print(f"Error decoding token: {e}")
    
    return None

def get_user(user: str) -> User | None:
    """
    Retrieve the user information.
    This function should check against a database or user store.
    """

    try:
        with open(USERS_FILE, "r") as f:
            users_dict = json.load(f)
            user_dict = users_dict.get(user)
            
        # If user doesn't exist, return None
        if user_dict is None:
            return None

    except Exception as e:
        return None

    disabled_value = user_dict.get("disabled", False)

    return User(username=user_dict["username"],
                disabled=disabled_value,
                sha512_hash=user_dict["sha512_hash"])

def user_exists(user: User) -> bool:
    """
    Verify if the user already exists in the system.
    """
    return bool(get_user(user.username))

def register_user(user: User) -> None:
    """
    Register a new user in the system. For now, registration is done by writing to a JSON file.
    """
    print(f"Received user registration request: \n{user}")
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        
        try:
            with open(USERS_FILE, "r") as f:
                users_dict = json.load(f)
        except FileNotFoundError:
            users_dict = {}
        
        users_dict[user.username] = {
            "username": user.username,
            "disabled": user.disabled,
            "sha512_hash": user.sha512_hash,
            "token": None,
            "token_validity": None
        }

        with open(USERS_FILE, "w") as f:
            json.dump(users_dict, f, indent=4)

    except Exception as e:
        raise RuntimeError(f"Failed to register user: {e}")

def update_user_token(username: str, token: str) -> None:
    """
    Update the user's token in the user store.
    """
    try:
        with open(USERS_FILE, "r") as f:
            users_dict = json.load(f)

        if username not in users_dict:
            raise ValueError("User does not exist")

        users_dict[username]["token"] = token
        users_dict[username]["token_validity"] = int(time.time()) + 3600  # Token valid for 1 hour

        with open(USERS_FILE, "w") as f:
            json.dump(users_dict, f, indent=4)

    except Exception as e:
        raise RuntimeError(f"Failed to update user token: {e}")

def is_token_valid(token: str) -> bool:
    """
    Check if the provided token is valid.
    This function should check the token's validity against the user store.
    """
    user = decode_token(token)
    if user is None or user.disabled:
        return False

    current_time = int(time.time())
    return user.token_validity is not None and user.token_validity > current_time