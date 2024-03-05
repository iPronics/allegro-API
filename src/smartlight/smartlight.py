"""API for Allegro project."""

from dataclasses import dataclass
from math import pi
from random import random, uniform
from typing import Optional


@dataclass
class PUCState:
    """Object to store PUCs attributes."""

    k: float = 1.0
    phase: float = 0.0


class AllegroExceptionError(Exception):
    """General Exception for this app."""


NUM_CHANNELS = 35
NUM_PUCS = 71
NUM_PORTS = 60
CONN_MSG = "Hardware subsystem are not conencted."


class Smartlight:
    """Class for SmartLight object."""

    connected = False

    def __give_pucs(self) -> dict[int, PUCState]:
        """Method to return random PUCStates."""
        d = {}
        for i in range(NUM_PUCS):
            d[i] = PUCState(k=round(random(), 3), phase=round(uniform(0, 2 * pi), 3))
        return d

    def __validate_pucstate(self, pucstate) -> None:  # noqa: ANN001
        if not isinstance(pucstate.k, float):
            msg = "Coupling factor format not valid"
            raise AllegroExceptionError(msg)
        if not isinstance(pucstate.phase, float):
            msg = "Phase format not valid"
            raise AllegroExceptionError(msg)
        if not (0 <= pucstate.k <= 1):
            msg = "Coupling factor out of range"
            raise AllegroExceptionError(msg)
        if not (0 <= pucstate.phase <= (2 * pi)):
            msg = "Phase out of range"
            raise AllegroExceptionError(msg)

    def __validate_port(self, port) -> None:  # noqa: ANN001
        if not isinstance(port, int):
            msg = "Wrong port format."
            raise AllegroExceptionError(msg)
        if port not in range(NUM_PORTS):
            msg = "Port out of range."
            raise AllegroExceptionError(msg)

    def connect(self) -> None:
        """Connects the hardware subsystems and gets the system ready to be configured."""
        self.connected = True

    def disconnect(self) -> None:
        """Disconnects the hardware subsystems."""
        self.connected = False

    def set_puc_states(self, puc_states: dict[int, PUCState]) -> None:
        """Sets the given PUC states."""
        if not self.connected:
            raise AllegroExceptionError(CONN_MSG)
        if any(not isinstance(i, int) for i in puc_states):
            msg = "PUC format not valid"
            raise AllegroExceptionError(msg)
        if any(i > NUM_PUCS - 1 for i in puc_states):
            msg = "PUC out of range"
            raise AllegroExceptionError(msg)
        for i in puc_states.values():
            self.__validate_pucstate(i)

    def get_puc_states(self) -> dict[int, PUCState]:
        """Returns the current PUC states of the mesh."""
        if not self.connected:
            raise AllegroExceptionError(CONN_MSG)
        return self.__give_pucs()

    def reset(self) -> None:
        """Reset to inactive the active PUCs of the mesh."""
        if not self.connected:
            raise AllegroExceptionError(CONN_MSG)

    def interconnect(
        self,
        inport: int,
        outport: int,
        *,
        reset: bool = True,  # noqa: ARG002
    ) -> dict[int, PUCState]:
        """Create a circuit connection between the specified input and output port of the mesh."""
        self.__validate_port(inport)
        self.__validate_port(outport)
        if inport == outport:
            msg = "Input port can't be the same than ouput port"
            raise AllegroExceptionError(msg)
        return self.__give_pucs()

        # AllegroExceptionError when interconnection between the given ports is not posible
        # AllegroExceptionError when hardware is not connected

    def beamsplitter(
        self,
        inport: int,
        outports: list[int],
        *,
        reset: bool = True,  # noqa: ARG002
    ) -> dict[int, PUCState]:
        """Create a splitter between the given mesh input and outports.

        Optical power is divided equally in the outports.
        """
        if not self.connected:
            raise AllegroExceptionError(CONN_MSG)

        self.__validate_port(inport)
        [self.__validate_port(i) for i in outports]

        if inport in outports:
            msg = "Input port in ouput port list"
            raise AllegroExceptionError(msg)
        return self.__give_pucs()
        # AllegroExceptionError when beamsplitter between the given ports is not possible
        # AllegroExceptionError when hardware is not connected

    def combiner(
        self,
        inports: list[int],
        outport: int,
        *,
        reset: bool = True,  # noqa: ARG002
    ) -> dict[int, PUCState]:
        """Create a combiner between the given mesh inputs and outport.

        Optical power is combined with equal ratio of the input port signals.
        """
        if not self.connected:
            raise AllegroExceptionError(CONN_MSG)

        self.__validate_port(outport)
        [self.__validate_port(i) for i in inports]

        if outport in inports:
            msg = "Output port in input port list"
            raise AllegroExceptionError(msg)
        return self.__give_pucs()
        # AllegroExceptionError when combiner between the given ports is not possible
        # AllegroExceptionError when hardware is not connected

    def switch(
        self,
        inports: list[int],
        outports: list[int],
        *,
        reset: bool = True,  # noqa: ARG002
    ) -> dict[int, PUCState]:
        """Create a switch between the given mesh inputs and outports."""
        if not self.connected:
            raise AllegroExceptionError(CONN_MSG)

        [self.__validate_port(i) for i in inports]
        [self.__validate_port(i) for i in outports]

        if set(inports) & set(outports):
            msg = "Two state set for the same port"
            raise AllegroExceptionError(msg)
        return self.__give_pucs()

    # TODO(Lluis): central_wavelength,bandwidth and gd_slope values to be defined
    def compensate_dispersion(  # noqa: PLR0913  # pragma: no cover
        self,
        inport: int,
        outport: int,
        central_wavelength: float,  # noqa: ARG002
        bandwidth: float,  # noqa: ARG002
        gd_slope: float,  # noqa: ARG002
    ) -> None:
        """Configures the lattice filter HPB to compensate the given dispersion slope for the specified central wavelength and bandwidth."""  # noqa: E501
        if not self.connected:
            raise AllegroExceptionError(CONN_MSG)

        self.__validate_port(inport)
        self.__validate_port(outport)

        # AllegroExceptionError when given combination of bandwidth and gd_slope specification were not reachable by the lattice filter HPB  # noqa: E501

    def interrogate_fiber(
        self,
        inport: int,
        channels: Optional[list[int]] = None,
    ) -> dict[int, float]:
        """Interrogates the specified mesh inport signal using the AWG HPB."""
        if not self.connected:
            raise AllegroExceptionError(CONN_MSG)

        self.__validate_port(inport)
        if channels == None:
            channels = list(range(NUM_CHANNELS - 1))
        if inport in channels:
            channels.remove(inport)
        if any(i not in range(NUM_CHANNELS - 1) for i in channels):
            msg = "Num channel out of range"
            raise AllegroExceptionError(msg)
        d = {}

        for i in channels:
            d[i] = uniform(-50, 0)
        return d
