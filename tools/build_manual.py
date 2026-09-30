from pathlib import Path
from urllib.parse import urlencode
import json, html, math

ROOT = Path(__file__).resolve().parents[1]
E = html.escape
PLACES = {}
def place(key, name, lat, lng, query=None):
    PLACES[key] = dict(name=name, lat=lat, lng=lng, query=query or name)

for args in [
 ('pvg1','浦东机场 T1',31.144,121.802,'Shanghai Pudong International Airport Terminal 1'),
 ('pvg2','浦东机场 T2',31.144,121.812,'Shanghai Pudong International Airport Terminal 2'),
 ('ams','史基浦机场',52.309,4.764,'Amsterdam Airport Schiphol'),
 ('central','阿姆斯特丹中央车站',52.3791,4.9003,'Amsterdam Centraal'),
 ('damrak','Damrak 运河屋',52.3754,4.8978,'Damrak Amsterdam'),
 ('dam','水坝广场',52.3731,4.8933,'Dam Square Amsterdam'),
 ('royal','阿姆斯特丹王宫',52.3732,4.8914,'Royal Palace Amsterdam'),
 ('anne','安妮之家外观',52.3752,4.8839,'Anne Frank House Westermarkt 20 Amsterdam'),
 ('nine','九街',52.3695,4.8847,'De 9 Straatjes Amsterdam'),
 ('begijn','贝居安院',52.3692,4.8901,'Begijnhof Amsterdam'),
 ('flower','花市',52.3669,4.8919,'Bloemenmarkt Amsterdam'),
 ('osl','奥斯陆机场',60.1939,11.1004,'Oslo Airport Gardermoen'),
 ('boo','博德机场',67.2692,14.3653,'Bodø Airport'),
 ('svj','斯沃尔维尔机场',68.2433,14.6691,'Svolvær Airport Helle'),
 ('nordis','Nordis Hotel Lofoten',68.2352,14.5722,'Nordis Hotel Lofoten Austnesfjordgata 36 Svolvær'),
 ('svol','斯沃尔维尔市中心',68.2323,14.5640,'Svolvær sentrum Norway'),
 ('devilstart','恶魔之门徒步起点',68.2438,14.5645,'Parkering for Sherpatrappa Djevelporten Svolvær'),
 ('devil','Djevelporten 恶魔之门',68.2519,14.5740,'Djevelporten Svolvær'),
 ('kiwi','KIWI Svolvær',68.2310,14.5620,'KIWI Svolvær Norway'),
 ('rema','REMA 1000 Svolvær',68.2305,14.5625,'REMA 1000 Svolvær'),
 ('lofotenshop','Lofotenshop',68.2328,14.5661,'Lofotenshop Svolvær'),
 ('arcticlights','Arctic Lights Lofoten',68.2318,14.5635,'Arctic Lights Lofoten Svolvær'),
 ('sport','Sport 1 Sportshuset',68.232,14.566,'Sport 1 Sportshuset Svolvær'),
 ('kabel','卡伯尔沃格',68.2112,14.4802,'Kabelvåg Norway'),
 ('church','Vågan Church',68.2121,14.4880,'Vågan Church Kabelvåg'),
 ('henn','亨宁斯维尔',68.1543,14.2033,'Henningsvær Norway'),
 ('stadium','亨宁斯维尔足球场',68.1459,14.2001,'Henningsvær Football Stadium'),
 ('haddock','Haddock 毛线帽店',68.154,14.201,'Haddock Henningsvær'),
 ('mors','Mors Hus',68.155,14.203,'Mors Hus Henningsvær'),
 ('hennsouvenir','Henningsvær Souvenir Butikk',68.155,14.204,'Henningsvær Souvenir Butikk'),
 ('mix','MIX Joh Malnes Handleri',68.154,14.205,'MIX Joh Malnes Handleri Henningsvær'),
 ('eggum','Eggum',68.3072,13.6727,'Eggum Norway'),
 ('unstad','Unstad Beach',68.2637,13.5718,'Unstad Beach Norway'),
 ('hauk','Haukland 海滩',68.1990,13.5279,'Hauklandstranda Parking Norway'),
 ('skag','Skagsanden 海滩',68.1046,13.2853,'Skagsanden beach Norway'),
 ('ramberg','Ramberg 海滩',68.0986,13.2388,'Ramberg Beach Norway'),
 ('fredvang','Fredvang 桥群',68.0869,13.1605,'Fredvangskrysset Norway'),
 ('hamn','Hamnøy 红房子',67.9456,13.1327,'Hamnøy viewpoint Norway'),
 ('sakri','Sakrisøy 黄房子',67.9410,13.1122,'Anita’s Sjømat Sakrisøy Norway'),
 ('reine','雷纳 Reine',67.9327,13.0895,'Reine Norway'),
 ('reinepark','Ytre Havn 官方指定停车区',67.9324,13.1034,'Reine Ytre Havn Parking Reinebringen Norway'),
 ('reinetrail','Reinebringen 徒步起点',67.9209,13.0736,'Reinebringen trailhead Norway'),
 ('coop','Coop Prix Reine',67.9366,13.0939,'Coop Prix Reine'),
 ('a','Å村',67.8803,12.9810,'Å i Lofoten Norway'),
 ('apark','Å村停车场',67.8809,12.9762,'Å Parking Lofoten Norway'),
 ('amuseum','挪威渔村博物馆',67.8801,12.9825,'Norsk Fiskeværsmuseum Åvegen 21 Sørvågen Norway'),
 ('svjport','斯沃尔维尔邮轮码头',68.2296,14.5682,'Fiskergata 23 8300 Svolvær Norway'),
 ('tosport','特罗姆瑟邮轮码头',69.6471,18.9577,'Samuel Arnesens gate 5 9008 Tromsø Norway'),
 ('tromso','特罗姆瑟市中心',69.6492,18.9553,'Tromsø sentrum Norway'),
 ('storgata','Storgata 步行街',69.6494,18.9547,'Storgata Tromsø Norway'),
 ('toscath','特罗姆瑟主教座堂',69.6482,18.9553,'Tromsø Cathedral Norway'),
 ('gift','Tromsø Gift & Souvenir',69.6510,18.9560,'Tromsø Gift & Souvenir Shop AS'),
 ('waynor','WAY NOR Tromsø',69.649,18.957,'WAY NOR Tromsø'),
 ('touristshop','Tourist Shop Tromsø',69.649,18.957,'Tourist Shop Tromsø'),
 ('snarby','Snarby Strikkestudio',69.6524,18.9556,'Snarby Strikkestudio Storgata 90 Tromsø'),
 ('eurospar','EUROSPAR Storgata',69.654,18.954,'EUROSPAR Storgata Tromsø'),
 ('mcd','McDonald’s Tromsø',69.650,18.956,'McDonald’s Tromsø'),
 ('bridge','Tromsøbrua 大桥',69.651,18.976,'Tromsø Bridge Norway'),
 ('arcticcat','北极大教堂',69.6482,18.9878,'Arctic Cathedral Tromsø'),
 ('cable','Fjellheisen 缆车下站',69.6407,18.9861,'Fjellheisen Solliveien 12 Tromsdalen'),
 ('polar','极地博物馆',69.6524,18.9607,'The Polar Museum Søndre Tollbodgate 11 Tromsø'),
 ('prest','Prestvannet 湖',69.6610,18.9411,'Prestvannet Tromsø'),
 ('telegraf','Telegrafbukta 海湾',69.6307,18.9109,'Telegrafbukta Tromsø'),
 ('tos','特罗姆瑟机场',69.6833,18.9189,'Tromsø Airport Langnes'),
 ('gdn','格但斯克机场',54.3776,18.4662,'Gdańsk Lech Wałęsa Airport'),
 ('ltn','伦敦卢顿机场',51.8791,-0.3766,'London Luton Airport'),
 ('parkway','Luton Airport Parkway',51.871,-0.394,'Luton Airport Parkway railway station'),
 ('pancras','St Pancras 车站',51.5316,-0.1265,'St Pancras International London'),
 ('westminster','西敏寺外观',51.4994,-0.1273,'Westminster Abbey London'),
 ('bigben','大本钟',51.5007,-0.1246,'Big Ben London'),
 ('eye','伦敦眼河岸',51.5033,-0.1195,'London Eye London'),
 ('james','圣詹姆斯公园',51.5025,-0.1348,'St James’s Park London'),
 ('buckingham','白金汉宫外观',51.5014,-0.1419,'Buckingham Palace London'),
 ('trafalgar','特拉法加广场',51.5080,-0.1281,'Trafalgar Square London'),
 ('covent','科文特花园',51.5117,-0.1240,'Covent Garden London'),
 ('soho','Soho／唐人街',51.5129,-0.1319,'Chinatown London'),
 ('museum','大英博物馆',51.5194,-0.1269,'British Museum Great Russell Street London'),
 ('stpaul','圣保罗大教堂外观',51.5138,-0.0984,'St Paul’s Cathedral London'),
 ('millennium','千禧桥',51.5095,-0.0985,'Millennium Bridge London'),
 ('borough','博罗市场',51.5055,-0.0910,'Borough Market London'),
 ('towerbridge','伦敦塔桥',51.5055,-0.0754,'Tower Bridge London'),
 ('tower','伦敦塔外观',51.5081,-0.0759,'Tower of London'),
 ('sky','Sky Garden',51.5113,-0.0836,'Sky Garden 1 Sky Garden Walk London'),
 ('lhr','希思罗机场 T3',51.4716,-0.4568,'Heathrow Airport Terminal 3'),
 ('tao','青岛胶东机场',36.362,120.088,'Qingdao Jiaodong International Airport')
]: place(*args)

def nav(key, mode=None):
    p=PLACES[key]
    params={'api':'1','destination':p['query'],'dir_action':'navigate'}
    if mode: params['travelmode']=mode
    return 'https://www.google.com/maps/dir/?'+urlencode(params)
def link(key, label=None, mode=None):
    return f'<a class="place" href="{E(nav(key,mode))}" target="_blank" rel="noopener noreferrer">{E(label or PLACES[key]["name"])}<span aria-hidden="true">↗</span></a>'
