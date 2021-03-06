from .calculator import Calculator
from kanata import InjectableCatalog, LifetimeScope, find_injectables

def run() -> None:
    """Runs the sample."""

    # Find and print all the injectable registrations in our samples.calculator module.
    catalog = InjectableCatalog(find_injectables("samples.calculator"))
    print("Found the following registrations:")
    for registration in catalog.get_registrations():
        print(f"{registration.injectable_type} registered as: {registration.contract_types}")

    # Create a lifetime scope that will hold our injectable instances.
    scope = LifetimeScope(catalog)

    # Resolve the root node.
    calculator = scope.resolve(Calculator)

    # Start accepting commands.
    print("The calculator supports addition (+) and subtraction (-) for the purpose of a sample.")
    print("Command syntax: <value1> <operation> <value2>")
    print("Example: 4 + 9")
    print("Example: 10 - 3")
    print()

    while True:
        command = input()
        arguments = command.split(" ")
        if len(arguments) != 3:
            print("Invalid syntax, expected: <value1> <operation> <value2>")
            continue

        operation_code = arguments[1]
        value1 = float(arguments[0])
        value2 = float(arguments[2])
        result = calculator.calculate(operation_code, value1, value2)
        print(f"Result: {result}")
