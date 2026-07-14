# Vendored from https://github.com/potassco/guess_and_check (commit ac92d8e),
# combined into a single module and reduced to the code used by anthem-cx:
# only the reification via a clingo observer is kept, dropping the command line
# interface and the reification via the clingo binary or a translation to SAT.
# The remaining code is unchanged, except for the removal of the `binary` and
# `toSat` parameters of solve_guess_and_check(), which selected the dropped
# reifications.
#
# The meta encoding metaD_program below is metaD.lp from clingo (MIT,
# Copyright 2017 Roland Kaminski), see
# https://github.com/potassco/clingo/blob/master/examples/reify/common/metaD.lp
#
# MIT License
#
# Copyright (c) 2017 Javier Romero
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -*- coding: utf-8 -*-

#
# IMPORTS
#

import clingo
import re

#
# DEFINES
#

HOLDS = "holds"
ANSWER = """\
Answer {}:
{}"""
BINDING_PYTHON = """
##true(atom(A)) :-     holds(X), ##output(holds(X),A).
##fail(atom(A)) :- not holds(X), ##output(holds(X),A).
:- not ##bot.
"""

metaD_program = """

% NOTE: assumes that a rule has no more than one head

##sum(B,G,T) :- ##rule(_,sum(B,G)), T = #sum { W,L : ##weighted_literal_tuple(B,L,W) }.

% extract supports of atoms and facts

##supp(A,B) :- ##rule(     choice(H),B), ##atom_tuple(H,A).
##supp(A,B) :- ##rule(disjunction(H),B), ##atom_tuple(H,A).

##supp(A) :- ##supp(A,_).

##atom(|L|) :- ##weighted_literal_tuple(_,L,_).
##atom(|L|) :- ##literal_tuple(_,L).
##atom( A ) :- ##atom_tuple(_,A).

##fact(A) :- ##rule(disjunction(H),normal(B)), ##atom_tuple(H,A), not ##literal_tuple(B,_).

% generate interpretation

##true(atom(A))                :- ##fact(A).
##true(atom(A)); ##fail(atom(A)) :- ##supp(A), not ##fact(A).
                 ##fail(atom(A)) :- ##atom(A), not ##supp(A).

##true(normal(B)) :- ##literal_tuple(B),
    ##true(atom(L)) : ##literal_tuple(B, L), L > 0;
    ##fail(atom(L)) : ##literal_tuple(B,-L), L > 0.
##fail(normal(B)) :- ##literal_tuple(B, L), ##fail(atom(L)), L > 0.
##fail(normal(B)) :- ##literal_tuple(B,-L), ##true(atom(L)), L > 0.

##true(sum(B,G)) :- ##sum(B,G,T),
    #sum { W,L : ##true(atom(L)), ##weighted_literal_tuple(B, L,W), L > 0 ;
           W,L : ##fail(atom(L)), ##weighted_literal_tuple(B,-L,W), L > 0 } >= G.
##fail(sum(B,G)) :- ##sum(B,G,T),
    #sum { W,L : ##fail(atom(L)), ##weighted_literal_tuple(B, L,W), L > 0 ;
           W,L : ##true(atom(L)), ##weighted_literal_tuple(B,-L,W), L > 0 } >= T-G+1.

% verify supported model properties

##bot :- ##rule(disjunction(H),B), ##true(B), ##fail(atom(A)) : ##atom_tuple(H,A).
##bot :- ##true(atom(A)), ##fail(B) : ##supp(A,B).

% verify acyclic derivability

##internal(C,normal(B)) :- ##scc(C,A), ##supp(A,normal(B)), ##scc(C,A'), ##literal_tuple(B,A').
##internal(C,sum(B,G))  :- ##scc(C,A), ##supp(A,sum(B,G)),  ##scc(C,A'), ##weighted_literal_tuple(B,A',W).

##external(C,normal(B)) :- ##scc(C,A), ##supp(A,normal(B)), not ##internal(C,normal(B)).
##external(C,sum(B,G))  :- ##scc(C,A), ##supp(A,sum(B,G)),  not ##internal(C,sum(B,G)).

##steps(C,Z-1) :- ##scc(C,_), Z = { ##scc(C,A) : not ##fact(A) }.

##wait(C,atom(A),0)   :- ##scc(C,A), ##fail(B) : ##external(C,B), ##supp(A,B).
##wait(C,normal(B),I) :- ##internal(C,normal(B)), ##fail(normal(B)), ##steps(C,Z), I = 0..Z-1.
##wait(C,normal(B),I) :- ##internal(C,normal(B)), ##literal_tuple(B,A), ##wait(C,atom(A),I), ##steps(C,Z), I < Z.
##wait(C,sum(B,G),I)  :- ##internal(C,sum(B,G)), ##steps(C,Z), I = 0..Z-1, ##sum(B,G,T),
    #sum { W,L :   ##fail(atom(L)),   ##weighted_literal_tuple(B, L,W), L > 0, not ##scc(C,L) ;
           W,L : ##wait(C,atom(L),I), ##weighted_literal_tuple(B, L,W), L > 0,     ##scc(C,L) ;
           W,L :   ##true(atom(L)),   ##weighted_literal_tuple(B,-L,W), L > 0               } >= T-G+1.
##wait(C,atom(A),I)   :- ##wait(C,atom(A),0), ##steps(C,Z), I = 1..Z, ##wait(C,B,I-1) : ##supp(A,B), ##internal(C,B).

##bot :- ##scc(C,A), ##true(atom(A)), ##wait(C,atom(A),Z), ##steps(C,Z).

% saturate interpretations that are not answer sets

##true(atom(A)) :- ##supp(A), not ##fact(A), ##bot.
##fail(atom(A)) :- ##supp(A), not ##fact(A), ##bot.

%
% added by Javier
%

%#show.
%#show T : ##output(T,L), ##true(atom(L)).
#defined ##literal_tuple/1.
#defined ##literal_tuple/2.
#defined ##rule/2.
#defined ##atom_tuple/2.
#defined ##weighted_literal_tuple/3.
#defined ##scc/2.
"""