def official(url,label='官网'): return f'<a href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(label)} ↗</a>'
def route_url(keys,mode):
    if len(keys)==1:return nav(keys[0],mode)
    params={'api':'1','origin':PLACES[keys[0]]['query'],'destination':PLACES[keys[-1]]['query'],'travelmode':mode,'dir_action':'navigate'}
    if len(keys)>2:params['waypoints']='|'.join(PLACES[x]['query'] for x in keys[1:-1])
    assert len(keys)<=5
    return 'https://www.google.com/maps/dir/?'+urlencode(params)

SOURCES={
 'nordis':'https://nordishotel.bylofoten.no/en/map-practical/',
 'havila':'https://www.havilavoyages.com/',
 'havcheck':'https://support.havilavoyages.com/en/check-in-times',
 'havseats':'https://support.havilavoyages.com/en/deck-space-comfort-chair-or-cabin',
 'havports':'https://support.havilavoyages.com/en/port-addresses',
 'museumA':'https://www.museumnord.no/vare-museer/norsk-fiskevaersmuseum/',
 'devil':'https://visitlofoten.com/en/guide/floya-and-djevelporten-590-m/',
 'reinehike':'https://visitlofoten.com/en/guide/reinebringen-hike/',
 'reinesafety':'https://reinebringen.no/safety/',
 'reineparking':'https://reinebringen.no/parking/',
 'cable':'https://www.fjellheisen.no/engelsk/practical-info',
 'polar':'https://en.uit.no/tmu/polarmuseet/planlegg',
 'british':'https://www.britishmuseum.org/visit',
 'sky':'https://skygarden.london/booking/',
 'anne':'https://www.annefrank.org/en/museum/tickets/',
 'luggage':'https://www.schiphol.nl/en/at-schiphol/services/luggage-storage/',
 'lofoten':'https://visitlofoten.com/en/topic/plan-your-trip/travel-within-lofoten/',
 'luton':'https://www.lutonairportexpress.co.uk/routes/luton-airport-to-london',
 'road':'https://www.vegvesen.no/en/traffic-information/traffic-information/',
 'aurora':'https://www.visittromso.no/northern-lights/faq',
 'holiday':'https://www.gov.uk/bank-holidays',
 'maps':'https://developers.google.com/maps/documentation/urls/get-started'
}
SOURCES['ceair']='https://global.ceair.com/global/en_USD/Announcement/AnnouncementMessage/202505/t20250529_28241.html'
SOURCES['wideroe']='https://help.wideroe.no/hc/no/articles/29541777305746-Kontakt-oss'

COLORS=['#ad603f','#287c91','#bb8e27','#34766a','#655e9a','#496da8','#ad5374','#956143','#638858','#3b7184']
DAYS=[]
def day(n,title,region,tz,offset,sleep,keys,routes,note):
    d=dict(date=f'2026-10-{n:02}',n=n,title=title,region=region,tz=tz,offset=offset,sleep=sleep,keys=keys,routes=routes,note=note,color=COLORS[n-2],rows=[])
    DAYS.append(d);return d
def row(d,time,title,body,keys=[],tag=None,kind='plan',event=True):
    d['rows'].append(dict(time=time,title=title,body=body,keys=keys,tag=tag,kind=kind,event=event))

d=day(2,'阿姆斯特丹短停 · 奥斯陆转机','上海 → 荷兰 → 挪威','Europe/Amsterdam','+02:00','奥斯陆机场 · 过夜休息方案待定',['central','damrak','dam','royal','anne','nine'],[('全天市区主线','walking',['central','dam','anne','nine','central'])],'市区时间取决于出关速度。18:25左右返机场；延误时缩短散步，博物馆入内留待下一次。')
row(d,'06:00','抵达浦东机场T1','建议起飞前3小时到机场；护照、登机资料随身。',['pvg1'],kind='buffer')
row(d,'09:00','上海起飞 · MU209','浦东T1 → 阿姆斯特丹；上海时间 CST / UTC+8。',['pvg1','ams'],tag='已出票',kind='confirmed')
row(d,'14:55','阿姆斯特丹落地','当地 CEST / UTC+2。入境、取行李；以机场实时排队为准。',['ams'],tag='已出票',kind='confirmed')
row(d,'15:45','行李寄存 · 火车进城','计划时间。抵达层 -1、Arrivals 1与2之间 Baggage Storage；大件行李€9.50/件/日，24小时开放。跟随Trains指示，乘火车至Amsterdam Centraal。'+official(SOURCES['luggage'],'寄存位置与价格'),['ams','central'])
row(d,'16:15','中央车站 → 运河屋 → 水坝广场','轻装步行，王宫以外观拍照为主。',['central','damrak','dam','royal'])
row(d,'17:00','安妮之家外观 · 九街','安妮之家入内须官网预约指定时段；目前未订票，主线按外观安排。九街自由逛、吃早晚饭。'+official(SOURCES['anne'],'安妮之家预约'),['anne','nine'])
row(d,'18:25','结束市区行程 · 返回机场','乘返程火车，取寄存行李。不要把剩余时间全部留给排队或购物。',['central','ams'],kind='buffer')
row(d,'19:30','抵达出发区 · 办理托运与安检','此为建议缓冲时间；以航空公司规定的柜台及截止时间为准。',['ams'],kind='buffer')
row(d,'21:45','阿姆斯特丹起飞','前往奥斯陆；两地均为 CEST / UTC+2。',['ams','osl'],tag='已出票',kind='confirmed')
row(d,'23:30','抵达奥斯陆 · 过夜转机','转机8小时，截图标注重新托运行李。先确认是否需要提取行李、早班柜台开放时间；机场酒店／机场休息待安排。',['osl'],tag='已出票',kind='confirmed')

d=day(3,'斯沃尔维尔 · 恶魔之门','挪威 · 罗佛敦','Europe/Oslo','+02:00','Nordis Hotel Lofoten · 已订',['svj','nordis','devilstart','devil','svol'],[('全天市区主线','walking',['nordis','devilstart','svol','nordis'])],'11:20抵达；酒店订单16:00后入住。提前入住未获确认，先寄存行李。恶魔之门保留，湿滑、大风或疲劳时折返。')
row(d,'05:30','奥斯陆机场 · 早班准备','建议时间；完成行李重新托运及安检。',['osl'],kind='buffer')
row(d,'07:30','奥斯陆起飞 → 博德','09:00抵达博德。',['osl','boo'],tag='已出票',kind='confirmed')
row(d,'09:00','博德转机','与10:55起飞相隔1小时55分；若分开出票／行李未直挂，优先处理行李和下一程登机。',['boo'],tag='已出票',kind='confirmed')
row(d,'10:55','博德起飞 · WF824','11:20抵达斯沃尔维尔机场。',['boo','svj'],tag='已出票',kind='confirmed')
row(d,'11:20','抵达斯沃尔维尔','机场到酒店约5.5公里。接驳先核对当日公交与站点，时间不合适用出租车；不预设有机场直达巴士。',['svj','nordis'],tag='已出票',kind='confirmed')
row(d,'12:00','酒店寄存 · 午饭与休整','先询问提前入住；无法提前入房时寄存行李、午饭。早餐为次日两人份。',['nordis'])
row(d,'13:00','Djevelporten 恶魔之门徒步','预留约3小时往返，含市区到起点及拍照。只到恶魔之门，Fløya完整登顶需增加时间；官方完整路线标示单程约2小时。湿滑时不上巨石。'+official(SOURCES['devil'],'路线与难度'),['devilstart','devil'])
row(d,'16:00','返回酒店 · 办理入住','入住码由酒店通过邮件／短信发送。洗澡休息后再逛市区。',['nordis'],tag='已订酒店',kind='confirmed')
row(d,'17:15','纪念品店 · 采购两天补给','10/4为周日，超市与小店营业以分店为准；饮水、早餐、徒步午餐尽量今天备齐。',['lofotenshop','arcticlights','sport','kiwi','rema'])
row(d,'18:30','晚饭 · 休息','次日自驾停靠多，今晚优先补足睡眠。',['svol'])
row(d,'21:00','斯沃尔维尔取车','租期已口头确认；公司、取车地址、晚间交接办法、保险与押金待订单补齐。不要直接导航去任一家租车门店。',tag='待补租车订单',kind='anchor')

d=day(4,'向南自驾 · 海滩与渔村','挪威 · 罗佛敦','Europe/Oslo','+02:00','雷纳／哈姆诺伊一带 · 待订',['svol','church','henn','eggum','unstad','hauk','skag','ramberg','fredvang','hamn','sakri','reine'],[('全天主线','driving',['svol','henn','unstad','hauk','reine']),('北段全部停靠','driving',['svol','church','henn','eggum','unstad']),('海滩与桥群','driving',['unstad','hauk','skag','ramberg','fredvang']),('南段渔村','driving',['fredvang','hamn','sakri','reine'])],'纯驾驶估算约5–6小时，含北侧绕行；停靠后是一整天。Eggum、Unstad是优先缩减项。时间仅为规划，雨风、施工、停车会影响实际到达。')
row(d,'07:00','早餐 · 整理行李退房','酒店早餐官网为07:00–10:00；11:00前退房。检查油量、轮胎和路况。',['nordis'],kind='buffer')
row(d,'08:00','从斯沃尔维尔出发','向南自驾，行李放后备箱；目的地停车规则到场确认。',['svol'])
row(d,'08:20','卡伯尔沃格 · Vågan Church','教堂外观短停；不预设周日礼拜时可入内参观。',['church','kabel'])
row(d,'09:00','亨宁斯维尔 · 足球场','约45分钟至1小时。先足球场，再渔港；周日商店是否开门到场确认。',['stadium','henn','haddock','mors','hennsouvenir','mix'])
row(d,'10:45','Eggum · 可选短停','计划约20分钟。若出发晚、雨风大或前面逛久，直接跳过，保护南段白天拍摄时间。',['eggum'],tag='可选')
row(d,'11:30','Unstad Beach · 可选短停','不走远程徒步，沙滩拍照后离开。与Eggum可二选一。',['unstad'],tag='可选')
row(d,'12:20','Haukland 海滩 · 午餐','约45分钟至1小时，今天以海滩散步为主。停车是否收费看现场标牌；不保证免费。',['hauk'])
row(d,'14:00','Skagsanden 海滩','短停约20分钟；可留意今晚云量，是否返回追光视住宿位置与疲劳决定。',['skag'])
row(d,'14:35','Ramberg 海滩','约20分钟；在合法停车位停稳后再拍照。',['ramberg'])
row(d,'15:10','Fredvang 桥群','短停约20分钟；导航至附近停车点。桥上和路肩不随意停车。',['fredvang'])
row(d,'16:10','Hamnøy · 经典红房子','先找合法停车位，再步行至桥上视角；留意车辆。',['hamn'])
row(d,'16:40','Sakrisøy · 黄房子与Anita’s','黄房子拍照。Anita’s鱼汤、汉堡视当天营业情况；没开门就雷纳晚饭。',['sakri'])
row(d,'17:25','雷纳 · 入住与晚饭','住宿尚未订，建议雷纳／哈姆诺伊一带，方便次日徒步；具体地址等订单补齐。',['reine'],tag='住宿待订')
row(d,'20:30','可选近距离看极光','仅在天晴、道路适合且精神充足时出门；以住宿附近安全开阔点为主。海滩大风、桥上、狭窄路肩不作为停留点。',['reine','hamn'],tag='天气决定')

