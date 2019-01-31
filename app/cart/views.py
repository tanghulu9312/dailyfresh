from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import View
from goods.models import GoodsSKU
from django.http import JsonResponse
from django_redis import get_redis_connection
# Create your views here.
class CartAddView(View):
    '''购物车记录添加'''
    def post(self,request):
        user = request.user
        if not user.is_authenticated:
            #用户未登录
            return JsonResponse({'res':0,'errmsg':'未登录，不能添加'})
        #接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        #数据校验
        if not all([sku_id,count]):
            return JsonResponse({'res':1,'errmsg':'数据不完整！'})
        #校验添加的商品数量
        try:
            count=int(count)
        except Exception as e:
            return JsonResponse({'res':2,'errmsg':'商品数目出错'})
        #校验商品是否存在
        try:
            goods = GoodsSKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'res':3,'errmsg':'商品不存在！'})
        #业务处理：添加购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        #尝试获取sku_id的值->hget cart_key属性
        #如果sku_id在hash中不存在，hget返回None
        cart_count = conn.hget(cart_key,sku_id)
        if cart_count:
            #累加购物车中的数量
            count+=int(cart_count)
        #校验商品的库存

        if count > goods.stock:
            return JsonResponse({'res':4,'errmsg':'商品库存不足！'})
        #设置hash中sku_id对应的值
        #hset->如果sku_id已经存在，更新数据，如果sku_id不存在，添加数据
        conn.hset(cart_key,sku_id,count)
        #计算用户购物车中商品的条目数
        total_count = conn.hlen(cart_key)
        #返回应答
        return JsonResponse({'res':5,'total_count':total_count,'message':'添加成功！'})

class CartInfoView(View):
    '''显示购物车信息'''
    def get(self,request):
        #获取当前登录的用户
        user = request.user
        #获取redis连接
        conn = get_redis_connection('default')
        #获取购物车信息
        cart_key = 'cart_%d'%user.id
        #skus是一个字典{'商品id':'数量'}
        cart_dict = conn.hgetall(cart_key)
        skus=[]

        total_count = 0   #商品总数
        total_price = 0   #商品总价
        #遍历skus
        for sku_id,count in cart_dict.items():
            #根据商品ID查出商品信息
            sku = GoodsSKU.objects.get(id=sku_id)
            #动态给商品添加属性‘数量’count
            sku.count = int(count)
            #动态给商品添加属性‘小计’amount
            sku.amount = int(count)*sku.price
            #将商品添加到列表中
            skus.append(sku)

            total_count+=int(count)
            total_price+=int(count)*sku.price
            #上下文信息
            context = {
                'skus':skus,
                'total_count':total_count,
                'total_price':total_price
            }
        #给页面返回值
        return render(request,'cart.html',context)

class CarUpdateView(View):
    '''购物车记录更新'''
    def post(self,request):
        user = request.user
        if not user.is_authenticated:
            #用户未登录
            return JsonResponse({'res':0,'errmsg':'未登录，不能更新'})
        #接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        #数据校验
        if not all([sku_id,count]):
            return JsonResponse({'res':1,'errmsg':'数据不完整！'})
        #校验添加的商品数量
        try:
            count=int(count)
        except Exception as e:
            return JsonResponse({'res':2,'errmsg':'商品数目出错'})
        #校验商品是否存在
        try:
            goods = GoodsSKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'res':3,'errmsg':'商品不存在！'})
        #业务处理：添加购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id

        #校验商品的库存

        if count > goods.stock:
            return JsonResponse({'res':4,'errmsg':'商品库存不足！'})
        #设置hash中sku_id对应的值
        #hset->如果sku_id已经存在，更新数据，如果sku_id不存在，添加数据
        conn.hset(cart_key,sku_id,count)
        #获取购物车商品的数量
        total_count=0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count+=int(val)

        #返回应答
        return JsonResponse({'res':5,'total_count':total_count,'message':'添加成功！'})


class CartDeleteView(View):
    '''删除购物车商品'''
    def post(self,request):
        #获取要删除的商品的id
        sku_id = request.POST.get('sku_id')
        #获取用户
        user = request.user

        #判断用户是否登录
        if not user.is_authenticated:
            return JsonResponse({'res':1,'errmsg':'用户未登录,不能删除商品'})

        #判断商品id是否合法
        if not sku_id:
            return JsonResponse({'res':2,'errmsg':'无效的商品id'})

        #判断商品是否存在
        try:
            goods=GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res':3,'errmsg':'商品不存在！'})

        #业务处理
        #获取redis连接
        conn = get_redis_connection('default')

        cart_key = 'cart_%d'%user.id
        conn.hdel(cart_key,sku_id)
        #计算购物车中商品的总件数
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count+=int(val)

        return JsonResponse({'res':'4','message':'删除成功','total_count':total_count})












