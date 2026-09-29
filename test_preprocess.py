import unittest

from a2 import CommandInterface, HeapGo, BLACK, WHITE, MAX_HEAPS, MAX_TOKENS, MAX_VALUE


def make_interface(heaps, komi=0.5):
    ci = CommandInterface()
    ci.game = HeapGo(komi, heaps)
    ci.preprocess_game_state()
    return ci


class TestPreprocessGameState(unittest.TestCase):
    # --- Encoding ---------------------------------------------------------
    def test_single_black_token_is_negative(self):
        ci = make_interface([[('b', 1)]])
        self.assertEqual(ci.game.numerical_game_state, [[-1]])

    def test_single_white_token_is_positive(self):
        ci = make_interface([[('w', 1)]])
        self.assertEqual(ci.game.numerical_game_state, [[1]])

    def test_mixed_heap_preserves_order(self):
        # index 0 is the bottom, index -1 is the top; order must not change
        ci = make_interface([[('b', 3), ('w', 5), ('b', 2), ('w', 7)]])
        self.assertEqual(ci.game.numerical_game_state, [[-3, 5, -2, 7]])

    def test_multiple_heaps_preserve_heap_order(self):
        heaps = [[('w', 1)], [('b', 2), ('b', 3)], [('w', 4), ('b', 5)]]
        ci = make_interface(heaps)
        self.assertEqual(ci.game.numerical_game_state, [[1], [-2, -3], [4, -5]])

    def test_max_value_tokens(self):
        ci = make_interface([[('b', MAX_VALUE), ('w', MAX_VALUE)]])
        self.assertEqual(ci.game.numerical_game_state, [[-MAX_VALUE, MAX_VALUE]])

    def test_max_size_board(self):
        heaps = [[('b' if (i + j) % 2 else 'w', j + 1) for j in range(MAX_TOKENS)]
                 for i in range(MAX_HEAPS)]
        ci = make_interface(heaps)
        state = ci.game.numerical_game_state
        self.assertEqual(len(state), MAX_HEAPS)
        self.assertTrue(all(len(h) == MAX_TOKENS for h in state))

    def test_round_trip_decodes_to_original(self):
        heaps = [[('b', 3), ('w', 5)], [('w', 20), ('b', 1), ('b', 1)]]
        ci = make_interface(heaps)
        decoded = [[(WHITE if v > 0 else BLACK, abs(v)) for v in h]
                   for h in ci.game.numerical_game_state]
        self.assertEqual(decoded, heaps)

    def test_no_zero_values(self):
        # sign carries the colour, so 0 would be ambiguous
        heaps = [[('b', 1), ('w', 1)], [('w', 1)]]
        ci = make_interface(heaps)
        self.assertTrue(all(v != 0 for h in ci.game.numerical_game_state for v in h))

    # --- Independence from self.game.heaps --------------------------------
    def test_original_heaps_unchanged(self):
        heaps = [[('b', 3), ('w', 5)]]
        ci = make_interface(heaps)
        self.assertEqual(ci.game.heaps, [[('b', 3), ('w', 5)]])

    def test_state_is_not_aliased_to_heaps(self):
        ci = make_interface([[('b', 3), ('w', 5)]])
        ci.game.numerical_game_state[0].pop()
        self.assertEqual(ci.game.heaps, [[('b', 3), ('w', 5)]])

    def test_heaps_are_independent_lists(self):
        ci = make_interface([[('w', 1)], [('w', 1)]])
        state = ci.game.numerical_game_state
        self.assertIsNot(state[0], state[1])

    # --- Integration with cmd_heapgo --------------------------------------
    def test_heapgo_populates_state(self):
        ci = CommandInterface()
        self.assertTrue(ci.cmd_heapgo("0.5 [[('b', 2), ('w', 3)], [('w', 4)]]"))
        self.assertEqual(ci.game.numerical_game_state, [[-2, 3], [4]])

    def test_heapgo_replaces_previous_state(self):
        ci = CommandInterface()
        ci.cmd_heapgo("0.5 [[('b', 2)]]")
        ci.cmd_heapgo("1.5 [[('w', 9)]]")
        self.assertEqual(ci.game.numerical_game_state, [[9]])

    def test_invalid_heapgo_keeps_old_state(self):
        ci = CommandInterface()
        ci.cmd_heapgo("0.5 [[('b', 2)]]")
        self.assertFalse(ci.cmd_heapgo("0.5 [[('x', 2)]]"))
        self.assertEqual(ci.game.numerical_game_state, [[-2]])

    def test_no_game_raises(self):
        ci = CommandInterface()
        with self.assertRaises(AttributeError):
            ci.preprocess_game_state()

    # --- Staleness after moves --------------------------------------------
    @unittest.expectedFailure
    def test_state_stays_in_sync_after_play(self):
        # Currently fails: play() mutates heaps but not numerical_game_state.
        # Remove @expectedFailure once play/solve keep them in sync (or re-preprocess).
        ci = CommandInterface()
        ci.cmd_heapgo("0.5 [[('w', 1), ('b', 2)]]")
        ci.cmd_play("0")
        self.assertEqual(ci.game.numerical_game_state, [[]])


if __name__ == "__main__":
    unittest.main()
