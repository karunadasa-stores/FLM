from pyrogram import Client
import pyrogram
import urllib.parse
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import urllib
from pack_downloader import compressed_file_downloader
from info import (
    bot_username
)
from urllib.parse import quote
from info import database_channel




def create_client(session_name, api_id, api_hash, phone_number=None, bot_token=None):
    try:
        client = Client(
            session_name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone_number,
            bot_token=bot_token
        )
        return client
    except Exception as e:
        return "Error in create_client :\n" + str(e)


def send_to_admin(client, admin_ids, text=None):
    for i in admin_ids:
        try:
            client.send_message(i, text)
        except:
            pass


# save user
Mclient = MongoClient("mongodb+srv://GavinduTharaka:Gavindu123@sinhalasubdownbot.1v9ix.mongodb.net/Bot?retryWrites"
                      "=true&w=majority")
db = Mclient["Bot"]


def save_user(client, message, admin_ids):
    try:
        userid = message.chat.id
        username = message.chat.username
        users = db["all_users"]
        x = {}
        results = users.find({"_id": str(userid)})
        for result in results:
            x = result["_id"]
        if str(userid) != str(x):
            users.insert_one({'_id': userid, 'username': "@" + str(username), 'type': message.chat.type, 'refcount': 0})
            print("New Data Added")
            if message.chat.type == 'private':
                send_to_admin_message = "<b>New User Added</b>\n🔘 ID : {}\n🔘 Name : {}\n🔘 User Name : {}\n🔘 Status : " \
                                        "{}".format(
                    message.chat.id, message.chat.first_name, message.chat.username, message.from_user.status)
                send_to_admin(client, admin_ids, send_to_admin_message)
            else:
                send_to_admin_message = "<b>New Group Added</b>\n🔘 ID : {}\n🔘 Name : {}\n🔘 User Name : {}\n🔘 Group Type : " \
                                        "{}".format(
                    message.chat.id, message.chat.title, message.chat.username, message.chat.type)
                send_to_admin(client, admin_ids, send_to_admin_message)
    except Exception as e:
        print("Saved User")


def get_all_users(type=None):
    users = db["all_users"]
    _ids = []
    if type is None:
        results = users.find()
    else:
        results = users.find({"type": str(type)})
    for result in results:
        _ids.append(result['_id'])
    return _ids


# buttons
def buttons(button_as_dictionary):
    def rows(lines):
        button = []
        for b in lines:
            buto = []
            for i in b.keys():
                '''if "query" in b[i]:
                    buto.append(pyrogram.types.InlineKeyboardButton(  # Generates a callback query when pressed
                        i,
                        callback_data=None,
                        url=None,
                        switch_inline_query_current_chat=b[i].replace("query", "")
                    ))
                    continue'''
                if '/' in b[i] or '.' in b[i]:
                    buto.append(pyrogram.types.InlineKeyboardButton(  # Generates a callback query when pressed
                        i,
                        callback_data=None,
                        url=b[i]
                    ))
                else:
                    buto.append(pyrogram.types.InlineKeyboardButton(  # Generates a callback query when pressed
                        i,
                        callback_data=b[i],
                        url=None
                    ))
            button.append(buto)
        return button

    reply_markup = pyrogram.types.InlineKeyboardMarkup(
        rows(button_as_dictionary)
    )
    return reply_markup


# channels and groups
def search_message(client, chat_id, query, filter=None, limit=None):
    try:
        data = []
        for msg in client.search_messages(chat_id=chat_id, filter=filter, query=query, limit=limit):
            data.append(msg)
        return data
    except Exception as e:
        return "Error in search_message :\n" + str(e)


def get_members(client, chat_id, _filter=None):
    try:
        if _filter is None:
            members = client.get_chat_members(chat_id)
        else:
            members = client.get_chat_members(chat_id, filter=_filter)
        return members
    except Exception as e:
        return "Error in get_members :\n" + str(e)


def get_admins(client, chat_id):
    admins = client.get_chat_members(chat_id, filter="administrators")
    return admins


