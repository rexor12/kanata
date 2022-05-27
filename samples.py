from os.path import dirname, join

import structlog
import sys

sys.path.append(join(dirname(__file__), "samples"))

# Disable the log spam for the samples.
structlog.configure_once(logger_factory=structlog.ReturnLoggerFactory())

from samples.calculator import run as run_sample_calculator # pylint: disable=no-name-in-module,wrong-import-position

VALID_SAMPLES = ["calculator"]

def print_valid_samples() -> None:
    """Prints the names of the samples available for selection."""

    print("List of available samples:")
    for sample_name in VALID_SAMPLES:
        print(f"- {sample_name}")

if __name__ == "__main__":
    print("Press Ctrl+C to exit at any time.")
    print_valid_samples()
    while not (selected_sample := input("Selected sample: ")) in VALID_SAMPLES:
        print_valid_samples()

    try:
        if selected_sample == "calculator":
            run_sample_calculator()
    except KeyboardInterrupt:
        pass
