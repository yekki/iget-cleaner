from album_factory import create_album
from parsers.lyh_parser import LYHParser


def main():
    SOURCE_PATH = '/Users/gniu//(lyh)罗永浩干货日记'
    DEST_PATH = '/Users/gniu/Temp.localized/lyh'

    album = create_album('lyh')
    parser = LYHParser(SOURCE_PATH, DEST_PATH, album)
    parser.dump_meta()
    parser.check_meta()
    parser.handle_files()

if __name__ == '__main__':
    main()
