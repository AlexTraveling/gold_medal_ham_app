import streamlit as sl
import sys
import pandas as pd

from to_database import get_user_identity, select_from_table
from home_page import set_background


def get_information_section():

   index = sys.argv.index("information")
   information = sys.argv[index + 1]

   return information


def title_section(username):

   user_identity = get_user_identity(username)

   chinese_identity = {'farmer': '养殖户',
                       'supervisor': '监管员',
                       'salesperson': '售货员',
                       'customer': '客户'}
   user_chinese_identity = chinese_identity[user_identity]

   sl.title(f'晚上好，{user_chinese_identity} {username}')


def trace_section():
   
   sl.subheader('产品溯源')
   default_id = '1001'
   # sl.text('您可扫描火腿包装上的二维码，查看火腿品质及生产来源')

   id = sl.text_input('您可扫描火腿包装上的二维码，查看火腿品质及生产来源', default_id)

   sl.subheader('品质评级')
   quality = select_from_table('evaluate', f"id = '{id}'")[0][1]
   # sl.info(quality)
   column = sl.columns([2, 6, 2])
   with column[1]:
      if quality == 'gold_medal':
         sl.image('image/quality_gold_medal.png')
      elif quality == 'regular':
         sl.image('image/quality_regular.png')

   sl.subheader('生产来源')
   l = select_from_table('ham', f"ham_id = '{id}'")
   
   ham_id_list = [x[0] for x in l]
   user_list = [x[1] for x in l]
   ham_time_list = [x[2] for x in l]
   ham_place_list = [x[3] for x in l]
   ham_state_list = [x[4] for x in l]

   data = {
    '编号': ham_id_list,
    '角色': user_list,
    '时间': ham_time_list,
    '城市': ham_place_list,
    '状态': ham_state_list
   }
   df = pd.DataFrame(data)
   sl.table(df)


if __name__ == '__main__':

   page_name = 'Customer · Gold medal ham'
   page_icon = '🍗'
   sl.set_page_config(page_name, page_icon)

   set_background('./image/customer_background_2.png')

   username = get_information_section()

   title_section(username)
   sl.markdown('---')
   trace_section()