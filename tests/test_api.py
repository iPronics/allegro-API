import pytest
from allegro import (
    Allegro,
    AllegroConnectionError,
    AllegroError,
    PUCState,
)


@pytest.fixture()
def allegro():
    """Fixture that provides a Allegro instance."""
    allegro = Allegro()
    yield allegro
    allegro.disconnect()


def assert_valid_pucstate_dict(d):
    assert isinstance(d, dict)
    for k, v in d.items():
        assert isinstance(k, int)
        assert isinstance(v, PUCState)


def test_connect(allegro):
    assert allegro.connect() is None


def test_disconnect(allegro):
    assert allegro.disconnect() is None


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
    allegro,
    number,
    couple,
    phase,
):
    with pytest.raises(AllegroConnectionError):
        allegro.set_puc_states({0: PUCState(k=1, phase=2)})
    allegro.connect()
    with pytest.raises(AllegroError):
        allegro.set_puc_states({number: PUCState(k=couple, phase=phase)})


def test_happy_set_puc_states(allegro):
    with pytest.raises(AllegroConnectionError):
        allegro.set_puc_states({2: PUCState(k=0.5, phase=1.0)})
    allegro.connect()
    assert (allegro.set_puc_states({2: PUCState(k=0.5, phase=1.0)})) is None


def test_get_puc_states(allegro):
    with pytest.raises(AllegroConnectionError):
        allegro.get_puc_states()
    allegro.connect()
    a = allegro.get_puc_states()
    assert_valid_pucstate_dict(a)


def test_reset(allegro):
    with pytest.raises(AllegroConnectionError):
        allegro.reset()
    allegro.connect()
    assert allegro.reset() is None


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
def test_interconnect(allegro, inputport, outputport):
    with pytest.raises(AllegroConnectionError):
        allegro.interconnect(inputport, outputport, reset=True)
    allegro.connect()
    with pytest.raises(AllegroError):
        allegro.interconnect(inputport, outputport, reset=True)


def test_happy_interconnect(allegro):
    with pytest.raises(AllegroConnectionError):
        allegro.interconnect(1, 10, reset=True)
    allegro.connect()
    a = allegro.interconnect(1, 10, reset=True)
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
def test_beamsplitter(allegro, inputport, outputport):
    with pytest.raises(AllegroConnectionError):
        allegro.beamsplitter(inputport, outputport, reset=True)
    allegro.connect()
    with pytest.raises(AllegroError):
        allegro.beamsplitter(inputport, outputport, reset=True)


def test_happy_beamsplitter(allegro):
    allegro.connect()
    a = allegro.beamsplitter(0, [10, 18], reset=True)
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
def test_combiner(allegro, inputport, outputport):
    with pytest.raises(AllegroConnectionError):
        allegro.combiner(inputport, outputport, reset=True)
    allegro.connect()
    with pytest.raises(AllegroError):
        allegro.combiner(inputport, outputport, reset=True)


def test_happy_combiner(allegro):
    allegro.connect()
    a = allegro.combiner([10, 18], 0, reset=True)
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
def test_switch(allegro, inputport, outputport, reset):
    with pytest.raises(AllegroConnectionError):
        allegro.switch(inputport, outputport, reset=reset)
    allegro.connect()
    with pytest.raises(AllegroError):
        allegro.switch(inputport, outputport, reset=reset)


def test_happy_switch(allegro):
    allegro.connect()
    a = allegro.switch([1, 2], [10, 12], reset=True)
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
def test_interrogate_fiber(allegro, inputportport, outputport):
    with pytest.raises(AllegroConnectionError):
        allegro.interrogate_fiber(inputportport, outputport)
    allegro.connect()
    with pytest.raises(AllegroError):
        allegro.interrogate_fiber(inputportport, outputport)


def test_happy_interrogate_fiber_1(allegro):
    allegro.connect()
    a = allegro.interrogate_fiber(1, [1, 10])
    assert isinstance(a, dict)
    for k, v in a.items():
        assert isinstance(k, int)
        assert isinstance(v, float)


def test_happy_interrogate_fiber_2(allegro):
    allegro.connect()
    a = allegro.interrogate_fiber(1)
    assert isinstance(a, dict)
    for k, v in a.items():
        assert isinstance(k, int)
        assert isinstance(v, float)


def test_get_temp(allegro):
    with pytest.raises(AllegroConnectionError):
        allegro.get_temp()
    allegro.connect()
    t = allegro.get_temp()
    assert 35 <= t <= 50


def test_output_power(allegro):
    with pytest.raises(AllegroConnectionError):
        allegro.get_output_power([1, 2, 3])
    allegro.connect()
    a = allegro.get_output_power([1, 2, 3])
    assert isinstance(a, dict)
    for k, v in a.items():
        assert k == v


def test_input_power(allegro):
    with pytest.raises(AllegroConnectionError):
        allegro.get_input_power([1, 2, 3])
    allegro.connect()
    a = allegro.get_input_power([1, 2, 3])
    assert isinstance(a, dict)
    for k, v in a.items():
        assert k * 0.1 == v
