from lucenequerybuilder import Q

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
    print repr(str(q1))
    assert str(q1) == '('+a+' OR '+b+')'
    q2 = Q(c) & q1
    print q2
    assert str(q2) == '('+c+' AND ('+a+' OR '+b+'))'
    q3 = +Q(a) | +Q(b) | Q(f, Q(c) & ~Q(Q(d) | Q(e)))
    print q3
    assert str(q3) == '+'+a+' +'+b+' '+f+':(('+c+' AND NOT '+'("'+d+'" OR '+e+')))'
    q4 = Q(a,b) | Q(c, Q(d) & Q(e)) | Q(f, +Q(inrange=(g,h)) | Q(h))
    print q4
    assert str(q4) == a+':('+b+') '+c+':(("'+d+'" AND '+e+')) '+f+':(+['+str(g)+' TO '+str(h)+'] '+str(h)+')'
    try:
        q5 = Q(a, Q(b, Q(c, d) & Q(e)) | Q(f))
    except:
        pass
    else:
        raise AssertionError("Shouldn't allow nested fields.")

test_lol()
