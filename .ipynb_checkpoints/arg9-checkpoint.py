import argparse
import getpass
import logging

import tableauserverclient as TSC


def main(i):
    i = '-s host -u rlp 189 --pdf -p bob'
    parser = argparse.ArgumentParser(description='Export a view as an image, pdf, or csv')
    parser.add_argument('--server', '-s', required=True, help='server address')
    parser.add_argument('--username', '-u', required=True, help='username to sign into server')
    parser.add_argument('--site', '-S', default=None)
    parser.add_argument('-p', default=None)

    parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                        help='desired logging level (set to error by default)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pdf', dest='type', action='store_const', const=('populate_pdf', 'PDFRequestOptions', 'pdf',
                                                                          'pdf'))
    group.add_argument('--png', dest='type', action='store_const', const=('populate_image', 'ImageRequestOptions',
                                                                          'image', 'png'))
    group.add_argument('--csv', dest='type', action='store_const', const=('populate_csv', 'CSVRequestOptions', 'csv',
                                                                          'csv'))

    parser.add_argument('--file', '-f', help='filename to store the exported data')
    parser.add_argument('--filter', '-vf', metavar='COLUMN:VALUE',
                        help='View filter to apply to the view')
    parser.add_argument('resource_id', help='LUID for the view')

    args = parser.parse_args()

    if args.p is None:
        password = getpass.getpass("Password: ")
    else:
        password = args.p

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)
    
    print(args)

if __name__ == '__main__':
    main(i)