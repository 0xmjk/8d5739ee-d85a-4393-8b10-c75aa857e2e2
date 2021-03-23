#!/usr/bin/env python
import argparse
import multiprocessing
import sys
import numpy as np
from numbers import Number
from numba import jit, prange

num_cores = multiprocessing.cpu_count()


def get_hurricane_loss(
    florida_landfall_rate,
    florida_mean,
    florida_stddev,
    gulf_landfall_rate,
    gulf_mean,
    gulf_stddev,
    samples=1,
) -> tuple[np.number, int]:
    """
    Calculate total loss due to tha landfalling hurricans in Florida and the Gulf States

    Args:
        florida_landfall_rate – The annual rate of landfalling hurricanes in Florida
        florida_mean, florida_stddev – The LogNormal parameters that describe the economic loss of a landfalling hurricane in Florida.
        gulf_landfall_rate - The annual rate of landfalling hurricanes in the Gulf states
        gulf_mean, gulf_stddev - The LogNormal parameters that describe the economic loss of a a landfalling hurricane in the Gulf states
        samples - total number of samples to run
    Returns:
        (total_loss, total_samples_run) - a tuple containing sum of total loss of the simulation and number of total samples run
                                          (this could be a bit bigger than `samples` argument, becaus we use a rounding function when
                                           splitting work across cores)
    """
    # do argument type and range checking
    # note, minimum value for `samples` argument is 1, for all others it is 0
    for arg, value in locals().items():
        if not isinstance(value, Number):
            raise TypeError(f"Argument `{arg}` should be a number")
        if value < (min_value := 1 if arg == "samples" else 0):
            raise ValueError(f"Argument `{arg}` should be >= {min_value}")

    samples_per_core = int(np.ceil(samples / num_cores))
    simulation_loss = np.full([num_cores], 0, dtype=np.float64, order="C")

    @jit(nopython=True, parallel=True)
    def simulator(out):
        for core in prange(num_cores):
            # Rate of events in the whole simulation interval
            florida_events = np.sum(
                np.random.poisson(florida_landfall_rate, samples_per_core)
            )
            gulf_events = np.sum(
                np.random.poisson(gulf_landfall_rate, samples_per_core)
            )

            # Losses for all events in that interval
            florida_loss = np.random.lognormal(
                florida_mean, florida_stddev, florida_events
            )
            gulf_loss = np.random.lognormal(gulf_mean, gulf_stddev, gulf_events)

            # Result is the sum of losses
            out[core] = np.sum(florida_loss) + np.sum(gulf_loss)

    simulator(simulation_loss)

    return np.sum(simulation_loss), samples_per_core * num_cores


def _parse_arguments(*args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate total loss due to tha landfalling hurricans in Florida and the Gulf States."
    )
    for k, desc in {
        "florida_landfall_rate": "The annual rate of landfalling hurricanes in Florida",
        "florida_mean": "The LogNormal parameters that describe the economic loss of a landfalling hurricane in Florida.",
        "florida_stddev": "The LogNormal parameters that describe the economic loss of a landfalling hurricane in Florida.",
        "gulf_landfall_rate": "The annual rate of landfalling hurricanes in the Gulf states",
        "gulf_mean": "The LogNormal parameters that describe the economic loss of a a landfalling hurricane in the Gulf states",
        "gulf_stddev": "The LogNormal parameters that describe the economic loss of a a landfalling hurricane in the Gulf states",
    }.items():
        parser.add_argument(k, type=float, help=desc)
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        dest="samples",
        help="total number of samples to run",
        required=True,
    )
    parameters = parser.parse_args(args)
    return parameters


if __name__ == "__main__":
    parameters = _parse_arguments(*sys.argv[1:])
    try:
        total_loss, total_samples = get_hurricane_loss(
            parameters.florida_landfall_rate,
            parameters.florida_mean,
            parameters.florida_stddev,
            parameters.gulf_landfall_rate,
            parameters.gulf_mean,
            parameters.gulf_stddev,
            samples=parameters.samples,
        )
    except Exception as e:
        print("FOO")
    print(total_loss / total_samples)
