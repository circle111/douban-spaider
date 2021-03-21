#-*- coding = utf-8 -*-
# @Time    : 2021/3/15 14:38
# @Author  : circle
# @File    : spider.py
# @Software: PyCharm
from bs4 import BeautifulSoup
import re
from urllib import request as req, error
# import xlwt
import sqlite3
def main() :
    beanurl = "https://movie.douban.com/top250?start="
    #savepath = '豆瓣电影top250.xls'
    dbpath = "movie.db"
    #1.爬取网页
    # 2.解析数据
    datalist = getData(beanurl)
    #3.保存数据
    #saveData(datalist, savepath)
    saveDate2DB(datalist, dbpath)

#影片的超链接的规则
findlink = re.compile(r'<a href="(.*?)">')
#匹配影片图片的规则
findimg = re.compile(r'<img.*src="(.*?)"', re.S)
#影片的片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片的评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def getData(beaseurl):
    datalist = []
    for i in range(0,10):
        url = beaseurl + str(i * 25)
        html = askURL(url)
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_='item'):
            data = []
            item = str(item)
            #获取到影片的超链接
            link = re.findall(findlink, item)[0]
            data.append(link)
            img = re.findall(findimg, item)[0]
            data.append(img)
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                zh_title = titles[0]
                data.append(zh_title)
                other_title = titles[1].replace('/','')
                data.append(other_title)
            else:
                data.append(titles[0])
                data.append('  ')
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)
            inq = re.findall(findInq, item)
            if len(inq) != 0 :
                str1 = inq[0].replace('。',' ')
                data.append(str1)
            else:
                data.append('   ')
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', ' ', bd)
            bd = re.sub('/', ' ', bd)
            data.append(bd.strip())
            datalist.append(data)
    return datalist


#得到指定一个url的网页内容
def askURL(url):
    html = ''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    request = req.Request(url = url, headers = headers)
    try:
        response = req.urlopen(request)
        html = response.read().decode('utf-8')
    except error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html

#保存数据到Excel表格
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i]) #列名
    for i in range(0, 250):
        print("第%d条"%i)
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)

#保存到数据库
def saveDate2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    for data in datalist:
        sql = '''
                    insert into movie250
                    (info_link, pic_link, zh_title, oth_title, score, rated, instroduction, info)
                    values (?,?,?,?,?,?,?,?)
                '''
        cursor.execute(sql, data)
        conn.commit()
        # for idx in range(len(data)):
        #     data[idx] = '"'+data[idx]+'"'
        #     sql = '''insert into movie250
        #             (info_link, pic_link, zh_title, oth_title, score, rated, instroduction, info)
        #             values (%s)'''%','.join(data)
        #     print(sql)
        # cursor.execute(sql)
        # conn.commit()
    conn.close()

def init_db(dbpath):
    sql = '''
        create table movie250(
            id integer primary key autoincrement ,
            info_link text,
            pic_link text,
            zh_title varchar,
            oth_title varchar,
            score numeric ,
            rated numeric ,
            instroduction text,
            info text
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    #调用函数
    main()
    print('爬取完毕:)')