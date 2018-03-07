import requests, lxml, time, csv, random, datetime, os, sys, shutil
from bs4 import BeautifulSoup


print('------')
findflag = False
#查找当前目录下品牌主信息更新时间，若小于一周，则不更新
csvm = 'pinpai_main.csv'
if os.path.exists(csvm):
    futime = datetime.datetime.fromtimestamp(os.stat(csvm).st_mtime)
    cptime = datetime.datetime.now() - datetime.timedelta(days=7)
    if futime > cptime:
        findflag = False
    else:
        findflag = True
else:
    findflag = True

if findflag:
    print('品牌主信息需要更新，下面开始品牌主信息更新')
else:
    print('品牌主信息不需要更新')


print('------')
#获取赢商网上的品牌主信息
prows = []
px = 1
urlbase = "http://bizsearch.winshangdata.com/pinpai/y0-t0-m0-q0-p0-d0-z0-n0-c0-l0-x0-b0-pn"
print('get primary info: ')
print('time begin :', datetime.datetime.now())
while findflag:
    urlx = urlbase + str(px) + ".html"
    print('get url: ', urlx)
    rpx = requests.get(urlx)
    bsx = BeautifulSoup(rpx.text, 'lxml')
    rsx = bsx.find_all('li', attrs={'data-id':True, 'data-name':True})

    #无结果，停止抓取
    if len(rsx) == 0:
        print('已到最后页，抓取无结果，停止抓取')
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

    # if px > 1:
    #     break

    #time.sleep(random.uniform(1,3))

print('time end :', datetime.datetime.now())
print('total qty: %s ' % len(prows))


#品牌主信息有更新，则重命名原文件，更新品牌主信息
if findflag :
    print('更新品牌主信息')
    headx = ['data-id', 'data-name', 'data-leixing', 'data-url', 'data-logo', 'cyear', 'pstat', 'rsize']
    if os.path.isfile(csvm):
        os.rename(csvm, csvm + datetime.datetime.now().strftime('%Y%m%d') + '.csv')
    with open(csvm, 'w', newline='', encoding='gbk', errors='ignore') as f:
        wrtx = csv.DictWriter(f, headx)
        wrtx.writeheader()
        for row in prows:
            #print('save : %s ' % row['data-name'])
            wrtx.writerow(row)
    print('品牌主信息更新完毕')
else:
    print('品牌主信息无更新')


# 获取赢商网上的品牌详细信息
print('------')
print('get pinpai detail info ...')
print('time begin :', datetime.datetime.now())
headx = ['data-utime','data-id', 'data-name', 'data-leixing', 'data-url', 'data-logo', 'cyear', 'pstat', 'rsize', 'data-cname', 'data-labels', 'data-kdmethod', 'data-cptime', 'data-oqty', 'data-pqty', 'data-intro']
csvd = 'pinpai_detail.csv'

if not os.path.isfile(csvd):
    with open(csvd, 'a+', newline='', encoding='gbk', errors='ignore') as f:
        wrtx = csv.DictWriter(f, headx)
        wrtx.writeheader()

if not findflag:
    if os.path.isfile(csvd):
        shutil.copyfile(csvd, 'pinpai_detail' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv')
        #os.rename(csvd, 'pinpai_detail' + datetime.datetime.now().strftime('%Y%m%d') + '.csv')

# 获取未更新的品牌列表
idsetm = set()
idsetd = set()
prows = list()
# 读取品牌主信息、ID
with open(csvm, 'r') as f:
    readerx = csv.DictReader(f)
    for row in readerx:
        prows.append(row)
        idsetm.add(row['data-id'])

# 读取品牌详细信息、ID
with open(csvd, 'r') as f:
    readerx = csv.DictReader(f)
    for row in readerx:
        idsetd.add(row['data-id'])

# 获取未更新的品牌ID
idsetf = idsetm - idsetd
print('待更新明细信息品牌数: ', len(idsetf))



for prx in prows:
    if prx['data-id'] in idsetf:
        urlx = prx['data-url']
        #print(urlx)
        rpx = requests.get(urlx)
        bsx = BeautifulSoup(rpx.text, 'lxml')

        #cname 公司名称
        cname = bsx.find('p', class_='colora d-des-txt')
        if cname:
            data_cname = cname.string
        else:
            data_cname = ''

        #data_utime 更新时间
        utime = bsx.find('span', class_='fr d-update-time')
        if utime:
            data_utime = utime.string.split('：')[1]
        else:
            data_utime = ''

        #data_labels 品牌标签
        labx = bsx.find('span', class_='brand-new')
        if labx:
            data_labels = labx.get_text()
        else:
            data_labels = ''
        
        #获取开店方式、合作期限、已开数量、今年计划
        kdmethod = None
        cptime = None
        oqty = None
        pqty = None
        spxs = bsx.find_all('span', class_='colora mr60')

        for spx in spxs:
            if spx.string == '开店方式':
                kdmethod = spx.next_sibling
            elif spx.string == '合作期限':
                cptime = spx.next_sibling
            elif spx.string == '已开数量':
                oqty = spx.next_sibling
            elif spx.string == '今年计划':
                pqty = spx.next_sibling
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
        
        h3s = bsx.find_all('h3', class_='d-sub-tit')

        for hx in h3s:
            if hx.get_text() == '品牌介绍':
                #print(hx.find_next('p').get_text())
                introx = hx.find_next('p')
                if introx:
                    data_intro = introx.get_text()
                else:
                    data_intro = ''

        setx = dict()
        setx['data-id'] = prx['data-id']
        setx['data-name'] = prx['data-name']
        setx['data-leixing'] = prx['data-leixing']
        setx['data-url'] = prx['data-url']
        setx['data-logo'] = prx['data-logo']
        setx['cyear'] = prx['cyear']
        setx['pstat'] = prx['pstat']
        setx['rsize'] = prx['rsize']
        setx['data-utime'] = data_utime.strip()
        setx['data-cname'] = data_cname.strip()
        setx['data-labels'] = data_labels.strip()
        setx['data-kdmethod'] = data_kdmethod.strip()
        setx['data-cptime'] = data_cptime.strip()
        setx['data-oqty'] = data_oqty.strip()
        setx['data-pqty'] = data_pqty.strip()
        setx['data-intro'] = data_intro.strip()

        with open(csvd, 'a+', newline='', encoding='gbk', errors='ignore') as f:
            wrtx = csv.DictWriter(f, headx)
            print('get detail info about：', setx['data-name'])
            wrtx.writerow(setx)

        time.sleep(random.uniform(1,2))

print('time end :', datetime.datetime.now())
print('data detail get end')
print('------')
