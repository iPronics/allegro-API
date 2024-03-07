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
    ("number", "couple", "phase"),
    [
        (100, 0.1, 2),
        (2, 5, 1),
        ("one", 0.1, 2),
        (2, "one", 1.2),
        (2, 0.2, "one"),
    ],
)
def test_set_puc_states(
    smartlight,
    number,
    couple,
    phase,
):
    with pytest.raises(AllegroConnectionError):
        smartlight.set_puc_states({0: PUCState(k=1, phase=2)})
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.set_puc_states({number: PUCState(k=couple, phase=phase)})


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
    ("inputport", "outputport"),
    [
        (70, 0),
        (0, 70),
        ("one", 0),
        (1, "one"),
        (0, 0),
    ],
)
def test_interconnect(smartlight, inputport, outputport):
    with pytest.raises(AllegroConnectionError):
        smartlight.interconnect(inputport, outputport, reset=True)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.interconnect(inputport, outputport, reset=True)


def test_happy_interconnect(smartlight):
    with pytest.raises(AllegroConnectionError):
        smartlight.interconnect(1, 10, reset=True)
    smartlight.connect()
    a = smartlight.interconnect(1, 10, reset=True)
    assert_valid_pucstate_dict(a)


@pytest.mark.parametrize(
    ("inputport", "outputport"),
    [
        (70, [0, 1]),
        (0, [1, 70]),
        ("one", [0, 1]),
        (0, [0, 1]),
    ],
)
def test_beamsplitter(smartlight, inputport, outputport):
    with pytest.raises(AllegroConnectionError):
        smartlight.beamsplitter(inputport, outputport, reset=True)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.beamsplitter(inputport, outputport, reset=True)


def test_happy_beamsplitter(smartlight):
    smartlight.connect()
    a = smartlight.beamsplitter(0, [10, 18], reset=True)
    assert_valid_pucstate_dict(a)


@pytest.mark.parametrize(
    ("inputport", "outputport"),
    [
        ([0, 1], 70),
        ([1, 70], 0),
        ([0, 1], "one"),
        ([0, 1], 0),
    ],
)
def test_combiner(smartlight, inputport, outputport):
    with pytest.raises(AllegroConnectionError):
        smartlight.combiner(inputport, outputport, reset=True)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.combiner(inputport, outputport, reset=True)


def test_happy_combiner(smartlight):
    smartlight.connect()
    a = smartlight.combiner([10, 18], 0, reset=True)
    assert_valid_pucstate_dict(a)


@pytest.mark.parametrize(
    ("inputport", "outputport", "reset"),
    [
        ([0, 1], [3, 70], False),
        ([70, 0], [3, 5], True),
        ([0, 1], [0, 5], False),
        ([1, 0], [2, 0], True),
    ],
)
def test_switch(smartlight, inputport, outputport, reset):
    with pytest.raises(AllegroConnectionError):
        smartlight.switch(inputport, outputport, reset=reset)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.switch(inputport, outputport, reset=reset)


def test_happy_switch(smartlight):
    smartlight.connect()
    a = smartlight.switch([1, 2], [10, 12], reset=True)
    assert_valid_pucstate_dict(a)


# TODO(Lluís):needed to define parameters
# def test_compensate_dispersion():


@pytest.mark.parametrize(
    ("inputportport", "outputport"),
    [
        (70, [10, 11]),
        (1, [45, 2]),
    ],
)
def test_interrogate_fiber(smartlight, inputportport, outputport):
    with pytest.raises(AllegroConnectionError):
        smartlight.interrogate_fiber(inputportport, outputport)
    smartlight.connect()
    with pytest.raises(AllegroError):
        smartlight.interrogate_fiber(inputportport, outputport)


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


def test_get_temp(smartlight):
    with pytest.raises(AllegroConnectionError):
        smartlight.get_temp()
    smartlight.connect()
    t = smartlight.get_temp()
    assert 35 <= t <= 50


def test_output_power(smartlight):
    with pytest.raises(AllegroConnectionError):
        smartlight.get_output_power([1, 2, 3])
    smartlight.connect()
    a = smartlight.get_output_power([1, 2, 3])
    assert isinstance(a, dict)
    assert set(a.keys()) & set(a.values())


def test_input_power(smartlight):
    with pytest.raises(AllegroConnectionError):
        smartlight.get_input_power([1, 2, 3])
    smartlight.connect()
    a = smartlight.get_input_power([1, 2, 3])
    assert isinstance(a, dict)
    assert (b == c * 0.1 for b, c in zip(a.keys(), a.values(), strict=False))
