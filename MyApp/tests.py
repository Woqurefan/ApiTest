class Person:
    def __init__(self,nicheng):
        self.nicheng = nicheng

    def get_nicheng(self):
        print(self.nicheng)

class mj(Person):
    def __init__(self ):
        print("-----------------\n正在创建买家对象:" )
        self.nicheng = '小邪😈同学'
        self.driver = ''
        self.login()

    def login(self):
        print('运行appium买家登陆脚本\n')
        # self.driver.find('')

    def xiadan(self):
        print('买家在下单')
        # self.driver.find('')

    def quxiao(self):
        print('买家取消订单')
        # self.driver.find('')

class sj(Person):
    def __init__(self):
        print("-----------------\n正在创建商家对象:")
        self.nicheng = '小饭同学'
        self.driver = ''
        self.login()

    def login(self):
        print('运行appium 商家登陆脚本\n')
        # self.driver.find('')

    def queren(self):
        print('商家在确认订单')
        # self.driver.find('')

    def tousu(self):
        print('商家在投诉')
        # self.driver.find('')

    def shoubiao(self):
        print('商家在上架手表')
        # self.driver.find('')

class KF(Person):
    def __init__(self):
        print("-----------------\n正在创建客服:")
        self.driver = ''
        self.login()
    def login(self):
        print('运行selenium 客服登陆脚本\n')
        # self.driver.find('')

    def jiufen(self):
        print('运行客服处理纠纷脚本')
        #self.driver.find('')
        print('客服在看闹事双方昵称都叫什么：')
        print('买家昵称：')
        new_mj.get_nicheng()
        print('商家昵称：')
        new_sj.get_nicheng()

class Factory:
    def create_user(self, shenfen):
        if shenfen == 'mj':
            return mj()
        if shenfen == 'sj':
            return sj()
        if shenfen == 'kf':
            return KF()


if __name__ == '__main__':
    factory = Factory()
    new_mj = factory.create_user('mj')
    new_sj = factory.create_user('sj')
    new_kf = factory.create_user('kf')
    new_sj.shoubiao()
    new_mj.xiadan()
    new_sj.queren()
    new_mj.quxiao()
    new_sj.tousu()
    new_kf.jiufen()

