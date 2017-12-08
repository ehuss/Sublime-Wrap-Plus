

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

    def setText(self, string, start_point=0):
        self.view.run_command("append", {"characters": wrap_text( string ) })

        self.wrap_plus        = wrap_plus_module.WrapLinesPlusCommand( None )
        self.wrap_plus.view   = self.view
        self.wrap_plus._width = 50

        self.wrap_plus._determine_tab_size()
        self.wrap_plus._determine_comment_style()

        selections = self.view.sel()
        selections.clear()
        selections.add( sublime.Region( start_point, start_point ) )

    def get_view_contents(self):
        return self.view.substr( sublime.Region( 0, self.view.size() ) )

    def test_triple_quotes_comment(self):
        self.setText( """\
                /// This is a doxygen
                /// style multiline
                /// C++ comment.""" )

        paragraph_results = self.wrap_plus._find_paragraphs( sublime.Region(0, 0) )
        region, paragraphs, comment_prefix = paragraph_results[0]

        # print( "self.wrap_plus._find_paragraphs: " + str( paragraph_results ) )
        self.assertEqual( '///', comment_prefix )
        self.assertEqual( sublime.Region(0, 58), region )

    def test_triple_quotes_wrappting(self):
        self.setText( """\
                /// This is a doxygen is a doxygen is a doxygen is a doxygen
                /// style multiline
                /// C++ comment.""" )

        self.view.run_command( "wrap_lines_plus", {"width": 50} )
        self.assertEqual( wrap_text( """\
                /// This is a doxygen is a doxygen is a doxygen is
                /// a doxygen style multiline C++ comment.""" ),
                self.get_view_contents() )

    def test_double_quotes_wrappting(self):
        self.setText( """\
                // This is a doxygen is a doxygen is a doxygen is a doxygen
                // style multiline
                // C++ comment.""" )

        self.view.run_command( "wrap_lines_plus", {"width": 50} )
        self.assertEqual( wrap_text( """\
                // This is a doxygen is a doxygen is a doxygen is
                // a doxygen style multiline C++ comment.""" ),
                self.get_view_contents() )

    def test_double_quotes_wrappting_without_leading_whitespace(self):
        self.setText( """\
                //This is a doxygen is a doxygen is a doxygen is a doxygen
                //style multiline
                //C++ comment.""" )

        self.view.run_command( "wrap_lines_plus", {"width": 50} )
        self.assertEqual( wrap_text( """\
                //This is a doxygen is a doxygen is a doxygen is a
                //doxygen style multiline C++ comment.""" ),
                self.get_view_contents() )

    def test_triple_quotes_wrappting_without_leading_whitespace(self):
        self.setText( """\
                ///This is a doxygen is a doxygen is a doxygen is a doxygen
                ///style multiline
                ///C++ comment.""" )

        self.view.run_command( "wrap_lines_plus", {"width": 50} )
        self.assertEqual( wrap_text( """\
                ///This is a doxygen is a doxygen is a doxygen is
                ///a doxygen style multiline C++ comment.""" ),
                self.get_view_contents() )

    def test_markdown_triple_quotes_line_start(self):
        self.setText( """\
                1. Although if you prefer, you can provide a menu entry forMyBrandNewChannel` directory:
                   ```javascript
                   [
                   ]
                   ```""" )

        self.view.run_command( "wrap_lines_plus", {"width": 100} )
        self.assertEqual( wrap_text( """\
                1. Although if you prefer, you can provide a menu entry forMyBrandNewChannel` directory:
                   ```javascript
                   [
                   ]
                   ```""" ), self.get_view_contents() )

