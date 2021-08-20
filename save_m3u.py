from os import name
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


def getm3u(url, path):
    rqs = urllib.request.urlopen(url, timeout=120)
    html = rqs.read().decode()
    soup = BeautifulSoup(html, 'lxml')
    atag = soup.find_all(lambda tag: tag.has_attr('href')
                         and tag.has_attr('rel'))
    for a in atag:
        m3u_url = a.attrs['href']
        if('.m3u' in m3u_url and len(a.attrs['rel']) == 1 and a.attrs['rel'][0] == 'nofollow'):
            # m3u_url_arr = m3u_url.split('/')
            # file_name = m3u_url_arr[len(m3u_url_arr)-1]
            # chinese_file_name = urllib.parse.unquote(file_name)
            chinese_file_name = a.text[:-1]
            m3u_rqs = urllib.request.urlopen(m3u_url, timeout=120)
            if '陕西电信' in chinese_file_name or '贵州联通' in chinese_file_name or '山东联通' in chinese_file_name:
                content = m3u_rqs.read().decode(encoding='cp1252')
            else:
                content = m3u_rqs.read().decode(encoding='utf-8')
            with open(path + '\\' + chinese_file_name, 'wt', encoding='utf-8') as f:
                f.write(content)
        else:
            print(m3u_url)


def getm3u_2(url, path):
    rqs = urllib.request.urlopen(url, timeout=120)
    html = rqs.read().decode()
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find_all(name='table')
    for index, table in enumerate(tables):
        path_folder = path + '\\Category' if index == 0 else (
            path + '\\Language' if index == 1 else path + '\\Country')
        thead = table.find(name='thead')
        tbody = table.find(name='tbody')
        for tr in tbody.find_all(name='tr'):
            tds = tr.find_all(name='td')
            title = tds[0].text
            count = tds[1].text
            m3u_url = tds[2].text
            m3u_url_arr = m3u_url.split('/')
            file_name = m3u_url_arr[len(m3u_url_arr)-1]
            m3u_rqs = urllib.request.urlopen(m3u_url, timeout=120)
            content = m3u_rqs.read().decode()
            file_path = path_folder + '\\' + title + '_' + count + '_' + file_name
            with open(file_path, 'wt', encoding='utf-8') as f:
                f.write(content)


url = 'https://github.com/imDazui/Tvlist-awesome-m3u-m3u8'
path = r'd:\kodi\China'
getm3u(url, path)


url = 'https://github.com/iptv-org/iptv'
path = r'd:\kodi'
getm3u_2(url, path)
