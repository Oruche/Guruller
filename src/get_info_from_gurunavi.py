import os
import urllib.request
import urllib.parse
import json
import pandas as pd
import re


class info_collecter_from_gurunavi:


    def __init__(self, format='json'):
        self.keyid = os.environ['GURUNAVI_API_KEY']
        self.request_url = 'https://api.gnavi.co.jp/RestSearchAPI/20150630/'
        self.offset = 0
        self.query = [('format', format)]
        self.rest_df = pd.DataFrame()


    def create_request_url(self, *request_parameters):
        self.__init__()
        self.request_parameters = request_parameters
        self.query.append(('keyid',self.keyid))
        self.query.append(('offset',self.offset))
        for request_parameter in request_parameters:
            query_element = request_parameter.split('=')
            self.query.append((query_element[0], query_element[1]))
        self.request_url += '?{0}'.format(urllib.parse.urlencode(self.query))


    def create_request_url_offset(self, offset):
        self.request_url = re.sub('offset=[0-9]+', 'offset=' + str(offset), self.request_url)


    def send_request(self):
        try:
            result = urllib.request.urlopen(self.request_url).read()
        except ValueError:
            print('APIアクセスに失敗しました')
            return
        self.data = json.loads(result.decode('utf-8'))
        if self.check_result():
            print('データの取得に成功しました')
            print('total hit count : ', self.data['total_hit_count'])
            self.create_rest_dataframe()
            if int(self.data['total_hit_count']) > len(self.data['rest']):
                for offset in range(int(int(self.data['total_hit_count']) / len(self.data['rest'])) + 1):
                    if offset == 0:continue
                    self.create_request_url_offset(offset * 10)
                    self.send_request_offset()


    def send_request_offset(self):
        try:
            result = urllib.request.urlopen(self.request_url).read()
        except ValueError:
            print('APIアクセスに失敗しました')
            return
        self.data = json.loads(result.decode('utf-8'))
        if self.check_result():
            self.create_rest_dataframe_offset()


    def check_result(self):
        if 'error' in self.data:
            if 'message' in self.data:
                print('{0}'.format(self.data['message']))
            else:
                print('データ取得に失敗しました')
            return 0
        else:
            return 1


    def create_rest_dataframe(self):
        temp_dict = self.create_temp_dict()
        self.rest_df = pd.DataFrame(temp_dict)


    def create_rest_dataframe_offset(self):
        temp_dict = self.create_temp_dict()
        temp_df = pd.DataFrame(temp_dict)
        self.rest_df = pd.concat([self.rest_df, temp_df])


    def create_temp_dict(self):
        headers = self.data['rest'][0].keys()
        temp_dict = {}
        for rest_idx, rest in enumerate(self.data['rest']):
            values = list(self.data['rest'][rest_idx].values())
            for header_idx, header in enumerate(headers):
                if rest_idx == 0:
                    temp_dict[header] = [values[header_idx]]
                else:
                    temp_dict[header].append(values[header_idx])
        return temp_dict


    def write_to_csv(self, file_name='rest.csv'):
        self.rest_df.to_csv(str(file_name), encoding="cp932")


