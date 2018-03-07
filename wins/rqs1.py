import requests, lxml, time, csv
from bs4 import BeautifulSoup

''' url1 = "http://bizsearch.winshangdata.com/pinpai/y0-t0-m0-q0-p0-d0-z0-n0-c0-l0-x0-b0-pn1.html"

rp1 = requests.get(url1)
bs1 = BeautifulSoup(rp1.text, 'lxml')
rs1 = bs1.find('li',attrs={'data-id':True, 'data-name':True})
li1 = rs1.find('div', class_='l-logo fl')
li1.a.get('href')
li1.img.get('src')
ul1 = rs1.find('ul', class_='l-inf-list clearfix')
s1 = ul1.find_all('span', class_='colora')
for sx in s1:
    print(sx.string, sx.next_sibling.string) '''

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

    #如果采集页返回数据集为空， 不再继续
    if len(rsx) == 0:
        break

    for lx in rsx:
        # print(lx.get('data-id'), lx.get('data-name'), lx.get('data-leixing'), )
        dx = lx.find('div', class_='l-logo fl')
        # print(dx.a.get('href').split('#')[0])
        # print(dx.img.get('src').split('?')[0])
        sx = lx.find_all('span', class_='colora')
        cyear = ''
        pstat = ''
        rsize = ''

        for sxn in sx:
            # print(sxn.string, sxn.next_sibling.string)
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
    # 采集满10页后终止
    if px > 10:
        break
    time.sleep(0.05)

    # if px > 10:
    #     findflag = False

#print(prows)

csvfx = 'pinpai.csv'
headx = ['data-id', 'data-name', 'data-leixing', 'data-url', 'data-logo', 'cyear', 'pstat', 'rsize']

with open(csvfx, 'w', newline='') as f:
    wrtx = csv.DictWriter(f, headx)
    wrtx.writeheader()
    for row in prows:
        wrtx.writerow(row)

