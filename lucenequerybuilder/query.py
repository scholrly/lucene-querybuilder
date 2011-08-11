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
        self._and = None
        self._or = None
        self._not = None
        self.inrange = None
        self.exrange = None
        self._child_has_field = False
        self.field = None
        if len(args) == 1 and not kwargs:
            if isinstance(args[0], Q):
                if args[0].fielded:
                    self._child_has_field = True
                self.should.append(args[0])
            else:
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
        elif len(args) == 2:
            if Q._check_whitespace(args[0]):
                raise ValueError('No whitespace allowed in field names.')
            self.field = args[0]
            if isinstance(args[1], Q):
                if args[1].fielded:
                    raise ValueError('No nested fields allowed.')
                self.should.append(args[1])
            else:
                if Q._check_whitespace(args[1]):
                    self.should.append('"'+self._escape(args[1])+'"')
                else:
                    self.should.append(self._escape(args[1]))

    @property
    def fielded(self):
        return self.field is not None or\
                any(Q._has_field(l) for l in [self.must, self.must_not,
                                              self.should, self._and, self._or,
                                              self._not])
    @staticmethod
    def _has_field(val):
        if hasattr(val, '__iter__'):
            return any(Q._has_field(t) for t in val)
        else:
            return hasattr(val, 'field') and val.field is not None


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
        q._and = (q1, q2)
        return q

    def _make_not(q1):
        q = Q()
        q._not = q1
        return q

    def _make_or(q1, q2):
        q = Q()
        q._or = (q1, q2)
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
                     self.exrange, self.inrange, self.field))

    def __str__(self):
        rv = ''
        for o in self.must:
            rv += '+' + str(o)
        for o in self.must_not:
            rv += str(o)
        for o in self.should:
            rv += str(o)
        if self._and is not None:
            rv += '(' + str(self._and[0]) + ' AND ' + str(self._and[1]) + ')'
        if self._not is not None:
            rv += 'NOT ' + str(self._not)
        if self._or is not None:
            if self._or[0].field is not None or self._or[1].field is not None\
               or self._or[0].must or self._or[1].must or self._or[0].must_not\
               or self._or[1].must_not:
                rv += str(self._or[0]) + ' ' + str(self._or[1])
            else:
                rv += '(' + str(self._or[0]) + ' OR ' + str(self._or[1]) + ')'
        if self.inrange is not None:
            rv += '[' + str(self.inrange[0]) + ' TO ' + str(self.inrange[1]) + ']'
        if self.exrange is not None:
            rv += '{' + str(self.exrange[0]) + ' TO ' + str(self.exrange[1]) + '}'
        if self.field is not None:
            rv = '{0}:({1})'.format(self.field, rv)
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

