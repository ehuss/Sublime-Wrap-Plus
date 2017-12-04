

import sys

import sublime
import sublime_plugin

import textwrap
import unittest


wrap_plus_module = sys.modules["Wrap Plus.wrap_plus"]


def wrap_text(text):
    return textwrap.dedent( text ).strip( " " ).strip( "\n" )


class PrefixStrippingViewUnitTests(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.maxDiff = None

        # Create a new Sublime Text view to perform the Unit Tests
        self.view = sublime.active_window().new_file()
        self.view.set_syntax_file( "Packages/C++/C++.sublime-syntax" )

        # make sure we have a window to work with
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("append", {"characters": wrap_text( string ) })

    def test_triple_doxygen_quotes_comment(self):
        view_min = 0
        view_max = 57

        self.setText( """\
                /// This is a doxygen
                /// style multiline
                /// C++ comment.
                """ )

        self.wrap_plus        = wrap_plus_module.WrapLinesPlusCommand( None )
        self.wrap_plus.view   = self.view
        self.wrap_plus._width = 50

        self.wrap_plus._determine_tab_size()
        self.wrap_plus._determine_comment_style()

        paragraph_results = self.wrap_plus._find_paragraphs( sublime.Region(view_min, view_max) )
        region, paragraphs, comment_prefix = paragraph_results[0]

        print( "self.wrap_plus._find_paragraphs: " + str( paragraph_results ) )
        # self.assertEqual( '///', comment_prefix )


