class Q(object):
    """ Q is a query builder for the lucene language."""

    specialchars = r'+-!(){}[]^"~*?\:'
    doublechars = '&&||'

    def __init__(self, *args, **kwargs):
        """
        """
        self.must = []
        self.must_not = []
        self.should = []
        self._has_field = False
        self._child_has_field = False
        if len(args) == 1 and not kwargs:
            if Q._check_whitespace(args[0]):
                self.should.append('"'+self._escape(args[0])+'"')
            else:
                self.should.append(self._escape(args[0]))
        elif len(args) <= 1 and kwargs:
            if kwargs.get('inrange'):
                self.inrange = tuple(kwargs['inrange'])
            elif kwargs.get('exrange'):
                self.exrange = tuple(kwargs['exrange'])
            if len(args) == 1:
                if Q._check_whitespace(args[0]):
                    raise ValueError('No whitepsace allowed in field names.')
                self.field = args[0]
                self._has_field = True
        elif len(args) == 2:
            if Q._check_whitespace(args[0]):
                raise ValueError('No whitespace allowed in field names.')
            self.field = args[0]
            self._has_field = True
            if Q._check_whitespace(args[1]):
                self.should.append('"'+self._escape(args[1])+'"')
            else:
                self.should.append(self._escape(args[1]))
        if self._check_nested_fields():
            raise ValueError('No nested fields allowed.')

    fielded = property(lambda self: (self._has_field or self._child_has_field))

    @classmethod
    def _check_whitespace(cls, s):
        import string
        if isinstance(s, basestring):
            for c in string.whitespace:
                if c in s:
                    return True
        return False

    @classmethod
    def _escape(cls, s):
        if isinstance(s, basestring):
            rv = ''
            for c in s:
                if c in cls.specialchars:
                    rv += '\\' + c
                else:
                    rv += c
            return rv
        return s

    def _make_and(q1, q2):
        q = Q()
        setattr(q, '_and', (q1, q2))
        return q

    def _make_not(q1):
        q = Q()
        setattr(q, '_not', q1)
        return q

    def _make_or(q1, q2):
        q = Q()
        setattr(q, '_or', (q1, q2))
        return q

    def _make_must(q1):
        q = Q()
        q.must.append(q1)
        return q

    def _make_must_not(q1):
        q = Q()
        q.must_not.append(q1)
        return q

    def __and__(self, other):
        return Q._make_and(self, other)

    def __or__(self, other):
        return Q._make_or(self, other)

    def __invert__(self):
        return Q._make_not(self)

    def __pos__(self):
        return Q._make_must(self)

    def __neg__(self):
        return Q._make_must_not(self)

    def __add__(self, other):
        return self | Q._make_must(other)

    def __sub__(self, other):
        return self | Q._make_must_not(self)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((tuple(self.should), tuple(self.must),tuple(self.must_not),
                     self.exrange if hasattr(self, 'exrange') else None,
                     self.inrange if hasattr(self, 'inrange') else None,
                     self.field if hasattr(self, 'field') else None))

    def __str__(self):
        rv = ''
        if hasattr(self, 'field'):
            rv += self.field + ':('
        for o in self.must:
            rv += '+' +  o.__str__() + ''
        for o in self.must_not:
            rv += '-' + o.__str__() + ''
        for o in self.should:
            rv += '' + o.__str__() + ''
        if hasattr(self, '_and'):
            rv += '(' + str(self._and[0]) + ' AND ' + str(self._and[1]) + ')'
        if hasattr(self, '_not'):
            rv += 'NOT ' + str(self._not)
        if hasattr(self, '_or'):
            if hasattr(self._or[0], 'field') or hasattr(self._or[1],
                        'field') or self._or[0].must or self._or[1].must\
                         or self._or[0].must_not or self._or[1].must_not:
                rv += str(self._or[0]) + ' ' + str(self._or[1])
            else:
                rv += '(' + str(self._or[0]) + ' OR ' + str(self._or[1]) + ')'
        if hasattr(self, 'inrange'):
            rv += '[' + str(self.inrange[0]) + ' TO ' + str(self.inrange[1]) + ']'
        if hasattr(self, 'exrange'):
            rv += '{' + str(self.exrange[0]) + ' TO ' + str(self.exrange[1]) + '}'
        if hasattr(self, 'field'):
            rv += ')'
        return rv

    def _check_nested_fields(self):
        stack = []
        stack.extend(self.must)
        stack.extend(self.must_not)
        stack.extend(self.should)
        if hasattr(self, '_and'):
            stack.extend(self._and)
        if hasattr(self, '_not'):
            stack.append(self._not)
        if hasattr(self, '_or'):
            stack.extend(self._or)
        while stack:
            o = stack.pop()
            if not isinstance(o, Q):
                continue
            if hasattr(o, 'field') or o._child_has_field:
                self._child_has_field = True
                if self._has_field:
                    return True
            else:
                stack.extend(o.must)
                stack.extend(o.must_not)
                stack.extend(o.should)
                if hasattr(o, '_and'):
                    stack.extend(o._and)
                if hasattr(o, '_not'):
                    stack.append(o._not)
                if hasattr(o, '_or'):
                    stack.extend(o._or)
        return False
           
    #probably dfs here, build a flag tree as you go so dfs won't be run 100 times

