#处理main业务中的路由和视图处理函数
import os

from . import main
from .. import db
from ..models import *
from flask import render_template, request, session, redirect
import datetime

@main.route('/')
def main_index():
    # 查询Category中的所有数据
    categories = Category.query.all()
    # 查询Topic中所有的数据
    topices = Topic.query.all()
    # 从session中获取登录信息(id,loginname)
    if 'id' in session and 'loginname' in session:
        user = User.query.filter_by(ID=session['id']).first()
    return render_template('index.html',params=locals())


@main.route('/list')
def main_list():
    return render_template('list.html')


@main.route('/login', methods=["GET", "POST"])
def main_login():
    if request.method == "GET":
        #判断id和loginname是否在session中
        if 'id' in session and 'loginname' in session:
            return redirect('/')
        else:
            # 记录请求源地址,并将请求源地址保存进session
            url = request.headers.get('Refere', '/')
            session['url'] = url
            Msg = ''
            return render_template('login.html', params=locals())
    else:
        # 接收传递过来的用户名和密码
        loginname = request.form['username']
        upwd = request.form['password']
        user = User.query.filter_by(loginname=loginname,upwd=upwd).first()
        # 验证用户名和密码是否正确
        if user:
            # 登录成功存session
            session['id'] = user.ID
            session['loginname'] = loginname
            # 如果成功,则返回到请求的源地址
            return redirect(session['url'])
        # 如果失败,则返回到登录的页面
        else:
            Msg = '用户名或密码错误!'
            return render_template('login.html', params=locals())


@main.route('/logout')
def main_logout():
    # 获取请求源地址,如果没有则将 / 作为源地址
    url = request.headers.get('Referer', '/')
    # 判断session中是否有登录信息,如果有则清除
    if 'id' in session and 'loginname' in session:
        del session['id']
        del session['loginname']
    # 重定向到请求地址
    return redirect(url)


@main.route('/release', methods=['GET', 'POST'])
def main_release():
    if request.method == "GET":
        # 判断是否有登录用户
        if 'id' in session and 'loginname' in session:
            # 有登录用户,则取出信息判断is_author
            user = User.query.filter_by(ID=session['id']).first()
            if user.is_author:
                # 读取category所有信息
                categories = Category.query.all()
                return render_template('release.html', params=locals())
        url = request.headers.get('Refere', '/')
        return redirect(url)

    else:
        # post 请求处理发表博客的相关操作
        # 1. 创建一个Topic对象 - topic
        topic = Topic()
        # 2. 接收前端传递过来的值,并赋值给topic
        # 2.1 接收传递过来的标题 title - author
        topic.title = request.form['author']
        # 2.2 接收传递过来的bolgtype_id - list
        topic.blogtype_id = request.form['list']
        # 2.3 接收传递过来的category_id - category
        topic.category_id = request.form['category']
        # 2.4 从session中获取用户的user_id - session['id']
        topic.user_id = session['id']
        # 2.5 接收传递过来的content - content
        topic.content = request.form['content']
        # 2.6 获取系统时间(年月日时分秒)给pub_date
        topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("标题:%s,类型:%s,内容类型:%s,用户:%s,内容:%s,时间:%s" % (
        topic.title, topic.blogtype_id, topic.category_id, topic.user_id, topic.content, topic.pub_date))

        # 3. 判断是否有文件上传,如果有的话则将文件保存至static/upload下,并将路径给images
        if request.files:
            # 获取要上传的文件名
            f = request.files['picture']
            # 处理文件名: 时间,扩展名
            ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext = f.filename.split('.')[1]
            filename = ftime + '.' + ext
            # 处理上传路径: static/upload
            topic.images = "upload/" + filename
            # 将文件以文件名的形式保存到指定路径下
            basedir = os.path.dirname(os.path.dirname(__file__))
            print(basedir)
            upload_path = os.path.join(basedir,'static/upload',filename)
            print(upload_path)
            f.save(upload_path)
        # 4. 将topic保存回数据库
            db.session.add(topic)
            return redirect('/')














