import pytest

from src.smartlight.smartlight import AllegroExceptionError, PUCState, Smartlight


sm = Smartlight()


def check_dict_intpucstate(d):
    a = isinstance(d, dict)
    k = list(d.keys())
    v = list(d.values())
    b = (isinstance(i, int) for i in k)
    c = (isinstance(i, PUCState) for i in v)
    return bool(a and b and c)


def test_connect():
    assert sm.connect() is None


def test_disconnect():
    assert sm.disconnect() is None


@pytest.mark.parametrize(
    "n,c,p",
    [
        (100, 0.1, 2),
        (2, 5, 1),
        (2, 0.5, 10),
        ("one", 0.1, 2),
        (2, "one", 1.2),
        (2, 0.2, "one"),
    ],
)
def test_set_puc_states(n, c, p):
    sm.connect()
    with pytest.raises(AllegroExceptionError):
        sm.set_puc_states({n: PUCState(k=c, phase=p)})


def test_happy_set_puc_states():
    sm.connect()
    assert (sm.set_puc_states({2: PUCState(k=0.5, phase=1.0)})) is None


def test_get_puc_states():
    sm.connect()
    a = sm.get_puc_states()
    assert check_dict_intpucstate(a) is True


def test_reset():
    sm.connect()
    assert sm.reset() is None


@pytest.mark.parametrize(
    "i,o",
    [
        (70, 0),
        (0, 70),
        ("one", 0),
        (1, "one"),
        (0, 0),
    ],
)
def test_interconnect(i, o):
    sm.connect()
    with pytest.raises(AllegroExceptionError):
        sm.interconnect(i, o, reset=True)


def test_happy_interconnect():
    sm.connect()
    a = sm.interconnect(1, 10, reset=True)
    assert check_dict_intpucstate(a) is True


@pytest.mark.parametrize(
    "i,o",
    [
        (70, [0, 1]),
        (0, [1, 70]),
        ("one", [0, 1]),
        (0, [0, 1]),
    ],
)
def test_beamsplitter(i, o):
    sm.connect()
    with pytest.raises(AllegroExceptionError):
        sm.beamsplitter(i, o, reset=True)


def test_happy_beamsplitter():
    sm.connect()
    a = sm.beamsplitter(0, [10, 18], reset=True)
    assert check_dict_intpucstate(a) is True


@pytest.mark.parametrize(
    "i,o",
    [
        ([0, 1], 70),
        ([1, 70], 0),
        ([0, 1], "one"),
        ([0, 1], 0),
    ],
)
def test_combiner(i, o):
    sm.connect()
    with pytest.raises(AllegroExceptionError):
        sm.combiner(i, o, reset=True)


def test_happy_combiner():
    sm.connect()
    a = sm.combiner([10, 18], 0, reset=True)
    assert check_dict_intpucstate(a) is True


@pytest.mark.parametrize(
    "i,o,r",
    [
        ([0, 1], [3, 70], False),
        ([70, 0], [3, 5], True),
        ([0, 1], [0, 5], False),
        ([1, 0], [2, 0], True),
    ],
)
def test_switch(i, o, r):
    sm.connect()
    with pytest.raises(AllegroExceptionError):
        sm.switch(i, o, reset=r)


def test_happy_switch():
    sm.connect()
    a = sm.switch([1, 2], [10, 12], reset=True)
    assert check_dict_intpucstate(a) is True


# TODO(Lluís):needed to define parameters
# def test_compensate_dispersion():


@pytest.mark.parametrize(
    "i,o",
    [
        (70, [10, 11]),
        (1, [45, 2]),
    ],
)
def test_interrogate_fiber(i, o):
    sm.connect()
    with pytest.raises(AllegroExceptionError):
        sm.interrogate_fiber(i, o)


def test_happy_interrogate_fiber_1():
    sm.connect()
    a = sm.interrogate_fiber(1, [1, 10])
    assert isinstance(a, dict)
    for k, v in a.items():
        assert isinstance(k, int)
        assert isinstance(v, float)


def test_happy_interrogate_fiber_2():
    sm.connect()
    a = sm.interrogate_fiber(1)
    assert isinstance(a, dict)
    k = list(a.keys())
    for k, v in a.items():
        assert isinstance(k, int)
        assert isinstance(v, float)
