from pathlib import Path
import json, os

SOURCE_PATH = '/Users/gniu//(lyh)罗永浩干货日记'
DEST_PATH = '/Users/gniu/Temp.localized/lyh'

meta = dict()
meta['name'] = '罗永浩干货日记'
meta['author'] = '罗永浩'
meta['abbr'] = 'lyh'
meta['seasons'] = [dict(no='1', months=list())]


class AlbumParser:
    def __init__(self, root, title, author, abbreviation, year, season_no):
        self._title = title
        self._author = author
        self._abbreviation = abbreviation
        self._root = root
        self._season_no = season_no
        self._year = year
        self._files = list()

        for root, dirs, files in os.walk(self._root):
            for file in files:
                self._files.append(Path(os.path.join(root, file)))

    def files(self, prefix=None, suffix=None):

        if suffix and prefix:
            return set(filter(lambda x: x.suffix == suffix and x.stem.startswith(prefix), self._files))
        elif prefix:
            return set(filter(lambda x: x.stem.startswith(prefix), self._files))
        elif suffix:
            return set(filter(lambda x: x.suffix == suffix, self._files))
        else:
            return self._files

    def months(self):
        mp3s = self.files(suffix='.mp3')
        func = lambda x: self._year + '年' + x.stem[0:len(self._abbreviation) + 2].replace(self._abbreviation, '') + '月'

        return set(map(func, mp3s))

    def episodes(self):
        pass

    def episodes_in_month(self, month):
        days = set([f.stem for f in self.files(suffix='.mp3', prefix=f'{self._abbreviation}{month}')])
        episodes = dict()
        for d in days:
            index = len(self._abbreviation)
            episodes[d[index:]] = self.media(d)

        return episodes

    def media(self, prefix):
        mp3s = list(self.files(prefix=prefix, suffix='.mp3'))
        pics = list(self.files(prefix=prefix, suffix='.jpg'))

        title = pics[0].stem
        title = title[title.index('第'):]

        if title[-1].isdigit():
            title = title[:-1]

        return dict(title=title, mp3s=[f.name for f in mp3s], pics=[f.name for f in pics])

    def dump_to_file(data, output='meta.json'):
        data = json.dumps(meta, ensure_ascii=False, indent=4)

        with open('meta.json', 'w', encoding='utf-8') as fp:
            fp.write(data)


def main():
    album = AlbumParser(SOURCE_PATH, '罗永浩干货日记', '罗永浩', 'lyh', '2017', '01')
    print(album.episodes_in_month('05'))


if __name__ == '__main__':
    main()
