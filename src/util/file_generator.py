from pathlib import Path


class FileGenerator:

    def __init__(self, candidate_count: int = 8):
        self.candidate_count = candidate_count

    @classmethod
    def classify_channel(cls, channel_name: str) -> str:
            if 'cctv' in channel_name.lower():
                return "央视频道"
            elif '卫视' in channel_name:
                return "卫视频道"
            else:
                return "其他频道"

    def _content_header_template(self) -> str:
        pass

    def _content_body_template(self, items: list) -> str:
        pass

    def _content_footer_template(self, items: list) -> str:
        pass

    def export(self, raw_data: list[tuple], file_name: str):
        OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"
        with open(OUTPUT_DIR / file_name, 'w', encoding='utf-8') as m3uFileHandler:
            counterMap = dict()
            m3uFileHandler.write(self._content_header_template())
            for (name, url, _) in raw_data:
                if name in counterMap:
                    if counterMap.get(name) < self.candidate_count:
                        m3uFileHandler.write(self._content_body_template([name, url]))
                        m3uFileHandler.write(self._content_footer_template([name, url]))
                        counterMap.update({name: counterMap.get(name) + 1})
                    else:
                        continue
                else:
                    m3uFileHandler.write(self._content_body_template([name, url]))
                    m3uFileHandler.write(self._content_footer_template([name, url]))
                    counterMap.setdefault(name, 1)
