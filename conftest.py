import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run integration tests against the real Wialon API",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        return
    skip = pytest.mark.skip(reason="pass --integration to run")
    for item in items:
        if item.get_closest_marker("integration"):
            item.add_marker(skip)
