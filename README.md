Markdown Graphviz SVG (for Python 3 and ReText)
===============================================

This is a rewrite/continuation of the following modules:
 - `markdown-inline-graphviz`
 - `python-markdown-graphviz`
 - `markdown-dot`

At some point in the development of `python-markdown` the original method that these modules used to embed Graphviz was broken because the way it inserted the rendered SVG was dumb ([see:](https://github.com/cesaremorel/markdown-inline-graphviz/issues/6)).

I have poorly reimplemented the original functionality with the `BlockProcessors` class, this is a bit finnicky with the parsing of blocks (sometimes you need to use double newlines). But it is more robust than using the `Preprocessor` method.

I did not implement the PNG rendering functionality because I don't use it. If you want to make significantly smaller documents you might wish to implement SVGZ with the original PNG method from `python-markdown-graphviz`.

Because this uses the special `{% %}` syntax, it should be compatible with Jinja and other platforms that recognise it as such, however this is untested.

# Usage
 - Put this plugin in your $PYTHONPATH (I haven't added it to pip)
 - Add `markdown-graphviz-svg` to your extensions list in ReText's configuration
 - Use like this:

```
{% dot
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
%}
```

Where `dot` can be any of: `dot`, `neato`, `fdp`, `sfdp`, `twopi`, `circo`.

# KNOWN BUGS
 - Sometimes the block parser doesn't think you have made a separate block. **Insert two newlines above and below your code block to fix it.**
 - If you don't insert an ending `%}`, the parser will eat the rest of your document. I am not fixing this.

# Credits

- [jawher/markdown-dot](https://github.com/jawher/markdown-dot)
- [sprin/markdown-inline-graphviz](https://github.com/sprin/markdown-inline-graphviz)
- [cesaremorel/markdown-python-graphviz](https://github.com/cesaremorel/markdown-inline-graphviz)


# License
[MIT License](http://www.opensource.org/licenses/mit-license.php)
