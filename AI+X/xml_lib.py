from xml.dom.minidom import parse
import xml.dom.minidom
import threading

# 用来做xml文件的操作，导入xml.dom库来进行操作，
# 写一个read_movies函数来对xml里的视频信息进行读取
from cffi.cparser import lock

xml_file = 'E:/A-10-Temporary_test/last_test/flask-qa-main/AI+X/file/movie.xml'


def read_movies():
    lock.acquire()  # 锁住读
    DOMTree = xml.dom.minidom.parse(xml_file)
    lock.release()  # 释放锁
    root = DOMTree.documentElement
    movies = root.getElementsByTagName('movie')

    movie_arr = []
    for movie in movies:
        movie_dic = {'file': movie.getAttribute('file'),
                     'title': movie.getAttribute('title')}
        if movie.hasAttribute('count'):
            movie_dic['count'] = int(movie.getAttribute('count'))
        else:
            movie_dic['count'] = 0
        movie_arr.append(movie_dic)

    return movie_arr


# 我们要保存每个视频的点击次数，
# 写一个incr_movie的函数，
# 用以给对应的视频增加次数

def incr_movie(name):
    movies = read_movies()  # 先读出电影
    dom = xml.dom.minidom.Document()  # 创建dom树
    root_node = dom.createElement('root')  # 创建根节点
    dom.appendChild(root_node)  # 将根节点加入dom树
    for movie_dic in movies:  # 遍历xml读出来的所有的电影
        movie_node = dom.createElement('movie')  # 创建movie节点
        filename = movie_dic['file']  # 字典中获取名称
        movie_node.setAttribute('file', filename)  # 给movie节点设置file属性
        title = movie_dic['title']  # 字典中获取标题
        movie_node.setAttribute('title', title)  # 给movie节点设置title属性
        count = movie_dic.get('count', 0)  # 字典中获取视频的点击次数，如果没有次数默认为0
        if filename == name:  # 如果正是当前要增加点击次数的，那么点击次数+1
            count += 1
        movie_node.setAttribute('count', str(count))  # 给movie节点设置count属性
        root_node.appendChild(movie_node)  # 将movie节点加入root节点

    lock.acquire()  # 锁住写
    with open(xml_file, 'w', encoding='utf-8') as fs:
        dom.writexml(fs, indent='', addindent='\t', newl='\n', encoding='UTF-8')
    lock.release()  # 释放锁
