import pytest
from smartlight import (
    AllegroConnectionError,
    AllegroError,
    PUCState,
    Smartlight,
)


@pytest.fixture()
def smartlight():
    """Fixture that provides a Smartlight instance."""
    smartlight = Smartlight()
    yield smartlight
    smartlight.disconnect()


def assert_valid_pucstate_dict(d):
    assert isinstance(d, dict)
    for k, v in d.items():
        assert isinstance(k, int)
        assert isinstance(v, PUCState)


def test_connect(smartlight):
    assert smartlight.connect() is None


def test_disconnect(smartlight):
    assert smartlight.disconnect() is None


@pytest.mark.parametrize(
    "n,c,p",
    [
        (100, 0.1, 2),
        (2, 5, 1),
        ("one", 0.1, 2),
        (2, "one", 1.2),
        (2, 0.2, "one"),
    ],
)
def test_set_puc_states(smartlight, n, c, p):
    with pytest.raises(AllegroConnectionError):
        smartlight.set_puc_states({0: PUCState(k=1, phase=2)})
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.set_puc_states({n: PUCState(k=c, phase=p)})


def test_happy_set_puc_states(smartlight):
    with pytest.raises(AllegroConnectionError):
        smartlight.set_puc_states({2: PUCState(k=0.5, phase=1.0)})
    smartlight.connect()
    assert (smartlight.set_puc_states({2: PUCState(k=0.5, phase=1.0)})) is None


def test_get_puc_states(smartlight):
    with pytest.raises(AllegroConnectionError):
        smartlight.get_puc_states()
    smartlight.connect()
    a = smartlight.get_puc_states()
    assert_valid_pucstate_dict(a)


def test_reset(smartlight):
    with pytest.raises(AllegroConnectionError):
        smartlight.reset()
    smartlight.connect()
    assert smartlight.reset() is None


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
def test_interconnect(smartlight, i, o):
    with pytest.raises(AllegroConnectionError):
        smartlight.interconnect(i, o, reset=True)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.interconnect(i, o, reset=True)


def test_happy_interconnect(smartlight):
    with pytest.raises(AllegroConnectionError):
        smartlight.interconnect(1, 10, reset=True)
    smartlight.connect()
    a = smartlight.interconnect(1, 10, reset=True)
    assert_valid_pucstate_dict(a)


@pytest.mark.parametrize(
    "i,o",
    [
        (70, [0, 1]),
        (0, [1, 70]),
        ("one", [0, 1]),
        (0, [0, 1]),
    ],
)
def test_beamsplitter(smartlight, i, o):
    with pytest.raises(AllegroConnectionError):
        smartlight.beamsplitter(i, o, reset=True)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.beamsplitter(i, o, reset=True)


def test_happy_beamsplitter(smartlight):
    smartlight.connect()
    a = smartlight.beamsplitter(0, [10, 18], reset=True)
    assert_valid_pucstate_dict(a)


@pytest.mark.parametrize(
    "i,o",
    [
        ([0, 1], 70),
        ([1, 70], 0),
        ([0, 1], "one"),
        ([0, 1], 0),
    ],
)
def test_combiner(smartlight, i, o):
    with pytest.raises(AllegroConnectionError):
        smartlight.combiner(i, o, reset=True)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.combiner(i, o, reset=True)


def test_happy_combiner(smartlight):
    smartlight.connect()
    a = smartlight.combiner([10, 18], 0, reset=True)
    assert_valid_pucstate_dict(a)


@pytest.mark.parametrize(
    "i,o,r",
    [
        ([0, 1], [3, 70], False),
        ([70, 0], [3, 5], True),
        ([0, 1], [0, 5], False),
        ([1, 0], [2, 0], True),
    ],
)
def test_switch(smartlight, i, o, r):
    with pytest.raises(AllegroConnectionError):
        smartlight.switch(i, o, reset=r)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.switch(i, o, reset=r)


def test_happy_switch(smartlight):
    smartlight.connect()
    a = smartlight.switch([1, 2], [10, 12], reset=True)
    assert_valid_pucstate_dict(a)


# TODO(Lluís):needed to define parameters
# def test_compensate_dispersion():


@pytest.mark.parametrize(
    "i,o",
    [
        (70, [10, 11]),
        (1, [45, 2]),
    ],
)
def test_interrogate_fiber(smartlight, i, o):
    with pytest.raises(AllegroConnectionError):
        smartlight.interrogate_fiber(i, o)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.interrogate_fiber(i, o)


def test_happy_interrogate_fiber_1(smartlight):
    smartlight.connect()
    a = smartlight.interrogate_fiber(1, [1, 10])
    assert isinstance(a, dict)
    for k, v in a.items():
        assert isinstance(k, int)
        assert isinstance(v, float)


def test_happy_interrogate_fiber_2(smartlight):
    smartlight.connect()
    a = smartlight.interrogate_fiber(1)
    assert isinstance(a, dict)
    for k, v in a.items():
        assert isinstance(k, int)
        assert isinstance(v, float)
