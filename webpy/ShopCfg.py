
# 商城版本号
SHOP_VERSION = 20240717184900  # datetime做版本号 一天可以多次更新版本
# 消耗型 1 
# 时间型 2
USE_TYPE = 1
TIME_TYPE = 2

# money 1 
# coin 2
PAY_TYPE_MONEY = 1
PAY_TYPE_COIN = 2

# 不限制购买 0
# 限制每天购买 1
# 限制每周购买 2
# 限制每月购买 3
# 限制每年购买 4
LIMIT_BUY_TYPE_NON = 0
LIMIT_BUY_TYPE_DAY = 1
LIMIT_BUY_TYPE_WEEK = 2
LIMIT_BUY_TYPE_MONTH = 3
LIMIT_BUY_TYPE_YEAR = 4

ID_EXP_CARD = 1001
ID_RENAME_CARD = 1002
ID_GAME_CLEAR_CARD = 1003
ID_YEAR_VIP_PACKGE = 1004
ID_MONTH_VIP_PACKGE = 1005

ID_YEAR_VIP = 1006
ID_MONTH_VIP = 1007

ShopList = [
    ID_EXP_CARD,
    ID_RENAME_CARD,
    ID_GAME_CLEAR_CARD,
    ID_YEAR_VIP_PACKGE,
    ID_MONTH_VIP_PACKGE,
]

SHOP_CFG = {
    ID_EXP_CARD: {"pid": ID_EXP_CARD, 'name': "双倍经验卡", 'type': USE_TYPE, "momey": 100, "coin": -1, "paytype": PAY_TYPE_MONEY, "iconid": 1001, "version": 10000, "discount": 1, "inventory": -1, "buylimittype": LIMIT_BUY_TYPE_NON, "buylimitnum": -1, "proplist":[{"pid": ID_EXP_CARD, "num": 1}]},
    ID_RENAME_CARD: {"pid": ID_RENAME_CARD, 'name': "改名卡", 'type': USE_TYPE, "momey": 100, "coin": -1, "paytype": PAY_TYPE_MONEY, "iconid": 1002, "version": 10000, "discount": 1, "inventory": -1, "buylimittype": LIMIT_BUY_TYPE_NON, "buylimitnum": -1, "proplist":[{"pid": ID_RENAME_CARD, "num": 1}]},
    ID_GAME_CLEAR_CARD: {"pid": ID_GAME_CLEAR_CARD, 'name': "战机清零卡", 'type': USE_TYPE, "momey": 100, "coin": -1, "paytype": PAY_TYPE_MONEY, "iconid": 1003, "version": 10000, "discount": 1, "inventory": -1, "buylimittype": LIMIT_BUY_TYPE_NON, "buylimitnum": -1, "proplist":[{"pid": ID_GAME_CLEAR_CARD, "num": 1}]},
    ID_YEAR_VIP_PACKGE: {"pid": ID_YEAR_VIP, 'name': "年会员礼包", 'type': USE_TYPE, "momey": -1, "coin": 1000, "paytype": PAY_TYPE_COIN, "iconid": 1004, "version": 10000, "discount": 1, "inventory": -1, "buylimittype": LIMIT_BUY_TYPE_NON, "buylimitnum": -1, "proplist":[{"pid": ID_EXP_CARD, "num": 10}, {"pid": ID_RENAME_CARD , "num": 10}, {"pid": ID_YEAR_VIP, "num": 1}]},
    ID_MONTH_VIP_PACKGE: {"pid": ID_MONTH_VIP_PACKGE, 'name': "月会月卡", 'type': USE_TYPE, "momey": -1, "coin": 10, "paytype": PAY_TYPE_COIN, "iconid": 1005, "version": 10000, "discount": 1, "inventory": -1, "buylimittype": LIMIT_BUY_TYPE_NON, "buylimitnum": -1, "proplist":[{"pid": ID_EXP_CARD, "num": 1}, {"pid": ID_RENAME_CARD , "num": 10}, {"pid": ID_MONTH_VIP, "num": 1}]},
}
# 接口的幂等性
# 幂等性-->多次重复请求, a = 1自身就满足幂等性, 但是 a = a + 1就不满足幂等性