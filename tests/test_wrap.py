import os
import sys
import re
import sublime
import unittest

plugin_path = os.path.dirname(os.path.dirname(__file__))

# Sentinel to indicate that a setting should not be set.
UNSET = '__UNSET__'

DEFAULT_SETTINGS = {
    'word_wrap': False,
    'wrap_width': 0,
    'rulers': [],
    'tab_size': 4,
    'translate_tabs_to_spaces': False,
    'WrapPlus.break_long_words': False,
    'WrapPlus.break_on_hyphens': False,
    'WrapPlus.after_wrap': 'cursor_below',
    'WrapPlus.semantic_line_wrap': False,
    'WrapPlus.include_line_endings': 'auto',
    'WrapPlus.wrap_width': UNSET,
    'WrapPlus.skip_range': False,  # Workaround for a bug.
}

has_failures = []

def make_wrap_tests():
    base = os.path.join(plugin_path, 'tests', 'wrap_tests')
    to_test = os.listdir(base)

    for filename in to_test:
        abspath = os.path.join(base, filename)
        contents = open(abspath, encoding='utf8').read()
        contents = contents.replace('\r\n', '\n')
        index = contents.find('\n')
        syntax = contents[:index]
        contents = contents[index + 1:]
        assert contents.startswith('==='), 'bad file %r' % (filename,)

        # _test_wrap(filename, contents, syntax)
        # Split test file into separate tests.
        starts = re.finditer(r'^===((?:[A-Za-z0-9._-]+=[^,\n]+,?)+)?$',
                             contents, flags=re.MULTILINE)
        starts = list(starts)
        sys.stderr.write('Creating %s tests from %s <%s>...\n' % (len(starts), filename, syntax))

        for index, start in enumerate(starts):

            class IntegrationTests(unittest.TestCase):
                # https://stackoverflow.com/questions/4414234/getting-pythons-unittest-results-in-a-teardown-method
                old_failureException = unittest.TestCase.failureException

                @property
                def failureException(self):
                    has_failures.append('fail')
                    return self.old_failureException

                def setUp(self):
                    # https://stackoverflow.com/questions/23741133/if-condition-in-setup-ignore-test
                    if has_failures:
                        self.skipTest("An test has failed, skipping everything else!")

                def test_thing(self):
                    # Fix appveyor/travis thinking Sublime Text is not responding
                    sys.stderr.write('%s. %s <%s>' % (self.index + 1, self.filename, self.syntax))
                    sys.stderr.flush()
                    # Get individual test substring.
                    try:
                        end = self.starts[self.index + 1]
                    except IndexError:
                        end = len(self.contents)
                    else:
                        end = end.start(0)
                    test_str = self.contents[self.start.end(0) + 1:end]
                    orig, expected = re.split('^---\n', test_str, flags=re.MULTILINE)
                    # Get optional settings.
                    settings = {}
                    if self.start.group(1):
                        for setting in self.start.group(1).split(','):
                            setting_name, value = setting.split('=')
                            settings[setting_name] = eval(value)
                    # Open a new view to run the test in.
                    self._wrap_with_scratch(self.filename, orig, expected, self.syntax, settings,
                                            self._test_wrap_individual)
                    if not settings.get('WrapPlus.skip_range', False):
                        self._wrap_with_scratch(self.filename, orig, expected, self.syntax, settings,
                                                self._test_wrap_ranges)

                def _test_wrap_individual(self, view):
                    # Test wrapping every line.
                    for r in self._tagged_regions(view):
                        pos = r[0]
                        rel_end = view.size() - r[1]
                        sel = view.sel()
                        sel.clear()
                        sel.add(pos)
                        while pos < view.size() - rel_end:
                            view.run_command('wrap_lines_plus')
                            next_pos = view.sel()[0].a
                            if next_pos < view.size() - rel_end:
                                self.assertGreater(next_pos, pos,
                                    'The cursor did not advanced up to the end of the file!\n'
                                    + view.substr(sublime.Region(0, view.size())))
                            pos = next_pos

                def _tagged_regions(self, view):
                    if not view.find('<START>', 0):
                        yield (0, view.size())
                        return

                    while True:
                        start = view.find('<START>', 0)
                        if not start:
                            return
                        view.sel().clear()
                        view.sel().add(start)
                        view.run_command('left_delete')
                        end = view.find('<END>', 0)
                        view.sel().clear()
                        view.sel().add(end)
                        view.run_command('left_delete')
                        yield (start.a, end.a)

                def _test_wrap_ranges(self, view):
                    regions = [sublime.Region(*r) for r in self._tagged_regions(view)]
                    view.sel().clear()
                    view.sel().add_all(regions)
                    view.run_command('wrap_lines_plus')

                def _wrap_with_scratch(self, filename, contents, expected, syntax, settings, f):
                    window = sublime.active_window()
                    view = window.new_file()
                    view.set_scratch(True)
                    view.set_syntax_file(syntax)
                    # Update settings.
                    view_settings = view.settings()
                    bad_keys = set(settings.keys()) - set(DEFAULT_SETTINGS.keys())
                    self.assertEqual(bad_keys, set())
                    for setting_name, value in DEFAULT_SETTINGS.items():
                        value = settings.get(setting_name, value)
                        if value == UNSET:
                            view_settings.erase(setting_name)
                        else:
                            view_settings.set(setting_name, value)
                    view.run_command('append', {'characters': contents})
                    f(view)
                    actual = view.substr(sublime.Region(0, view.size()))
                    if actual != expected:
                        raise AssertionError('Wrapping did not match: %s %r\n%s---Expected:\n%s---' % (
                            filename, settings, actual, expected))
                    window.focus_view(view)
                    window.run_command('close_file')

            test_name = "".join( character for character in filename if character.isalpha() )
            _NAME = "Integration{}{:03d}Tests".format( test_name.title(), index )
            IntegrationTests.__name__ = _NAME
            IntegrationTests.index = index
            IntegrationTests.start = start
            IntegrationTests.starts = starts
            IntegrationTests.filename = filename
            IntegrationTests.syntax = syntax
            IntegrationTests.contents = contents
            globals()[_NAME] = IntegrationTests

make_wrap_tests()

def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    # See _NAME above to get the test class name pattern
    suite.addTest( IntegrationTesttex001Tests( 'test_thing' ) )
    suite.addTest( IntegrationTesttxt020Tests( 'test_thing' ) )
    return suite

# Comment this to run individual Unit Tests
load_tests = None
