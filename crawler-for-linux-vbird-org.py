import os
from urllib import (request, error)
from pyquery import PyQuery as pq
import pdfkit
from PyPDF2 import PdfFileMerger


def get_html(url):
    html = None
    try:
        html = request.urlopen(url, timeout=5)
    except error.URLError as e:
        print(e.reason)
    return html


def get_catalog(html):
    doc = pq(html.read().decode('utf-8'))
    block = doc('.block1').eq(0)
    catalog = [[a.text(), []] for a in block.items('a')]
    for i in range(len(catalog)):
        block = doc('.block1').eq(i + 1)
        for tr in block.items('tr'):
            chapter = tr('td').eq(0).children('a').text().replace('\n', '')
            link = tr('td').eq(0).children('a').attr('href')
            catalog[i][1].append([chapter, link])
    return catalog


def down_as_pdf(catalog):
    i = 0
    for part in catalog:
        for chapter in part[1]:
            print(('/pdf/ch%02d') % i)
            pdfkit.from_url(chapter[1], ('./pdf/ch%02d.pdf') % i)
            i = i + 1


def get_pdf_list(path):
    pdf_list = []
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        if '.pdf' in filename and not os.path.isdir(filename):
            pdf_list.append(filename)
    return pdf_list


def merge_pdf(catalog, pdf_list, output_path):
    bookmark_list = []
    i = 0
    for part in catalog:
        for chapter in part[1]:
            bookmark_list.append(('第%02d章 ' % i) + chapter[0])
            i = i + 1
    merger = PdfFileMerger()
    for i in range(len(pdf_list)):
        merger.append(open(pdf_list[i], 'rb'), bookmark=bookmark_list[i])
    with open(output_path, 'wb') as fout:
        merger.write(fout)


if __name__ == '__main__':
    html = get_html('http://cn.linux.vbird.org/linux_basic/linux_basic.php')
    catalog = get_catalog(html)
    # down_as_pdf(catalog)
    pdf_list = get_pdf_list('./pdf')
    pdf_list.sort()
    merge_pdf(catalog, pdf_list, '鸟哥的Linux私房菜：基础学习篇.pdf')