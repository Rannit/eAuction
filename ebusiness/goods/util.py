#coding=utf-8
from django.shortcuts import render,get_object_or_404
from goods.models import Goods,Address,Order,Orders,User
from goods.object import Chart_list,Order_list,Orders_list
import hashlib

# 以下是类模型定义部分
class Util:
	#检查用户是否登录
    def check_user(self,request):
        #从cookies中取出username
        username = str(request.session.get('username',''))
        #判断数据库中是否存在
        user = User.objects.filter(username = username)
        #如果不存在，返回空串
        if (user is None):
            return ""
        #否则返回username
        else:
            return username

    #MD5加密
    def md5(self,mystr):
        if isinstance(mystr,str):
            m = hashlib.md5()   
            m.update(mystr.encode('utf8'))
            return m.hexdigest()
        else:
            return ""

	#通过addressId判断这个地址是否属于当前登录用户
    def check_User_By_Address(self,request,username,addressId):
        #获取addressId对应的address信息
        address = get_object_or_404(Address,id=addressId)
        #通过username获取对应的user信息
        user = get_object_or_404(User,username=username)
        #判断addressId对应的userid与username获取对应的userid是否相等
        if address.user_id ==user.id:
            return 1
        else:
            return 0

    #通过orderId判断这个订单是否属于当前登录用户
    def check_User_By_Order(self,request,username,orderId):
        #获取orderId对应的order信息
        order = get_object_or_404(Order,id=orderId)
        #通过username获取对应的user信息
        user = get_object_or_404(User,username=username)
        #判断addressId对应的userid与username获取对应的userid是否相等
        if order.user_id ==user.id:
            return 1
        else:
            return 0

    #通过ordersId判断这个地址是否属于当前登录用户
    def check_User_By_Orders(self,request,username,orderId):
        #获取orderId对应的orders信息
        orders = get_object_or_404(Orders,id=orderId)
        #获取orders.id对应的order信息
        order = Order.objects.filter(order_id=orders.id)
        #通过username获取对应的user信息
        user = get_object_or_404(User,username=username)
        #判断addressId对应的userid与username获取对应的userid是否相等
        if len(order)>0:
            if order[0].user_id == user.id:
                return 1
        else:
            return 0

    #返回参与的拍卖中所有拍卖品的个数
    def cookies_count(self,request):
        #返回本地所有的cookie
        cookie_list = request.COOKIES
        #只要进入网站，系统中就会产生一个名为sessionid的cookie
        #如果后台同时在运行，会产生一个名为csrftoken的cookie
        length = len(request.COOKIES)
        for i in cookie_list:
            if (i == "csrftoken") or (i == "sessionid") or (i.startswith("Hm_lvt_")) or(i.startswith("Hm_lpvt_")):
                length = length-1
        return length

    #获取参与的拍卖中的所有内容
    def deal_cookes(self,request):
        #获取本地所有内COOKIES
        cookie_list = request.COOKIES
        #去除COOKIES内的sessionid
        cookie_list.pop("sessionid")
        #如果COOKIES内含有csrftoken，去除COOKIES内的csrftoken
        for key in list(cookie_list.keys()):
            if (key == "csrftoken") or (key == "sessionid") or (key.startswith("Hm_lvt_")) or(key.startswith("Hm_lpvt_")):
                del cookie_list[key]
        #返回处理好的参与的拍卖中的所有内容
        return cookie_list

    #参与拍卖
    def add_chart(self,request):
        #获取参与的拍卖中所有内容
        cookie_list = self.deal_cookes(request)
        #定义my_chart_list列表
        my_chart_list = []
        #遍历cookie_list，把里面的内容加入类Chart_list列my_chart_list中
        for key in cookie_list:
            chart_object = Chart_list
            chart_object = self.set_chart_list(key,cookie_list)
            my_chart_list.append(chart_object)
        #返回 my_chart_list
        return my_chart_list


    #定义单个拍卖的变量
    def set_order_list(self,key):
        order_list = Order_list()
        order_list.set_id(key.id)#主键
        good_list = get_object_or_404(Goods,id=key.goods_id)#获得当前拍卖品信息
        order_list.set_good_id(good_list.id)#订单中拍卖品编号
        order_list.set_name(good_list.name)#订单中拍卖品名字
        order_list.set_price(good_list.price)#订单中拍卖品的最低价
        order_list.set_count(key.count)#报价
        order_list.set_deadline(good_list.time)#报价
        return order_list

    def set_orders_list(self,key):
        order_list = Orders_list()
        order_list.set_id(key.id)#主键
        order_list.set_address(key.address)#地址信息
        order_list.set_create_time(key.create_time)#创建时间
        return order_list

    #把参与拍卖的拍卖品放在一个名为Chart_list()的类中，返回给模板
    def set_chart_list(self,key,cookie_list):
        chart_list = Chart_list()
        good_list = get_object_or_404(Goods, id=key)
        chart_list.set_id(key)#拍卖品的标号
        chart_list.set_name(good_list.name)#拍卖品的名称
        chart_list.set_price(good_list.price)#拍卖品的起拍价
        chart_list.set_count(cookie_list[key])#拍卖品的报价
        return chart_list
