class UI(object):
    @classmethod
    def ask(cls):
        pass

    @classmethod
    def gets(cls):
        pass

    @classmethod
    def puts(cls, message):
        pass

    @classmethod
    def request(cls, message):
        pass

    @classmethod
    def choose(cls, item, options):
        if len(options) == 1:
            response = options[0]
        else:
            for idx, option in enumerate(options):
                label = option
                if isinstance(option, list):
                    label = option[-1]
                cls.puts("[%s] %s" % (idx+1, label))

            choice = cls.request("Choose %s by typing the number: ")
            response = options[int(choice)-1]

        if isinstance(response, list):
            response = response[0]

        return response
