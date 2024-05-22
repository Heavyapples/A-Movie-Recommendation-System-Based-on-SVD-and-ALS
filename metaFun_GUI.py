import requests
from PIL import Image,ImageTk
import io
from lxml import etree
import re
import tkinter as tk
import tkinter.messagebox
import GlobalFun
import TkinterGUI.meFrame
import time
import RecommendationAlogrithm.OnlineRecommend
import GlobalFun


def get_movie_url(movieid):# 根据movieid获取对应的IMDb网页链接
    '''
    :param movieid:
    :return: url_imdbid
    根据movieid得到对应的网页链接
    '''
    #抓取movieid对应的imdbid
    conn, cur = GlobalFun.ConnectSql()
    cur.execute("select imdbid from MovieRecommender.links where movieId = {}".format(movieid))
    imdbid = str(cur.fetchall()[0][0])
    GlobalFun.Closesql(conn,cur)
    imdbid = "0" * (7 - len(imdbid)) + imdbid
    url_imdbid = "http://www.imdb.com/title/tt{}/".format(imdbid)
    return url_imdbid

def get_src(url,movieId):# 根据网页链接和数据库抓取电影信息
    """
    :param url:
    :return: src,title,date,genres
    根据网页连接和数据库，抓取电影海报地址，电影名称，电影上映时间，电影类型
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42'
    }
    html = requests.get(url,verify=False, headers=headers)
    bs = etree.HTML(html.text)
    conn,cur = GlobalFun.ConnectSql()
    sql = "select title,genres from MovieRecommender.movies where movieid = {}".format(movieId)
    cur.execute(sql)
    data = cur.fetchall()

    text1 = bs.xpath('//script[@type="application/ld+json"]')[0].text

    src = re.findall('^.*?"image":"(.*?)",.*?', text1)[0]
    briefinfo = re.findall('^.*?"description":"(.*?)",.*?',text1)[0]
    title = re.findall('(.*)\(', data[0][0])[0].strip(' ')
    date = re.findall('\((\d*)\)', data[0][0])[0].strip(' ')
    genres_list = data[0][1].strip('\r').split('|')
    genres = "\n".join(genres_list)
    GlobalFun.Closesql(conn,cur)
    return src,title,date,genres,briefinfo

def resize(w, h, w_box, h_box, pil_image):# 对PIL格式的图片进行缩放处理以适应图形界面显示
    '''resize a pil_image object so it will fit into a box of size w_box times h_box,but retain aspect ratio'''
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def get_image(src,w_box=80,h_box=120):# 获取电影海报图像并将其转换为Tkinter可以使用的图像格式
    html = requests.get(src).content
    data_stream = io.BytesIO(html)
    pil_image = Image.open(data_stream)  # 转成pil格式的图片
    w, h = pil_image.size
    pil_image_resized = resize(w, h, w_box, h_box, pil_image)
    tk_image = ImageTk.PhotoImage(pil_image_resized)  # 转tk_image
    return tk_image

def destroy(frame):# 销毁Tkinter窗口中的所有控件
    for widget in frame.winfo_children():
        widget.destroy()


def get_score(userid,movieid):# 获取用户对特定电影的评分数据
    conn, cur = GlobalFun.ConnectSql()
    # 获取用户打分信息
    sql = "select rating,timestamp from MovieRecommender.ratings where movieid={} and userid={};".format(movieid,userid)
    cur.execute(sql)
    data = cur.fetchall()
    GlobalFun.Closesql(conn,cur)
    return data


#rating部分GUI
class rating_frame():# 提供评分功能的界面，包括创建评分界面和修改评分界面
    def __init__(self,window,type,userid,movieid):
        self.window = window
        self.type = type
        self.Content = tk.StringVar()
        self.Rating_Frame = tk.Frame(self.window)
        self.Entry = tk.Spinbox(self.Rating_Frame, from_=1, to=5, textvariable=self.Content,width=5)
        self.Entry.pack(side="left")
        self.B = tk.Button(self.Rating_Frame, text="rate",command=self.rate)
        self.B.pack(side="left")
        self.Rating_Frame.place(x=140,y=350,anchor="nw")
        self.userid=userid
        self.movieid=movieid

    def rate(self):
        try:
            Score = eval(self.Content.get())
            userid=self.userid
            movieid=self.movieid
            if isinstance(Score,int) and Score <= 5 and Score >= 0:
                timestamp=int(time.time())
                rate_score = Score
                conn, cur = GlobalFun.ConnectSql()
                if self.type == "edit":
                    sql = "update MovieRecommender.ratings set userid={},movieid={},rating={},timestamp={} where userid={} and movieid={};".format(userid, movieid,Score, timestamp,userid, movieid,Score)
                else:
                    sql = "insert into MovieRecommender.ratings values({},{},{},{});".format(userid, movieid,Score, timestamp)
                cur.execute(sql)
                conn.commit()
                GlobalFun.Closesql(conn,cur)
                tk.messagebox.showinfo(title="成功!", message="感谢评分",command=destroy(self.Rating_Frame))
                self.Rating_Frame.destroy()
                print('problem is destroy')
                rated_frame(self.window,rate_score,timestamp,userid,movieid)
                print('prolem is trigger')
                #触发在线推荐名单的改变
                print("userid is",userid,"movieid is ",movieid)
                RecommendationAlogrithm.OnlineRecommend.updateonline(userid, movieid)
                print('prolem is here')
            else:
                tk.messagebox.showwarning(title="失败!",message="评分只能为1-5之间")
                self.Content.set(3)
        except Exception as e:
            tk.messagebox.showwarning(title="异常!",message=e)
            self.Content.set(3)

class rated_frame():
    def __init__(self,window,userrate,ratetime,userid,movieid):
        self.window = window
        self.Rated_Frame = tk.Frame(self.window)
        self.L = tk.Label(self.Rated_Frame,text="已评分: {}\t时间: {}".format(userrate,time.strftime("%Y-%m-%d %H: %M",time.localtime(ratetime))))
        self.L.pack()
        self.B = tk.Button(self.Rated_Frame,text="修改",command=self.modify)
        self.B.pack()
        self.Rated_Frame.place(x=25,y=350,anchor="nw")
        self.userid=userid
        self.moiveid=movieid

    def modify(self):
        self.Rated_Frame.destroy()
        rating_frame(self.window,"edit",self.userid,self.moiveid)

class basedFrame():# 显示用户已评分的界面
    def __init__(self,window,userid,moiveid):
        self.window = window
        self.userid = userid
        self.movieid = moiveid
        data = get_score(self.userid,self.movieid)

        if len(data) == 0:
            rating_frame(self.window,"insert",self.userid,self.movieid)
        else:
            timestamp, userrate = data[0][1], data[0][0]
            rated_frame(self.window,userrate,timestamp,self.userid,self.movieid)

def get_similar_movie_list(movieId,type="ALS"):# 根据相似度算法(SVD或ALS)获取与指定电影相似的电影列表
    conn, cur = GlobalFun.ConnectSql()
    if type == "SVD":
        sql = "select similarId,similarDegree from MovieRecommender.movie_similar_svd where movieId={} order by similarDegree desc limit 5;".format(movieId)
    else:
        sql = "select similarId,similarDegree from MovieRecommender.movie_similar_als where movieId={} order by similarDegree desc limit 5;".format(movieId)
    cur.execute(sql)
    data = cur.fetchall()
    return data

if __name__=="__main__":


    window = tk.Tk()
    window.geometry("800x600")
    movielist = [1,2,3,4,5]
    for i in movielist:

        exec("frm,tk_image{} = meFrame({},window)".format(i,i))
        frm.pack(side='left')


    window.mainloop()