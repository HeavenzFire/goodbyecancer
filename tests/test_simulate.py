import math
import unittest

from src.simulate import logistic_exact, simulate


class LogisticSimulationTests(unittest.TestCase):
    def test_rk4_tracks_analytic_reference(self):
        record = simulate(duration=10.0, dt=0.1)
        self.assertLess(record["result"]["absolute_error"], 1e-6)
        self.assertAlmostEqual(
            record["result"]["final_normalized_burden"],
            record["result"]["analytic_reference"],
            places=6,
        )

    def test_refining_step_reduces_error(self):
        coarse = simulate(duration=8.0, dt=0.4)["result"]["absolute_error"]
        fine = simulate(duration=8.0, dt=0.2)["result"]["absolute_error"]
        finer = simulate(duration=8.0, dt=0.1)["result"]["absolute_error"]
        self.assertGreater(coarse, fine)
        self.assertGreater(fine, finer)

    def test_result_is_bounded_for_reference_parameters(self):
        result = simulate(duration=100.0, dt=0.1)["result"]["final_normalized_burden"]
        self.assertGreater(result, 0.0)
        self.assertLessEqual(result, 1.0 + 1e-12)

    def test_zero_duration_returns_initial_state(self):
        record = simulate(duration=0.0)
        self.assertEqual(record["result"]["steps"], 0)
        self.assertAlmostEqual(record["result"]["final_normalized_burden"], 0.1)

    def test_invalid_step_rejected(self):
        with self.assertRaises(ValueError):
            simulate(dt=0.0)

    def test_invalid_initial_state_rejected(self):
        with self.assertRaises(ValueError):
            simulate(x0=0.0)

    def test_exact_solution_rejects_negative_time(self):
        with self.assertRaises(ValueError):
            logistic_exact(-1.0, 0.1, 0.6, 1.0)

    def test_record_disclaims_biological_validity(self):
        record = simulate()
        self.assertIn("not a validated cancer model", record["model_scope"])
        self.assertIn("does not accelerate real biology", record["interpretation_limit"])


if __name__ == "__main__":
    unittest.main()
