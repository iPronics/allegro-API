"""API for Allegro project."""

from math import pi
from random import random, uniform
from dataclasses import dataclass


@dataclass
class PUCState:
    k: float = 1.0
    phase: float = 0.0


class AllegroException(Exception):
    pass


NUM_PUCS = 71


class Ipronics:
    def __give_pucs(self) -> dict[int, PUCState]:
        d = {}
        for i in range(NUM_PUCS):
            d[i] = PUCState(k=round(random(), 3), phase=round(uniform(0, 2 * pi), 3))
        return d

    def connect(self) -> None:
        """Connects the hardware subsystems and gets the system ready to be configured by the user."""

    def disconnect(self) -> None:
        """Disconnects the hardware subsystems,"""

    def set_puc_states(puc_states: dict[int, PUCState]) -> None:
        """Sets the given PUC states."""

        for i in puc_states.keys:
            if i > NUM_PUCS - 1:
                raise AllegroException
        # AllegroException when an invalid PUC id or state is given-
        # AllegroException when hardware is not connected

    def get_puc_states(self) -> dict[int, PUCState]:
        """Returns the current PUC states of the mesh."""

        return self.__give_pucs()
        # AllegroException when hardware is not connected

    def reset(self) -> None:
        """Reset to inactive the active PUCs of the mesh."""
        # AllegroException when hardware is not connected

    def interconnect(
        self, inport: int, outport: int, reset: bool = True
    ) -> dict[int, PUCState]:
        """Create a circuit connection between the specified input and output port of the mesh."""

        return self.__give_pucs()

        # AllegroException when interconnection between the given ports is not posible
        # AllegroException when hardware is not connected

    def beamsplitter(
        self, inport: int, outports: list[int], reset: bool = True
    ) -> dict[int, PUCState]:
        """Create a splitter between the given mesh input and outports. Optical power is divided equally in the outports."""
        return self.__give_pucs()
        # AllegroException when beamsplitter between the given ports is not possible
        # AllegroException when hardware is not connected

    def combiner(
        self, inports: list[int], outport: int, reset: bool = True
    ) -> dict[int, PUCState]:
        """Create a combiner between the given mesh inputs and outport. Optical power is combined with equal ratio of the input port signals"""
        return self.__give_pucs()
        # AllegroException when combiner between the given ports is not possible
        # AllegroException when hardware is not connected

    def switch(
        self, inports: list[int], outports: list[int], reset: bool = True
    ) -> dict[int, PUCState]:
        return self.__give_pucs()
        # AllegroException when switch between the given ports is not possible
        # AllegroException when hardware is not connected

    def compensate_dispersion(
        self,
        inport: int,
        outport: int,
        central_wavelength: float,
        bandwidth: float,
        gd_slope: float,
    ) -> None:
        """Configures the lattice filter HPB to compensate the given dispersion slope for the specified central wavelength and bandwidth."""

        # AllegroException when given combination of bandwidth and gd_slope specification were not reachable by the lattice filter HPB
        # AllegroException when hardware is not connected

    def interrogate_fiber(
        self, inport: int, channels: list[int] = None
    ) -> dict[int, float]:
        """Interrogates the specified mesh inport signal using the AWG HPB."""

        d = {}
        for i in channels:
            d[i] = uniform(-50, 0)
        return d

        # AllegroException when the given channels are not valid
        # AllegroException when hardware is not connected
