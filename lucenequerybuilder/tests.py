<<<<<<< Updated upstream:lucenequerybuilder/tests.py
from lucenequerybuilder import Q
=======
from query import Q
>>>>>>> Stashed changes:querybuilder/tests.py

def test_lol():
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

test_lol()
