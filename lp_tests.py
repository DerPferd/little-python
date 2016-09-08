# Copyright (C) Jonathan Beaulieu (beau0307@d.umn.edu)
# Copyright (C) Aleksandar Straumann (alstraumann@gmail.com)

import unittest
from lp import Compiler


class TestLPComplierMethods(unittest.TestCase):
    def setUp(self):
        self.compiler = Compiler()

    def tearDown(self):
        self.compiler = None

    # Here is a sample test. You should copy this to create a new test
    def test_sample(self):
        beginning_state = {}
        code = """"""
        expected_state = {}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_blank(self):
        beginning_state = {}
        code = """"""
        expected_state = {}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_only_newlines(self):
        beginning_state = {}
        code = """\n\n\n\n\n"""
        expected_state = {}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_trailing_newlines(self):
        beginning_state = {}
        code = """a = 2\n\n\n\n\n"""
        expected_state = {"a": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_int(self):
        beginning_state = {}
        code = """a = 2"""
        expected_state = {"a": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_with_underscore(self):
        beginning_state = {}
        code = """a_b = 2"""
        expected_state = {"a_b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_with_underscore_at_beginning(self):
        beginning_state = {}
        code = """_b = 2"""
        expected_state = {"_b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_simple_expression(self):
        beginning_state = {}
        code = """b = 40 % 1"""
        expected_state = {"b": 40 % 1}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_variable_assignment_to_other_variables(self):
        beginning_state = {}
        code = """a = 2\nb = 0\nc = b + a"""
        expected_state = {"a": 2, "b": 0, "c": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_is_no_trailing_newline(self):
        beginning_state = {}
        code = """if 0 is 0 {
 c = 3
}"""
        expected_state = {"c": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_not(self):
        beginning_state = {}
        code = """if 0 is not 1 {
            c = 3
        }"""
        expected_state = {"c": 3}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_var(self):
        beginning_state = {}
        code = """
        c = 3
        if c is 3 {
            d = 4
        }"""
        expected_state = {"c": 3, "d":4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_if_with_var_reassignment(self):
        beginning_state = {}
        code = """
        c = 3
        if c is 3 {
            c = 5
        }"""
        expected_state = {"c": 5}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_nested_if(self):
            beginning_state = {}
            code = """if 0 is 0 {
                if 1 is 1 {
                    c = 3
                }
            }"""
            expected_state = {"c": 3}

            # compile code into LPProg
            prog = self.compiler.compile(code.split("\n"))

            ending_state = prog.run(beginning_state)
            self.assertEqual(expected_state, ending_state)
    
    def test_nested_if_with_var_reassignment(self):
        beginning_state = {}
        code = """
        c = 3
        if c is 3 {
            c = 4
            if c is 4 {
                c = 5
            }
        }"""
        expected_state = {"c": 5}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_long_alphanumeric_variable_name(self):
        beginning_state = {}
        code = """asdfasdfasdfasdifgasdfhga232hjkbljh123b1jh2b31j2hb = 23"""
        expected_state = {"asdfasdfasdfasdifgasdfhga232hjkbljh123b1jh2b31j2hb": 23}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_line_comment(self):
        beginning_state = {}
        code = """a=3\n# This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_with_spaces(self):
        beginning_state = {}
        code = """a=3 # This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_inline_comment_without_space(self):
        beginning_state = {}
        code = """a=3#This is a comment\nb=4"""
        expected_state = {"a": 3, "b": 4}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)

    def test_beginning_state(self):
        beginning_state = {"b": 2}
        code = """a=b"""
        expected_state = {"a": 2, "b": 2}

        # compile code into LPProg
        prog = self.compiler.compile(code.split("\n"))

        ending_state = prog.run(beginning_state)
        self.assertEqual(expected_state, ending_state)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLPComplierMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)