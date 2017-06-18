from pathlib import Path
import json

SOURCE_PATH = '/Users/gniu/(lyh)罗永浩干货日记'
DEST_PATH = '/Users/gniu/Temp.localized/lyh'
ALBUM_ABBR = 'lyh'

meta = dict()

meta['name'] = '罗永浩干货日记'
meta['author'] = '罗永浩'
meta['abbr'] = 'lyh'


def main():
    all_days = set([f.stem.replace(meta['abbr'], '')[0:4] for f in Path(SOURCE_PATH).glob('**/*.mp3') if
            f.is_file() and f.stem.startswith(ALBUM_ABBR)])
    months = dict.fromkeys(set(m[0:2] for m in all_days))
    season = dict(no='01', months=months)
    for m in months:
        days = list(filter(lambda x: x.startswith(m), all_days))
        episodes = list()
        for day in days:
            pics = [f.name for f in Path(SOURCE_PATH).glob('**/*.jpg') if
                    f.is_file() and f.stem.startswith(meta['abbr'] + day)]
            mp3s = [f.name for f in Path(SOURCE_PATH).glob('**/*.mp3') if
                    f.is_file() and f.stem.startswith(meta['abbr'] + day)]

            title = min(pics, key=len)
            title = title.replace(day, '')
            if title[-1].isdigit():
                title = title[:-1]
            episode = dict(day=day, title=title, mp3s=mp3s, pics=pics)
            episodes.append(episode)
        season['months'][m] = episodes


    meta['seasons'] = list()
    meta['seasons'].append(season)

    data = json.dumps(meta, ensure_ascii=False, indent=4)

    with open('meta.json', 'w', encoding='utf-8') as fp:
        fp.write(data)


if __name__ == '__main__':
    main()
