import requests, lxml, time, csv
from bs4 import BeautifulSoup


prows = []
findflag = True
px = 1
urlbase = "http://bizsearch.winshangdata.com/pinpai/y0-t0-m0-q0-p0-d0-z0-n0-c0-l0-x0-b0-pn"
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

        dictx = {'data-id': lx.get('data-id'),
                'data-name': lx.get('data-name'),
                'data-leixing': lx.get('data-leixing'),
                'data-url': dx.a.get('href').split('#')[0],
                'data-logo': dx.img.get('src').split('?')[0],
                'cyear': cyear,
                'pstat': pstat,
                'rsize': rsize,
                }
        
        prows.append(dictx)

    px += 1

    if px > 10:
        break

    time.sleep(0.05)



# csvfx = 'pinpai.csv'
# headx = ['data-id', 'data-name', 'data-leixing', 'data-url', 'data-logo', 'cyear', 'pstat', 'rsize']

# with open(csvfx, 'w', newline='') as f:
#     wrtx = csv.DictWriter(f, headx)
#     wrtx.writeheader()
#     for row in prows:
#         wrtx.writerow(row) '''


for prx in prows:
    urly = prx['data-url']
    rpy = requests.get(urly)
    bsy = BeautifulSoup(rpy.text, 'lxml') 
    data-cname = bsy.find('p', class_='colora d-des-txt').get_text()
    data-labels = bsy.find('span', class_='brand-new').get_text()
    spys = bsy.find_all('span', class_='colora mr60')

    for spy in spys:
        if spy.string == '开店方式':
            data-kdmethod = spy.next_sibling.string
        elif spy.string == '合作期限':
            data-cptime = spy.next_sibling.string
        elif spy.string == '已开数量':
            data-oqty = spy.next_sibling.string
        elif spy.string == '今年计划':
            data-pqty = spy.next_sibling.string
        else:
            pass

    h3s = bsy.find_all('h3', class_='d-sub-tit')
    for hx in h3s:
        if hx.get_text() == '品牌介绍':
            #print(hx.find_next('p').get_text())
            data-intro = hx.find_next('p').get_text()

    prx['data-cname'] = data-cname
    prx['data-labels'] = data-labels
    prx['data-kdmethod'] = data-kdmethod
    prx['data-cptime'] = data-cptime
    prx['data-oqty'] = data-oqty
    prx['data-pqty'] = data-pqty
    prx['data-intro'] = data-intro


print(prows)
