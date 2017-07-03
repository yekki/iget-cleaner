from parsers.base_parser import AlbumParser, Parser

def main():
    src = '/Users/gniu/get'
    dest = '/Users/gniu/Temp.localized/wj'

    parser = AlbumParser.create_parser(src, dest, Parser.WJ)
    parser.dump_meta()
    parser.handle_files()

if __name__ == '__main__':
    main()