d=day(5,'雷纳徒步 · Å村 · 返程登船','挪威 · 罗佛敦','Europe/Oslo','+02:00','MS Havila Castor · Relax Chairs座椅',['reine','reinepark','reinetrail','a','ramberg','svol','svjport'],[('全天自驾主线','driving',['reine','a','ramberg','svol','svjport']),('徒步入口步行','walking',['reinepark','reinetrail'])],'雷纳徒步官方推荐5–9月，10月仅在步道开放、干燥无冰且风况适合时考虑；条件不合适直接改镇内拍照。17:30前回斯沃尔维尔，20:30争取完成还车；接驳待订单复核。')
row(d,'07:00','早餐 · 打包退房与徒步准备','按酒店要求提前完成退房，整理行李放入车内，徒步只背必需品。带水、防水外套、防滑徒步鞋、头灯和补给；天气不适合就改镇内拍照。',['reine'])
row(d,'07:30','Reinebringen · 条件适合才徒步','先查官方步道状态和山顶风雨；推荐季节为5–9月，秋季可能结冰。雨、雾、冰雪或强风时取消。由Ytre Havn停车区出发，往返约5.8公里、爬升约484米，预留3.5–4小时含接近步行与拍照；约2000级陡台阶。若进度慢，提前折返，保护登船时间。'+official(SOURCES['reinesafety'],'步道状态与安全')+' · '+official(SOURCES['reineparking'],'指定停车'),['reinepark','reinetrail'],tag='季节风险·先查状态')
row(d,'11:45','雷纳出发 → Å村','徒步结束后前往Å村，行李和退房手续提前处理好，避免超过酒店退房时限。取消徒步时可提前逛镇，博物馆11:00开门。',['reine','apark'])
row(d,'12:20','Å村 · 挪威渔村博物馆','博物馆10月每天11:00–15:00，成人NOK125；目前未订票。先博物馆，再村内散步与简餐；13:45前离开。'+official(SOURCES['museumA'],'官方开放与票价'),['amuseum','a'],tag='付费·未订票')
row(d,'13:45','开始向北返程','从Å返回斯沃尔维尔，纯驾驶规划约2.5–3小时，另留休息和天气缓冲。只按需短停；不新增长徒步。',['a','ramberg','svol'])
row(d,'16:45','斯沃尔维尔 · 补给与晚餐','目标到达时间，允许路况缓冲至17:30。加油、收好车内物品；船票未含餐食，准备晚饭和次日早餐。',['svol','kiwi','rema'],kind='buffer')
row(d,'20:30','争取提前完成还车','合同截止21:00。提前还车、钥匙交接及到码头交通需与租车公司确认；拍摄车辆状态留存。',tag='需确认还车地点',kind='buffer')
row(d,'21:15','抵达邮轮码头 · 登船准备','建议时间，Fiskergata 23。船方通常出发前15分钟截止办理；不要以22:00为到达目标。'+official(SOURCES['havcheck'],'登船要求'),['svjport'],kind='buffer')
row(d,'22:15','Havila Castor 开船','两人已付款，Relax Chairs座椅区，未订餐食。座椅附近有厕所，无淋浴；带眼罩、耳塞、薄毯与充电设备。'+official(SOURCES['havseats'],'座椅设施'),['svjport','tosport'],tag='已付款',kind='confirmed')

d=day(6,'海上航程 · 特罗姆瑟夜景','挪威 · 特罗姆瑟','Europe/Oslo','+02:00','特罗姆瑟市中心 · 待订',['tosport','storgata','bridge','arcticcat','cable'],[('全天市区主线','walking',['tosport','storgata','arcticcat','cable']),('不爬山的市中心路线','walking',['tosport','toscath','storgata','polar'])],'14:15到港。下午先安顿，傍晚缆车看城市夜景；风大可能停运，保留10/7白天补去的窗口。')
row(d,'09:00','船上早餐 · 海岸风景','自行购买或使用准备的食物；不要把船上过夜等同于已订酒店床位。')
row(d,'14:15','抵达特罗姆瑟','Samuel Arnesens gate 5码头。下船、取行李，前往待订的市中心住宿。',['tosport','tromso'],tag='已出票船程',kind='confirmed')
row(d,'15:00','入住 · 午后休整','酒店未订，具体入住时间等订单补齐；建议市中心，方便步行与机场接驳。',['tromso'],tag='住宿待订')
row(d,'16:00','主教座堂 · Storgata散步','逛纪念品、银饰与毛线店；购物点来自原行程，营业时间以当天为准。',['toscath','storgata','gift','waynor','touristshop','snarby','mcd'])
row(d,'17:00','过桥 · 北极大教堂外观','步行过桥注意风力；大风时改公交或出租车。教堂入内票未订，主线按外观。',['bridge','arcticcat'])
row(d,'18:00','Fjellheisen 缆车 · 夜景','官网常规开放09:00–00:00，风况可能造成停运，先看当日公告再购票。公交26／出租车前往，10月上旬不依赖冬季专线。'+official(SOURCES['cable'],'运营与接驳'),['cable'],tag='需购票·天气决定')
row(d,'20:00','晚饭 · 晴夜可看极光','缆车不运行时，市区晚饭后可考虑Prestvannet。极光需暗夜、较少云和活动支持，不能保证看到。',['tromso','prest'],tag='可选')

d=day(7,'极地博物馆 · 晚班飞格但斯克','挪威 → 波兰','Europe/Oslo','+02:00','格但斯克机场 · 过夜休息方案待定',['polar','storgata','telegraf','tos'],[('全天市区主线','walking',['polar','storgata','toscath','telegraf']),('前往机场','transit',['tromso','tos'])],'22:10飞行是今天的硬锚。今天不安排晚间追光团；缆车若昨日停运，可替换海湾散步，仍按时回城取行李。')
row(d,'09:00','早餐 · 退房寄存行李','退房时间等酒店订单；保留一份随身换洗和防雨衣物。',['tromso'])
row(d,'10:00','极地博物馆 Polarmuseet','官方开放每天10:00–18:00；成人NOK130，未订票。安排约1.5小时。'+official(SOURCES['polar'],'开放与票价'),['polar'],tag='付费·未订票')
row(d,'11:45','午餐 · 纪念品补购','Storgata及市中心；不要携带行李箱进馆。',['storgata','gift','waynor','snarby','eurospar'])
row(d,'14:00','Telegrafbukta 海湾 · 松弛散步','天气好时坐公交／步行到海湾；步行全程较长，可用公交缩短。若补缆车，替换此项。',['telegraf'],tag='可替换')
row(d,'17:30','早晚饭 · 取行李','回住宿取寄存行李，检查下一程登机资料；夜里在格但斯克不依赖餐厅营业。',['tromso'],kind='buffer')
row(d,'18:45','从市中心前往机场','公交班次用Svipper查当日计划，或出租车；为22:10航班留足缓冲。',['tromso','tos'],kind='buffer')
row(d,'19:15','抵达特罗姆瑟机场','建议抵达时间；柜台、托运行李及登机截止以航空公司规定为准。',['tos'],kind='buffer')
row(d,'22:10','特罗姆瑟起飞 → 格但斯克','次日00:55抵达；挪威与波兰均CEST / UTC+2。转机需重新托运行李、重新办理登机。',['tos','gdn'],tag='已出票',kind='confirmed')

d=day(8,'伦敦经典 · 西敏与皇家公园','波兰 → 英国 · 伦敦','Europe/London','+01:00','伦敦 · 待订',['westminster','bigben','eye','james','buckingham','trafalgar','covent','soho'],[('全天步行主线','walking',['westminster','eye','buckingham','trafalgar','covent']),('西敏与公园','walking',['westminster','bigben','eye','james','buckingham']),('广场与晚饭','walking',['buckingham','trafalgar','covent','soho'])],'07:35到卢顿。机场入境、交通、寄存优先；上午安排较松，给前一晚转机后的体力留余地。景点入内都不默认已订。')
row(d,'00:55','抵达格但斯克 · 过夜转机','当地CEST / UTC+2，转机5小时15分。按订单领取行李并重新办理登机；优先休息。',['gdn'],tag='已出票',kind='confirmed')
row(d,'04:00','下一程托运与安检准备','建议缓冲时间；先核对柜台开放及截止时间，行李是否可以提前交运以航司为准。',['gdn'],kind='buffer')
row(d,'06:10','格但斯克起飞','波兰 CEST / UTC+2。',['gdn','ltn'],tag='已出票',kind='confirmed')
row(d,'07:35','抵达伦敦卢顿','英国 BST / UTC+1；两地时差1小时。办理英国入境及取行李。',['ltn'],tag='已出票',kind='confirmed')
row(d,'09:00','DART + 火车进伦敦','计划时间。DART到Luton Airport Parkway，换乘至St Pancras；最快约32分钟，不含入境、候车和到酒店时间。'+official(SOURCES['luton'],'机场快线'),['ltn','parkway','pancras'])
row(d,'10:00','市区寄存行李 · 早餐','建议伦敦住宿选择Soho／Bloomsbury／St Pancras周边，具体地址等订单补齐；提前入住待酒店确认。',['pancras','soho'],tag='住宿待订')
row(d,'11:00','西敏寺外观 · 大本钟','步行拍照，不预设西敏寺入内票；不占用长队时间。',['westminster','bigben'])
row(d,'12:00','泰晤士河 · 伦敦眼河岸','伦敦眼以河岸外观为主，乘坐需另外订票；午饭后慢走。',['eye'])
row(d,'13:30','圣詹姆斯公园 · 白金汉宫','公园散步与宫殿外观；不把未核实的换岗仪式列为固定事件。',['james','buckingham'])
row(d,'15:00','回酒店入住 · 午后休息','以最终酒店入住时间为准，补眠后再出门；疲劳时直接取消后续自由散步。',tag='依酒店订单调整')
row(d,'16:30','特拉法加广场 · 科文特花园','城市步行、街头表演与小店；晚饭可在Soho／唐人街。',['trafalgar','covent','soho'])
row(d,'19:00','晚饭 · 早点休息','今天经历红眼转机，保留体力给次日博物馆。',['soho'])

