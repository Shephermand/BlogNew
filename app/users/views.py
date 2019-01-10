#处理与users业务相关的路由和视图处理函数

from . import user
from .. import db
from ..models import *

@user.route('/han')
def han_views():
    return "这是韩伟杰的主页!"