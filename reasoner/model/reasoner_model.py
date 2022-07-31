import problog
import pandas as pd

from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable
from problog.logic import Var, Term
from problog.program import SimpleProgram

TRIPLE = Term('triple')

def reasoner_rules(triples, relations):

    query = Term('query')

    for key, value in relations.items():
        if value == 'subclass':
            subclass = Term(str(key))
        elif value == 'type':
            type_ = Term(str(key))
        elif value == 'domain':
            domain_ = Term(str(key))
        elif value == 'range':
            range_ = Term(str(key))
        elif value == 'subproperty':
            subproperty = Term(str(key))
        else:
            pass

    C, C3, C2, C1, X, Y, Z, R, R1, R2, R3 = Var('C'), Var('C3'), Var('C2'), Var('C1'), Var('X'), Var('Y'), Var('Z'), Var('R'), \
                                            Var('R1'), Var('R2'), Var('R3')
    rdfs2 = TRIPLE(X, type_, C) << ( TRIPLE(R, domain_, C) & TRIPLE(X, R, Y) )
    rdfs3 = TRIPLE(Y, type_, C) << ( TRIPLE(R, range_, C) & TRIPLE(X, R, Y) )
    rdfs5 = TRIPLE(R1, subproperty, R3) << ( TRIPLE(R1, subproperty, R2) & TRIPLE(R2, subproperty, R2) )
    rdfs7 = TRIPLE(X, R2, Y) << ( TRIPLE(R1, subproperty, R2) & TRIPLE(X, R1, Y) )
    rdfs9 = TRIPLE(X, type_, C2) << ( TRIPLE(C1, subclass, C2) & TRIPLE(X, type_, C1) )
    rdfs11 = TRIPLE(C1, subclass, C3) << ( TRIPLE(C1, subclass, C2) & TRIPLE(C2, subclass, C3) )

    p = SimpleProgram()

    for t in triples:
        p += t 

    p += rdfs2
    p += rdfs3
    p += rdfs5
    p += rdfs7
    p += rdfs9
    p += rdfs11

    p += query(TRIPLE(X, type_, C))
    p += query(TRIPLE(Y, type_, C))
    p += query(TRIPLE(R1, subproperty, R3))
    p += query(TRIPLE(X, R2, Y))
    p += query(TRIPLE(X, type_, C2))
    p += query(TRIPLE(C1, subclass, C3))

    result = get_evaluatable().create_from(p).evaluate()
    for it in result.items() :
        print ('%s : %s' % (it))

def _read_triple(file_path):
    triples = []
    with open(file_path) as fin:
        for line in fin:
            h, r, t = line.strip().split('\t')
            triples.append(TRIPLE(Term(h), Term(r), Term(t),p=1.0))
    return triples


def _read_relations(file_path):
    rel_dict = {}
    with open(file_path) as fin:
        for line in fin:    
            k,v=line.split(sep=None,maxsplit=1)
            rel_dict[k]=v.rstrip()
    return rel_dict

triples = _read_triple("/Users/karel/Documents/Master/Thesis/Combining-Machine-Learning-with-Reasoning/github/kge-reasoning/reasoner/test/sample/train.del")
relations = _read_relations('/Users/karel/Documents/Master/Thesis/Combining-Machine-Learning-with-Reasoning/github/kge-reasoning/reasoner/test/sample/relation_ids.del')
print(triples)
print(relations)
reasoner_rules(triples, relations)  