d=day(9,'大英博物馆 · 塔桥 · 回国','英国 · 伦敦','Europe/London','+01:00','回国航班上',['museum','stpaul','millennium','borough','towerbridge','tower','lhr'],[('全天市区主线','walking',['museum','stpaul','borough','towerbridge','tower']),('博物馆到圣保罗','transit',['museum','stpaul']),('泰晤士河步行','walking',['stpaul','millennium','borough','towerbridge','tower'])],'22:05希思罗T3起飞；17:30取行李并出发、19:00到机场。Sky Garden只作预约成功后的替换，不与所有景点叠加。')
row(d,'08:30','早餐 · 退房寄存行李','出门前打包行李，确认酒店寄存取回时间；不携带大行李进大英博物馆。')
row(d,'10:00','大英博物馆 · 重点参观','免费常设展，建议提前预约10:00入馆，预留约2小时。官网常规10:00–17:00，周五延长开放；今天不使用晚场，因为要赶飞机。'+official(SOURCES['british'],'免费预约'),['museum'],tag='免费·建议预约')
row(d,'12:15','午餐 · 前往圣保罗','优先用公交／地铁缩短博物馆到圣保罗的移动时间；全天步行主线可查看方向，不强制全部走完。',['stpaul'])
row(d,'13:15','圣保罗外观 · 千禧桥','外观与河景，教堂入内需另购票，当前未订。',['stpaul','millennium'])
row(d,'14:00','博罗市场 · 塔桥','市场补充食物后沿河步行；塔桥外观和过桥免费，展览需另购票。',['borough','towerbridge','tower'])
row(d,'15:30','自由拍照／Sky Garden替换项','若提前拿到免费时段，可替换部分圣保罗／河岸散步；不要临时排队挤占机场时间。Sky Garden目前有电梯故障、容量减少的官方提示。'+official(SOURCES['sky'],'免费预约与公告'),['sky'],tag='可选·先预约')
row(d,'16:30','结束景点 · 返回取行李','从河岸回酒店，具体交通按最终住宿位置调整。',kind='buffer')
row(d,'17:30','带行李前往希思罗T3','根据住宿选Elizabeth line／地铁等；核对目的地为Terminal 3，留出换乘与步行时间。',['lhr'],kind='buffer')
row(d,'19:00','抵达希思罗T3','建议抵达时间，办理国际航班托运、安检；实际截止时间以航司为准。',['lhr'],kind='buffer')
row(d,'22:05','伦敦起飞 → 青岛','英国 BST / UTC+1；次日16:10抵达青岛，中国 CST / UTC+8。截图标注行李直达，仍须按入境和转机要求办理手续。',['lhr','tao'],tag='已出票',kind='confirmed')

d=day(10,'青岛转机 · 夜航上海','中国','Asia/Shanghai','+08:00','青岛转机 → 上海夜航',['tao','pvg2'],[('机场位置','driving',['tao'])],'中国时间UTC+8。青岛转机6小时25分，优先入境与转机，不安排出机场赶景点。')
row(d,'16:10','抵达青岛胶东机场','办理入境及国内转机；虽截图标注行李直达，托运行李是否需海关检查按现场流程确认。',['tao'],tag='已出票',kind='confirmed')
row(d,'18:00','机场晚饭 · 休息','在机场内等候，核对下一程登机口及登机时间。',['tao'])
row(d,'21:30','进入候机状态','建议缓冲时间，留意登机通知，不把22:35起飞时间当成登机时间。',['tao'],kind='buffer')
row(d,'22:35','青岛起飞 → 上海','次日00:10抵达浦东T2，中国CST / UTC+8。',['tao','pvg2'],tag='已出票',kind='confirmed')

d=day(11,'凌晨抵沪 · 回家休息','中国 · 上海','Asia/Shanghai','+08:00','上海',['pvg2'],[('到达航站楼','driving',['pvg2'])],'00:10为落地时间，出机场还需取行李和通行时间。提前安排深夜接送，回家后休息。')
row(d,'00:10','抵达上海浦东T2','两人旅行结束，取行李后乘预约车／出租车返家。',['pvg2'],tag='已出票',kind='confirmed')
row(d,'01:00','取行李 · 深夜接送','计划时间，实际以航班和取行李进度为准。',['pvg2'],event=False)

EVENTS=[]
for d in DAYS:
 for r in d['rows']:
  if not r['event']:continue
  offset=d['offset']; tz=d['tz']
  if d['n']==2 and r['time'] in ['06:00','09:00']:offset='+08:00';tz='Asia/Shanghai'
  if d['n']==8 and r['time'] in ['00:55','04:00','06:10']:offset='+02:00';tz='Europe/Warsaw'
  EVENTS.append(dict(at=d['date']+'T'+r['time']+':00'+offset,tz=tz,title=r['title'],day=d['n'],kind=r['kind'],place=r['keys'][0] if r['keys'] else None,note= ('已确认时间' if r['kind']=='confirmed' else '建议时间，按现场情况调整') if r['kind']!='anchor' else '时间已口头确认，地址待订单补齐'))

def zone(tz):return {'Asia/Shanghai':'CST · UTC+8','Europe/Amsterdam':'CEST · UTC+2','Europe/Oslo':'CEST · UTC+2','Europe/Warsaw':'CEST · UTC+2','Europe/London':'BST · UTC+1'}[tz]
def svg_route(keys,color,ident,route_layers=None):
    pts=[PLACES[k] for k in keys];w,h=680,310
    latmid=sum(p['lat'] for p in pts)/len(pts)
    coords=[(p['lng']*math.cos(math.radians(latmid)),-p['lat']) for p in pts]
    mnx=min(x for x,y in coords);mxx=max(x for x,y in coords);mny=min(y for x,y in coords);mxy=max(y for x,y in coords)
    dx=max(mxx-mnx,.01);dy=max(mxy-mny,.01);scale=min(530/dx,205/dy)
    out=[]
    for x,y in coords:out.append((w/2+(x-(mnx+mxx)/2)*scale,h/2+(y-(mny+mxy)/2)*scale))
    projected=dict(zip(keys,out))
    content=f'<svg class="route-svg" viewBox="0 0 {w} {h}" role="img" aria-label="{E(ident)}的地点与路线示意"><defs><pattern id="grid{ident}" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M 28 0 H 0 V 28" fill="none" stroke="currentColor" stroke-opacity=".07"/></pattern></defs><rect width="680" height="310" rx="18" fill="var(--sea)"/><rect width="680" height="310" rx="18" fill="url(#grid{ident})"/><path d="M0 244 Q98 174 184 223 T370 205 T540 235 T680 166 V310 H0Z" fill="var(--land)" opacity=".65"/>'
    for i,(route_keys,route_color) in enumerate(route_layers or [(keys,color)]):
        lines=' '.join(f'{projected[k][0]+i*5:.1f},{projected[k][1]+i*3:.1f}' for k in route_keys)
        content+=f'<polyline points="{lines}" fill="none" stroke="{route_color}" stroke-width="{5 if i==0 else 3}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="7 7"/>'
    for i,(key,(x,y)) in enumerate(zip(keys,out)):
        content+=f'<a href="{E(nav(key))}" target="_blank" aria-label="导航至{E(PLACES[key]["name"])}"><title>{E(PLACES[key]["name"])}</title><circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{color}" stroke="var(--paper)" stroke-width="3"/><text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" fill="white" font-size="13" font-weight="700">{i+1}</text></a>'
    content+='<text x="22" y="29" fill="currentColor" font-size="13" opacity=".6">N ↑ · 地点路线示意</text></svg>'
    content+='<div class="map-key">'+''.join(f'<span><i style="background:{color}">{i+1}</i>{link(k)}</span>' for i,k in enumerate(keys))+'</div>'
    return content

def route_details(d):
    btns=''.join(f'<a class="button {"primary" if i==0 else "secondary"}" href="{E(route_url(keys,mode))}" target="_blank" rel="noopener noreferrer">{E(label)}导航 ↗</a>' for i,(label,mode,keys) in enumerate(d['routes']))
    return f'<details class="day-map"><summary>展开当日路线地图 <span>地图与多点导航</span></summary><div class="map-content">{svg_route(d["keys"],d["color"],str(d["n"]))}<div class="route-buttons">{btns}</div><p class="micro">主线含关键停靠点；更多地点按分段导航。Google手机网页最多支持3个中途点，徒步山路请使用专用离线徒步地图。</p></div></details>'

