import file_generator


class TXTFileGenerator(file_generator.FileGenerator):

    def _content_header_template(self) -> str:
        return ""

    def _content_body_template(self, items: list) -> str:
        return "{0},{1}\n".format(items[0], items[1])

    def _content_footer_template(self, items: list) -> str:
        return ""

