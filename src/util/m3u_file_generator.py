import file_generator


class M3UFileGenerator(file_generator.FileGenerator):

    def _content_header_template(self) -> str:
        return '#EXTM3U\n'

    def _content_body_template(self, items: list) -> str:
        return ("#EXTINF:-1 group-title=\"{0}\",{1}\n{2}\n"
                .format(FileGenerator.classify_channel(items[0]), items[0], items[1]))

    def _content_footer_template(self, items: list) -> str:
        return ""