def timeline(d):
    rows=''
    for r in d['rows']:
        tz=d['tz']
        if d['n']==2 and r['time'] in ['06:00','09:00']:tz='Asia/Shanghai'
        if d['n']==8 and r['time'] in ['00:55','04:00','06:10']:tz='Europe/Warsaw'
        tag=f'<span class="tag {"ok" if r["kind"]=="confirmed" else "warn" if r["tag"] and ("预约" in r["tag"] or "待" in r["tag"] or "未订" in r["tag"]) else ""}">{E(r["tag"])}</span>' if r['tag'] else ''
        links='<div class="locations">'+''.join(link(k) for k in r['keys'])+'</div>' if r['keys'] else ''
        rows+=f'<li class="timeline-row {r["kind"]}"><div class="time"><strong>{r["time"]}</strong><small>{zone(tz)}</small></div><div class="timeline-content"><div class="row-title"><h4>{E(r["title"])}</h4>{tag}</div><p>{r["body"]}</p>{links}</div></li>'
    weekday=['周五','周六','周日','周一','周二','周三','周四','周五','周六','周日'][d['n']-2]
    return f'<article class="day-card" id="day-{d["n"]}" style="--day:{d["color"]}"><div class="day-heading"><span class="day-number">10.{d["n"]:02}<small>{weekday}</small></span><div><p class="eyebrow">{E(d["region"])}</p><h3>{E(d["title"])}</h3></div></div><div class="day-meta"><span>{zone(d["tz"])}</span><span>夜宿 · {E(d["sleep"])}</span></div>{route_details(d)}<p class="day-note">{E(d["note"])}</p><ol class="timeline">{rows}</ol></article>'

def overview():
    # Hand-drawn schematic panels keep both countries and the Lofoten detail legible on a phone.
    pts={'ams':(125,228),'osl':(240,172),'boo':(328,117),'svj':(355,85),'tromso':(436,51),'gdn':(270,274),'ltn':(62,292),'lhr':(34,324),'tao':(456,333),'pvg2':(460,365)}
    s='<svg class="overview-svg" viewBox="0 0 530 408" role="img" aria-label="10月2日至11日，上海、阿姆斯特丹、罗佛敦、特罗姆瑟、伦敦与回程路线"><rect width="530" height="408" rx="18" fill="var(--sea)"/><path d="M195 294 C165 238 225 216 217 177 S262 135 278 95 L339 22 L379 11 L345 64 Q324 115 295 147 L289 206 L309 238 L352 296 Z" fill="var(--land)" stroke="var(--map-stroke)" stroke-width="1.5"/><path d="M20 290 Q12 267 35 253 L52 266 L59 294 L80 315 L54 337 L25 327 Z M5 305 L16 294 L21 326 L7 333Z" fill="var(--land)" stroke="var(--map-stroke)"/><path d="M96 219 Q139 202 175 230 L220 250 L242 290 L204 365 L123 377 L98 327 Z" fill="var(--land)" stroke="var(--map-stroke)"/><text x="365" y="186" fill="currentColor" opacity=".45" font-size="19" transform="rotate(-25 365 186)">NORWAY</text><text x="21" y="235" fill="currentColor" opacity=".45" font-size="15">UK</text><text x="27" y="29" fill="currentColor" font-size="12">N ↑ · 行程示意，非实路比例</text>'
    s+=f'<defs><linearGradient id="ship-days"><stop offset="0" stop-color="{COLORS[3]}"/><stop offset="50%" stop-color="{COLORS[3]}"/><stop offset="51%" stop-color="{COLORS[4]}"/><stop offset="100%" stop-color="{COLORS[4]}"/></linearGradient></defs>'
    routes=[('pvg2','ams',COLORS[0],'10/2 去程'),('ams','osl',COLORS[0],'10/2'),('osl','boo',COLORS[1],'10/3'),('boo','svj',COLORS[1],''),('svj','tromso',COLORS[3],'10/5–6 船'),('tromso','gdn',COLORS[5],'10/7'),('gdn','ltn',COLORS[6],'10/8'),('lhr','tao',COLORS[7],'10/9–10'),('tao','pvg2',COLORS[8],'10/10–11')]
    for a,b,c,label in routes:
        x,y=pts[a];xx,yy=pts[b];mx=(x+xx)/2+15;my=(y+yy)/2-14
        paint='url(#ship-days)' if a=='svj' and b=='tromso' else c
        s+=f'<path d="M{x} {y} Q{mx} {my} {xx} {yy}" fill="none" stroke="{paint}" stroke-width="2.5" stroke-dasharray="5 4"/>'
        if label:s+=f'<text x="{mx}" y="{my-3}" fill="{c}" font-size="10">{label}</text>'
    for key,(x,y) in pts.items():
        name={'ams':'阿姆斯特丹','osl':'奥斯陆','boo':'博德','svj':'斯沃尔维尔','tromso':'特罗姆瑟','gdn':'格但斯克','ltn':'卢顿','lhr':'希思罗','tao':'青岛','pvg2':'上海'}[key]
        labelx=x+8 if x<430 else x-8;anchor='start' if x<430 else 'end'
        s+=f'<a href="{E(nav(key))}" target="_blank" aria-label="导航至{E(name)}"><circle cx="{x}" cy="{y}" r="4.5" fill="var(--ink)"/><text x="{labelx}" y="{y-6}" fill="currentColor" text-anchor="{anchor}" font-size="12" font-weight="600">{name}</text></a>'
    for x,y,c,text_value,anchor in [(245,190,COLORS[0],'10/2 机场过夜·待定','start'),(364,103,COLORS[1],'10/3 Nordis·已订','start'),(444,71,COLORS[4],'10/6 市中心·待订','end'),(281,290,COLORS[5],'10/7 机场过夜·待定','start'),(25,350,COLORS[6],'10/8 伦敦·待订','start')]:
        s+=f'<text x="{x}" y="{y}" fill="{c}" text-anchor="{anchor}" font-size="9">{text_value}</text>'
    s+='<path d="M80 61 l18 -24 21 25 19 -17 24 31" fill="none" stroke="var(--map-stroke)" stroke-width="2"/><path d="M328 313 l8 -17 8 17 m-8 -17 v27" stroke="var(--map-stroke)" fill="none"/><text x="360" y="389" fill="currentColor" font-size="11" opacity=".6">↘ 中国回程示意</text></svg>'
    # Lofoten inset uses geographic point positions, day colors and a northbound return.
    inset=svg_route(['svol','henn','hauk','ramberg','hamn','reine','a'],COLORS[2],'lofoten',[
        (['svol','henn','hauk','ramberg','hamn','reine'],COLORS[2]),
        (['reine','a','ramberg','svol'],COLORS[3])])
    inset=inset.replace('</svg>',f'<text x="430" y="270" fill="{COLORS[3]}" font-size="13">10/5 向北返程 ↗</text><text x="22" y="291" fill="{COLORS[2]}" font-size="13">10/4 雷纳／哈姆诺伊·待订</text></svg>')
    sleeps=''.join(f'<li><span style="color:{d["color"]}">10/{d["n"]}</span><b>{E(d["sleep"])}</b></li>' for d in DAYS if d['n']<11)
    legend=''.join(f'<a href="#day-{d["n"]}"><i style="background:{d["color"]}"></i>10/{d["n"]}</a>' for d in DAYS)
    return f'<div class="overview-grid"><div>{s}<div class="day-legend">{legend}</div></div><div class="lofoten-inset"><p class="eyebrow">LOFOTEN · 罗佛敦自驾</p>{inset}<div class="inset-legend"><span><i style="background:{COLORS[2]}"></i>10/4 向南</span><span><i style="background:{COLORS[3]}"></i>10/5 返程登船</span></div></div></div><div class="nights"><h3>每晚落脚点</h3><ul>{sleeps}</ul></div>'

FLIGHTS=[
 ('10/2','上海 → 阿姆斯特丹','pvg1','ams','09:00 CST · UTC+8','14:55 CEST · UTC+2','MU209 · 浦东T1出发'),
 ('10/2–3','阿姆斯特丹 → 奥斯陆 → 博德','ams','boo','10/2 21:45 CEST · UTC+2','10/3 09:00 CEST · UTC+2','奥斯陆23:30到／次日07:30走 · 重新托运'),
 ('10/3','博德 → 斯沃尔维尔','boo','svj','10:55 CEST · UTC+2','11:20 CEST · UTC+2','WF824 · 博德转机1小时55分'),
 ('10/7–8','特罗姆瑟 → 格但斯克 → 卢顿','tos','ltn','10/7 22:10 CEST · UTC+2','10/8 07:35 BST · UTC+1','格但斯克00:55到／06:10走（UTC+2）· 重新托运与登机'),
 ('10/9–11','希思罗 → 青岛 → 浦东','lhr','pvg2','10/9 22:05 BST · UTC+1','10/11 00:10 CST · UTC+8','希思罗T3 · 青岛10/10 16:10到／22:35走（UTC+8）· 浦东T2到达')
]
def bookings():
    s='<div class="booking-grid">'
    for date,title,a,b,depart,arrive,note in FLIGHTS:
        if 'MU209' in note:
            contact='<p>东方航空 · <a href="tel:+862120695530">+86 21 20695530</a><br>中国境内 <a href="tel:95530">95530</a></p>'+official(SOURCES['ceair'],'官方客服电话')
        elif 'WF824' in note:
            contact='<p>Widerøe · <a href="tel:+4775535010">+47 75 53 50 10</a><br>客服选项3</p>'+official(SOURCES['wideroe'],'官方客服')
        else:
            contact='<p class="micro">航司电话／其余航班号：截图未提供，待完整订单补齐</p>'
        s+=f'<article class="booking flight"><div class="booking-top"><span>✈ {date}</span><span class="tag ok">2人已出票</span></div><h3>{E(title)}</h3><p class="flight-times"><b>{E(depart)}</b><span>→</span><b>{E(arrive)}</b></p><p>{E(note)}</p><div class="locations">{link(a)}{link(b)}</div>{contact}</article>'
    s+=f'<article class="booking"><div class="booking-top"><span>住宿 · 10/3–4</span><span class="tag ok">已付款</span></div><h3>Nordis Hotel Lofoten</h3><p><b>10/3 16:00后 → 10/4 11:00前</b><br>CEST · UTC+2 · Europe/Oslo</p><p>豪华双人房1间 · 2人早餐<br>已付 ¥900.16</p><p>{link("nordis","Austnesfjordgata 36, 8300 Svolvær")}</p><p><a href="tel:+4741298000">+47 412 98 000</a><br><a href="mailto:stay@nordishotel.no">stay@nordishotel.no</a></p><p class="micro">提前入住／寄存需确认；入住码通过短信或邮件发送。</p>{official(SOURCES["nordis"],"酒店实用信息")}</article>'
    s+=f'<article class="booking"><div class="booking-top"><span>邮轮 · 10/5–6</span><span class="tag ok">已付款</span></div><h3>MS Havila Castor</h3><p><b>10/5 22:15 → 10/6 14:15</b><br>CEST · UTC+2 · Europe/Oslo</p><p>2人 · Relax Chairs · Saver<br>共 €186 · 未订餐食 · 无淋浴</p><p>{link("svjport","上船：Fiskergata 23, Svolvær")}<br>{link("tosport","下船：Samuel Arnesens gate 5, Tromsø")}</p><p><a href="tel:+4770007070">+47 7000 7070</a></p><p class="micro">建议21:15到码头。休息座椅区，无床铺舱房。</p>{official(SOURCES["havcheck"],"登船要求")}</article>'
    s+='<article class="booking pending"><div class="booking-top"><span>租车 · 10/3–5</span><span class="tag warn">订单待补</span></div><h3>斯沃尔维尔取还车</h3><p><b>10/3 21:00 → 10/5 21:00</b><br>CEST · UTC+2 · Europe/Oslo</p><p>两天租期，时间由本人确认。公司、准确门店地址、电话、车型与保险等订单补齐。</p><p class="micro">21:00取车是否可交接、提前还车及还车后前往码头，都需要确认。</p></article>'
    s+='</div><p class="section-note">其他住宿尚未预订；未收到景点门票订单。公开页面仅保留旅行所需信息，订单号、护照号、登机二维码、入住码和支付资料不展示。</p>'
    return s

