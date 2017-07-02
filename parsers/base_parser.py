import json, os, shutil, logging
from pathlib import Path

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

class AlbumParser:
    _KEYS = set(['name', 'author', 'abbr', 'season'])

    def __init__(self, src, dest, album):
        self._src = src
        self._dest = dest
        self._album = album

        if not all(k in self._album for k in AlbumParser._KEYS):
            raise KeyError(f'parameter album lost key in one of {AlbumParser._KEYS}')

    def get_episode(self, day):
        mp3s = sorted(list(self.find_all(prefix=day, suffix='.mp3')))
        pics = sorted(list(self.find_all(prefix=day, suffix='.jpg')))

        if len(pics) < 1:
            logging.debug(f'no pics for {day}')
            return None
        else:
            title = self.get_title(pics[0].stem, day)
            return dict(title=title, mp3s=[f.name for f in mp3s], pics=[f.name for f in pics])

    def get_days_by_month(self, month):
        days = set([f.stem.replace(self._album["abbr"], '') for f in
                    self.find_all(suffix='.mp3', prefix=month)])
        return sorted(list(days))

    def get_months(self):
        mp3s = self.find_all(suffix='.mp3')
        months = set([f.stem[0:len(self._album['abbr']) + 2].replace(self._album['abbr'], '') for f in mp3s])

        return sorted(list(months))

    def get_title(self, t, day):
        if '第' in t:
            title = t[t.index('第'):]
        else:
            title = t[t.index(day)+len(day):]

        if title[-1].isdigit():
            return title[:-1]
        else:
            return title

    def get_episodes(self, year):
        episodes = dict()
        months = self.get_months()

        for m in months:
            episodes_in_month = dict()
            days = self.get_days_by_month(m)
            for d in days:
                episode = self.get_episode(d)
                if episode:
                    episodes_in_month[d] = self.get_episode(d)
            episodes[f'{year}年{m}月'] = episodes_in_month

        return episodes

    def check_meta(self, meta_file='meta.json'):
        all_files = set([f.name for f in self.find_all()])

        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)

        files = list()

        for year in meta['season']['years']:
            for month in meta['season']['years'][year]:
                for day in meta['season']['years'][year][month]:
                    files.extend(meta['season']['years'][year][month][day]['pics'])
                    files.extend(meta['season']['years'][year][month][day]['mp3s'])

        for f in files:
            if f not in all_files:
                raise FileNotFoundError(f)

    def dump_meta(self, output='meta.json'):

        for year in self._album['season']['years']:
            self._album['season']['years'][year] = self.get_episodes(year)

        data = json.dumps(self._album, ensure_ascii=False, indent=4)
        with open(output, 'w', encoding='utf-8') as fp:
            fp.write(data)

        with open(os.path.join(self._dest, output), 'w', encoding='utf-8') as fp:
            fp.write(data)

    def handle_files(self, meta_file='meta.json'):
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)

        for year in meta['season']['years']:
            mkdir(os.path.join(self._dest, year))
            for month in meta['season']['years'][year]:
                mkdir(os.path.join(self._dest, year, month))
                for day in meta['season']['years'][year][month]:
                    mkdir(os.path.join(self._dest, year, month, day))
                    for pic in meta['season']['years'][year][month][day]['pics']:
                        shutil.copy2(self.find(pic), os.path.join(self._dest, year, month, day))
                    for mp3 in meta['season']['years'][year][month][day]['mp3s']:
                        shutil.copy2(self.find(mp3), os.path.join(self._dest, year, month, day))

    def find(self, name):
        for root, dirs, files in os.walk(self._src):
            if name in files:
                return os.path.join(root, name)

    def find_all(self, prefix=None, suffix=None):
        _files = list()

        for root, dirs, files in os.walk(self._src):
            for file in files:
                if not file.startswith('.'):
                    _files.append(Path(os.path.join(root, file)))

        if suffix and prefix:
            return set(filter(lambda x: x.suffix == suffix and x.stem.startswith(f"{self._album['abbr']}{prefix}"), _files))
        elif prefix:
            return set(filter(lambda x: x.stem.startswith(f"{self._album['abbr']}{prefix}"), _files))
        elif suffix:
            return set(filter(lambda x: x.suffix == suffix and x.stem.startswith(f"{self._album['abbr']}"), _files))
        else:
            return _files