#
# classes Node and Graph used by reify_from_observer()
#

# by Roland Kaminski, modified by Javier Romero
class Node:

    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.visited_  = 0
        self.finished_ = 1

    def add_neighbor(self, neighbor): self.neighbors.append(neighbor)
    def get_neighbors(self): return self.neighbors
    def next_neighbors(self): return self.neighbors[self.finished_ - 1:]

    def visit(self, visited): self.visited_ = visited + 1
    def visited(self): return self.visited_ - 1

    def mark(self): self.visited_ = 1
    def marked(self): return self.visited_ >= 1

    def pop(self): self.finished_ = 0
    def popped(self): return self.finished_ == 0
    def inc_finished(self): self.finished_ += 1


# by Roland Kaminski, modified by Javier Romero
class Graph:

    def __init__(self):
        self.graph = {}
        self.sccs = []
        self.singletons = set()

    def add_edge(self, head, body):
        if head == body:
            self.singletons.add(head)
            return
        node = self.graph.get(head, None)
        if not node:
            node = Node(head)
            self.graph[head] = node
        node.add_neighbor(body)

    def reify_sccs(self, prefix=""):
        # compute sccs and update self.singletons
        for _, v in self.graph.items():
            if not v.marked():
                self.tarjan(v)
        # return string
        out = ""
        for idx, item in enumerate(list(self.singletons) + self.sccs):
            out += " ".join(["{}scc({},{}).".format(prefix, idx, i) for i in item]) + "\n"
        return out

    # private
    def next(self, v):
        for y in v.next_neighbors():
            v.inc_finished()
            node = self.graph.get(y, None)
            if node and not node.marked():
                return node
        return None

    # private
    def root(self, v):
        root = True
        for y in v.get_neighbors():
            node = self.graph.get(y, None)
            if node and not node.popped() and node.visited() < v.visited():
                root = False
                v.visit(node.visited())
        return root

    # private
    def tarjan(self, start):

        s, t = [], []
        visited = 0
        s.append(start)
        start.mark()

        def top(s): return s[-1]

        while len(s) > 0:
            x = top(s)
            if x.visited() == 0:
                visited  += 1
                x.visit(visited)
            y = self.next(x)
            if y != None:
                s.append(y)
                y.mark()
            else:
                s.pop()
                if self.root(x):
                    scc = [x.name]
                    x.pop()
                    while len(t) > 0 and top(t).visited() >= x.visited():
                        y = t.pop()
                        y.pop()
                        scc.append(y.name)
                        self.singletons.discard(y.name) # update self.singletons
                    if len(scc)>1:
                        self.sccs.append(scc)           # update self.sccs
                        self.singletons.discard(x.name) # update self.singletons
                else: t.append(x)


#
# reify_from_observer()
#
# * uses a clingo observer with fields:
#   - rules
#   - weight_rules
#   - output_atoms
#   - output_terms
#

