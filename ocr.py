from paddleocr import PaddleOCR
import os
import re
import guider.constant as constant

class Ocr():
    def __init__(self, path):
        self.img_path = path

    def ocr(self):
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
        datas = []
        for root, dirs, files in os.walk(self.img_path ):
            for file in files:
                if not file.endswith('.jpeg'):
                    continue

                print(self.img_path + file)
                result = ocr.ocr(os.path.join(self.img_path, file), cls=True)

                for line in result:
                    datas += self.excute_line(line)
        self.save(','.join(datas), os.path.join( self.img_path, constant.result_words_file_name))

    def save(self, datas, path):
        file = open(path, 'w+')
        file.write(datas)
        file.close()

    def excute_line(slef, line):
        result = []
        for items in line:
            for item in items:
                if isinstance(item, tuple):
                    rtn = re.findall(r'[（](.*?)[）]', str(item))
                    if slef.is_filter(rtn):
                        continue

                    result += rtn

        return result
    def is_filter(self, input):
        if len(input) <=0 :
            return True

        if len(input[0]) <= 1:
            print('--------{}--------'.format(input[0]))
            return True

        return False

if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), constant.result_words_neword_folder_name)
    print(path)
    Ocr(path).ocr()