TODOS=[
 '补租车订单：公司、取还车精确地址、电话、车型、保险、押金及21:00晚间取车办法。',
 '确认10/5提前还车、钥匙交接和前往Fiskergata 23邮轮码头的交通；争取20:30完成还车。',
 '订10/4雷纳／哈姆诺伊一带住宿，确认停车、早餐与退房时间。',
 '订10/6特罗姆瑟市中心住宿，确认10/7退房后的行李寄存。',
 '订10/8伦敦住宿；建议Soho／Bloomsbury／St Pancras周边，确认10/9寄存取回时间。',
 '安排10/2奥斯陆8小时及10/7–8格但斯克5小时15分的过夜休息。',
 '确认Nordis Hotel能否提前入住／寄存，以及斯沃尔维尔机场到酒店接驳。',
 '补齐其余航班号、航司联系方式；确认分开出票的行李与自助转机要求。',
 '预约10/9大英博物馆10:00免费入馆。'+official(SOURCES['british'],'官方预约'),
 '若想去Sky Garden，提前查10/9下午免费时段；预约成功后替换部分河岸行程。'+official(SOURCES['sky'],'官方预约'),
 '雷纳徒步出发前查步道状态、山顶风雨与结冰；10月条件不合适直接取消。'+official(SOURCES['reinesafety'],'官方状态入口'),
 '缆车购票前核对天气与停运公告；Å村、极地博物馆尚未订票。',
 '核对申根签证：实际到10/8从格但斯克出境；核对英国eVisa关联护照及旅行保险覆盖日期。',
 '备好实体驾照及租车公司要求的翻译件、主驾驶本人信用卡、订单和紧急联系方式。',
 '出发前在线值机，保存两人登机资料与订单离线副本；下载Google区域地图和徒步地图。',
 '采购邮轮晚餐／早餐、眼罩耳塞；准备防水外套、徒步鞋、头灯和充电宝。',
 '安排10/11浦东T2凌晨落地后的接送。'
]

TIPS=[
 ('时间与倒计时','每个时间点都按事件所在地时区显示。荷兰、挪威、波兰为CEST／UTC+2，英国为BST／UTC+1，中国为CST／UTC+8；切换手机时区不改变倒计时。昼夜配色按行程所在地的日照自动切换。活动时间是建议安排，航班／船程是硬锚。'),
 ('离线阅读与导航','先在线打开一次并完成缓存，断网后可重开同一网址；也可下载单个HTML保存。正文、手绘地图、倒计时均在文件内。导航、实时天气和预约需要联网，Google Maps离线导航需预先下载对应区域，山路使用专用徒步地图。'),
 ('徒步与自驾','雨、风、湿滑石阶和疲劳都会降低速度。恶魔之门只到巨石附近。Reinebringen推荐季节5–9月，10月可能结冰；雨、雾、冰雪或强风时取消徒步，不把登顶列为保证完成项。停车按Ytre Havn官方指定区域。E10施工、停车与天气留缓冲。'+official(SOURCES['road'],'官方路况')+' · '+official(SOURCES['reinesafety'],'雷纳步道状态')+' · '+official(SOURCES['devil'],'恶魔之门路线')),
 ('停车与周日购物','原攻略中的“免费停车”不能作为现场保证：看标牌、限时、收费App和酒店要求，不在桥上／路肩临停。10/4周日，饮食补给优先10/3买齐；店铺营业按具体分店确认。'),
 ('极光窗口','优先10/4住宿附近、10/5船上安全甲板和10/6特罗姆瑟。少云、暗夜和极光活动要同时配合；不靠固定日期保证看到。10/7晚班飞机前不安排追光团。'+official(SOURCES['aurora'],'官方极光说明')),
 ('开放时间与预约','Å村渔村博物馆10月每天11:00–15:00；极地博物馆每天10:00–18:00。大英博物馆常设展免费，建议预约。Sky Garden免费但需先约合适时段，官网现有容量减少提示。安妮之家入内须预约，本次按外观。'+official(SOURCES['museumA'],'Å村')+' · '+official(SOURCES['polar'],'极地博物馆')+' · '+official(SOURCES['british'],'大英博物馆')),
 ('假日与预订','伦敦10/8–9为周四、周五，未遇英格兰法定银行假日；免费热门景点仍可能无票。挪威行程含周末，住宿尚未锁定，尽早预订。热门预约提前查看可用时段，未约到就走外观和河岸路线。'+official(SOURCES['holiday'],'英国官方假日')),
 ('紧急联系','挪威：医疗113、警察112、火警110。英国：紧急999／112。酒店：+47 412 98 000；Havila：+47 7000 7070；缆车：+47 776 38 737。遇天气变化先保证安全和下一段交通。'),
 ('两人共用这份手册','待办由网页统一维护，完成事项告诉我后移除。离线时看到的是最后缓存的内容，联网打开可获取当前页面。未订的酒店与门票始终明确标注，付款前再核对。')
]

