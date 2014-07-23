__author__ = 'kevin'

import os

from django.template import Template, Context
from django.conf import settings

from formatters.base_formatter import BaseFormatter


class HtmlFormatter(BaseFormatter):

    def __init__(self, call_graph):
        super(HtmlFormatter, self).__init__(call_graph)

    def _get_template(self):
        template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template.html")
        settings.configure()

        return Template(open(template_file, 'r').read())

    def write_output(self):

        t = self._get_template()
        c = Context({ 'data': self })

        output = t.render(c)

        print(output)
