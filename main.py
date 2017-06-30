from pathlib import Path
import json, os


def filter_files(root, prefix=None, suffix=None):
    _files = list()

    for root, dirs, files in os.walk(root):
        for file in files:
            _files.append(Path(os.path.join(root, file)))

    if suffix and prefix:
        return set(filter(lambda x: x.suffix == suffix and x.stem.startswith(prefix), _files))
    elif prefix:
        return set(filter(lambda x: x.stem.startswith(prefix), _files))
    elif suffix:
        return set(filter(lambda x: x.suffix == suffix, _files))
    else:
        return _files


def get_episodes_in_month(root, album, month):
    days = set([f.stem for f in filter_files(root, suffix='.mp3', prefix=f'{album["abbr"]}{month}')])
    episodes = dict()
    for d in days:
        index = len(album['abbr'])
        episodes[d[index:]] = get_episode(root, d)

    return episodes


def get_episode(root, prefix):
    mp3s = list(filter_files(root, prefix=prefix, suffix='.mp3'))
    pics = list(filter_files(root, prefix=prefix, suffix='.jpg'))

    title = pics[0].stem
    title = title[title.index('第'):]

    if title[-1].isdigit():
        title = title[:-1]

    return dict(title=title, mp3s=[f.name for f in mp3s], pics=[f.name for f in pics])


def get_episodes(root, album, year):
    mp3s = filter_files(root, suffix='.mp3')
    months = [f.stem[0:len(album['abbr']) + 2].replace(album['abbr'], '') for f in mp3s]
    episodes = dict()

    for m in months:
        episodes[f'{year}年{m}月'] = get_episodes_in_month(root, album, m)

    return episodes


def build(root, album, year, output='meta.json'):
    album['season']['years'][year] = get_episodes(root, album, 2017)
    data = json.dumps(album, ensure_ascii=False, indent=4)
    with open('meta.json', 'w', encoding='utf-8') as fp:
        fp.write(data)

    print('finished.')


def main():
    SOURCE_PATH = '/Users/gniu//(lyh)罗永浩干货日记'
    DEST_PATH = '/Users/gniu/Temp.localized/lyh'

    album = dict()
    album['name'] = '罗永浩干货日记'
    album['author'] = '罗永浩'
    album['abbr'] = 'lyh'
    album['season'] = dict(no='1', years={'2017': dict()})


    build(SOURCE_PATH, album, '2017')


if __name__ == '__main__':
    main()
