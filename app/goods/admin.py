from django.contrib import admin
from goods.models import GoodsType
from goods.models import GoodsSKU
from goods.models import Goods
from goods.models import GoodsImage
from goods.models import IndexGoodsBanner
from goods.models import IndexTypeGoodsBanner
from goods.models import IndexPromotionBanner


# Register your models here.
admin.site.register(GoodsType)
admin.site.register(GoodsSKU)
admin.site.register(Goods)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexPromotionBanner)
