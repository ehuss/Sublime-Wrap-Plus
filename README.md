# Sublime Wrap Plus #
Enhanced "wrap lines" command for Sublime Text 2 or 3.  This is for the *manual* hard line wrap command (<kbd>Alt</kbd><kbd>Q</kbd> in Windows and Linux, <kbd>Command</kbd><kbd>Alt</kbd><kbd>Q</kbd> in OS X).  It does not affect the automatic soft line wrapping.

## Downloading ##
The best way to download and install Sublime Wrap Plus is to use the [Package Control](https://packagecontrol.io) plugin.  If you do not already have it installed, it's really the best way to manage your packages.

For users new to the package manager:

* Go to https://packagecontrol.io/installation and install Package Control.
* Restart Sublime Text.

Install Sublime Wrap Plus:

* Bring up the Command Palette (<kbd>Command</kbd><kbd>Shift</kbd><kbd>P</kbd> on OS X, <kbd>Ctrl</kbd><kbd>Shift</kbd><kbd>P</kbd> on Linux/Windows).
* Select ***`Package Control: Install Package`*** and wait while Package Control fetches the latest package list.
* Select Wrap Plus when the list appears.

Package Control will handle automatically updating your packages.

Alternatively, you can fetch from Github:

```
git clone git://github.com/ehuss/Sublime-Wrap-Plus.git
```

and place it in your Packages directory, which can be found by selecting **`Preferences → Browse Packages...`**.

## Configuring ##
No need to configure anything.  By default it uses the default keystroke for wrap lines:

* Windows/Linux: <kbd>Alt</kbd><kbd>Q</kbd>
* OS X: <kbd>Command</kbd><kbd>Alt</kbd><kbd>Q</kbd>

If you want to use a different keystroke, go to **`Preferences → Key Bindings — User`**, and add an entry like this:

```javascript
{ "keys": ["alt+q"], "command": "wrap_lines_plus" }
```

If you want to, you can add keystrokes that use specific wrap sizes:

```javascript
{ "keys": ["alt+q", "7"], "command": "wrap_lines_plus", "args": {"width": 70}}
```

There are a few settings you can tweak if you so desire.  You can set them in **`Preferences → Settings — User`**.  They are:

<table>
    <tr>
        <th>Name</th><th>Default</th><th>Description</th>
    </tr>
    <tr>
        <td><code>"wrap_width"</code></td>
        <td>0</td>
        <td>The maximum line width.  If 0, defaults to the first ruler, or 78.  Also set via <b><code>View → Word Wrap Column</code></b>.</td>
    </tr>
    <tr>
        <td><code>"WrapPlus.wrap_width"</code></td>
        <td></td>
        <td>If set, this will override Sublime's <code>"wrap_width"</code> setting.  You might want to use this if you have automatic soft word wrapping enabled, but want hard wraps at a different width.
        </td>
    </tr>
    <tr>
        <td><code>"word_wrap"</code></td>
        <td><code>"auto"</code></td>
        <td>This disables horizontal scrolling (*soft* or *automatic* word wrapping).  May be <code>true</code>, <code>false</code>, or <code>"auto"</code> where it will be disabled for source code.  Also toggled via <b><code>View → Word Wrap</code></b>.</td>
    </tr>
    <tr>
        <td><code>"WrapPlus.break_long_words"</code></td>
        <td><code>true</code></td>
        <td>A single word that is longer than your wrap column will be forced to be break at the wrap column.</td>
    </tr>
    <tr>
        <td><code>"WrapPlus.break_on_hyphens"</code></td>
        <td><code>true</code></td>
        <td>Whether or not to break lines on hyphens.</td>
    </tr>
    <tr>
        <td><code>"WrapPlus.include_line_endings"</code></td>
        <td><code>"auto"</code></td>
        <td>Determines whether or not line endings are included in the line size:
            <ul>
                <li><code>true</code>: Always included.
                <li><code>false</code>: Never included.
                <li><code>"auto"</code>: Included only if Sublime's <code>"word_wrap"</code> is enabled (<b><code>View → Word Wrap</code></b>) and Sublime's wrap column is not 0 (<b><code>View → Word Wrap Column → Automatic</code></b>).
            </ul>
        </td>
    </tr>
</table>

### Advanced Configuration ###
Sublime supports placing configuration options in a variety of places.  You can put any of these settings in one of the following files (last file wins):

1. Packages/User/Preferences.sublime-settings
2. Project Settings (The "settings" key inside your project file.)
3. Packages/User/***SyntaxName***.sublime-settings
4. Packages/User/Distraction Free.sublime-settings

## Using ##
Whenever the cursor is anywhere within a paragraph, hitting the Wrap Plus keystroke will cause it to try to discover where the paragraph starts and where it ends.  It will then wrap all of those lines according to the wrap width you currently have set (**`View → Word Wrap Column`**).

### Lists ###
It handles a variety of lists, like bulleted lists or numbered lists. They should line up nicely:

```
- Kielbasa beef andouille chuck short loin, filet mignon jerky
    tail fatback ball tip meatloaf sausage spare ribs bresaola
    rump.
* Shankle shoulder ham, strip steak pastrami ground round shank
    sausage tail corned beef drumstick boudin bacon prosciutto
    turkey.
1. Jerky prosciutto pork loin shankle, corned beef capicola
     pork pastrami fatback short loin ground round.
        a. Sirloin fatback pancetta pork belly ham hock strip
             steak chuck, drumstick brisket chicken corned
             beef speck pig kielbasa short loin.
```

### Subsequent Indents ###
Lines with subsequent indents should maintain their indent:

```rst
:param cupcake: Cupcake ipsum dolor sit amet marzipan faworki.
        Wafer I love croissant. Tart carrot cake pastry applicake
        lollipop I love cotton brownie.
```

### Comment Lines ###
In a source code file, it should transparently handle single-line
comment characters, like:

```python
# Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
# Aenean commodo ligula eget dolor. Aenean massa. Cum sociis
# natoque penatibus et magnis dis parturient montes, nascetur
```

If you use block-style comments in C or C++, it will restrict the wrapping to only the contents in the comment (it won't jump out and wrap nearby code lines).  Also, if you use funny C block comments that start with an asterisk, that should be preserved:

```c
/*
 * This is a multiline C-style comment.  The asterisk characters on the
 * left should be preserved (when in C or C++ mode), if they are already
 * there.
 */
```

In addition, JavaDoc or JsDoc style documentation should work, too:

```java
/**
 * Sample function description.  Just in case the description is very long.
 * Cupcake ipsum dolor sit amet marzipan faworki. Wafer I love croissant. Tart
 * carrot cake pastry applicake lollipop I love cotton brownie.
 * @param {string} paramname Multi-line parameter description (or any javadoc
 *     tag) should indent with 4 spaces.  Cupcake ipsum dolor sit amet
 *     marzipan faworki. Wafer I love croissant. Tart carrot cake pastry
 *     applicake lollipop I love cotton brownie.
 */
```

### Python Strings ###
When wrapping inside a Python triple quoted string, wrapping will be constrained to the inside of the string.  That way, doc strings won't get wrapped with function definitions:


```python
def foo():
        """Pressing the wrap lines character while inside this string should wrap it
        nicely, without affecting the def foo line.
        """
```

### Email Quotes ###
Lines with email-style quoting should be handled.  Nested quotes should be treated as separate paragraphs.

```
> This is a quoted paragraph.
> > This is a nested quoted paragraph.  Wrapping the first paragraph won't
> > touch this paragraph.
> And continuing with a third paragraph.
```

### Selection Wrapping ###
If you select a range of characters, *only* the lines that are selected will be wrapped (the stock Sublime wrap lines extends the selection to what it thinks is a paragraph).  I find this behavior preferable to give me more control.

## Epilogue ##
Wrap Plus handles a lot of situations that the stock Sublime word wrapper doesn't handle, but it's likely there are many situations where it doesn't work quite right.  If you come across a problem, the immediate solution is to manually select the lines you want to wrap (this will constrain wrapping to just those lines).  If you'd like, feel free to post an [issue](https://github.com/ehuss/Sublime-Wrap-Plus/issues) on the Github page.

## License ##

This code is released under the MIT License. For more details see the [LICENSE](/LICENSE.txt) File.