def get_member_ids(members):
    ids = []
    for i in range(len(members)):
        ids.append(members[i]['user']['id'])
    return ids


def is_subcriber(client, channel_id, user_id):
    if user_id in get_member_ids(get_members(client, channel_id)):
        return True
    else:
        return False


# Document
def get_documents(client, chat_id, query, limit=300):
    documents = search_message(client, chat_id, query, filter='document', limit=limit)
    files = {}
    for i in range(len(documents)):
        file_name = documents[i]['document']['file_name']
        message_id = documents[i]['message_id']
        file_size = documents[i]['document']['file_size']
        file_unique_id = documents[i]['document']['file_unique_id']
        caption = documents[i]['caption'].replace("SinhalaSubDown", "")
        files[file_name] = [message_id, caption, file_size, file_unique_id]
    sorted_keys = sorted(files.keys())
    sorted_files = {}
    for i in sorted_keys:
        sorted_files[i] = files[i]
    return sorted_files


def format_bytes(size):
    # 2**10 = 1024
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size //= power
        n += 1
    return str(size) + power_labels[n] + 'B'


def jump(variable, query, type, condition=True, number=0, math=10):
    if condition:
        button = InlineKeyboardButton(
            text=variable,
            callback_data='jump{}{}?{}'.format(type,query, number + math)
        )
        return button


def add_button(text, call_back, url=None):
    if url is not None:
        button = InlineKeyboardButton(
            text=text,
            url=url
        )
    else:
        button = InlineKeyboardButton(
            text=text,
            callback_data=call_back
        )
    return [button]


