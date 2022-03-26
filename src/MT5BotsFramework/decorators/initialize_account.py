import MetaTrader5


class MessageLimitUsers(object):
    def __init__(self, users: list) -> None:
        self.users = users

    def __call__(self, message_to_order):
        def wrapper(*args, **kwargs):
            result = message_to_order(*args, **kwargs)
            if result.get("user") not in self.users:
                raise ValueError("This user is not from this bot")
            return result

        return wrapper


class ChangeAccountUser(object):
    def __init__(self, message_to_order):
        self.message_to_order = message_to_order

    def __call__(self, *args, **kwargs):
        result = self.message_to_order(self, *args, **kwargs)
        user = result.get("user")
        if user not in COPY_TRADING_USERS.keys():
            raise ValueError("This user is not from this bot")
        account = COPY_TRADING_USERS[user]["account"]
        if not MetaTrader5.login(
                login=account,
                password=BROKER_PASSWORD,
                server=BROKER_SERVER,
        ):
            raise AuthorizedError(
                f"Failed to connect at account, error code:{MetaTrader5.last_error()}"
            )
        if CUSTOM_LOT:
            result.update(
                {"balance_to_lot": COPY_TRADING_USERS[user].get("balance_to_lot", 40)}
            )
        return result
