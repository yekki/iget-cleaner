from pathlib import Path
import json, os

SOURCE_PATH = '/Users/gniu/(lyh)罗永浩干货日记'
DEST_PATH = '/Users/gniu/Temp.localized/lyh'
ALBUM_ABBR = 'lyh'

meta = dict()

meta['name'] = '罗永浩干货日记'
meta['author'] = '罗永浩'
meta['abbr'] = 'lyh'


def get_files_from_dir(root, endswith):
    findings = list()
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith(endswith):
                findings.append(os.path.join(root, file))

    return findings

def get_months_zh(root, year):
    files = get_files_from_dir(root, '.mp3')
    months = set([Path(f).stem[0:5].replace('lyh', '') for f in files])
    months_zh = set([f'{year}年{mon}月' for mon in months])
    return months_zh

def get_months(root):
    files = get_files_from_dir(root, '.mp3')
    return set([Path(f).stem[0:5].replace('lyh', '') for f in files])


def get_days_in_month(root, month):
    mp3_files = set(get_files_from_dir(root, '.mp3'))

    return filter(lambda x: Path(x).stem.startswith(meta['abbr'] + month), mp3_files)


def generate_meta():
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


def main():
    mons = get_months_zh(SOURCE_PATH, '2017')
    print(mons.pop()[-3:-1])
if __name__ == '__main__':
    main()
