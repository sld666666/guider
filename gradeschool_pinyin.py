
import os
import pypinyin
import datetime
import constant as constant
import random
import codecs


class PinyinGenerator():
    def __init__(self, path):
        self.base_path = path

    def generate_words(self):
        path = os.path.join(self.base_path, constant.result_words_neword_folder_name)
        path = os.path.join(path, constant.result_words_file_name)
        file = codecs.open(path, 'r', encoding='utf-8')
        rtn = file.read()
        file.close()
        words = rtn.split(',')
        words = [words[random.randint(0, len(words) - 1)] for _ in range(constant.generate_words_counts)]

        for word in words:
            if (len(word) <= 1):
                words.remove(word)

        return words


    def to_pinyin(self, words):
        rtn = []
        for word in words:
            tmp = (pypinyin.lazy_pinyin(word))
            tmp = ' '.join(tmp)
            rtn.append(tmp)
        return  rtn

    def render(self, pinyins):
        content = self.generate_contents(pinyins)
        self.save_to_html(content)

    def get_template_info(self, file_name):
        cur_path = os.path.join(self.base_path, file_name)
        print(cur_path)
        file = codecs.open(cur_path, 'r', encoding='utf-8')
        rtn = file.read()
        file.close()
        return rtn

    def save_to_html(self, content):
        index_template_info = self.get_template_info(constant.index_template_info)
        sytle_info = self.get_template_info(constant.style_template_info)
        content = index_template_info.format(datetime.datetime.today(), content, sytle_info)

        path = os.path.join(self.base_path,constant.result_html_path)
        file = codecs.open(path, 'w', encoding='utf-8')
        file.write(content)
        file.close()

    def generate_one_pinyin(self, pinyin):
        pinyin = '({})'.format(pinyin)
        counts = len(pinyin.split(' '))
        if len(pinyin) > constant.one_item_size * counts:
            return pinyin
        else:
            for index in range(constant.one_item_size*counts - len(pinyin)):
                pinyin += '&nbsp'
            return pinyin

    def generate_contents(self, pinyins):
        grid_template_info = self.get_template_info(constant.grid_template_info)

        content = ''
        count = 0
        one_p = ''
        grid = ''
        for item in pinyins:
            count += len(item.split(' '))
            one_p = one_p + self.generate_one_pinyin(item)
            for i in range(0, len(item.split(' '))):
                grid += grid_template_info
            grid += constant.empty_grid
            if count >= 10:
                content += constant.pinyin_template.format(one_p)
                content += grid
                count = 0
                one_p = ''
                grid = ''

        content += constant.pinyin_template.format(one_p)
        content += grid
        return content



if __name__ == '__main__':
    pinyinGenerator = PinyinGenerator(os.path.dirname(os.path.abspath(__file__)))
    words = pinyinGenerator.generate_words()
    print(words)
    rtn = pinyinGenerator.to_pinyin(words)
    print(rtn)
    pinyinGenerator.render(rtn)