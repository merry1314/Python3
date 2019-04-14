import itchat as ic
from wordcloud import WordCloud
import re, os, random, math
from matplotlib import pyplot as plt
import jieba
from scipy.misc import imread
from PIL import Image

'''处理图形中文显示问题'''
plt.rcParams['font.sans-serif'] = ['simhei']
plt.rcParams['axes.unicode_minus'] = False

'''本次要做的是拼接好友头像，统计性别、省份、城市，生成个性签名的词云，保存好友信息'''
ic.login()
friends = ic.get_friends(update=True)


# 获取好友头像
def get_images():
    # count 下标 f 文件
    for count, f in enumerate(friends):
        # 根据userName获取头像
        images = ic.get_head_img(userName=f['UserName'])
        imgFile = open('images/' + str(count) + '.png', 'wb')
        imgFile.write(images)
        imgFile.close()


# 拼接头像
def create_png():
    x = 0
    y = 0
    # 遍历文件夹
    pngs = os.listdir('images')
    random.shuffle(pngs)
    # 创建图像来填充头像
    newImg = Image.new('RGBA', (1280, 1280))
    # 计算头像的大小
    width = int(math.sqrt(1280 * 1280 / len(pngs)))
    # 每行图片数
    numLine = int(1280 / width)

    for i in pngs:
        png = Image.open('images/' + i)
        # 缩小图片
        png = png.resize((width, width), Image.ANTIALIAS)
        # 拼接图片
        newImg.paste(png, (x * width, y * width))
        x += 1
        if x >= numLine:
            x = 0
            y += 1
    newImg.save("files/微信好友头像拼接图.png")


# 性别统计图
def sex_count():
    sex = dict()
    # 性别分类
    male = '男性'
    female = '女性'
    other = '未知'
    for c in friends:
        f = c['Sex']
        if f == 1:
            sex[male] = sex.get(male, 0) + 1
        elif f == 2:
            sex[female] = sex.get(female, 0) + 1
        else:
            sex[other] = sex.get(other, 0) + 1

    # 微信好友总数
    total_count = len(friends)

    # 计算性别占比
    percentage = [float(sex[male]) / total_count * 100,
                  float(sex[female]) / total_count * 100,
                  float(sex[other]) / total_count * 100]

    print(
        '男性：% .2f%% ' % (percentage[0]) + '\n' +
        '女性：% .2f%% ' % (percentage[1]) + '\n' +
        '未知： % .2f%% ' % (percentage[2])
    )

    # 使用柱状图表示
    for key in sex.keys():
        plt.bar(key, sex[key])

    plt.xlabel('性别')
    plt.ylabel('百分比')
    plt.title('微信好友性别统计分布图')
    plt.savefig('files/微信好友性别统计图.png')
    plt.close()


# 获取个性签名文本
def get_signature(friends):
    with open('files/微信好友个性签名.txt', 'a', encoding='utf-8') as f:
        for v in friends:
            signature = v['Signature'].strip().replace('emoji', '') \
                .replace('span', '').replace('class', '')

            # 正则 取出特殊符号
            reg = re.compile('1f\d+\w*|[<>/=]')
            signature = reg.sub('', signature)
            f.write(signature + '\n')


# 制作词云图
def create_word_png(filename):
    # 读取文本内容
    text = open(filename, encoding='utf-8').read()
    # jieba分词
    wordlist = jieba.cut(text, cut_all=True)
    word_space_split = ' '.join(wordlist)
    # 词云背景
    bg = imread('files/aa.jpg')
    wc = WordCloud(
        scale=10,
        background_color="black",
        max_words=2000,
        font_path='C:/Windows/Fonts//STXINGKA.ttf',
        mask=bg,
        max_font_size=30,
        random_state=50)
    wc.generate(word_space_split)
    plt.axis('off')
    wc.to_file('files/微信好友个性签名词云图.png')


# 指定变量获取数据
def get_var(var):
    variable = []
    for i in friends:
        value = i[var]
        variable.append(value)
    return variable


# 统计省份并画图
def province_count():
    Province = get_var('Province')
    # 去重
    pros = set(Province)
    pros_array = []
    for item in pros:
        # 统计
        pros_array.append((item, Province.count(item)))

    def by_num(p):
        return p[1]

    # 排序 根据统计的个数
    pros_sorted = sorted(pros_array, key=by_num, reverse=True)

    # print(pros_sorted)
    # 省份  统计个数
    p = []
    c = []
    count = 0
    for v in pros_sorted:
        p.append(v[0])
        if p is None:
            p = '未知'
        c.append(v[1])
        count = count + 1
        if count > 18:
            break
    plt.bar(p, c)
    plt.xlabel("省份")
    plt.ylabel("人数")
    plt.title("微信好友省份分布统计图")
    plt.savefig("files/微信好友省份分布统计图.png")
    plt.close()


# 微信好友城市分布
def city_count():
    City = get_var('City')
    # 去重
    pros = set(City)
    pros_array = []
    for item in pros:
        # 统计
        pros_array.append((item, City.count(item)))

    def by_num(p):
        return p[1]

    # 排序 根据统计的个数
    pros_sorted = sorted(pros_array, key=by_num, reverse=True)

    print(pros_sorted)
    # 省份  统计个数
    p = []
    c = []
    count = 0
    for v in pros_sorted:
        p.append(v[0])
        c.append(v[1])
        count = count + 1
        if count > 18:
            break
    plt.bar(p, c)
    plt.xlabel("城市")
    plt.ylabel("人数")
    plt.title("微信好友城市分布统计图")
    plt.savefig("files/微信好友全国城市分布统计图.png")
    plt.close()


# 将微信好友信息保存到csv
def save_info():
    from pandas import DataFrame
    UserName = get_var('UserName')
    Sex = get_var('Sex')
    Province = get_var('Province')
    City = get_var('City')
    Signature = get_var('Signature')
    NickName = get_var('NickName')
    RemarkName = get_var('RemarkName')
    HeadImgUrl = get_var('HeadImgUrl')

    data = {'用户昵称': NickName, '用户性别': Sex,
            '好友备注': RemarkName, '所在省份': Province,
            '所在城市': City, '个性签名': Signature,
            '用户账号': UserName, '头像地址': HeadImgUrl
            }
    frame = DataFrame(data)
    frame.to_csv('files/微信好友信息表.csv', index=True, encoding='utf_8_sig')


if __name__ == '__main__':
    get_images()
    create_png()
    sex_count()
    get_signature(friends)
    create_word_png('files/微信好友个性签名.txt')
    province_count()
    city_count()
    save_info()
