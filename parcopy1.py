# Based on Algorithm 13 from Benoit Boisinot's thesis, with fixes and
# extensions by Paul Sokolovsky.

import logging


log = logging.getLogger(__name__)


def sequentialize(copies, filter_dup_dests=False, allow_fan_out=True):
    # If filter_dup_dests is True, consider pairs ordered, and if multiple
    # pairs have the same dest var, the last one takes effect. Otherwise,
    # such duplicate dest vars is an error.
    if filter_dup_dests:
        # If there're multiple assignments to the same var, keep only the latest
        copies = list(dict(copies).items())

    available = []
    to_do = []
    pred = {}
    resource = {}
    res = []

    def emit_copy(a, b):
        #print("%s <- %s" % (b, a))
        res.append((b, a))

    for b, a in copies:
        resource[b] = None

    for b, a in copies:
        resource[a] = a
        pred[b] = a

        # Extra check
        if not filter_dup_dests:
            if b in to_do:
                raise ValueError("Conflicting assignments to destination %s, latest: %s" % (b, (b, a)))

        to_do.append(b)

    for b, a in copies:
        if resource[b] is None:
            available.append(b)

    log.debug("resource: %s", resource)
    log.debug("pred: %s", pred)
    log.debug("available: %s", available)
    log.debug("to_do: %s", to_do)

    while to_do:
        while available:
            b = available.pop()
            log.debug("* avail %s", b)
            if b not in pred:
                continue
            a = resource[pred[b]]
            emit_copy(a, b)

            # Addition by Paul Sokolovsky to handle fan-out case (when same
            # source is assigned to multiple destinations).
            if allow_fan_out and a in to_do:
                to_do.remove(a)

            resource[pred[b]] = b
            if pred[b] == a:
                available.append(a)

        # Addition to handle fan-out.
        if allow_fan_out and not to_do:
            break

        b = to_do.pop()
        log.debug("* to_do %s", b)
        if b != resource[pred[b]]:
            emit_copy(b, "tmp")
            resource[b] = "tmp"
            available.append(b)

    return res