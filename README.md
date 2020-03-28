Sequentializing Parallel Copies
===============================

In computer science, a parallel copy can be represented as a set of pairs
`a_i = b_i`, with the semantics of value contained in `b_i` to be copied
(or assigned) to `a_i`, all in parallel, where `a_i` and `b_i` are
variables (or memory locations). As most of the actual computer hardware
cannot handle arbitrary parallel copies, there is a problem of
sequentializing parallel copies. Note that the same variable may appear
both as a source and destination in a parallel copy set, which make the
problem somewhat more complex than trivial. A basic example is representing
a variable swap as a parallel copy:

    { a = b, b = a }

Or, using Python-inspired notation:

    a, b = b, a

Intuitively, one can sequentialize parallel copy of size N with either N
single-variable copy statements in the best case, when there's no circular
dependencies among variables, or with N+1 copies and one extra variable
otherwise. Note that there may be multiple dependency cycles, but they can
be handled sequentially, so one extra variable is enough. So, the essence
of the sequentializing algorithm is to find correct and optimal order of
individual copies.

Parallel copies (and their sequentializing) have different applications,
of which we consider two, roughly at the opposite edges of spectrum
regarding generality:

* Converting out of SSA (Static Single Assignment) program representation
  form, specifically resolving Phi functions.
* Optimizing Python multiple assignments.

In SSA form, some basic blocks of a program may start with a set of Phi
functions, like:

    a2 = phi(a0, a1)
    b2 = phi(b0, b1)

When converting out of SSA form, these get replaced with parallel copies
in each of preceding basic block:

    block 1:
    a2, b2 = a0, b0

    block 2:
    a2, b2 = a1, b1

By construction of SSA form, all variables on the right side are distinct.
(Actually, even more, in a freshly constructed SSA form, there're no
interdependencies among variables, and parallel copies are trivially
sequentializable). However, if some transformations are applied on an
SSA program, like copy propagation, this may be no longer true. For
example, some parallel copies can be of a form:

    a2, b2 = a0, a0

In other words, same variable can be copied to more than destination
variable. We call this "fan-out" case. (And independently from that,
interdependencies among variables may appear, not accounting for those
leads to "lost copy" problem of out-of-SSA conversion).

To present next complication, consider following statement:

    a, a = b, c

From the point of view of classical definition of parallel copy, stating
that parallel copy is unordered set of assignments, all occuring in
parallel, the above doesn't make sense: destination `a` gets conflicting
assignments. However, the above is valid Python code with well defined
semantics: assignments are actually ordered, and last assignemt affecting
a variabe "wins".

Based on these examples, we can define consecutively "more general" cases
of parallel copies:

1. The baseline is: unordered set of copies, both sources and destinations
   are mutually distinct among themselves (but again, a source may also be
   a destination, or it's a degenerate case of parallel copy, trivially
   sequentializable by just performing copies in arbitrary order).
2. In "fan-out" case, it's still unordered set, but the same source may
   appear multiple times (i.e. may be assigned to different destinations).
3. In "conflicting assignments" case, same variable may appear multiple
   times as a destination. If we still consider set of copies as unordered,
   we must detect this case and report as an error. Alternatively, copies
   can be considered as an ordered sequence, and last one should prevail.

Algorithms for sequentializing parallel copies are known. But most of them
handle only the baseline case above. This repository provides an
implementation(s) which is extended to handle cases 2 and 3 above (this
handling is configurable, and implementation can be easily "scaled down"
to handle only simpler forms, if more generals forms don't appear in
your application).

References
----------
1. The Parallel Assignment Problem Redefined. Cathy May. IEEE Transactions
   on Software Engineering. Vol. 15, No. 6, June 1989
2. Revisiting Out-of-SSA Translation for Correctness, Code Quality, and
   Efficiency. Benoit Boissinot, Alain Darte, Fabrice Rastello, Benoit
   Dupont de Dinechin, and Christophe Guillon. LIP Research Report RR2008-40.
   2008
3. Towards an SSA based compiler back-end: some interesting properties of
   SSA and its extensions. Benoit Boisinot. PhD Thesis. 30 September 2010
4. [Static Single Assignment Book](http://ssabook.gforge.inria.fr/latest/book-full.pdf).
   Lots of authors. 8 June 2018

[2] contains a typo in the sequentilization algorithm, faithfully copied
to [4]. [3] from the same author however doesn't have it.



(c) Copyright 2020 Paul Sokolovsky, released under the terms of MIT license.
