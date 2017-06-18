

import sublime, sublime_plugin

class WrapLinesEnhancementCommand(sublime_plugin.TextCommand):
    """
    Wrap without loosing cursor position
    https://github.com/ehuss/Sublime-Wrap-Plus/issues/19

    My workaround is simple. Create a new plugin with the following implementations:
    https://github.com/ggutierrez
    """

    def run(self, edit, **kwargs):

        pos = self.view.sel()[0].begin()

        self.view.run_command('wrap_lines_plus', kwargs)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pos))



