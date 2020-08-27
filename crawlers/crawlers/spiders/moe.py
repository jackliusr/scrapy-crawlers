import scrapy
from scrapy.selector import Selector
from scrapy.http import FormRequest,Request

from crawlers.items import SchoolItem

class MoeSpider(scrapy.Spider):
    name = "moe"
    allowed_domains = ["moe.edu.sg"]    
 
    def start_requests(self):
      """
      school_codes = ['1150', '1234', '1249', '1230', '1196', '1129', '1145',
      '1640', '1020', '1247', '1209', '1751', '1256', '1771', 
      '1211', '1239', '1203', '1244', '1772', '1757', '1760', 
      '1754', '1132', '1168', '1102', '1229', '1183', '1755', 
      '1237', '1769', '1737', '1252', '1119', '1756', '1246', 
      '1657', '1177', '1610', '1257', '1208', '1107', '1221', 
      '1222', '1251', '1245', '1765', '1733', '1735', '1038', 
      '1121', '1739', '1255', '1763', '1223', '1250', '1207', 
      '1166', '1727', '1045', '1753', '1726', '1238', '1745', 
      '1248', '1232', '1242', '1619', '1645', '1151', '1764', 
      '1730', '1621', '1761', '1740', '1253', '1729', '1212', 
      '1263', '1743', '1243', '1650', '1236', '1741', '1228', 
      '1259', '1742', '1260', '1202', '1197', '1734', '1071', 
      '1072', '1073', '1217', '1264', '1752', '1077', '1195', 
      '1759', '1746', '1261', '1220', '1161', '1241', '1262', 
      '1174', '1736', '1201', '1773', '1158', '1043', '1218', 
      '1160', '1189', '1750', '1767', '1770', '1748', '1258', 
      '1749', '1758', '1114', '1747', '1205', '1731', '1724', 
      '1227', '1725', '1762', '1143', '1172', '1658', '1656', 
      '1219', '1199', '1240', '1235', '5625', '5001', '5638', 
      '5003', '5637', '5005', '5017', '5007', '5019', '5004', 
      '5636', '5008', '5020', '5022', '5634', '5626', '5608', 
      '5168', '5024', '5601', '7301', '5183', '5027', '5018', 
      '5028', '5622', '5258', '5197', '5635', '5602', '5623', 
      '5603', '5214', '5026', '5009', '5011', '5259', '5012', 
      '5025', '5014', '5013', '5015', '5240']
      """
      """
      school_codes =['3072', '3201', '3001', '3026', '3501', '3002', '3003', '3069', '3033', '3027', '3229', 
        '3225', '3021', '3054', '3224', '3043', '3202', '3044', '3203', '3204', '3040', '3621', 
        '3004', '3402', '3206', '3057', '3055', '3029', '3404', '3012', '3622', '3610', '3005', 
        '3056', '3228', '3503', '3207', '3609', '3237', '3075', '3623', '3064', '3208', '3024', 
        '3614', '3006', '3074', '3051', '3059', '3238', '3016', '3048', '3060', '3046', '3226', 
        '3608', '3211', '3068', '3063', '3066', '3619', '3065', '3049', '3212', '3615', '3031', 
        '3047', '3214', '3507', '3602', '3071', '3612', '3058', '3605', '3215', '3613', '3235', 
        '3073', '3232', '3061', '3231', '3062', '3070', '3508', '3007', '3618', '3239', '3606', 
        '3607', '3509', '3010', '3234', '3227', '3011', '3053', '3304', '3037', '3511', '3013', 
        '3512', '3403', '3030', '3611', '3014', '3067', '3620', '3015', '3616', '3604', '3041', 
        '3050', '3222', '3020', '3045', '3223', '3019', '3307', '3617', '3240']
      """
      school_codes = ['0803', '0802', '0805', '0804', '0705', '0713', 
      '0703', '0712', '0711', '0710', '0709', '0708']
      for code in school_codes:
        yield Request(url='http://sis.moe.gov.sg/SchoolDetails.aspx?schoolCode={0}'.format(code),callback= self.parse_school)
      

      
    def parse_school(self, response):
      sel = Selector(response)
      item = SchoolItem()
      url = response.url
      item["name"] = sel.xpath("//a[@id='ctl00_schoolDetailContainer_fieldSchoolName']/text()").extract()
      item["email"] = sel.xpath("//a[@id='ctl00_schoolDetailContainer_fieldEmail']/text()").extract()
      item["phone"] = sel.xpath("//div[@id='ctl00_schoolDetailContainer_fieldTelephone']/text()").extract()
      item["fax"] = sel.xpath("//div[@id='ctl00_schoolDetailContainer_fieldFax']/text()").extract()
      item["address"] = sel.xpath("//div[@id='ctl00_schoolDetailContainer_fieldSchoolAddress']/text()").extract()
      yield item
      #http://sis.moe.gov.sg/Pages/SchoolDetails/GeneralInformation.aspx?schoolCode=1020
      #request = Request(url ="http://sis.moe.gov.sg/Pages/SchoolDetails/GeneralInformation.aspx?schoolCode={0}".format(url[-4:]), callback=self.parse_principal)
      #request.meta["item"] = item      
      #return request
    
    def parse_principal(self,response):
      item = response.meta['item']
      sel = Selector(response)
      item['principal'] = sel.xpath("//div[@id='principalNames']/text()").extract()
      yield item
      
