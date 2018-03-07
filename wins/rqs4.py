import requests, lxml, time, csv, random
from bs4 import BeautifulSoup


#获取品牌主信息
prows = []
findflag = True
px = 1
urlbase = "http://bizsearch.winshangdata.com/pinpai/y0-t0-m0-q0-p0-d0-z0-n0-c0-l0-x0-b0-pn"
print('get primary info: ')
while findflag:
    urlx = urlbase + str(px) + ".html"
    print(urlx)
    rpx = requests.get(urlx)
    bsx = BeautifulSoup(rpx.text, 'lxml')
    rsx = bsx.find_all('li', attrs={'data-id':True, 'data-name':True})

    if len(rsx) == 0:
        break

    for lx in rsx:
        dx = lx.find('div', class_='l-logo fl')
        sx = lx.find_all('span', class_='colora')
        cyear = ''
        pstat = ''
        rsize = ''

        for sxn in sx:
            if sxn.string == '拓展状态：':
                pstat = sxn.next_sibling.string
            elif sxn.string == '创立时间：':
                cyear = sxn.next_sibling.string
            elif sxn.string == '面积要求：':
                rsize = sxn.next_sibling.string
            else:
                pass

        dictx = {'data-id': lx.get('data-id').strip(),
                'data-name': lx.get('data-name').strip(),
                'data-leixing': lx.get('data-leixing').strip(),
                'data-url': dx.a.get('href').split('#')[0].strip(),
                'data-logo': dx.img.get('src').split('?')[0].strip(),
                'cyear': cyear.strip(),
                'pstat': pstat.strip(),
                'rsize': rsize.strip(),
                }
        
        prows.append(dictx)

    px += 1

    # if px > 10:
    #     break

    time.sleep(random.random())
print('total qty: %s ' % len(prows))


# 获取品牌详细信息
for prx in prows:
    urly = prx['data-url']
    print('get detai info: %s ' % prx['data-name'])
    rpy = requests.get(urly)
    bsy = BeautifulSoup(rpy.text, 'lxml') 

    cname = bsy.find('p', class_='colora d-des-txt')
    if cname:
        data_cname = cname.string
    else:
        cname = ''

    data_utime = bsy.find('span', class_='fr d-update-time').string.split('：')[1]
    
    labx = bsy.find('span', class_='brand-new')
    if labx:
        data_labels = labx.get_text()
    else:
        data_labels = ''

    spys = bsy.find_all('span', class_='colora mr60')
    for spy in spys:
        if spy.string == '开店方式':
            data_kdmethod = spy.next_sibling.string
        elif spy.string == '合作期限':
            data_cptime = spy.next_sibling.string
        elif spy.string == '已开数量':
            data_oqty = spy.next_sibling.string
        elif spy.string == '今年计划':
            data_pqty = spy.next_sibling.string
        else:
            pass

    h3s = bsy.find_all('h3', class_='d-sub-tit')

    for hx in h3s:
        if hx.get_text() == '品牌介绍':
            #print(hx.find_next('p').get_text())
            data_intro = hx.find_next('p').get_text().strip()

    prx['data-utime'] = data_utime.strip()
    prx['data-cname'] = data_cname.strip()
    prx['data-labels'] = data_labels.strip()
    prx['data-kdmethod'] = data_kdmethod.strip()
    prx['data-cptime'] = data_cptime.strip()
    prx['data-oqty'] = data_oqty.strip()
    prx['data-pqty'] = data_pqty.strip()
    prx['data-intro'] = data_intro.strip()

    # time.sleep(random.random())

#print(prows)
#导出品牌信息为csv文件,文件编码为utf-8
print('data get end')
time.sleep(3)
print('data export begin')

csvfx = 'pinpai' + str(random.random()) + '.csv'
headx = ['data-utime','data-id', 'data-name', 'data-leixing', 'data-url', 'data-logo', 'cyear', 'pstat', 'rsize', 'data-cname', 'data-labels', 'data-kdmethod', 'data-cptime', 'data-oqty', 'data-pqty', 'data-intro']

with open(csvfx, 'w', newline='', encoding='utf-8') as f:
    wrtx = csv.DictWriter(f, headx)
    wrtx.writeheader()
    for row in prows:
        print('save : %s ' % row['data-name'])
        wrtx.writerow(row)

print('data export end')