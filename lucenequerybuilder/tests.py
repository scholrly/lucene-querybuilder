"""
Simple tests for Q. In the future, comparing output to an actual Lucene index
would be a good idea.
"""

from lucenequerybuilder import Q
from nose.tools import eq_

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
    assert str(q1) == '('+a+' OR '+b+')', str(q1)
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

    q4 = Q('field', inrange=(1,2))
    q5 = Q('field', inrange=(1,3))
    assert q4 != q5
    assert hash(q4) != hash(q5)

def test_field_restrictions():
    q1 = Q('field', 'test query')
    assert q1.fielded

    q2 = Q('a') & q1
    assert q2.fielded

    try:
        Q('another_field', q2)
    except:
        pass
    else:
        raise AssertionError('Query allowed nested fields, which are invalid.')

def test_fuzzy():
    eq_(str(Q(fuzzy='fuzzi')), 'fuzzi~')

    try:
        Q(fuzzy='test fuzz')
    except:
        pass
    else:
        raise AssertionError("Fuzzy queries shouldn't have whitespace.")

    eq_(str(Q(fuzzy=('fuzzi', .2))), 'fuzzi~0.200')
    eq_(str(Q('field', fuzzy='fuzzi')), 'field:(fuzzi~)')

def test_wildcard():
    eq_(str(Q('lol*', wildcard=True)), 'lol*')
    eq_(str(Q('field_with_*', 'some query')), 'field_with_*:("some query")')
    eq_(str(Q('field_with_*', 'some*query', wildcard=True)), 'field_with_*:(some*query)')
