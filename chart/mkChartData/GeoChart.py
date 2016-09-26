# coding:utf-8
'''
地图类，生成地图展现时需要的数据
'''

import datetime
import sys

from django.db.models import Sum, Max

sys.path.append("../../")

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ywreport.settings")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''
import django

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()

from chart.models import itoms_count


class GeoChart:
    """
    echart 地图, 数据集合与数据生成
    类变量命名规范：从echart配置项开始，逐级append参数名称，并用下划线相连．
    如：series_data; series_data_label_normal_show 等．
    """
    PERIOD_DAYS = 30  # 展示两周１４天的数据
    TOP_N = 5  # 突出显示TOP 3
    GEO_COORD_MAP = {
        '总行': [116, 39],
        '北京': [116.40, 39.90],
        '深圳': [114.05, 22.55],
        '海门': [121.15, 31.89],
        '鄂尔多斯': [109.781327, 39.608266],
        '招远': [120.38, 37.35],
        '舟山': [122.207216, 29.985295],
        '齐齐哈尔': [123.97, 47.33],
        '盐城': [120.13, 33.38],
        '赤峰': [118.87, 42.28],
        '青岛': [120.33, 36.07],
        '乳山': [121.52, 36.89],
        '金昌': [102.188043, 38.520089],
        '泉州': [118.58, 24.93],
        '莱西': [120.53, 36.86],
        '日照': [119.46, 35.42],
        '胶南': [119.97, 35.88],
        '南通': [121.05, 32.08],
        '拉萨': [91.11, 29.97],
        '云浮': [112.02, 22.93],
        '梅州': [116.1, 24.55],
        '文登': [122.05, 37.2],
        '上海': [121.48, 31.22],
        '攀枝花': [101.718637, 26.582347],
        '威海': [122.1, 37.5],
        '承德': [117.93, 40.97],
        '厦门': [118.1, 24.46],
        '汕尾': [115.375279, 22.786211],
        '潮州': [116.63, 23.68],
        '丹东': [124.37, 40.13],
        '太仓': [121.1, 31.45],
        '曲靖': [103.79, 25.51],
        '烟台': [121.39, 37.52],
        '福州': [119.3, 26.08],
        '瓦房店': [121.979603, 39.627114],
        '即墨': [120.45, 36.38],
        '抚顺': [123.97, 41.97],
        '玉溪': [102.52, 24.35],
        '张家口': [114.87, 40.82],
        '阳泉': [113.57, 37.85],
        '莱州': [119.942327, 37.177017],
        '湖州': [120.1, 30.86],
        '汕头': [116.69, 23.39],
        '昆山': [120.95, 31.39],
        '宁波': [121.56, 29.86],
        '湛江': [110.359377, 21.270708],
        '揭阳': [116.35, 23.55],
        '荣成': [122.41, 37.16],
        '连云港': [119.16, 34.59],
        '葫芦岛': [120.836932, 40.711052],
        '常熟': [120.74, 31.64],
        '东莞': [113.75, 23.04],
        '河源': [114.68, 23.73],
        '淮安': [119.15, 33.5],
        '泰州': [119.9, 32.49],
        '南宁': [108.33, 22.84],
        '营口': [122.18, 40.65],
        '惠州': [114.4, 23.09],
        '江阴': [120.26, 31.91],
        '蓬莱': [120.75, 37.8],
        '韶关': [113.62, 24.84],
        '嘉峪关': [98.289152, 39.77313],
        '广州': [113.23, 23.16],
        '延安': [109.47, 36.6],
        '太原': [112.53, 37.87],
        '清远': [113.01, 23.7],
        '中山': [113.38, 22.52],
        '昆明': [102.73, 25.04],
        '寿光': [118.73, 36.86],
        '盘锦': [122.070714, 41.119997],
        '长治': [113.08, 36.18],
        '珠海': [113.52, 22.3],
        '宿迁': [118.3, 33.96],
        '咸阳': [108.72, 34.36],
        '铜川': [109.11, 35.09],
        '平度': [119.97, 36.77],
        '佛山': [113.11, 23.05],
        '海口': [110.35, 20.02],
        '江门': [113.06, 22.61],
        '章丘': [117.53, 36.72],
        '肇庆': [112.44, 23.05],
        '大连': [121.62, 38.92],
        '临汾': [111.5, 36.08],
        '吴江': [120.63, 31.16],
        '石嘴山': [106.39, 39.04],
        '沈阳': [123.38, 41.8],
        '苏州': [120.62, 31.32],
        '茂名': [110.88, 21.68],
        '嘉兴': [120.76, 30.77],
        '长春': [125.35, 43.88],
        '胶州': [120.03336, 36.264622],
        '银川': [106.27, 38.47],
        '张家港': [120.555821, 31.875428],
        '三门峡': [111.19, 34.76],
        '锦州': [121.15, 41.13],
        '南昌': [115.89, 28.68],
        '柳州': [109.4, 24.33],
        '三亚': [109.511909, 18.252847],
        '自贡': [104.778442, 29.33903],
        '吉林': [126.57, 43.87],
        '阳江': [111.95, 21.85],
        '泸州': [105.39, 28.91],
        '西宁': [101.74, 36.56],
        '宜宾': [104.56, 29.77],
        '呼和浩特': [111.65, 40.82],
        '成都': [104.06, 30.67],
        '大同': [113.3, 40.12],
        '镇江': [119.44, 32.2],
        '桂林': [110.28, 25.29],
        '张家界': [110.479191, 29.117096],
        '宜兴': [119.82, 31.36],
        '北海': [109.12, 21.49],
        '西安': [108.95, 34.27],
        '金坛': [119.56, 31.74],
        '东营': [118.49, 37.46],
        '牡丹江': [129.58, 44.6],
        '遵义': [106.9, 27.7],
        '绍兴': [120.58, 30.01],
        '扬州': [119.42, 32.39],
        '常州': [119.95, 31.79],
        '潍坊': [119.1, 36.62],
        '重庆': [106.54, 29.59],
        '台州': [121.420757, 28.656386],
        '南京': [118.78, 32.04],
        '滨州': [118.03, 37.36],
        '贵阳': [106.71, 26.57],
        '无锡': [120.29, 31.59],
        '本溪': [123.73, 41.3],
        '克拉玛依': [84.77, 45.59],
        '渭南': [109.5, 34.52],
        '马鞍山': [118.48, 31.56],
        '宝鸡': [107.15, 34.38],
        '焦作': [113.21, 35.24],
        '句容': [119.16, 31.95],
        '徐州': [117.2, 34.26],
        '衡水': [115.72, 37.72],
        '包头': [110, 40.58],
        '绵阳': [104.73, 31.48],
        '乌鲁木齐': [87.68, 43.77],
        '枣庄': [117.57, 34.86],
        '杭州': [120.19, 30.26],
        '淄博': [118.05, 36.78],
        '鞍山': [122.85, 41.12],
        '溧阳': [119.48, 31.43],
        '库尔勒': [86.06, 41.68],
        '安阳': [114.35, 36.1],
        '开封': [114.35, 34.79],
        '济南': [117, 36.65],
        '德阳': [104.37, 31.13],
        '温州': [120.65, 28.01],
        '九江': [115.97, 29.71],
        '邯郸': [114.47, 36.6],
        '临安': [119.72, 30.23],
        '兰州': [103.73, 36.03],
        '沧州': [116.83, 38.33],
        '临沂': [118.35, 35.05],
        '南充': [106.110698, 30.837793],
        '天津': [117.2, 39.13],
        '富阳': [119.95, 30.07],
        '泰安': [117.13, 36.18],
        '诸暨': [120.23, 29.71],
        '郑州': [113.65, 34.76],
        '哈尔滨': [126.63, 45.75],
        '聊城': [115.97, 36.45],
        '芜湖': [118.38, 31.33],
        '唐山': [118.02, 39.63],
        '平顶山': [113.29, 33.75],
        '邢台': [114.48, 37.05],
        '德州': [116.29, 37.45],
        '济宁': [116.59, 35.38],
        '荆州': [112.239741, 30.335165],
        '宜昌': [111.3, 30.7],
        '义乌': [120.06, 29.32],
        '丽水': [119.92, 28.45],
        '洛阳': [112.44, 34.7],
        '秦皇岛': [119.57, 39.95],
        '株洲': [113.16, 27.83],
        '石家庄': [114.48, 38.03],
        '莱芜': [117.67, 36.19],
        '常德': [111.69, 29.05],
        '保定': [115.48, 38.85],
        '湘潭': [112.91, 27.87],
        '金华': [119.64, 29.12],
        '岳阳': [113.09, 29.37],
        '长沙': [113, 28.21],
        '衢州': [118.88, 28.97],
        '廊坊': [116.7, 39.53],
        '菏泽': [115.480656, 35.23375],
        '合肥': [117.27, 31.86],
        '武汉': [114.31, 30.52],
        '大庆': [125.03, 46.58]
    };

    CITY_PROVINCE_MAP = {
        '总行': '北京',
        '北京': '北京',
        '上海': '上海',
        '广州': '广东',
        '烟台': '山东',
        '武汉': '湖北',
        '大连': '辽宁',
        '杭州': '浙江',
        '南京': '江苏',
        '太原': '山西',
        '石家庄': '河北',
        '重庆': '重庆',
        '西安': '陕西',
        '贵阳': '贵州',
        '常德': '湖南',
        '福州': '福建',
        '济南': '山东',
        '汕头': '广东',
        '深圳': '广东',
        '宁波': '浙江',
        '成都': '四川',
        '天津': '天津',
        '昆明': '云南',
        '泉州': '福建',
        '三亚': '海南',
        '绍兴': '浙江',
        '苏州': '江苏',
        '青岛': '山东',
        '温州': '浙江',
        '厦门': '福建',
        '郑州': '河南',
        '长沙': '湖南',
        '无锡': '江苏',
        '长春': '吉林',
        '合肥': '安徽',
        '南昌': '江西',
        '邯郸': '河北',
        '常州': '江苏',
        '镇江': '江苏',
        '吕梁': '山西',
        '沧州': '河北',
        '潍坊': '山东',
        '曲靖': '云南',
        '洛阳': '河南',
        '衡阳': '湖南',
        '江门': '广东',
        '中山': '广东',
        '南阳': '河南',
        '衡水': '河北',
        '南通': '江苏',
        '襄阳': '湖北',
        '秦皇岛': '河北',
        '大同': '山西',
        '唐山': '河北',
        '泰州': '江苏',
        '南宁': '广西',
        '莆田': '福建',
        '嘉兴': '浙江',
        '德阳': '四川',
        '东营': '山东',
        '红河': '云南',
        '宜昌': '湖北',
        '株洲': '湖南',
        '宝鸡': '陕西',
        '呼和浩特': '内蒙古',
        '沈阳': '辽宁',
        # '总行': '北京',
        '珠海': '广东',
        # '总行': '北京',
        # '总行': '北京',
        '许昌': '河南',
        '盐城': '江苏',
        '湘潭': '湖南',
        '淮安': '江苏',
        '吉林': '吉林',
        '台州': '浙江',
        '龙岩': '福建',
        '马鞍山': '安徽',
        '上饶': '江西',
        '临沂': '山东',
        '徐州': '江苏',
        '赣州': '江西',
        '威海': '山东',
        '济宁': '山东',
        '柳州': '广西',
        # '总行': '北京',
        '金华': '浙江',
        '鄂尔多斯': '内蒙古',
        # '总行': '北京',
        '东莞': '广东',
        '香港': '香港',
        # '总行': '北京',
        '拉萨': '西藏',
        '揭阳': '广东',
        '舟山': '浙江',
        '盘锦': '辽宁',
        '张家口': '河北',
        '浏阳': '湖南',
        '哈尔滨': '黑龙江',
        # '上海': '上海',
        '兰州': '甘肃',
        # '上海': '上海',
        '运城': '山西',
        '遵义': '贵州',
        '宜宾': '四川',
        '宁德': '福建',
        '泰安': '山东',
        '新乡': '河南',
        '惠州': '广东',
        '乌鲁木齐': '新疆',
        # '总行': '北京',
        '银川': '宁夏',
        '葫芦岛': '辽宁',
        '宿迁': '江苏',
        '漯河': '河南',
        '大庆': '黑龙江',
        '西宁': '青海',
        '淄博': '山东',
        '日照': '山东',
    }

    def __init__(self):
        self.title_text = ''
        self.visualMap_max_day = 0
        self.visualMap_min_day = 999999
        self.visualMap_max_month = 0
        self.visualMap_min_month = 999999
        self.visualMap_max_mtop = 0
        self.visualMap_min_mtop = 999999
        self.series_data_mtop = []
        self.series_data_day = []
        self.series_data_day_province = []
        self.series_data_month = []
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.today_n_ago = (datetime.datetime.now() - datetime.timedelta(days=self.PERIOD_DAYS)).strftime("%Y%m%d")
        self.selected_date = ''

    # 由于查询涉及到具体的工单字段，因此图类的方法需要按名称区分不同数据源的处理,而不是统一函数名称
    # 系统类工单数据, group by date
    def mk_Areaitoms_gby_type_date(self, _itoms_type, _itoms_date):
        '''
        可以按机构区分的工单
        group by selected itoms_type and itoms_date
        lengend:按本日,本月,月TOP 由于类目固定,因此在前段JS中写死
        :param _itoms_type: 工单类型
        :param _itoms_date: 工单日期
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        self.selected_date = _itoms_date  # 当前选中日期,格式同源数据库，字符串保存
        f_month_1 = _itoms_date[0:6] + '01'
        f_month_31 = _itoms_date[0:6] + '31'

        self.title_text = u'%s按分行统计' % _itoms_type
        # self.legend_data = ['当天', '当月', '月TOP']

        # 查询当前要处理的数据集合，不做加工
        # from django.db.models import Q
        query_set = itoms_count.objects \
            .filter(crt_date=self.selected_date, itoms_type=_itoms_type)

        query_set_month = itoms_count.objects \
            .filter(crt_date__gte=f_month_1, crt_date__lte=f_month_31, itoms_type=_itoms_type)

        # 根据当前数据集，生成group by 统计数据的所有集合
        query_group_by = query_set.values('area_name') \
            .annotate(count_grp=Sum('count'))

        query_group_by_month = query_set_month.values('area_name') \
            .annotate(count_grp=Sum('count')).order_by('-count_grp')

        # 当天的数据
        f_dict_area_value = {}
        for itom in query_group_by:
            f_area_name = itom['area_name']
            if f_area_name == u"总行":
                f_city_name = u"北京市"
            else:
                f_city_name = u"%s市" % f_area_name  # 目前所有的城市加"市"得到城市名, 所以没有单独建映射表

            f_dict_area_value[f_city_name] = itom['count_grp']
            # 城市映射到省,累加
            for pcm in self.CITY_PROVINCE_MAP:
                # print type(pcm) str
                # print type(f_area_name) unicode
                if pcm.decode('utf-8') == f_area_name:
                    f_province_name = self.CITY_PROVINCE_MAP[pcm]
                    if f_province_name in f_dict_area_value:
                        f_dict_area_value[f_province_name] += itom['count_grp']
                    else:
                        f_dict_area_value[f_province_name] = itom['count_grp']

        for itom in f_dict_area_value:
            self.series_data_day.append({'name': itom, 'value': f_dict_area_value[itom]})
            self.visualMap_max_day = max(self.visualMap_max_day, f_dict_area_value[itom])
            self.visualMap_min_day = min(self.visualMap_min_day, f_dict_area_value[itom])

        # 当月的数据
        f_dict_area_value = {}
        for itom in query_group_by_month:
            f_area_name = itom['area_name']
            if f_area_name == u"总行":
                f_city_name = u"北京市"
            else:
                f_city_name = u"%s市" % f_area_name  # 目前所有的城市加"市"得到城市名, 所以没有单独建映射表

            f_dict_area_value[f_city_name] = itom['count_grp']
            # 城市映射到省,累加
            for pcm in self.CITY_PROVINCE_MAP:
                # print type(pcm) str
                # print type(f_area_name) unicode
                if pcm.decode('utf-8') == f_area_name:
                    f_province_name = self.CITY_PROVINCE_MAP[pcm]
                    if f_province_name in f_dict_area_value:
                        f_dict_area_value[f_province_name] += itom['count_grp']
                    else:
                        f_dict_area_value[f_province_name] = itom['count_grp']

        for itom in f_dict_area_value:
            self.series_data_month.append({'name': itom, 'value': f_dict_area_value[itom]})
            self.visualMap_max_month = max(self.visualMap_max_month, f_dict_area_value[itom])
            self.visualMap_min_month = min(self.visualMap_min_month, f_dict_area_value[itom])

        # 当月TOPN数据准备
        for i in range(self.TOP_N):
            f_area_name = query_group_by_month[i]['area_name']
            f_jing_wei=[]
            for j in self.GEO_COORD_MAP:
                # print type(j) str
                # print type(f_area_name) unicode
                if j.decode('utf-8') == f_area_name:
                    f_jing_wei = self.GEO_COORD_MAP[j][:]   #防止引用拷贝
                    break
                else:
                    f_jing_wei = [84, 45]  # 当经纬度不存在时,放在克拉玛依,以便观察

            # print "-----------"
            # print f_jing_wei
            # print query_group_by_month[i]['count_grp']
            f_jing_wei.append(query_group_by_month[i]['count_grp'])
            data_dict = {
                'name': f_area_name,
                'value': f_jing_wei
            }

            self.visualMap_max_mtop = max(self.visualMap_max_mtop, query_group_by_month[i]['count_grp'])
            self.visualMap_min_mtop = min(self.visualMap_min_mtop, query_group_by_month[i]['count_grp'])
            self.series_data_mtop.append(data_dict)
            # print self.series_data_mtop

        # visualMap分为5段,需要是5的倍数,适当扩大值
        self.visualMap_max_day = max(self.visualMap_max_day / 4 * 5, 5)
        self.visualMap_max_month = max(self.visualMap_max_month / 4 * 5, 5)
        self.visualMap_max_mtop = max(self.visualMap_max_mtop / 4 * 5, 5)

        self.visualMap_min_day = self.visualMap_min_day / 6 * 5
        self.visualMap_min_month = self.visualMap_min_month / 6 * 5
        self.visualMap_min_mtop = self.visualMap_min_mtop / 6 * 5

        # print self.series_data_day_province
        return self.get_dict_data()

    def get_dict_data(self):
        result = {
            'title_text': self.title_text,
            'visualMap_max_day': self.visualMap_max_day,
            'visualMap_max_month': self.visualMap_max_month,
            'visualMap_max_mtop': self.visualMap_max_mtop,
            'visualMap_min_day': self.visualMap_min_day,
            'visualMap_min_month': self.visualMap_min_month,
            'visualMap_min_mtop': self.visualMap_min_mtop,
            'series_data_mtop': self.series_data_mtop,
            'series_data_day': self.series_data_day,
            'series_data_day_province': self.series_data_day_province,
            'series_data_month': self.series_data_month,
        }
        return result
