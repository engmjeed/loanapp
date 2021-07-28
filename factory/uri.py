from django.db import models

class uri(tuple):

    __slots__ = ()

    _sep = "/"
    _allow_chars = ":=+*|"

    def __new__(cls, *paths):
        if len(paths) == 1 and isinstance(paths[0], cls):
            return paths[0]
        return super().__new__(cls, cls._parse(*paths))

    @property
    def parts(self):
        return tuple(self)

    def as_str(self):
        ln = len(self)
        return "" if ln == 0 else str(self[0]) if ln == 1 else self._sep.join(self)

    @classmethod
    def _parse(cls, *paths):
        for path in paths:
            if isinstance(path, uri):
                yield from path
                # for p in path:
                # 	yield p
            else:
                for p in path.split(cls._sep) if isinstance(path, str) else path:
                    if not isinstance(p, (str, int, float)):
                        raise TypeError("uri can only contain strings. %s" % type(p))
                    elif p:
                        yield str(p)

    # @classmethod
    # def _parse_part(cls, part):
    #     return part # and text.slug(str(part), allow=cls._allow_chars)

    def startswith(self, other, start=None, end=None):
        if not isinstance(other, tuple):
            other = self.__class__(other)

        target = self if start is None and end is None else self[start:end]
        olen, tlen = len(other), len(target)
        if tlen == olen:
            return target == other
        elif tlen > olen:
            return target[:olen] == other
        else:
            return False

    def endswith(self, other, start=None, end=None):
        if not isinstance(other, tuple):
            other = self.__class__(other)

        target = self if start is None and end is None else self[start:end]
        olen, tlen = len(other), len(target)
        if tlen == olen:
            return target == other
        elif tlen > olen:
            return target[(olen * -1) :] == other
        else:
            return False

    def copy(self):
        return self.__class__(iter(self))

    def join(self, *paths):
        return self.__class__(self, *paths)

    def __contains__(self, value):
        value = self.__class__(value)
        lv, ls = len(value), len(self)
        if lv == 0:
            return True
        elif ls == 0 or lv > ls:
            return False
        elif ls == lv:
            return self == value
        else:
            return value.as_str() in self.as_str()

    def __eq__(self, other):
        """Check equality against strings, lists and tuples.
		"""
        if isinstance(other, str):
            return str(self) == other
        else:
            return super().__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return self.__class__(self, other)

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(*(self for _ in range(other)))
        return super().__mul__(other)

    def __hash__(self):
        return hash(str(self))

    def __getitem__(self, index):
        rv = super().__getitem__(index)
        if isinstance(index, slice):
            return self.__class__(rv)
        else:
            return rv

    def __json__(self):
        return self.as_str()

    def __str__(self):
        return self.as_str()

    def __repr__(self):
        return '%s("%s")' % (self.__class__.__name__, self)


class UriField(models.CharField):

    description = "A slash '/' separated path"

    # def __init__(self, *args, **kwargs):
    # 	kwargs.setdefault('max_length', 255)
    # 	super().__init__(*args, **kwargs)

    def to_python(self, value):
        return None if value is None else uri(value)

    def from_db_value(self, value, expression, connection, context=None):
        return self.to_python(value)

    def get_prep_value(self, value):
        return self.to_python(value)
