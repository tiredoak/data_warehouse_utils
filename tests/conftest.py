import doctest
import importlib
import pathlib

import pytest


@pytest.fixture(scope="session")
def doctest_namespace():
    import data_warehouse_utils

    importlib.reload(data_warehouse_utils)
    return vars(data_warehouse_utils)


def load_tests(loader, tests, ignore):
    root = pathlib.Path(__file__).parent.parent / "data_warehouse_utils"
    for path in root.glob("**/*.py"):
        if path.name.startswith("_"):
            continue
        module_path = ".".join(path.relative_to(root).parts)[:-3]
        module = importlib.import_module(f"data_warehouse_utils.{module_path}")
        tests.addTests(doctest.DocTestSuite(module))
    return tests
