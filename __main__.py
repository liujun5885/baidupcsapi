import argparse
import os
import json
from pprint import pprint
import hashlib
import shutil

from application.api import PCS


def func_list(args, pcs):
    res = pcs.list_files(args.folder)
    pprint(json.loads(res.text))


def upload_file(path, dest, pcs):
    file_name = os.path.split(path)[-1]
    with open(path, 'rb') as fp:
        fmd5 = hashlib.md5(fp.read())
    with open(path, 'rb') as fp:
        res = pcs.upload(dest, fp, file_name)
        md5 = json.loads(res.text)['md5']
        if md5 == fmd5.hexdigest():
            shutil.rmtree(path, ignore_errors=True)
            print('OK, Baidupcsapi uploads "{}" onto "{}" as "{}"'.format(path, dest, file_name))
        else:
            print('ERR, Baidupcsapi uploads "{}" onto "{}" as "{}"'.format(path, dest, file_name))


def upload_folder(folder, dest, pcs):
    for i in os.listdir(folder):
        path = os.path.join(folder, i)
        if os.path.isdir(path):
            upload_folder(path, dest, pcs)
        else:
            upload_file(path, dest, pcs)


def func_upload(args, pcs):
    if os.path.isdir(args.path):
        upload_folder(args.path, args.folder, pcs)
    else:
        upload_file(args.path, args.folder, pcs)


parser = argparse.ArgumentParser(
    description='Crawl Safari Books Online book content',
)
parser.add_argument(
    '-u',
    '--username',
    help='Baidu user / e-mail address',
)
parser.add_argument(
    '-p',
    '--password',
    help='Baidu password',
)
parser.add_argument(
    '-c',
    '--cookie',
    default='',
    help='Baidu cookie',
)

subparsers = parser.add_subparsers()

download_parser = subparsers.add_parser(
    'upload',
    help='upload file to Baidu',
)
download_parser.set_defaults(func=func_upload)
download_parser.add_argument(
    dest='path', nargs='?'
)
download_parser.add_argument(
    '-f',
    '--folder',
    default='',
    help='Folder on Baidu',
)

list_parser = subparsers.add_parser(
    'list',
    help='List folder',
)
list_parser.add_argument(dest='folder', nargs='?')
list_parser.set_defaults(func=func_list)


def main():
    args = parser.parse_args()
    pcs = PCS(username=args.username, password=args.password, cookie=args.cookie)
    args.func(args, pcs)


if __name__ == '__main__':
    main()