CSS=r'''
:root{--paper:#fbf8ef;--bg:#f1eee4;--ink:#253d3b;--muted:#697975;--line:#dddcd0;--teal:#276761;--soft:#e6eee8;--sea:#e8efe9;--land:#f5ecd6;--map-stroke:#b1b8a5;--warn:#9a5630;--warnbg:#f6ead9;--shadow:0 5px 24px #354f4510;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:90px}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;font-size:15px;line-height:1.65}body[data-theme=dark]{--paper:#162724;--bg:#0f1d1c;--ink:#e3eee7;--muted:#a0b5ad;--line:#354641;--teal:#99c6b7;--soft:#263c34;--sea:#203932;--land:#394534;--map-stroke:#768b76;--warn:#e5b185;--warnbg:#42382a;--shadow:none;color-scheme:dark}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #bc8b3d;outline-offset:4px}button,a,summary{-webkit-tap-highlight-color:transparent}button{font:inherit;cursor:pointer}p{margin:.55em 0}h1,h2,h3,h4{line-height:1.35;margin:0}header{max-width:1100px;margin:auto;padding:24px 24px 13px;display:flex;align-items:center;justify-content:space-between;gap:16px}h1{font-size:21px;letter-spacing:.02em}.header-meta{font-size:12px;color:var(--muted);letter-spacing:.09em}.header-actions{display:flex;align-items:center;gap:10px}.status{font-size:11px;color:var(--muted)}.download{background:none;border:1px solid var(--line);color:var(--ink);padding:8px 12px;border-radius:10px;font-size:12px}.shell{max-width:1100px;margin:auto;padding:0 24px 90px}.focus{background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:25px 30px;box-shadow:var(--shadow);position:relative;overflow:hidden;display:grid;grid-template-columns:1fr auto;gap:20px}.focus:after{content:"";position:absolute;width:220px;height:220px;border:1px solid var(--line);border-radius:50%;right:-110px;top:-105px;pointer-events:none}.focus-info{min-width:0}.eyebrow{font-size:10px;letter-spacing:.15em;color:var(--muted);text-transform:uppercase;margin:0 0 7px;font-weight:600}.focus-label{display:flex;gap:8px;align-items:center;font-size:12px;letter-spacing:.15em;color:var(--teal);margin-bottom:12px}.focus-label:before{content:"";height:7px;width:7px;background:#bb8654;border-radius:50%;box-shadow:0 0 0 5px var(--warnbg)}.focus h2{font-size:25px;margin-bottom:9px}.focus-at{font-size:13px;color:var(--muted)}.focus-note{font-size:12px;color:var(--muted);margin:6px 0 11px}.focus-link{font-size:12px;font-weight:600}.countdown{display:flex;gap:11px;align-items:center;justify-content:flex-end;padding:12px 0 6px}.count-unit{min-width:58px;text-align:center}.count-unit strong{font-size:48px;line-height:1.1;font-variant-numeric:tabular-nums;letter-spacing:-.045em;font-weight:650;display:block}.count-unit span{font-size:10px;letter-spacing:.15em;color:var(--muted);display:block;margin-top:7px}.count-sep{font-size:23px;opacity:.25;padding-bottom:24px}.now-clock{font-size:11px;color:var(--muted);text-align:right;margin-top:8px;font-variant-numeric:tabular-nums}.quick-nav{position:sticky;top:0;z-index:10;background:var(--bg);border-bottom:1px solid var(--line);display:flex;gap:20px;margin-top:18px;padding:13px 2px;overflow-x:auto;white-space:nowrap;scrollbar-width:none}.quick-nav a{font-size:12px;color:var(--ink);font-weight:550}.section{margin-top:30px}.section-title{display:flex;align-items:baseline;gap:12px;margin-bottom:17px}.section-title .index{font-size:11px;font-weight:650;letter-spacing:.1em;color:var(--muted)}.section-title h2{font-size:19px}.section-title .aside{font-size:11px;color:var(--muted);margin-left:auto}.panel{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:20px}.overview-grid{display:grid;grid-template-columns:1fr 1fr;gap:23px;align-items:center}.overview-svg,.route-svg{width:100%;height:auto;display:block;color:var(--ink)}.day-legend{display:flex;gap:11px;flex-wrap:wrap;margin-top:15px}.day-legend a,.inset-legend span{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--muted)}.day-legend i,.inset-legend i{width:7px;height:7px;border-radius:50%;display:inline-block}.lofoten-inset{padding:10px 0}.lofoten-inset .map-key{font-size:11px}.map-key{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;margin-top:12px;font-size:12px}.map-key>span{display:flex;gap:7px;align-items:baseline;min-width:0}.map-key i{font-style:normal;font-size:9px;min-width:15px;height:15px;border-radius:50%;color:white;text-align:center;line-height:15px}.inset-legend{display:flex;gap:15px;margin-top:12px}.nights{border-top:1px solid var(--line);margin-top:20px;padding-top:16px}.nights h3{font-size:13px;margin-bottom:10px}.nights ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:10px 20px}.nights li{font-size:11px;display:flex;gap:8px}.nights li span{font-weight:650;white-space:nowrap}.nights li b{font-weight:450;color:var(--muted)}.booking-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.booking{border:1px solid var(--line);border-radius:15px;background:var(--paper);padding:18px;font-size:12px}.booking-top{display:flex;justify-content:space-between;align-items:center;gap:6px;font-size:11px;margin-bottom:14px}.booking h3{font-size:16px;margin-bottom:11px}.booking p{color:var(--muted);overflow-wrap:anywhere}.booking b{font-weight:600;color:var(--ink)}.flight-times{display:flex;flex-direction:column;gap:1px}.flight-times span{font-size:11px}.tag{font-size:10px;line-height:1.7;padding:2px 7px;white-space:nowrap;border-radius:5px;background:var(--soft);color:var(--muted);font-weight:500}.tag.ok{color:var(--teal);background:var(--soft)}.tag.warn{color:var(--warn);background:var(--warnbg)}.pending{border-style:dashed}.locations{display:flex;flex-wrap:wrap;gap:7px 12px;font-size:11px;margin-top:9px}.place span{font-size:.85em;margin-left:4px}.micro{font-size:10px!important;color:var(--muted);line-height:1.65}.section-note{font-size:11px;color:var(--muted);margin-top:13px}.date-nav{display:flex;gap:8px;overflow:auto;padding:0 0 14px;scrollbar-width:none}.date-nav a{background:var(--paper);border:1px solid var(--line);padding:7px 13px;border-radius:8px;white-space:nowrap;font-size:12px}.days{display:flex;flex-direction:column;gap:18px}.day-card{background:var(--paper);border:1px solid var(--line);border-radius:18px;overflow:hidden;scroll-margin-top:65px}.day-heading{display:flex;align-items:center;gap:18px;padding:22px 25px 12px;border-top:4px solid var(--day)}.day-number{font-size:25px;letter-spacing:-.05em;font-weight:650;color:var(--day);flex:0 0 70px}.day-number small{display:block;letter-spacing:.1em;font-size:10px;font-weight:500}.day-heading h3{font-size:19px}.day-meta{display:flex;gap:8px 18px;flex-wrap:wrap;margin:0 25px 15px;font-size:11px;color:var(--muted)}.day-map{margin:0 25px;border:1px solid var(--line);border-radius:10px}.day-map summary{padding:10px 13px;cursor:pointer;font-size:12px;font-weight:550}.day-map summary span{float:right;color:var(--muted);font-size:10px;font-weight:400}.map-content{padding:12px;border-top:1px solid var(--line)}.route-buttons{display:flex;gap:8px;flex-wrap:wrap;margin-top:15px}.button{font-size:11px;border-radius:7px;padding:9px 12px;font-weight:550;display:inline-flex;align-items:center;justify-content:center;gap:4px;min-height:39px}.button.primary{background:var(--ink);color:var(--paper)}.button.secondary{border:1px solid var(--line);color:var(--ink)}.day-note{margin:15px 25px 0;padding:12px 14px;background:var(--soft);border-radius:9px;font-size:12px;line-height:1.7;color:var(--muted)}.timeline{list-style:none;padding:8px 25px 13px;margin:0}.timeline-row{display:grid;grid-template-columns:84px 1fr;gap:18px;position:relative;padding:17px 0}.timeline-row:not(:last-child):after{content:"";position:absolute;left:84px;top:18px;bottom:-18px;border-left:1px solid var(--line)}.timeline-content{padding-left:4px;position:relative;min-width:0}.timeline-content:before{content:"";position:absolute;width:6px;height:6px;border-radius:50%;background:var(--day);left:-20px;top:7px;border:3px solid var(--paper);box-sizing:content-box}.timeline-row.confirmed .timeline-content:before{background:var(--day);box-shadow:0 0 0 2px var(--soft)}.time strong{font-size:17px;font-variant-numeric:tabular-nums;line-height:1.2}.time small{display:block;font-size:8px;line-height:1.5;color:var(--muted);margin-top:5px;white-space:nowrap}.row-title{display:flex;gap:9px;align-items:flex-start;flex-wrap:wrap}.row-title h4{font-size:14px;font-weight:600}.timeline-content p{font-size:12px;line-height:1.75;color:var(--muted);margin:6px 0 0}.todo-list{margin:0;padding:0;list-style:none;counter-reset:todo}.todo-list li{counter-increment:todo;position:relative;padding:13px 0 13px 37px;border-bottom:1px solid var(--line);font-size:13px;line-height:1.75}.todo-list li:last-child{border:0}.todo-list li:before{content:counter(todo,decimal-leading-zero);position:absolute;left:0;top:14px;color:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}.tips-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.tip{padding:19px;background:var(--paper);border:1px solid var(--line);border-radius:14px}.tip h3{font-size:14px;margin-bottom:8px}.tip p{font-size:12px;line-height:1.8;color:var(--muted);margin:0}.footer{font-size:10px;color:var(--muted);border-top:1px solid var(--line);padding-top:18px;margin-top:30px;display:flex;justify-content:space-between;gap:10px}.nojs{padding:12px;background:var(--warnbg);font-size:12px}.completed .countdown{opacity:.5}.visually-hidden{position:absolute;height:1px;width:1px;overflow:hidden;clip:rect(0,0,0,0)}
@media(max-width:760px){header{padding:18px 16px 12px}h1{font-size:18px}.shell{padding:0 16px 45px}.header-meta{font-size:10px}.header-actions{gap:5px}.status{display:none}.download{font-size:11px;padding:6px 9px}.focus{padding:21px 20px;grid-template-columns:1fr;gap:7px;border-radius:18px}.focus h2{font-size:22px}.focus-at{font-size:12px}.focus-label{margin-bottom:11px}.countdown{justify-content:space-between;gap:4px;padding:8px 0 0}.count-unit{min-width:45px}.count-unit strong{font-size:43px}.count-sep{font-size:19px}.now-clock{text-align:left;margin-top:12px}.quick-nav{gap:20px;padding:12px 0}.section{margin-top:25px}.section-title{gap:10px}.section-title h2{font-size:18px}.section-title .aside{font-size:10px}.panel{padding:14px}.overview-grid{grid-template-columns:1fr;gap:17px}.overview-svg{max-height:340px}.lofoten-inset{padding:0;border-top:1px solid var(--line);padding-top:15px}.nights ul{grid-template-columns:1fr 1fr;gap:10px 12px}.booking-grid{grid-template-columns:1fr 1fr;gap:9px}.booking{padding:13px;font-size:11px}.booking h3{font-size:14px}.booking-top{font-size:10px;flex-wrap:wrap;margin-bottom:9px}.tag{font-size:9px}.flight-times{line-height:1.65}.booking .locations{font-size:10px}.booking p{font-size:11px}.day-heading{padding:18px 16px 10px;gap:12px}.day-number{font-size:23px;flex-basis:57px}.day-heading h3{font-size:17px}.day-meta{margin:0 16px 13px;font-size:10px;gap:6px 10px}.day-map{margin:0 16px}.day-map summary{font-size:11px;padding:10px}.day-map summary span{font-size:9px}.day-note{margin:12px 16px 0;padding:10px 11px;font-size:11px}.timeline{padding:6px 16px 12px}.timeline-row{grid-template-columns:67px 1fr;gap:15px;padding:16px 0}.timeline-row:not(:last-child):after{left:67px}.timeline-content:before{left:-17px}.time strong{font-size:16px}.time small{font-size:7px}.row-title h4{font-size:13px}.timeline-content p{font-size:11px}.locations{font-size:10px;gap:5px 10px}.tips-grid{grid-template-columns:1fr}.tip{padding:16px}.tip p{font-size:11px}.map-key{font-size:10px;gap:6px}.route-buttons{gap:6px}.button{font-size:10px;padding:8px 10px}.todo-list li{font-size:12px;padding-left:30px}.footer{display:block}.footer span{display:block;margin:5px 0}}
@media(max-width:380px){.booking-grid{grid-template-columns:1fr}.count-unit strong{font-size:38px}.focus h2{font-size:20px}.header-meta{letter-spacing:.02em}.day-map summary span{display:none}.nights ul{grid-template-columns:1fr}}
.time small{font-size:9px}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:white!important;color:#222!important}.shell{max-width:none;padding:0}.focus,.panel,.booking,.day-card,.tip{box-shadow:none;break-inside:avoid;background:white!important}header{padding:10px 0}.quick-nav,.download,.date-nav,.status{display:none}.day-map{display:none}.section{margin-top:20px}.locations a{color:#333}.booking-grid{grid-template-columns:repeat(2,1fr)}.tips-grid{grid-template-columns:repeat(2,1fr)}}
'''

