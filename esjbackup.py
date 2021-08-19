#!/usr/bin/env python
#coding=utf-8

import requests
import lxml.html
import re

symbol_list = {
    "\\": "-",
    "/": "-",
    ":": "：",
    "*": "☆",
    "?": "？",
    "\"": " ",
    "<": "《",
    ">": "》",
    "|": "-",
    ".": "。",
    "\t": " ",
    "\n": " ",
}

def write_page(url, dst_file):
    r = requests.get(url)
    html_element = lxml.html.document_fromstring(r.text)
    if html_element.xpath('//h2'):
        title = html_element.xpath('//h2')[0]
        author = html_element.xpath('//div[@class="single-post-meta m-t-20"]/div')[0]
        content = html_element.xpath('//div[@class="forum-content mt-3"]')[0]
        with open(dst_file, 'a') as f:
            f.write('[' + title.text_content().encode('utf-8') + '] ' + author.text_content().strip().encode('utf-8') + '\n')
            f.write(content.text_content().encode('utf-8')+'\n\n')

def contain(string, array):
    if isinstance(array, dict):
        return any(symbol in string for symbol in array.keys())
    elif isinstance(array, list) or isinstance(array, tuple):
        return any(symbol in string for symbol in array)
    return False


def escape_symbol(string):
    while contain(string, symbol_list):
        for char, replace_char in symbol_list.items():
            string = string.replace(char, replace_char)
    return string


if __name__ == "__main__":

    novel_id = ''  # the novel id which you want to download
    r = requests.get('https://www.esjzone.cc/detail/' + novel_id + '.html')
    html_element = lxml.html.document_fromstring(r.text)

    novel_name = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content()
    dst_filename = escape_symbol(novel_name.encode('utf-8')) + ".txt"

    novel_details_element = html_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]')[0]
    bad_div = novel_details_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]/li/div')[0]
    bad_div.getparent().remove(bad_div)
    novel_details = novel_details_element.text_content()
    with open(dst_filename, 'w') as f:
        f.write(novel_details.encode('utf-8'))

    if re.search('id="details"', r.text):
        novel_description = html_element.get_element_by_id("details").text_content()
        with open(dst_filename, 'a') as f:
            f.write(novel_description.encode('utf-8'))
    else:
        with open(dst_filename, 'a') as f:
            f.write('\n\n')

    if re.search('id="chapterList"', r.text):
        chapter_list = html_element.get_element_by_id("chapterList").getchildren()
        
        for element in chapter_list:
    
            with open(dst_filename, 'a') as f:
                f.write(element.text_content().encode('utf-8')+'\n')
            
            if element.tag == 'a':

                if re.search(r'esjzone\.cc/forum/\d+/\d+\.html', element.attrib['href']):
                    write_page(element.attrib['href'],dst_filename)
                else:
                    with open(dst_filename, 'a') as f:
                        f.write(element.attrib['href'] + u' {非站內連結，略過}\n\n'.encode('utf-8'))