def sub_button(search_message, query, number=0):
    button = []
    keys = []
    for x in search_message.keys():
        keys.append(x)
    try:
        for key in keys[number:number + 10]:
            fileSize = search_message[key][0]
            file_unique_id = search_message[key][-1]
            fileName = str(key).replace("@SinhalaSubDown_Bot", " ").replace("-", " ").replace("_","")
            if len(fileName) > 24:
                fileName = fileName[:20] + "..."
            text = "[{}] {} ".format(str(format_bytes(fileSize)), fileName)
            call_data = urllib.parse.quote('query?{}file?{}'.format(query, file_unique_id))
            b = [  # First row
                InlineKeyboardButton(
                    text,
                    callback_data=call_data
                )
            ]
            button.append(b)
    except:
        pass
    b2 = []
    next = jump('Next', query, "p", len(search_message) > 10 and len(search_message) - number > 10, math=10, number=number)
    previous = jump('Previous', query, "p", len(search_message) - 10 > 0 and number > 0, math=-10, number=number)
    if previous is not None:
        b2.append(previous)
    if next is not None:
        b2.append(next)
    if b2 is not None:
        button.append(b2)

    if len(search_message) == 0:
        button.append(add_button(" ⛔ Report to Admin ", "report?{}".format(query)) + add_button(" Search Global 🌐 ",
                                                                                                "global?{}".format(
                                                                                                    query)))
    else:
        pages = "📄 Pages [ {}/{} ] ".format((number // 10) + 1, (len(search_message) // 10) + 1)
        button.append(add_button(pages, "sinhalasubdown"))
        button.append(add_button(" ⛔ Report to Admin ", "report?{}".format(query)) + add_button(" Search Global 🌐 ",
                                                                                                "global?{}".format(
                                                                                                    query)))
    reply_markup = InlineKeyboardMarkup(button)
    return reply_markup


def sub_button_g(search_message, query, number=0):
    button = []
    keys = []
    for x in search_message.keys():
        keys.append(x)
    try:
        for key in keys[number:number + 10]:
            fileSize = search_message[key][0]
            file_unique_id = search_message[key][-1]
            fileName = str(key).replace("@SinhalaSubDown_Bot", " ").replace("-", " ").replace("_","")
            if len(fileName) > 24:
                fileName = fileName[:20] + "..."
            text = "[{}] {} ".format(str(format_bytes(fileSize)), fileName)
            call_data = quote('query?{}file?{}'.format(query, file_unique_id)).replace(" ","__").replace("%20","-_").replace("%3F","_-")
            b = [  # First row
                InlineKeyboardButton(
                    text,
                    url="https://t.me/"+bot_username+"?start="+call_data
                )
            ]
            button.append(b)
    except Exception as e:
        print(e)
        pass
    b2 = []
    next = jump('Next', query, "g", len(search_message) > 10 and len(search_message) - number > 10, math=10, number=number)
    previous = jump('Previous', query, "g", len(search_message) - 10 > 0 and number > 0, math=-10, number=number)
    if previous is not None:
        b2.append(previous)
    if next is not None:
        b2.append(next)
    if b2 is not None:
        button.append(b2)
    pages = "📄 Pages [ {}/{} ] ".format((number // 10) + 1, (len(search_message) // 10) + 1)
    button.append(add_button(pages, "sinhalasubdown"))
    reply_markup = InlineKeyboardMarkup(button)
    return reply_markup


def search_in_channel(User, query):
    results = search_message(User, database_channel, query, filter="Documents", limit=350)
    for i in results:
        print(i)


def file_name_(na): # finished
    try:
        na = na[:na.index(']')]
    except:
        pass
    na = na.replace("-", ' ').replace('_', ' ').replace('?', '').replace('>', ' ').replace('<', ' ')
    na = na.replace("\\", ' ').replace('/', '-')
    na = na.replace(":", ' ').replace('[', ' ').replace(']', ' ').replace(' with ', '')
    return na


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


def download(url):# finished
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

    files_paths = compressed_file_downloader(site_message)

    '''r3 = requests.get(site_message)
    sv = str(site_message)
    if "Sinhala" in name:
        name = name[:name.index("Sinhala")]
    if "|" in name:
        name = name[:name.index("|")]
    if name.lower() == name.upper():
        pass'''

    '''if r3.status_code == 200:
        if "rar/" in site_message:
            file_name = file_name_(name) + " @SinhalaSubDown_Bot.rar"
        else:
            file_name = str(file_name_(name)).replace(".zip", "") + " @SinhalaSubDown_Bot.zip"
        file = open(file_name, "wb")
        file.write(r3.content)
        file.close()
        print("File download success !")
        print(file_name)
        doc = open(file_name, 'rb')
        return {'file': doc, "name": file_name}
    else:
        return None'''
    return files_paths


def check_in_channel(User, caption):# finished
    try:
        data = None
        print(data)
        for msg in User.search_messages(chat_id=database_channel, filter="document", query=caption, limit=1):
            data = msg.chat.id
        if data is not None:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return True

def download_count(n = 0):
    global db
    n = int(n)
    downloads = db.counts
    all = downloads.find({"type": "downloads"})
    for i in all:
        sdown = i["count"]
        sdown = int(sdown)
        downloads.update_one({"type": "downloads"}, {"$set": {"count": sdown + n}})
        sdown = downloads.find({"type": "downloads"})
        for x in sdown:
            sdown = x["count"]
            return sdown


def subtitle_count(n = 0):
    global db
    n = int(n)
    downloads = db.counts
    all = downloads.find({"type": "subtitles"})
    for i in all:
        sdown = i["count"]
        sdown = int(sdown)
        downloads.update_one({"type": "subtitles"}, {"$set": {"count": sdown + n}})
        sdown = downloads.find({"type": "subtitles"})
        for x in sdown:
            sdown = x["count"]
            return sdown


def last_update(time=None):
    global db
    n = time
    downloads = db.counts
    all = downloads.find({"type": "time"})
    if time is not None:
        for i in all:
            downloads.update_one({"type": "time"}, {"$set": {"count": n}})
            sdown = downloads.find({"type": "time"})
            for x in sdown:
                sdown = x["count"]
                return sdown
    else:
        for i in all:
            sdown = downloads.find({"type": "time"})
            for x in sdown:
                sdown = x["count"]
                return sdown


def check_group_admin(bot,message):
    for user_ in bot.get_chat_members(message.chat.id):
        me_id = bot.get_me()['id']
        if user_['user']['id']==me_id:
            if user_['status']!='member':
                return True
            else:
                return False
    else:
        return False
