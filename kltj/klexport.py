import os, sys, time
import xlwings as xw

ltime = 5 # 倒计时
print('\n')
print('此程序用于提取、合并客流原始数据。')
print('!!! 操作前请务必关闭所有已打开的excel文件 !!!')
print('请将此程序与客流数据的原始数据文件夹放在同一目录下后再运行 \n')
print('若要中断程序运行， 请在倒计时结束前按 ctrl + c \n')
print('操作将于 %d 秒后进行...... \n' % ltime )
while ltime: 
    print('    ', ltime)
    ltime += -1
    time.sleep(1)

print('\n')

#清除当前目录下excel文件
print('1#  删除当前目录下的excel文件')
for fx in os.listdir():
    #print(os.path.splitext(fx)[1])
    if os.path.splitext(fx)[1] == '.xlsx':
        os.remove(fx)

print('2#  提取原始数据 \n')
dirx = '原始数据'
fnamex = '客流统计信息表'
appx = xw.App(visible=False, add_book=False, )
appx.display_alerts = False
appx.screen_updating = False

wbo = appx.books.add()
shtz = wbo.sheets['Sheet1']
shtz.clear()
shtz.name = '客流数据总表'
shtz.range('A1').value = ['序号', '位置', '统计时间', '客流数']
sx = 2
klsz = 0
shtlocation = shtz.name
for fx in os.listdir(dirx):
    #读取客流数据
    pwdx = os.path.join(dirx, fx)
    wbx = appx.books.open(pwdx)
    shtx = wbx.sheets[0]
    klx = []
    klsx = 0
    for x in range(11, 26):
        tx = str(shtx.range('B' + str(x)).value)[4:-1].strip()
        cx = str(shtx.range('D' + str(x)).value)[4:-1].strip()
        kx = [tx, cx]
        klsx += int(cx)
        klx.append(kx)
    wbx.close()
    #写入客流明细数据
    namex = os.path.split(fx)[1][:-19]
    print('    提取数据：  %s' % namex )
    shto = wbo.sheets.add(namex, after=shtlocation)
    shtlocation = namex
    shto.range('A1').value = '时间'
    shto.range('A1').column_width = 20
    shto.range('A1').row_height = 20
    shto.range('B1').value = '客流数'
    shto.range('B1').column_width = 10
    shto.range('A2').value = klx
    #shto.range('A1').autofit()
    #写入客流汇总数据
    shtz.range('A' + str(sx)).value = namex[:2]
    shtz.range('B' + str(sx)).value = namex[3:]
    shtz.range('C' + str(sx)).value = str(shto.range('A2').value) + '-22:00'
    shtz.range('D' + str(sx)).value = klsx
    klsz += klsx
    sx += 1

#shtz.range('A13:C13').value = '客流数合计'
shtz.range('D13').value = klsz
shtz.range('D13').color = (255, 255, 0)
shtz.range('A1').column_width = 6
shtz.range('B1').column_width = 20
shtz.range('C1').column_width = 30
shtz.range('D1').column_width = 10
shtz.range('A1:A13').row_height = 20
shtz.activate()
fnamey = shtz.range('C2').value[:10].strip().replace('-', '')
wbo.save('tmp.xlsx')
wbo.close()
appx.kill()


if os.path.isfile('tmp.xlsx'):
    os.rename('tmp.xlsx', fnamex + fnamey + '.xlsx')

print('\n3#  客流数据整理完成， 程序将于3秒后退出')
time.sleep(3)
sys.exit()
