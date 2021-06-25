import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()

import pytest


@pytest.fixture(params=["nodict", "dict"])
def generate_initial_transform_parameters(request):

    pytest.mocker.patch.object("", "do_something")
    pytest.mocker.do_something.return_value(1)
    pytest.mocker.do_something.side_effect([1, 2])
