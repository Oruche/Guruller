import urllib.parse
import urllib.request
import json
import pandas as pd
import re
from get_info_from_gurunavi import info_collecter_from_gurunavi


class review_collecter_from_gurunavi(info_collecter_from_gurunavi):

    def __init__(self, format='json'):
        info_collecter_from_gurunavi.__init__(self)
        self.request_url = 'https://api.gnavi.co.jp/PhotoSearchAPI/20150630/'
        self.review_df = pd.DataFrame()
        self.query = [('format', format),('hit_per_page', 10)]


    def send_request(self):
        try:
            result = urllib.request.urlopen(self.request_url).read()
        except ValueError:
            print('APIアクセスに失敗しました')
            return
        self.data = json.loads(result.decode('utf-8'))['response']
        #print(json.dumps(self.data, ensure_ascii=False, indent=4, separators=(',', ': ')))
        if self.check_result():
            print('データの取得に成功しました')
            print('total hit count : ', self.data['total_hit_count'])
            self.create_review_dataframe()
            if int(self.data['total_hit_count']) > int(self.data['hit_per_page']):
                for offset in range(int(int(self.data['total_hit_count']) / int(self.data['hit_per_page'])) + 1):
                    if offset == 0:continue
                    self.create_request_url_offset(offset+1)
                    self.send_request_offset()


    def create_request_url_offset(self, offset):
        self.request_url = re.sub('offset=[0-9]+', 'offset_page=' + str(offset), self.request_url)


    def send_request_offset(self):
        try:
            result = urllib.request.urlopen(self.request_url).read()
        except ValueError:
            print('APIアクセスに失敗しました')
            return
        self.data = json.loads(result.decode('utf-8'))['response']
        #print(json.dumps(self.data, ensure_ascii=False, indent=4, separators=(',', ': ')))
        if self.check_result():
            self.create_review_dataframe_offset()


    def create_review_dataframe(self):
        temp_dict = self.create_temp_dict()
        self.review_df = pd.DataFrame(temp_dict)


    def create_review_dataframe_offset(self):
        temp_dict = self.create_temp_dict()
        temp_df = pd.DataFrame(temp_dict)
        self.review_df = pd.concat([self.review_df, temp_df])


    def create_temp_dict(self):
        headers = self.data['0']['photo'].keys()
        temp_dict = {}
        for rest_idx in range(self.data['hit_per_page']):
            values = list(self.data[str(rest_idx)]['photo'].values())
            for header_idx, header in enumerate(headers):
                if rest_idx == 0:
                    temp_dict[header] = [values[header_idx]]
                else:
                    temp_dict[header].append(values[header_idx])
        return temp_dict


    def write_to_csv(self, file_name='review.csv'):
        self.review_df.to_csv(str(file_name), encoding="cp932")




