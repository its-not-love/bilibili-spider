from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
# 生成词云
def create_word_cloud():
    frequencies = {}
    for line in open("./record.txt"):
        arr = line.split(" ")
        frequencies[arr[0]] = float(arr[1])
    # 支持中文, SimHei.ttf可从以下地址下载：https://github.com/cystanford/word_cloud
    mask_png = plt.imread("./wife.jpg")
    my_wordcloud  = WordCloud(
        font_path="./SimHei.ttf",
        background_color="white",  # 背景颜色
        max_words=500,  # 词云显示的最大词数
        max_font_size=100,  # 字体最大值
        random_state=42,
        mask=mask_png,
        width=1000, height=600, margin=2,
    ).generate_from_frequencies(frequencies)
    image_colors = ImageColorGenerator(mask_png)
    plt.figure()
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.axis("off")
    plt.figure()
    plt.imshow(mask_png, cmap=plt.cm.gray)
    plt.axis("off")
    plt.show()
    my_wordcloud.to_file("wordcloud.png")

# 根据词频生成词云
if __name__ == "__main__":
    create_word_cloud()