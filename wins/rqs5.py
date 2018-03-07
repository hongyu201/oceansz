import requests, lxml, time, csv, random, datetime, os
from bs4 import BeautifulSoup


#获取品牌主信息
prows = []
findflag = True
px = 1
urlbase = "http://bizsearch.winshangdata.com/pinpai/y0-t0-m0-q0-p0-d0-z0-n0-c0-l0-x0-b0-pn"
print('get primary info: ')
print('time begin :', datetime.datetime.now())
while findflag:
    urlx = urlbase + str(px) + ".html"
    print(urlx)
    rpx = requests.get(urlx)
    bsx = BeautifulSoup(rpx.text, 'lxml')
    rsx = bsx.find_all('li', attrs={'data-id':True, 'data-name':True})

    if len(rsx) == 0:
        findflag = False
        break

    for lx in rsx:
        dx = lx.find('div', class_='l-logo fl')
        sx = lx.find_all('span', class_='colora')
        
        for sxn in sx:
            if sxn.string == '拓展状态：':
                pstatx = sxn.next_sibling
            elif sxn.string == '创立时间：':
                cyearx = sxn.next_sibling
            elif sxn.string == '面积要求：':
                rsizex = sxn.next_sibling
            else:
                pass
        
        if pstatx:
            data_pstat = pstatx.string.strip()
        if cyearx:
            data_cyear = cyearx.string.strip()
        if rsizex:
            data_rsize = rsizex.string.strip()

        dictx = {'data-id': lx.get('data-id').strip(),
                'data-name': lx.get('data-name').strip(),
                'data-leixing': lx.get('data-leixing').strip(),
                'data-url': dx.a.get('href').split('#')[0].strip(),
                'data-logo': dx.img.get('src').split('?')[0].strip(),
                'cyear': data_cyear,
                'pstat': data_pstat,
                'rsize': data_rsize,
                }
        
        prows.append(dictx)

    px += 1

    # if px > 205:
    #     break

    # time.sleep(random.random())

print('total qty: %s ' % len(prows))
print('time end :', datetime.datetime.now())
print('time begin :', datetime.datetime.now())
print('saving main info...', )
#写入文件保存主信息
csvm = 'pinpai_main.csv'
headx = ['data-id', 'data-name', 'data-leixing', 'data-url', 'data-logo', 'cyear', 'pstat', 'rsize']

if os.path.isfile(csvm):
    os.remove(csvm)
with open(csvm, 'w', newline='', encoding='gbk', errors='ignore') as f:
    wrtx = csv.DictWriter(f, headx)
    wrtx.writeheader()
    for row in prows:
        print('save : %s ' % row['data-name'])
        wrtx.writerow(row)    

print('time end :', datetime.datetime.now())
print('time begin :', datetime.datetime.now())

# 获取品牌详细信息
print('get pinpai detail info ...')
print('time begin :', datetime.datetime.now())

headx = ['data-utime','data-id', 'data-name', 'data-leixing', 'data-url', 'data-logo', 'cyear', 'pstat', 'rsize', 'data-cname', 'data-labels', 'data-kdmethod', 'data-cptime', 'data-oqty', 'data-pqty', 'data-intro']
csvd = 'pinpai_detail.csv'

if os.path.isfile(csvd):
    os.remove(csvd)

with open(csvd, 'a+', newline='', encoding='gbk', errors='ignore') as f:
    wrtx = csv.DictWriter(f, headx)
    wrtx.writeheader()

for prx in prows:
    urly = prx['data-url']
    print('get detai info: %s ' % prx['data-name'])
    rpy = requests.get(urly)
    bsy = BeautifulSoup(rpy.text, 'lxml') 
    #data_cname 公司名称
    cname = bsy.find('p', class_='colora d-des-txt')
    if cname:
        data_cname = cname.string
    else:
        cname = ''
    #data_utime 更新时间
    utime = bsy.find('span', class_='fr d-update-time')
    if utime:
        data_utime = utime.string.split('：')[1]
    else:
        data_utime = ''
    #data_utime = bsy.find('span', class_='fr d-update-time').string.split('：')[1]
    
    #data_labels 品牌标签
    labx = bsy.find('span', class_='brand-new')
    if labx:
        data_labels = labx.get_text()
    else:
        data_labels = ''

    #获取开店方式、合作期限、已开数量、今年计划
    kdmethod = None
    cptime = None
    oqty = None
    pqty = None
    spys = bsy.find_all('span', class_='colora mr60')

    for spy in spys:
        if spy.string == '开店方式':
            kdmethod = spy.next_sibling
        elif spy.string == '合作期限':
            cptime = spy.next_sibling
        elif spy.string == '已开数量':
            oqty = spy.next_sibling
        elif spy.string == '今年计划':
            pqty = spy.next_sibling
        else:
            pass

    if kdmethod:
        data_kdmethod = kdmethod.string
    else:
        data_kdmethod = ''
    
    if cptime:
        data_cptime = cptime.string
    else:
        data_cptime = ''

    if oqty:
        data_oqty = oqty.string
    else:
        data_oqty = ''
    
    if pqty:
        data_pqty = pqty.string
    else:
        data_pqty = ''
        

    h3s = bsy.find_all('h3', class_='d-sub-tit')

    for hx in h3s:
        if hx.get_text() == '品牌介绍':
            #print(hx.find_next('p').get_text())
            introx = hx.find_next('p')
            if introx:
                data_intro = introx.get_text()
            else:
                data_intro = ''

    prx['data-utime'] = data_utime.strip()
    prx['data-cname'] = data_cname.strip()
    prx['data-labels'] = data_labels.strip()
    prx['data-kdmethod'] = data_kdmethod.strip()
    prx['data-cptime'] = data_cptime.strip()
    prx['data-oqty'] = data_oqty.strip()
    prx['data-pqty'] = data_pqty.strip()
    prx['data-intro'] = data_intro.strip()

    with open(csvd, 'a+', newline='', encoding='gbk', errors='ignore') as f:
        wrtx = csv.DictWriter(f, headx)
        wrtx.writerow(prx)
    
    # time.sleep(random.random())

print('time end :', datetime.datetime.now())

#print(prows)
#导出品牌信息为csv文件
print('data detail get end')
time.sleep(3)
print('data export begin')
print('time begin :', datetime.datetime.now())

csvfx = 'pinpai' + str(random.random()) + '.csv'

with open(csvfx, 'w', newline='', encoding='gbk', errors='ignore') as f:
    wrtx = csv.DictWriter(f, headx)
    wrtx.writeheader()
    for row in prows:
        print('save : %s ' % row['data-name'])
        wrtx.writerow(row)

print('data export end')
print('time end :', datetime.datetime.now())
