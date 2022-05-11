import os
import shutil
from urllib.parse import urlparse
from zipfile import ZipFile

import requests
import wget
from bs4 import BeautifulSoup



def is_new_file(file_name):
    files = db["files"]
    try:
        files.insert_one({'_id': file_name})
        return True
    except:
        return False


def search_sub(search, website, type='film'):# finished
    def baiscopelk_search(search, type='film'):
        urls = {'tv': 'tv/page/', 'film': 'සිංහල-උපසිරැසි/චිත්‍රපටි/page/'}
        baiscopelk_url = "https://www.baiscopelk.com/category/" + urls[type]
        url = baiscopelk_url + str(search)
        print(url)
        request_result = requests.get(url)
        soup = BeautifulSoup(request_result.text, "html.parser")
        site_items = soup.find_all('h2', {"class": "post-box-title"})
        links = []
        titles = []
        for x in range(len(site_items)):
            if "mega-menu-link" in str(site_items[x]) or "rel=\"bookmark\"" in str(site_items[x]) or "ttip" in str(
                    site_items[x]):
                pass
            else:
                htmldata = str(site_items[x])
                page_soup1 = BeautifulSoup(htmldata, "html.parser")
                hreflink = page_soup1.findAll('a')
                if len(hreflink) != 0:
                    links.append(hreflink[0]['href'])
                    titles.append(hreflink[0].getText())
        return {"title": titles, 'link': links}

    def upasirasi_search(search, type='film'):
        urls = {'tv': 'eps/page/', 'film': 'category/films/page/'}
        upasirasi_url = 'https://www.upasirasi.com/' + urls[type] + str(search)
        r = requests.get(upasirasi_url)
        soup = BeautifulSoup(r.text, "html.parser")
        files = soup.find_all('h2', {'class': 'entry-title'})
        links = []
        titles = []
        for i in files:
            links.append(i.find_all('a')[0]['href'])
            titles.append(i.find_all('a')[0].getText())
        return {"title": titles, 'link': links}

    def pirate_search(search, type='film'):
        urls = {'tv': 'tv-1/page/', 'film': 'සිංහල-උපසිරැසි/චිත්‍රපටි/page/'}
        pirate_url = "https://piratelk.com/category/" + urls[type]
        url = pirate_url + str(search)
        print(url)
        request_result = requests.get(url)
        soup = BeautifulSoup(request_result.text, "html.parser")
        site_items = soup.find_all('h2', {"class": "post-box-title"})

        links = []
        titles = []
        for x in range(len(site_items)):
            htmldata = str(site_items[x])
            page_soup1 = BeautifulSoup(htmldata, "html.parser")
            hreflink = page_soup1.findAll('a')
            if len(hreflink) != 0:
                links.append(hreflink[0]['href'])
                titles.append(hreflink[0].getText())
        return {"title": titles, 'link': links}

    def cineru_search(search, type='film'):
        urls = {'tv': 'රුපවාහිනී-කතාමාලා/page/', 'film': 'films/page/'}
        cineru_url = "https://cineru.lk/category/ඔක්කොම-එකට/" + urls[type]
        url = cineru_url + str(search)
        print(url)
        request_result = requests.get(url)
        soup = BeautifulSoup(request_result.text, "html.parser")
        site_items = soup.find_all('h2', {"class": "post-box-title"})

        links = []
        titles = []
        for x in range(len(site_items)):
            htmldata = str(site_items[x])
            page_soup1 = BeautifulSoup(htmldata, "html.parser")
            hreflink = page_soup1.findAll('a')
            if len(hreflink) != 0:
                links.append(hreflink[0]['href'])
                titles.append(hreflink[0].getText())
        return {"title": titles, 'link': links}

    if website == "baiscopelk":
        try:
            return baiscopelk_search(search, type)
        except:
            return None
    elif website == 'pirate':
        try:
            return pirate_search(search, type)
        except:
            return None
    elif website == 'cineru':
        try:
            return cineru_search(search, type)
        except:
            return None
    elif website == 'upasirasi':
        try:
            return upasirasi_search(search, type)
        except:
            return None
    else:
        return None


