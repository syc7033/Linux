
import ShopCfg
import ErrorCfg
import math
import Lobby
import Config
import DBManage
import datetime
import Account

def GetShopCfg(version):
    shop = ShopCfg.SHOP_CFG
    list = []
    for pid in ShopCfg.ShopList:  # ShopList里面放的都是pid，就是propid
        # 看该商品是否再商城中，如果再就把他的配置取出来
        if pid in shop:
            cfg = shop[pid]
            # 看该产品商城配置的版本号是否大于传过来了版本号，大于则无法取出
            if version < cfg['version']:
                continue
            # 把服务要求的商城配置拼接为字典
            propDict = {
                'pid': cfg['pid'], 'name': cfg['name'], 'type': cfg['type'], 'money': cfg['money'],
                'coin': cfg['coin'], 'paytype': cfg['paytype'], 'iconid': cfg['iconid'],
                'version': cfg['version'], 'discount': cfg['discount'], 'inventoy': cfg['inventoy'],
                'buylimittype': cfg['buylimittype'], 'buylimitnum': cfg['buylimitnum'], 'proplist': cfg['proplist'],
            }
        list.append(propDict)
    return {'shoplist': list, 'shopversion': ShopCfg.SHOP_VERSION}

def ShopBuy(userid, propid, propnum, shopversion, version):
    # 校验商城版本，防止版本号过低
    if shopversion < ShopCfg.SHOP_VERSION:
        return {'code': ErrorCfg.EC_SHOP_BUY_SHOPVERSION_LOW, 'reason': ErrorCfg.ER_SHOP_BUY_SHOPVERSION_LOW}
    
    # 再看该商品是否在商城配置里面
    if propid not in ShopCfg.SHOP_CFG:
        return {'code': ErrorCfg.EC_SHOP_BUY_PROPID_NOT_EXIST, 'reason': ErrorCfg.ER_SHOP_BUY_PROPID_NOT_EXIST}
    
    # 然后看该产品是否在产品列表里面
    if propid not in ShopCfg.ShopList:
        return {'code': ErrorCfg.EC_SHOP_BUY_PROPID_NOT_IN_SHOPLIST, 'reason': ErrorCfg.ER_SHOP_BUY_PROPID_NOT_IN_SHOPLIST}

    cfg = ShopCfg.SHOP_CFG['propid']

    # 然后判断客户端的版本
    if version < cfg['version']:
        return {'code': ErrorCfg.EC_SHOP_BUY_CLIENTVERSION_LOW, 'reason': ErrorCfg.ER_SHOP_BUY_CLIENTVERSION_LOW}
    
    # 计算购买数量是否大于库存数量,去缓存或者数据库中取出库存（后续需要修改）
    if propnum > cfg['inventory']:
        return {'code': ErrorCfg.EC_SHOP_BUY_INVENTORY_NOT_ENOUGH, 'reason': ErrorCfg.ER_SHOP_BUY_INVENTORY_NOT_ENOUGH}

    # 购买
    
    needmoney = int(math.floor(cfg['money'] * cfg['discount'] * propnum))
    money = Lobby.GetMoney(userid)
    if money < needmoney:
        return {'code': ErrorCfg.EC_SHOP_BUY_MONEY_NOTENOUGH, 'reason': ErrorCfg.ER_SHOP_BUY_MONEY_NOTENOUGH}

    strKey = Config.KEY_PACKAGE.format(userid=userid)
    money = Config.grds.hincrby(strKey, 'money', -needmoney)  # hincrby是原子性操作，不会读到脏数据
    '''
    此处为什么要选择incrby原子性操作扣钱
    比如现在又俩个服务器
    web1:getmoney 100 买了一个双倍经验卡 40
    web2:getmoney 100 买了一个战机清零卡 40
    最终结算 这个人买了一个双倍经验卡和一个战机清零卡但是确只扣了60
    造成这个问题的原因是web2读到了脏数据,解决这个问题的方法就是原子性操作
    hincrby(key, 'filed', +/- 'value')
    hincrby是原子性操作不可能读到脏数据
    但是扣钱结束后一定要判断money是否小于0，为什么？
    web1:getmoney 100 双倍经验卡 40
    web2:getmoney 40  战机清零卡 -20
    最后-20需要恢复,incrby(strKey, 'money', needmoney)
    return {错误码,错误原因}
    '''
    if money < 0:
        Config.grds.hincrby(strKey, 'money', needmoney)
        return {'code': ErrorCfg.EC_SHOP_BUY_MONEY_NOTENOUGH, 'reason': ErrorCfg.ER_SHOP_BUY_MONEY_NOTENOUGH}
    now = datetime.datetime.now()
    DBManage.ShopBuyUpdatePackage(userid, money, now)

    # 发货
    PresentProp(userid, propid, propnum)
    return {'code': 0, 'money': money}



def PresentProp(userid, propid, propnum):
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    now = datetime.datetime.now()
    cfg = ShopCfg.SHOP_CFG['propid']
    proplist = cfg['proplist']
    propdict = {}
    for prop in proplist:
        singlepropnum = Config.grds.hincrby(strKey, 'prop_' + str(prop['id']), prop['num'] * propnum)
        propdict['prop_' + str(prop['id'])] = singlepropnum
    Config.grds.hset(strKey, 'freshtime', str(now))
    DBManage.UpdateProp(userid, propdict, now)

def PresentMoney(userid, money):
    now = datetime.datetime.now()
    Account.InitPackage(userid, now)
    strKey = Config.KEY_PACKAGE.format(userid)
    money = Config.grds.hincrby(strKey, 'money', money)
    DBManage.ShopBuyUpdatePackage(userid, money, now)
    return {'code': 0, 'money': money}
