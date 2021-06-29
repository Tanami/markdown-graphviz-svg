import re

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown import util
import xml.etree.ElementTree as etree
import subprocess

class GraphvizBlocksExtension(Extension):
    def __init__(self, **kwargs):
        super(GraphvizBlocksExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add GraphvizBlocks to the Markdown instance. """
        md.registerExtension(self)

        processor = GraphvizBlocks(md.parser)
        processor.config = self.getConfigs()
        processor.md = md
        md.parser.blockprocessors.register(processor, 'graphvizblocks', 150)

class GraphvizBlocks(BlockProcessor):
    BLOCK_RE = re.compile(
        r'\{% (?P<command>\w+)\n(?P<content>.*?)%}\s*',
        re.MULTILINE | re.DOTALL)

    SUPPORTED_COMMAMDS = ['dot', 'neato', 'fdp', 'sfdp', 'twopi', 'circo']

    IN_GRAPH = 0
    ACCUM = ""

    def test(self, parent, block):
        if block.startswith('{%'):
            self.IN_GRAPH = 1
            return 1
        elif block.endswith('%}'):
            self.IN_GRAPH = 0
            self.RUN_GRAPH = 1
            return 1
        elif self.IN_GRAPH == 1:
            return 1
        else:
            return 0

    def run(self, parent, blocks):
        block = blocks.pop(0)
        if self.IN_GRAPH == 1:
            self.ACCUM += "\n" + block
        elif self.RUN_GRAPH == 1:
            self.ACCUM += "\n" + block
            self.RUN_GRAPH = 0
            # print(self.ACCUM)
            m = self.BLOCK_RE.search(self.ACCUM)
            # print(m)
            if m:
                command = m.group('command')
                content = m.group('content')
                try:
                    if command not in self.SUPPORTED_COMMAMDS:
                        raise Exception('Command not supported: %s' % command)

                    proc = subprocess.Popen(
                        [command, '-Tsvg'],
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE)
                    proc.stdin.write(content.encode('utf-8'))

                    output, err = proc.communicate()

                    if err:
                        raise Exception(err)

                    data_url_filetype = 'svg+xml'
                    encoding = 'utf-8'
                    img = output.decode(encoding)

                    div = etree.SubElement(parent, 'div')

                    # this trims the doctype tag, albeit poorly
                    start = img.index("<svg")
                    div.text = img[start:]
                    self.ACCUM = ''

                except Exception as e:
                        div = etree.SubElement(parent, 'h3')
                        div.text = '<pre style="color:red">Error : ' + str(e) + '</pre>'

def makeExtension(**kwargs):  # pragma: no cover
    return GraphvizBlocksExtension(**kwargs)
