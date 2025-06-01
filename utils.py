
def log_start(user_id):
    with open("start_log.txt", "a") as f:
        f.write(f"User {user_id} started the bot\n")
