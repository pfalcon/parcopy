import parcopy1
import parcopy2


def CASE(inp, exp):
    return (inp, exp)


test_cases = [
    # Trivial case
    CASE(
        [("a", "b"), ("b", "c")],
        [("a", "b"), ("b", "c")]
    ),
    # Reversed trivial case
    CASE(
        [("b", "c"), ("a", "b")],
        [("a", "b"), ("b", "c")]
    ),
    # Reorder trivial 3-var case
    CASE(
        [("c", "d"), ("b", "c"), ("a", "b")],
        [("a", "b"), ("b", "c"), ("c", "d")]
    ),
    # Self-loop is optimized away
    CASE(
        [("a", "a")],
        []
    ),
    # 2 self-loops
    CASE(
        [("a", "a"), ("b", "b")],
        []
    ),
    # Loop of 2 vars
    CASE(
        [("a", "b"), ("b", "a")],
        [("tmp", "b"), ("b", "a"), ("a", "tmp")]
    ),
    # Reversed loop of 2 vars
    CASE(
        [("b", "a"), ("a", "b")],
        [("tmp", "a"), ("a", "b"), ("b", "tmp")]
    ),
    # Loop of 3 vars
    CASE(
        [("a", "b"), ("b", "c"), ("c", "a")],
        [("tmp", "c"), ("c", "a"), ("a", "b"), ("b", "tmp")]
    ),
    # 2 loops each of 2 vars
    CASE(
        [("a", "b"), ("b", "a"), ("c", "d"), ("d", "c")],
        [("tmp", "d"), ("d", "c"), ("c", "tmp"), ("tmp", "b"), ("b", "a"), ("a", "tmp")]
    ),
]

for inp, exp in test_cases:
    print("i:", inp)
    r1 = parcopy1.sequentialize(inp)
    r2 = parcopy2.sequentialize(inp)
    print("#", r1)
    assert r1 == r2
    assert r1 == exp
    print()


def dup_dest(seq_func):
    try:
        seq_func([("a", "b"), ("b", "c"), ("b", "a")])
        assert 0, "Expected exception"
    except ValueError:
        pass

    r = seq_func([("a", "b"), ("b", "c"), ("b", "a")], filter_dup_dests=True)
    assert r == [("tmp", "b"), ("b", "a"), ("a", "tmp")]


dup_dest(parcopy1.sequentialize)
dup_dest(parcopy2.sequentialize)


def fan_out(seq_func):
    r = seq_func([("b", "a"), ("c", "a")])
    assert r == [("c", "a"), ("b", "c")]

    r = seq_func([("a", "d"), ("b", "a"), ("c", "a"), ("d", "c")])
    assert r == [("b", "a"), ("a", "d"), ("d", "c"), ("c", "b")]

    r = seq_func([("b", "a"), ("c", "b"), ("a", "c"), ("d", "c")])
    assert r == [("d", "c"), ("c", "b"), ("b", "a"), ("a", "d")]


fan_out(parcopy1.sequentialize)
fan_out(parcopy2.sequentialize)
