from application.api import PCS
from pprint import pprint
import json
pcs = PCS('juneggyy@126.com','2819413lJ..')
res = pcs.list_files('/books/Safari')
pprint(json.loads(res.text))
with open('README.md', 'rb') as fp:
    res = pcs.upload('/books/Safari', fp, 'README.md')
    pprint(json.loads(res.text))
