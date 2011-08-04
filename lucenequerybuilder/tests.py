"""
Simple tests for Q. In the future, comparing output to an actual Lucene index
would be a good idea.
"""

from lucenequerybuilder import Q

def test_general():
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd d'
    e = 'e'
    f = 'f'
    g = 1
    h = 5
    q1 = Q(a) | Q(b)
    assert str(q1) == '('+a+' OR '+b+')'
    q2 = Q(c) & q1
    assert str(q2) == '('+c+' AND ('+a+' OR '+b+'))'
    q3 = +Q(a) +Q(b) | Q(f, Q(c) & ~Q(Q(d) | Q(e)))
    assert str(q3) == '+'+a+' +'+b+' '+f+':(('+c+' AND NOT '+'("'+d+'" OR '+e+')))'
    q4 = Q(a,b) | Q(c, Q(d) & Q(e)) | Q(f, +Q(inrange=(g,h)) | Q(h))
    assert str(q4) == a+':('+b+') '+c+':(("'+d+'" AND '+e+')) '+f+':(+['+str(g)+' TO '+str(h)+'] '+str(h)+')'
    try:
        q5 = Q(a, Q(b, Q(c, d) & Q(e)) | Q(f))
    except:
        pass
    else:
        raise AssertionError("Shouldn't allow nested fields.")

def test_simple_term():
    query_string = str(Q('a'))
    assert query_string == 'a', query_string

def test_simple_phrase():
    query_string = str(Q('abc 123'))
    assert query_string == '"abc 123"', query_string

def test_hashing():
    q1 = Q('a') & Q('b') | Q('c')
    q2 = Q('a') & Q('b') | Q('c')
    q3 = q1 | Q('d')

    assert q1 == q2, "Queries aren't being properly evaluated for equality."
    assert q2 != q3, "Queries aren't being properly evaluated for inequality."

    d = {}
    try:
        d[q1] = 1
        d[q2] = 2
    except:
        raise AssertionError('There was an error using queries as dict keys.')
    assert d[q2] == 2, 'Got the wrong value back from the query dict!'


#this test doesn't work, but might be worth rewriting
#
#def test_escaping():
#    """ Tests basic character escaping. Doesn't test double char escape, eg &&, ||."""
#    special_lucene_chars = r'\+-!(){}[]^"~*?:'
#    unescaped_regex = '|'.join([r'(([^\\]|^)%s)' % re.escape(c) for c in special_lucene_chars])
#    unescaped_regex = re.compile(unescaped_regex)
#    #test the regex
#    assert unescaped_regex.match(r'\ [ )') is not None
#    query_string = str(Q(':') & Q('\\'))
#    #this won't work, dur
#    assert not unescaped_regex.match(query_string), query_string
