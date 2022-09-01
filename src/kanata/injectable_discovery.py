"""Utilities for discovering injectables."""

import importlib
import inspect
import pkgutil
from types import ModuleType
from typing import Any

import structlog

from .constants import LOGGER_NAME
from .models import InjectableRegistration

def find_injectables(module_name: str) -> tuple[InjectableRegistration, ...]:
    """Recursively discovers all injectables starting from the specified module.

    :param module_name: The name of the root module.
    :type module_name: str
    :return: The registration objects of the discovered injectables.
    :rtype: tuple[InjectableRegistration, ...]
    """

    logger = structlog.get_logger(logger_name=LOGGER_NAME)
    registrations: list[InjectableRegistration] = []
    module_names: list[str] = [module_name]
    while module_names:
        module_name = module_names.pop()
        logger.debug("Loading module", name=module_name)
        module = importlib.import_module(module_name)
        registrations.extend(__get_registrations(module, logger))

        if (path := getattr(module, "__path__", None)) is None:
            continue

        logger.debug("Walking path", path=path)
        for _, name, is_package in pkgutil.walk_packages(path):
            if not is_package:
                continue
            logger.debug("Found additional package", name=name, parent=module_name)
            module_names.append(f"{module_name}.{name}")

    return tuple(registrations)

def __get_registrations(module: ModuleType, logger: Any) -> tuple[InjectableRegistration, ...]:
    registrations: list[InjectableRegistration] = []
    for _, obj in inspect.getmembers(module, inspect.isclass):
        local_registration: InjectableRegistration | None = getattr(
            obj,
            InjectableRegistration.PROPERTY_NAME,
            None
        )
        if local_registration:
            logger.debug("Found injectable", type=local_registration.injectable_type)
            registrations.append(local_registration)

    return tuple(registrations)
