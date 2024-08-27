from .file_generator import FileGenerator


class SampleFileGenerator(FileGenerator):

    def _content_header_template(self) -> str:
        return '#EXTM3U\n'

    def _content_body_template(self, items: list) -> str:
        if FileGenerator.classify_channel(items[0]).startswith("央视"):
            return ("#EXTINF:-1 group-title=\"{0}\",{1}\n{2}\n"
                    .format("CCTV", items[0], items[1]))
        return ""

    def _content_footer_template(self, items: list) -> str:
        return ""