DATA=dict(events=EVENTS,places=PLACES,locations=[
 dict(at='2026-10-02T14:55:00+02:00',place='ams',tz='Europe/Amsterdam'),
 dict(at='2026-10-02T23:30:00+02:00',place='osl',tz='Europe/Oslo'),
 dict(at='2026-10-03T09:00:00+02:00',place='boo',tz='Europe/Oslo'),
 dict(at='2026-10-03T11:20:00+02:00',place='svol',tz='Europe/Oslo'),
 dict(at='2026-10-04T17:25:00+02:00',place='reine',tz='Europe/Oslo'),
 dict(at='2026-10-05T16:45:00+02:00',place='svol',tz='Europe/Oslo'),
 dict(at='2026-10-06T14:15:00+02:00',place='tromso',tz='Europe/Oslo'),
 dict(at='2026-10-08T00:55:00+02:00',place='gdn',tz='Europe/Warsaw'),
 dict(at='2026-10-08T07:35:00+01:00',place='ltn',tz='Europe/London'),
 dict(at='2026-10-08T10:00:00+01:00',place='museum',tz='Europe/London'),
 dict(at='2026-10-10T16:10:00+08:00',place='tao',tz='Asia/Shanghai'),
 dict(at='2026-10-11T00:10:00+08:00',place='pvg2',tz='Asia/Shanghai')
])
JS=r'''
(()=>{'use strict';
const data=JSON.parse(document.getElementById('trip-data').textContent);
const events=data.events.map(e=>({...e,ms:Date.parse(e.at)})).sort((a,b)=>a.ms-b.ms);
const places=data.places;
const tzLabels={'Asia/Shanghai':'中国 CST · UTC+8','Europe/Amsterdam':'荷兰 CEST · UTC+2','Europe/Oslo':'挪威 CEST · UTC+2','Europe/Warsaw':'波兰 CEST · UTC+2','Europe/London':'英国 BST · UTC+1'};
const locationAnchors=data.locations.map(x=>({...x,ms:Date.parse(x.at)})).sort((a,b)=>a.ms-b.ms);
const elements={title:document.getElementById('event-title'),at:document.getElementById('event-at'),note:document.getElementById('event-note'),link:document.getElementById('event-link'),clock:document.getElementById('now-clock'),focus:document.getElementById('focus')};
const units=['days','hours','minutes','seconds'].map(x=>document.getElementById(x));
let lastEvent='',lastMinute=-1;
function navTo(p){return 'https://www.google.com/maps/dir/?'+new URLSearchParams({api:'1',destination:p.query,dir_action:'navigate'});}
function currentLocation(now){let p={place:'pvg1',tz:'Asia/Shanghai'};for(const a of locationAnchors){if(a.ms>now)break;p=a;}return {...p,...places[p.place]};}
function solarDay(now,p){const t=new Date(now),start=Date.UTC(t.getUTCFullYear(),0,1),day=Math.floor((now-start)/86400000)+1,h=t.getUTCHours()+t.getUTCMinutes()/60;const g=2*Math.PI/365*(day-1+(h-12)/24);const dec=.006918-.399912*Math.cos(g)+.070257*Math.sin(g)-.006758*Math.cos(2*g)+.000907*Math.sin(2*g)-.002697*Math.cos(3*g)+.00148*Math.sin(3*g);const eq=229.18*(.000075+.001868*Math.cos(g)-.032077*Math.sin(g)-.014615*Math.cos(2*g)-.040849*Math.sin(2*g));const solar=((h*60+eq+4*p.lng)%1440+1440)%1440;const angle=(solar/4-180)*Math.PI/180,lat=p.lat*Math.PI/180;return Math.sin(lat)*Math.sin(dec)+Math.cos(lat)*Math.cos(dec)*Math.cos(angle)>Math.cos(90.833*Math.PI/180);}
function tick(){const now=Date.now();const next=events.find(e=>e.ms>now);const loc=currentLocation(now);if(next){const id=next.at+next.title;if(id!==lastEvent){elements.title.textContent=next.title;elements.at.textContent=new Intl.DateTimeFormat('zh-CN',{timeZone:next.tz,month:'long',day:'numeric',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date(next.ms))+' · '+tzLabels[next.tz];elements.note.textContent=next.note;elements.link.href='#day-'+next.day;elements.link.textContent='查看当天安排 ↓';lastEvent=id;}let sec=Math.max(0,Math.ceil((next.ms-now)/1000));const values=[Math.floor(sec/86400),Math.floor(sec%86400/3600),Math.floor(sec%3600/60),sec%60];values.forEach((v,i)=>units[i].textContent=String(v).padStart(2,'0'));}else{elements.title.textContent='已抵达上海 · 好好休息';elements.at.textContent='10月11日 00:10 · 中国 CST · UTC+8';elements.note.textContent='旅行手册可继续查看，所有时间保留当地时区。';elements.link.href='#day-11';elements.link.textContent='查看抵沪安排 ↓';units.forEach(x=>x.textContent='00');elements.focus.classList.add('completed');}const minute=Math.floor(now/60000);if(minute!==lastMinute){document.body.dataset.theme=solarDay(now,loc)?'light':'dark';elements.clock.textContent='行程所在地此刻 '+new Intl.DateTimeFormat('zh-CN',{timeZone:loc.tz,month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date(now))+' · '+tzLabels[loc.tz];lastMinute=minute;}}
tick();setInterval(tick,1000);document.addEventListener('visibilitychange',()=>{if(!document.hidden){lastMinute=-1;tick();}});
const status=document.getElementById('connection-status');let cachedReady=false;function networkStatus(){status.textContent=location.protocol==='file:'?'离线文件':!navigator.onLine?'离线阅读':cachedReady?'可离线阅读':'在线阅读';}window.addEventListener('online',networkStatus);window.addEventListener('offline',networkStatus);networkStatus();
if('serviceWorker' in navigator && /^https?:$/.test(location.protocol)){navigator.serviceWorker.register('/sw.js',{scope:'/'}).then(()=>navigator.serviceWorker.ready).then(()=>{cachedReady=true;networkStatus();}).catch(()=>{status.textContent='可下载离线版';});}
document.getElementById('download').addEventListener('click',()=>{const content='<!doctype html>\n'+document.documentElement.outerHTML;const blob=new Blob([content],{type:'text/html;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='挪威英国旅行手册_2026.html';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);});
})();
'''

focus='''<section class="focus" id="focus" aria-labelledby="event-title"><div class="focus-info"><div class="focus-label">此刻关注</div><h2 id="event-title">抵达浦东机场T1</h2><div class="focus-at" id="event-at">10月2日 06:00 · 中国 CST · UTC+8</div><p class="focus-note" id="event-note">建议时间，按现场情况调整</p><a class="focus-link" id="event-link" href="#day-2">查看当天安排 ↓</a></div><div><div class="countdown" role="timer" aria-label="距离下一行程事件的时间"><div class="count-unit"><strong id="days">--</strong><span>天</span></div><span class="count-sep">:</span><div class="count-unit"><strong id="hours">--</strong><span>时</span></div><span class="count-sep">:</span><div class="count-unit"><strong id="minutes">--</strong><span>分</span></div><span class="count-sep">:</span><div class="count-unit"><strong id="seconds">--</strong><span>秒</span></div></div><p class="now-clock" id="now-clock">倒计时以事件时区计算</p></div></section>'''
sections=[('overview','01','行程总览','每天一色 · 每晚一站','<div class="panel">'+overview()+'</div>'),('bookings','02','已确认预订','2人同行 · 当地时间',bookings()),('itinerary','03','逐日行程','航班为锚 · 留足缓冲','<div class="date-nav">'+''.join(f'<a href="#day-{d["n"]}" style="border-bottom-color:{d["color"]}">10/{d["n"]}</a>' for d in DAYS)+'</div><div class="days">'+''.join(timeline(d) for d in DAYS)+'</div>'),('todos','04','待办清单','完成后统一更新','<div class="panel"><ol class="todo-list">'+''.join('<li>'+x+'</li>' for x in TODOS)+'</ol></div>'),('tips','05','实用贴士','出发前与路上随时查','<div class="tips-grid">'+''.join(f'<article class="tip"><h3>{E(a)}</h3><p>{b}</p></article>' for a,b in TIPS)+'</div>')]
content=''.join(f'<section class="section" id="{id}"><div class="section-title"><span class="index">{num}</span><h2>{title}</h2><span class="aside">{aside}</span></div>{body}</section>' for id,num,title,aside,body in sections)
favicon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#276761"/><path d="M9 46L25 17L38 39L46 27L57 46Z" fill="#fbf8ef"/><path d="M22 23L25 17L30 26Z" fill="#bb8e27"/></svg>'
from urllib.parse import quote
doc='<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#276761"><meta name="description" content="2026年10月2日至11日，2人挪威与英国旅行手册：已订航班邮轮、每日路线、Google导航、离线阅读与时区倒计时。"><meta name="robots" content="noindex,nofollow"><title>挪威 & 英国 · 旅行手册 10.2–10.11</title><link rel="icon" href="data:image/svg+xml,'+quote(favicon)+'"><style>'+CSS+'</style></head><body><header><div><h1>挪威 <span style="color:var(--muted);font-weight:400">&</span> 英国</h1><div class="header-meta">TRAVEL NOTES · 2026.10.02—10.11 · 2人</div></div><div class="header-actions"><span class="status" id="connection-status">离线友好</span><button class="download" id="download" type="button">下载离线版 ↓</button></div></header><main class="shell">'+focus+'<noscript><p class="nojs">行程正文与地图可直接阅读；开启JavaScript后可使用倒计时和自动日夜配色。</p></noscript><nav class="quick-nav" aria-label="手册目录"><a href="#overview">总览地图</a><a href="#bookings">已确认预订</a><a href="#itinerary">逐日行程</a><a href="#todos">待办清单</a><a href="#tips">实用贴士</a></nav>'+content+'<footer class="footer"><span>上海 → 荷兰短停 → 罗佛敦 → 特罗姆瑟 → 伦敦 → 上海</span><span>时间均带当地时区 · 点地点打开Google导航</span></footer></main><script id="trip-data" type="application/json">'+json.dumps(DATA,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script><script>'+JS+'</script></body></html>'
(ROOT/'public/index.html').write_text(doc,encoding='utf-8')
print(f'Built {len(DAYS)} days, {sum(len(d["rows"]) for d in DAYS)} timeline rows, {len(EVENTS)} timezone-qualified events, {len(PLACES)} clickable places. HTML {len(doc.encode()):,} bytes.')
