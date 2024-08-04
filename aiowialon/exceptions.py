class WialonError(Exception):
    """
    Exception raised when an Wialon Remote API call fails due to a network
    related error or for a Wialon specific reason.
    """
    errors = {
        1: 'Invalid session',
        2: 'Invalid service',
        3: 'Invalid result',
        4: 'Invalid input',
        5: 'Error performing request',
        6: 'Unknown error',
        7: 'Access denied',
        8: 'Invalid user name or password',
        9: 'Authorization server is unavailable, please try again later',
        1001: 'No message for selected interval',
        1002: 'Item with such unique property already exists',
        1003: 'Only one request of given time is allowed at the moment'
    }

    def __init__(self, code, reason="", action_name=""):
        self.code = code
        self.reason = reason
        self.action_name = action_name
        try:
            self.code = int(code)
        except ValueError:
            pass

    def description(self):
        explanation = WialonError.errors.get(self.code, 6)
        action_name = f'"{self.action_name}" ' if self.action_name else ""
        reason = f": {self.reason}" if self.reason else ""
        return '{error} {action_name}({code}){reason}'.format(
            error=explanation, code=self.code, reason=reason,
            action_name=action_name
        )

    def __str__(self):
        return 'WialonError({message})'.format(message=self.description())

    def __repr__(self):
        return str(self)
