class Constants:
    __instance = None

    # remote_ip = 'http://192.168.1.6'
    remote_ip = 'http://localhost'
    port = 8000
    SERVER_URL = remote_ip + ":" + str(port)

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Constants.__instance == None:
            Constants()
        return Constants.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Constants.__instance != None:
            raise Exception("This class is a Singleton!")
        else:
            Constants.__instance = self


if __name__ == '__main__':
    s = Constants.getInstance()
    print(s)

    # Throws an exception
    # t = Constants()

    # print(s.remote_ip)
    # print(Constants.getInstance().SERVER_URL)

    print(s.SERVER_URL)
    print(s.remote_ip)
    print(s.port)
