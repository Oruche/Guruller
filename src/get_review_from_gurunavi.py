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
        self.responce_item_keys = ['vote_id','photo_genre_id','photo_genre_name',
                                   'photo_scene_id','photo_scene_name','nickname',
                                   'shop_id','shop_name','shop_url','prefname',
                                   'menu_id','menu_name','menu_finish_flag','areaname_l',
                                   'areaname_m','areaname_s','image_url','comment',
                                   'total_score','category','distance','latitude',
                                   'longitude','umaso_count','update_date','messages']


    def create_request_url(self, *request_parameters):
        self.__init__()
        self.request_parameters = request_parameters
        self.query.append(('keyid',self.keyid))
        self.query.append(('offset_page',1))
        for request_parameter in request_parameters:
            query_element = request_parameter.split('=')
            self.query.append((query_element[0], query_element[1]))
        self.request_url += '?{0}'.format(urllib.parse.urlencode(self.query))


    def create_request_url_offset(self, offset):
        self.request_url = re.sub('offset_page=[0-9]+', 'offset_page=' + str(offset), self.request_url)


    def send_request(self):
        try:
            result = json.loads(urllib.request.urlopen(self.request_url).read().decode('utf-8'))
        except ValueError:
            print('APIアクセスに失敗しました')
            return
        try:
            self.data = result['response']
        except:
            if 'error' in result['gnavi']:
                print(result['gnavi']['error'])
            else:
                print('error')
            return
        if self.check_result():
            print('データの取得に成功しました')
            print('total hit count : ', self.data['total_hit_count'])
            self.create_review_dataframe()
            if int(self.data['total_hit_count']) > int(self.data['hit_per_page']):
                for offset in range(int(int(self.data['total_hit_count']) / int(self.data['hit_per_page'])) + 1):
                    if offset == 0:continue
                    self.create_request_url_offset(offset+1)
                    self.send_request_offset()


    def send_request_offset(self):
        try:
            result = urllib.request.urlopen(self.request_url).read()
        except ValueError:
            print('APIアクセスに失敗しました')
            return
        self.data = json.loads(result.decode('utf-8'))['response']
        if self.check_result():
            self.create_review_dataframe_offset()


    def create_review_dataframe(self):
        temp_dict = self.create_temp_dict_modify()
        self.review_df = pd.DataFrame(temp_dict)


    def create_review_dataframe_offset(self):
        temp_dict = self.create_temp_dict_modify()
        temp_df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in temp_dict.items()]))
        self.review_df = pd.concat([self.review_df, temp_df])


    def create_temp_dict_modify(self):
        temp_dict = {}
        for rest_idx in range(self.data['hit_per_page']):
            filled_key = []
            for review_key in self.data[str(rest_idx)]['photo']:
                if review_key in temp_dict:
                    temp_dict[review_key].append(self.data[str(rest_idx)]['photo'][review_key])
                    filled_key.append(review_key)
                else:
                    temp_dict[review_key] = [self.data[str(rest_idx)]['photo'][review_key]]
                    filled_key.append(review_key)
            diff_item = self.compare_list(self.responce_item_keys, filled_key)
            if len(diff_item) != 0:
                for nan_item in diff_item:
                    if nan_item in temp_dict:
                        temp_dict[nan_item].append('')
                    else:
                        temp_dict[nan_item] = ['']


        return temp_dict


    def write_to_csv(self, file_name='review.csv'):
        self.review_df.to_csv(str(file_name), encoding="utf-8")


    def print_json(self, json_data):
        print(json.dumps(json_data, ensure_ascii=False, indent=4, separators=(',', ': ')))


    def compare_list(self, list_a, list_b):
        return list(set(list_a).symmetric_difference(set(list_b)))