def reify_from_observer(observer, prefix=""):

    # start
    out = ""
    literal_tuple, wliteral_tuple, atom_tuple = 1, 1, 1
    p = prefix

    # fact 0
    # out += "% fact 0\n"
    out += "{}rule(disjunction(0),normal(0)). ".format(p)
    out += "{}atom_tuple(0,0). {}literal_tuple(0).\n\n".format(p, p)

    # start graph
    graph = Graph()

    # normal rules
    for choice, head, body in observer.rules:

        # out += "% normal rule\n"
        # body
        if body:
            out += "{}literal_tuple({}).".format(p, literal_tuple) + "\n"
            out += " ".join([
                "{}literal_tuple({},{}).".format(p, literal_tuple, l)
                for l in body
            ]) + "\n"
        # head
        head_type = "choice" if choice else "disjunction"
        out += "{}rule({}({}),normal({})).".format(
            p, head_type, atom_tuple, literal_tuple if body else 0
        ) + "\n"
        out += " ".join([
            "{}atom_tuple({},{}).".format(p, atom_tuple, l) for l in head
        ]) + "\n\n"
        # update counters
        if body:
            literal_tuple += 1
        atom_tuple += 1
        # update graph (this can be interwined with the rules above)
        for l in body:
            if l >= 0:
                for atom in head:
                    graph.add_edge(atom, l)

    # weight rules
    for choice, head, lower_bound, body in observer.weight_rules:
        # out += "% weighted rule\n"
        # body
        out += " ".join([
            "{}weighted_literal_tuple({},{},{}).".format(
                p, wliteral_tuple, l, w
            ) for l, w in body
        ]) + "\n"
        # head
        head_type = "choice" if choice else "disjunction"
        out += "{}rule({}({}),sum({},{})).".format(
            p, head_type, atom_tuple, wliteral_tuple, lower_bound
        ) + "\n"
        out += " ".join([
            "{}atom_tuple({},{}).".format(p, atom_tuple, l) for l in head
        ]) + "\n\n"
        # update counters
        wliteral_tuple += 1
        atom_tuple += 1
        # update graph (this can be interwined with the rules above)
        for l, w in body:
            if l >= 0:
                for atom in head:
                    graph.add_edge(atom, l)

    # sccs
    # out += "% sccs\n"
    out += graph.reify_sccs(p) + "\n"

    # output atoms
    # out += "% output atoms\n"
    for symbol, atom in observer.output_atoms:
        out += "{}output({},{}).\n".format(p, symbol, atom)

    # output terms
    # out += "% output term\n"
    for symbol, condition in observer.output_terms:
        out += "{}output_term({}).\n".format(p, symbol) + "\n"
        out += " ".join([
            "{}output_term({},{}).".format(p, symbol, l) for l in condition
        ]) + "\n"

    return out


#
# METHODS
#


class Observer:

    def __init__(self):
        self.rules = []
        self.weight_rules = []
        self.output_atoms = []
        self.output_terms = []

    def rule(self, choice, head, body):
        self.rules.append((choice, head, body))

    def weight_rule(self, choice, head, lower_bound, body):
        self.weight_rules.append((choice, head, lower_bound, body))

    def output_atom(self, symbol, atom):
        self.output_atoms.append((symbol, atom))

    def output_term(self, symbol, condition):
        self.output_terms.append((symbol, condition))


def observe(program):
    observer = Observer()
    control = clingo.Control(["--warn=no-atom-undefined"])
    control.register_observer(observer, replace=True)
    control.add("base", [], program)
    control.ground([("base", [])])
    return observer


def get_prefix(control):
    prefix = "_"
    for name, _, _ in control.symbolic_atoms.signatures:
        if name.startswith(prefix):
            prefix = re.sub(r"(_+).*", r"\1", name) + "_"
    return prefix


def solve_guess_and_check(options, guess_files, check_files, on_model=None) -> bool:
    """
    Solve a guess and check program and return whether it is satisfiable.
    """
    control = clingo.Control(options)

    # load guess and ground
    for _file in guess_files:
        control.load(_file)
    control.ground([("base", [])])

    # get choices
    choices = (
        "{ "
        + "; ".join(
            str(atom.symbol) for atom in control.symbolic_atoms.by_signature(HOLDS, 1)
        )
        + " }."
    )
    choices = "" if choices == "{  }." else choices

    # create check
    check = choices + "\n#show holds/1.\n"
    for _file in check_files:
        with open(_file, "r") as f:
            check += f.read() + "\n"

    # fix prefix
    prefix = get_prefix(control)

    # reify check
    observer = observe(check)
    check_reified = reify_from_observer(observer, prefix)
    check_reified += BINDING_PYTHON.replace("##", prefix)
    # add meta encoding
    check_reified += metaD_program.replace("##", prefix)

    # add to control and ground
    control.add("check", [], check_reified)
    control.ground([("check", [])])

    # solve
    models = 0
    with control.solve(yield_=True, on_model=on_model) as handle:
        for m in handle:
            models += 1
            if not on_model:
                model = " ".join([str(x) for x in m.symbols(shown=True)])
                print(ANSWER.format(models, model))
        if not on_model:
            print(handle.get())

    return models > 0
