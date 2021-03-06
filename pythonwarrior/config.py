class Config(object):
    delay = None
    in_stream = None
    out_stream = None
    practice_level = None
    path_prefix = None
    skip_input = None

    _defaults = {
        'path_prefix': '.'
    }

    @classmethod
    def reset(cls):
        class_attrs = ['delay', 'in_stream', 'out_stream', 'practice_level',
                       'path_prefix', 'skip_input']
        for attr in class_attrs:
            setattr(cls, attr, None)

    @classmethod
    def get(cls, attr):
        value = getattr(cls, attr)
        if not value:
            value = cls._defaults.get(attr)

        return value
