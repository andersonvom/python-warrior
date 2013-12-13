import time

from pythonwarrior import Config


class UI(object):
    @classmethod
    def ask(cls, message):
        response = cls.request(message + ' [yn] ')
        return response.lower() in ('y', 'yes')

    @classmethod
    def readline(cls):
        if Config.get('in_stream'):
            return Config.get('in_stream').readline().rstrip()
        return ""

    @classmethod
    def write(cls, message):
        if Config.get('out_stream'):
            Config.get('out_stream').write(unicode(message))

    @classmethod
    def writeline(cls, message):
        cls.write(message + '\n')

    @classmethod
    def writeline_with_delay(cls, message):
        cls.writeline(message)
        if Config.get('delay'):
            time.sleep(Config.get('delay'))

    @classmethod
    def request(cls, message):
        cls.write(message)
        return cls.readline().rstrip()

    @classmethod
    def choose(cls, item, options):
        if len(options) == 1:
            response = options[0]
        else:
            cls._display_options(options)
            choice = cls.request("Choose %s by typing the number: " % item)
            response = options[int(choice)-1]

        if isinstance(response, list):
            response = response[0]

        return response

    @classmethod
    def _display_options(cls, options):
        for idx, option in enumerate(options):
            label = option
            if isinstance(option, list):
                label = option[-1]
            cls.writeline("[%s] %s" % (idx+1, label))
