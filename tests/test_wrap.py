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


class TestWrap(unittest.TestCase):

    def test_wrap(self):
        base = os.path.join(plugin_path, 'tests', 'wrap_tests')
        to_test = os.listdir(base)
        for filename in to_test:
            abspath = os.path.join(base, filename)
            contents = open(abspath, encoding='utf8').read()
            contents = contents.replace('\r\n', '\n')
            i = contents.find('\n')
            syntax = contents[:i]
            contents = contents[i + 1:]
            assert contents.startswith('==='), 'bad file %r' % (filename,)
            self._test_wrap(filename, contents, syntax)

    def _test_wrap(self, filename, contents, syntax):
        # Split test file into separate tests.
        starts = re.finditer(r'^===((?:[A-Za-z0-9._-]+=[^,\n]+,?)+)?$',
                             contents, flags=re.MULTILINE)
        starts = list(starts)
        sys.stderr.write('\nstarts: %s, ' % len(starts))
        for i, start in enumerate(starts):
            # Fix appveyor/travis thinking Sublime Text is not responding
            sys.stderr.write('%s. ' % (i + 1))
            sys.stderr.flush()
            # Get individual test substring.
            try:
                end = starts[i + 1]
            except IndexError:
                end = len(contents)
            else:
                end = end.start(0)
            test_str = contents[start.end(0) + 1:end]
            orig, expected = re.split('^---\n', test_str, flags=re.MULTILINE)
            # Get optional settings.
            settings = {}
            if start.group(1):
                for setting in start.group(1).split(','):
                    setting_name, value = setting.split('=')
                    settings[setting_name] = eval(value)
            # Open a new view to run the test in.
            self._wrap_with_scratch(filename, orig, expected, syntax, settings,
                                    self._test_wrap_individual)
            if not settings.get('WrapPlus.skip_range', False):
                self._wrap_with_scratch(filename, orig, expected, syntax, settings,
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
                # Assume it advances the cursor past the wrapped section.
                next_pos = view.sel()[0].a
                if next_pos < view.size() - rel_end:
                    self.assertGreater(next_pos, pos)
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
