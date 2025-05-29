# python3 -m unittest tests/test_rolling_connectedness.py

import unittest
from unittest.mock import Mock
from multi_time_series_connectedness.rolling_connectedness import RollingConnectedness
from tests.data_utils import get_volatilities_data


class TestRollingConnectedness(unittest.TestCase):
    # def setUp(self):

    def test_divide_timeseries_volatilities(self):
        pass

    def test_calculate_rolling(self):
        mock_volatilities_data = get_volatilities_data()
        roll_conn = RollingConnectedness(
            mock_volatilities_data,
            1,
            28,
        )
        roll_conn.data = get_volatilities_data().dropna()
        roll_conn.calculate()

        # Define the expected DataFrame
        expected_column_names = [
            "AUDNZD=X.csv_to_AUDNZD=X.csv",
            "AUDNZD=X.csv_to_AUDCAD=X.csv",
            "AUDNZD=X.csv_to_AUDUSD=X.csv",
            "AUDNZD=X.csv_to_to_other",
            "AUDCAD=X.csv_to_AUDNZD=X.csv",
            "AUDCAD=X.csv_to_AUDCAD=X.csv",
            "AUDCAD=X.csv_to_AUDUSD=X.csv",
            "AUDCAD=X.csv_to_to_other",
            "AUDUSD=X.csv_to_AUDNZD=X.csv",
            "AUDUSD=X.csv_to_AUDCAD=X.csv",
            "AUDUSD=X.csv_to_AUDUSD=X.csv",
            "AUDUSD=X.csv_to_to_other",
            "from_other_to_AUDNZD=X.csv",
            "from_other_to_AUDCAD=X.csv",
            "from_other_to_AUDUSD=X.csv",
            "from_other_to_to_other",
            "start_at",
            "end_at",
            "forecast_period",
            "forecast_at"
        ]
        expected_values = [
            [0.509513, 0.456351, 0.066045, 0.522396, 0.452378, 0.513988, 0.050956, 0.503334, 0.038110, 0.029661, 0.882999, 0.067771, 0.490487, 0.486012, 0.117001, 0.364500, 1729210980, 1729212600, 1, 1729212660],
            [0.501581, 0.458034, 0.072198, 0.530232, 0.456396, 0.503381, 0.066054, 0.522450, 0.042023, 0.038585, 0.861748, 0.080608, 0.498419, 0.496619, 0.138252, 0.377763, 1729211040, 1729212660, 1, None]
        ]

        result = roll_conn.rolling_connectedness

        assert result.columns.tolist() == expected_column_names
        assert [round(value, 6) for value in result.iloc[0].tolist()] == expected_values[0]

    def test_with_callback(self):
        mock_volatilities_data = get_volatilities_data()
        roll_conn = RollingConnectedness(
            mock_volatilities_data,
            1,
            29,
        )
        roll_conn.data = get_volatilities_data().dropna()

        def callback(restructured_connectedness):
            print("Callback called with:", restructured_connectedness)
        callback_mock = Mock(side_effect=callback)
        roll_conn.calculate(callback_after_one_connectedness=callback_mock)
        self.assertEqual(callback_mock.call_count, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
