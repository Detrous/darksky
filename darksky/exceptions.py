
class DarkSkyException(Exception):
    def __init__(self, code, msg):  # pylint: disable=W0231
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'Error[{code}]: {msg}'.format(
            code=self.code,
            msg=self.msg
        )
