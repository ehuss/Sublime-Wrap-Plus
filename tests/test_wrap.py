import os
import queue
import re
import sublime
import threading
import time
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
    'WrapPlus.include_line_endings': 'auto',
    'WrapPlus.wrap_width': UNSET,
    'WrapPlus.skip_range': False,  # Workaround for a bug.
}


class TestWrap(unittest.TestCase):

    def test_wrap(self):
        to_test = ['tests/test.txt',
                   'tests/test_tab.txt',
                   'tests/test.py',
                   'tests/test.c',
                   'tests/test.rs',
                   'tests/test.md',
                   'tests/test.tex',
                  ]

        for path in to_test:
            # Open the file with Sublime (mainly to just get the correct
            # syntax file).
            self._with_open_file(path, self._test_wrap)

    def _test_wrap(self, view):
        contents = view.substr(sublime.Region(0, view.size()))
        syntax = view.settings().get('syntax')
        # Split test file into separate tests.
        starts = re.finditer(r'^===((?:[A-Za-z0-9._-]+=[^,\n]+,?)+)?$',
                             contents, flags=re.MULTILINE)
        starts = list(starts)
        for i, start in enumerate(starts):
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
                    key, value = setting.split('=')
                    settings[key] = eval(value)
            # Open a new view to run the test in.
            filename = os.path.basename(view.file_name())
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
        for key, value in DEFAULT_SETTINGS.items():
            value = settings.get(key, value)
            if value == UNSET:
                view_settings.erase(key)
            else:
                view_settings.set(key, value)
        view.run_command('append', {'characters': contents})
        f(view)
        actual = view.substr(sublime.Region(0, view.size()))
        if actual != expected:
            raise AssertionError('Wrapping did not match: %s %r\n%s---Expected:\n%s---' % (
                filename, settings, actual, expected))
        window.focus_view(view)
        window.run_command('close_file')

    def _with_open_file(self, filename, f, **kwargs):
        """Opens filename (relative to the plugin) in a new view, calls
        f(view) to perform the tests.
        """
        window = sublime.active_window()
        path = os.path.join(plugin_path, filename)
        if not os.path.exists(path):
            # Unfortunately there doesn't seem to be a good way to detect a
            # failure to load.
            raise ValueError('Can\'t find path %r' % path)
        view = window.find_open_file(path)
        if view:
            window.focus_view(view)
            f(view, **kwargs)
            return
        view = window.open_file(path)
        q = queue.Queue()

        def async_test_view():
            try:
                # Wait for view to finish loading.
                for n in range(500):
                    if view.is_loading():
                        time.sleep(0.01)
                    else:
                        break
                else:
                    raise AssertionError('View never loaded.')
                f(view, **kwargs)
            except Exception as e:
                q.put(e)
            else:
                q.put(None)

        try:
            t = threading.Thread(target=async_test_view)
            t.start()
            t.join()
            msg = q.get()
            if msg:
                raise msg
        finally:
            if view.window():
                window.focus_view(view)
                if view.is_dirty():
                    view.run_command('revert')
                window.run_command('close_file')