def compressed_file_downloader(url):
    def return_sub_Names():
        file_names = []
        for path, subdirs, files in os.walk("Extract"):
            for name in files:
                x = 0
                rems = ['.htm', '.html', '.txt', '.jpeg', '.jpg', 'png']
                for rem in rems:
                    if rem in name:
                        x = 1
                if " @gt_subs" in name:
                    x = 1
                if x == 0:
                    _file_name = name.strip()
                    file_ex = _file_name[_file_name.rindex('.'):]
                    new_file_name = _file_name.replace("cineru", "").replace(file_ex, "") + " @gt_subs" + file_ex
                    os.rename(os.path.join(path, _file_name), os.path.join(path, new_file_name))
                    file_names.append(os.path.join(path, new_file_name))
        return file_names
    a = urlparse(url)
    file_name = os.path.basename(a.path)
    if file_name == "":
        file_name = str(a.path).replace("/Downloads/", "").replace("-zip/", ".zip").replace("-rar/", ".rar")
        file_name = file_name.replace('/download/',"").replace("/","")
    if '.zip' in file_name or '.rar' in file_name:
        pass
    else:
        file_name = file_name + ".zip"
    try:
        wget.download(url, file_name)
    except:
        import urllib.request
        opener = urllib.request.build_opener()
        opener.addheaders = [('user-agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/77.0.3865.90 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, file_name)
    try:
        os.makedirs('Extract')
    except:
        pass
    try:
        print(file_name)
        ZIP = ZipFile(file_name, 'r')
        ZIP.extractall('Extract')
        ZIP.close()
        os.remove(file_name)
    except:
        old_file_name = file_name
        file_name = file_name.replace('.zip', '.rar')
        shutil.copyfile(old_file_name, 'Extract/'+file_name)
        os.remove(old_file_name)
    return return_sub_Names()


def download(url, name):# finished
    r1 = requests.get(url)
    html_data = r1.text
    soup = BeautifulSoup(html_data, 'html.parser')

    def cineru():
        links = soup.select('a[data-link]')
        try:
            for i in links:
                lin = str(i)
                link = lin[lin.index('data-link="') + 11:lin.index('" href')]
                return link
        except Exception as e:
            print(e)
            return "error"

    def baiscopelk():
        links = soup.find_all("p", {"style": "padding: 0px; text-align: center;"})
        try:
            for i in links:
                lin = str(i)
                link = lin[lin.index('<a href="') + 9:lin.index('"><img ')]
                return link
        except Exception as e:
            print(e)
            return "error"

    def piratelk():
        links = soup.find_all("a", {"class": "aligncenter download-button"})
        try:
            for i in links:
                lin = str(i)
                link = lin[lin.index('href="') + 6:lin.index('" rel')]
                return link
        except Exception as e:
            print(e)
            return "error"

    def upasirasi(soup):
        links = soup.find_all('div', {'id': 'download'})[0].find_all('a', {'class': 'button button-shadow'})[0]['href']

        try:
            if 'wobomart' in links:
                link = str(links).replace('view/', 'view/m1.php?id=')
                r1 = requests.get(link)
                html_data = r1.text
                soup = BeautifulSoup(html_data, 'html.parser')
                links = soup.find_all('a', {'id': 'download'})[0]['href']
                print(links)
                return links
            else:
                print(links)
                return links
        except Exception as e:
            print(e)
            return "error"

    sites = ["https://cineru.lk", "https://www.baiscopelk.com", "https://piratelk.com",'https://www.upasirasi.com']
    if sites[0] in url:
        site_message = cineru()
    elif sites[1] in url:
        site_message = baiscopelk()
    elif sites[2] in url:
        site_message = piratelk()
    else:
        site_message = upasirasi(soup)
    return compressed_file_downloader(site_message)