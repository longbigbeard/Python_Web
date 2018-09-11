import os
import os.path

# UI 文件所在的路径
dir = './'

# 列出目录下的所有UI文件
def listUiFile():
    list = []
    files = os.listdir(dir)  # 列出当前目录下所有的文件
    for filename in files:
        #print(dir + os.sep +f)
        # print(filename)
        if os.path.splitext(filename)[1] == '.ui':  # 判断是否为UI文件
            list.append(filename)
    return list



'''
splitext()  作用 ：分离文件名与扩展名；默认返回(fname,fextension)元组，可做分片操作
例子如下：
    import os
    path_01='D:/User/wgy/workplace/data/notMNIST_large.tar.gar'
    path_02='D:/User/wgy/workplace/data/notMNIST_large'
    root_01=os.path.splitext(path_01)
    root_02=os.path.splitext(path_02)
    print(root_01)
    print(root_01[0])
    print(root_01[1])
    print(root_02)
'''


# 把UI文件改成拓展名为“.py”的文件
def transPyFile(filename):
    return os.path.splitext(filename)[0] +'.py'


# 调用系统命令，将UI文件转换为Python文件
def runmain():
    list = listUiFile()
    for uifile in list :
        pyfile = transPyFile(uifile)
        cmd = 'pyuic5 -o {pyfile} {uifile}'.format(pyfile=pyfile,uifile=uifile)
        # print(cmd)
        os.system(cmd)


if __name__=='__main__':
    runmain()