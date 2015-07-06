from attacksurfacemeter.formatters.base_formatter import BaseFormatter


class XmlFormatter(BaseFormatter):
    """Produces an xml report with the attack surface metrics calculated by
    call_graph and prints it to console.
    """
    def __init__(self, call_graph):
        super(XmlFormatter, self).__init__(call_graph)

    @property
    def template_file(self):
        return "template.xml"

    @property
    def summary_template_file(self):
        return "summary_template.xml"
