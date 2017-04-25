import numpy as np
from itertools import cycle, islice
from operator import itemgetter
from bolt.io import BinaryDataset

class MISelector(object):
    """Selects pivots according to mutual information.

    If the number of classes is larger than 2 than it creates `num classes` binary rankings - one-vs-all. Then, it selects the top ranks in a round robin fashion until a total of `k` pivots are selected.
    """

    def select(self, ds, preselection = None):
        if len(ds.classes) > 2:
            res = self.select_multi(ds, preselection)
        else:
            res = self.select_binary(ds, preselection)
        return res

    def select_multi(self, ds, preselection = None):
        fxset = set()
        rankings = []
        for c in ds.classes:
            bs = BinaryDataset(ds, c)
            _tmp = mutualinformation(bs, preselection)
            # print _tmp
            rankings.append(_tmp)

        for idx in roundrobin(*rankings):
            if idx not in fxset:
                fxset.add(idx)
                yield idx

    def select_binary(self, ds, preselection = None):
        return mutualinformation(ds, preselection)

def mutualinformation(bs, preselection = None):
    """Computes mutual information of each column of `docterms` and `labels`.
    Returns the indices of the top `k` columns according to MI.
    """
    N = 0
    N_pos = sum([1 for y in bs.iterlabels() if y == 1.0])
    N_neg = bs.n - N_pos
    N_term = {}
    POS = 1
    NEG = 2
    TOTAL = 0

    for doc, label in bs:
        for term, freq in doc:
            if freq == 0.0: continue
            term_stats = N_term.get(term, np.zeros((3,), dtype = int))
            if label == 1.0:
                term_stats[POS] += 1
            else:
                term_stats[NEG] += 1
            term_stats[TOTAL] += 1
            N_term[term] = term_stats
        N += 1

    mi = {}

    N += 2  # account for pseudo counts
    for term in N_term:
        term_stats = N_term[term]
        N_11 = term_stats[POS] + 1
        N_10 = term_stats[NEG] + 1
        N_01 = 1 + N_pos - N_11
        N_00 = 1 + N_neg - N_10
        N_1_ = term_stats[TOTAL] + 2
        assert (N_11 + N_10) == N_1_
        N_0_ = N - N_1_

        a = (float(N_11) / N) * np.log2(float(N * N_11) / (N_1_ * N_pos))
        b = (float(N_01) / N) * np.log2(float(N * N_01) / (N_0_ * N_pos))
        c = (float(N_10) / N) * np.log2(float(N * N_10) / (N_1_ * N_neg))
        d = (float(N_00) / N) * np.log2(float(N * N_00) / (N_0_ * N_neg))

        mi[term] = a + b + c + d

    mi = sorted(mi.items(), key = itemgetter(1))
    mi.reverse()
    if preselection != None:
        preselection = set(preselection)
        return (i for i, v in mi if i in preselection)
    else:
        return (i for i, v in mi)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))
