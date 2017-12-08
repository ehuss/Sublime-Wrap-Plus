

import sys
import unittest

CURRENT_DIRECTORY    = os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) )
CURRENT_PACKAGE_NAME = os.path.basename( CURRENT_DIRECTORY ).rsplit('.', 1)[0]


def run_unit_tests(unit_tests_to_run=[]):
    runner = unittest.TextTestRunner()

    classes = \
    [
        sys.modules[CURRENT_PACKAGE_NAME + ".tests.text_extraction_unit_tests"].PrefixStrippingViewUnitTests,
        sys.modules[CURRENT_PACKAGE_NAME + ".tests.semantic_linefeed_unit_tests"].LineBalancingUnitTests,
        sys.modules[CURRENT_PACKAGE_NAME + ".tests.semantic_linefeed_unit_tests"].SemanticLineWrapUnitTests,
    ]

    if len( unit_tests_to_run ) < 1:

        # Comment all the tests names on this list, to run all Unit Tests
        unit_tests_to_run = \
        [
            # "test_semantic_line_wrap_line_starting_with_comment",
            # "test_split_lines_with_trailing_new_line",
            # "test_split_lines_without_trailing_new_line",
            # "test_balance_characters_between_line_wraps_with_trailing_new_line",
            # "test_balance_characters_between_line_wraps_without_trailing_new_line",
            # "test_balance_characters_between_line_wraps_ending_with_long_word",
        ]

    runner.run( suite( classes, unit_tests_to_run ) )


def suite(classes, unit_tests_to_run):
    """
        Problem with sys.argv[1] when unittest module is in a script
        https://stackoverflow.com/questions/2812218/problem-with-sys-argv1-when-unittest-module-is-in-a-script

        Is there a way to loop through and execute all of the functions in a Python class?
        https://stackoverflow.com/questions/2597827/is-there-a-way-to-loop-through-and-execute-all-of-the-functions

        looping over all member variables of a class in python
        https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
    """
    suite = unittest.TestSuite()
    unit_tests_to_run_count = len( unit_tests_to_run )

    for _class in classes:
        _object = _class()

        for function_name in dir( _object ):

            if function_name.lower().startswith( "test" ):

                if unit_tests_to_run_count > 0 \
                        and function_name not in unit_tests_to_run:

                    continue

                suite.addTest( _class( function_name ) )

    return suite


