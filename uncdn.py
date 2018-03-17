#!/usr/bin/env python3

import os
import re

from argparse import ArgumentParser

OUTPUT_FOLDERNAME = 'external'
OUTPUT_LINKS_FILENAME = 'links.txt'

def get_file_list(directories_to_skip):
    files_to_scan = []
    for dirpath, dirnames, filenames in os.walk('.'):
        omit = False
        for skippable_dir in directories_to_skip:
            if skippable_dir in dirpath:
                omit = True
        if omit:
            continue
        for filename in filenames:
            files_to_scan.append(os.path.join(dirpath, filename))
    return files_to_scan

def external_urls(filename, url_pattern):
    print('Processing file %s...' % filename)
    with open(filename) as f:
        for line in f.readlines():
            match = url_pattern.search(line)
            if match:
                yield add_prefix_if_needed(match.group(0))

def add_prefix_if_needed(url):
    if url.startswith('//'):
        return 'http:' + url
    return url

def filename_for(url):
    return url.split('/')[-1]

def scrape(args):
    directories_to_skip = args.exclude
    url_pattern = re.compile(args.pattern)

    # Get all external asset urls
    urls = []
    for filename in get_file_list(directories_to_skip):
        urls.extend(external_urls(filename, url_pattern))
    urls = sorted(set(urls))

    # Save file list
    with open(OUTPUT_LINKS_FILENAME, 'w') as file_list:
        for url in urls:
            file_list.write(url + "\n")
            print('wrote url ' + url)

def download_assets(args):
    if not os.path.exists(OUTPUT_FOLDERNAME):
        os.mkdir(OUTPUT_FOLDERNAME)
    os.chdir(OUTPUT_FOLDERNAME)
    # TODO: Switch to a more portable approach
    os.system('wget -c -i ../' + OUTPUT_LINKS_FILENAME)
    os.chdir('..')

def internalize(args):
    data = []
    directories_to_skip = args.exclude

    with open(OUTPUT_LINKS_FILENAME) as file_list:
        for external_url in file_list.readlines():
            filename = external_url.strip().split('/')[-1]
            current_file_was_downloaded = os.path.exists(os.path.join(OUTPUT_FOLDERNAME, filename))
            data.append((external_url.strip(), filename, current_file_was_downloaded))

    for filename in get_file_list(directories_to_skip):
        if not filename.endswith('.tmp'):
            print('Processing %s...' % filename)
            with open(filename, 'r') as infile, open(filename + ".tmp", 'w') as outfile:
                content = infile.read()
                for datum in data:
                    if datum[2]:
                        new_internal_path = '/%s/%s' % (OUTPUT_FOLDERNAME, datum[1])
                        external_url = datum[0]

                        # print('replacing %s for %s ' % (external_url, new_internal_path))
                        content = content.replace(external_url, new_internal_path)

                        # for // urls
                        content = content.replace(external_url[5:], new_internal_path)
                outfile.write(content)

            os.rename(filename + '.tmp', filename)


def main():
    parser = ArgumentParser(
        description='an external resource downloader from source code'
    )

    subparsers = parser.add_subparsers(
        title='subcommands',
        description='Valid subcommands',
        help='Usually you want to run `scrape` first, `download` the assets, and then `internalize` the project',
        dest='parser'
    )
    subparsers.required = True

    # parser for 'scrape' action
    scrape_parser = subparsers.add_parser('scrape')
    scrape_parser.add_argument('--exclude', default=['.git', '.vscode', 'bower_components', 'node_modules', OUTPUT_FOLDERNAME])
    scrape_parser.add_argument('--pattern', default='(http(s)?:)?//(\w|\.|/|:|\-|\d|=|\?)+\.(svg|png|jpg|jpeg|js|css|ico|gif)')
    scrape_parser.set_defaults(func=scrape)

    # parser for 'download' action
    download_parser = subparsers.add_parser('download')
    download_parser.set_defaults(func=download_assets)

    # parser for 'internalize'
    internalize_parser = subparsers.add_parser('internalize')
    internalize_parser.add_argument('--exclude', default=['.git', '.vscode', 'bower_components', 'node_modules', OUTPUT_FOLDERNAME, 'links.txt'])
    internalize_parser.set_defaults(func=internalize)

    args = parser.parse_args()

    args.func(args)




if __name__ == '__main__':
    main()
