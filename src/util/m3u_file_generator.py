from src.util.file_generator import FileGenerator


class M3UFileGenerator(FileGenerator):

    def _content_header_template(self) -> str:
        return '#EXTM3U\n'

    def _content_body_template(self, items: list) -> str:
        return ("#EXTINF:-1 group-title=\"{0}\",{1}\n{2}\n"
                .format(FileGenerator.classify_channel(items[0]), items[0], items[1]))

    def _content_footer_template(self, items: list) -> str:
        return ""


if __name__ == '__main__':
    M3UFileGenerator().export([
        ('1', "aaa.bbb.ccc", 3),
        ('2', "aaa1.bbb.ccc", 4),
        ('3', "aaa2.bbb.ccc", 75),
        ('2', "aaa3.bbb.ccc", 7),
        ('3', "aaa4.bbb.ccc", 31),
        ('1', "aaa5.bbb.ccc", 35),
    ], "test.m3u")
