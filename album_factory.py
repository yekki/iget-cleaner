def create_album(abbr):
    album = dict()

    if abbr == 'lyh':
        album['name'] = '罗永浩干货日记'
        album['author'] = '罗永浩'
        album['abbr'] = abbr
        album['season'] = dict(no='1', years={'2017': dict()})
    else:
        raise ValueError(f'no definition for album:{abbr}')

    return album
