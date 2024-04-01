import streamlit as sl
import sys
import time
import pandas as pd

from to_database import get_user_identity, add_ham, select_from_table, get_quality_from_id
from home_page import set_background


def get_information_section():

   index = sys.argv.index("information")
   information = sys.argv[index + 1]

   return information


def title_section(username):

   user_identity = get_user_identity(username)

   chinese_identity = {'farmer': '养殖户',
                       'supervisor': '监管员',
                       'salesperson': '售货员'}
   user_chinese_identity = chinese_identity[user_identity]

   sl.title(f'下午好，{user_chinese_identity} {username}')


def sidebar_section(username, storage_ham_id_list):
   
   sl.sidebar.header('新的进货')

   default_ham_id = 1003
   default_place = 'Beijing City'

   ham_id = sl.sidebar.text_input('火腿编号', default_ham_id)
   sl.sidebar.text('品质评级')
   quality = select_from_table('evaluate', f"id = '{ham_id}'")[0][1]
   if quality == 'bad':
      sl.sidebar.error('不合格火腿')
      sl.sidebar.text('请与监管机构沟通处理')
   else:
      if quality == 'gold_medal':
         sl.sidebar.success('金牌宣威火腿')
      elif quality == 'regular':
         sl.sidebar.info('普通火腿')
      ham_date = sl.sidebar.date_input('进货日期')
      ham_time = sl.sidebar.time_input('进货时间')
      ham_place = sl.sidebar.text_input('进货商铺', default_place)

      if sl.sidebar.button('进货'):

         if add_ham(ham_id, username, f'{ham_date}-{ham_time}', ham_place, 'storage') == 'success':
            sl.sidebar.success(f'火腿{ham_id}进货成功')
            time.sleep(1)
            sl.experimental_rerun()

   sl.sidebar.markdown('---')

   sl.sidebar.header('新的售出')

   default_place = 'Beijing City'
   quality_option = ['gold_medal', 'regular', 'bad']

   ham_id = sl.sidebar.selectbox('编号', storage_ham_id_list)
   sl.sidebar.text('品质评级')
   quality = select_from_table('evaluate', f"id = '{ham_id}'")[0][1]
   if quality == 'gold_medal':
      sl.sidebar.success('金牌宣威火腿')
   elif quality == 'regular':
      sl.sidebar.info('普通火腿')
   ham_date = sl.sidebar.date_input('售出日期')
   ham_time = sl.sidebar.time_input('售出时间')
   ham_place = sl.sidebar.text_input('售出商铺', default_place)

   if sl.sidebar.button('售出'):
      if add_ham(ham_id, username, f'{ham_date}-{ham_time}', ham_place, 'bought') == 'success':
         sl.sidebar.success(f'火腿{ham_id}售出成功')
         time.sleep(1)
         sl.experimental_rerun()


def show_table_section():

   # split
   all_select = select_from_table('ham', f"ham_state = 'storage'")
   bought_select = select_from_table('ham', f"ham_state = 'bought'")
   bought_ham_id_list = [x[0] for x in bought_select]
   
   # storage = all - bought
   storage_select = []
   for single in all_select:
      if single[0] not in bought_ham_id_list:
         storage_select.append(single)

   # before table
   sl.subheader('库存中的火腿')
   ham_id_list = [x[0] for x in storage_select]
   user_list = [x[1] for x in storage_select]
   ham_time_list = [x[2] for x in storage_select]
   ham_place_list = [x[3] for x in storage_select]
   ham_state_list = [x[4] for x in storage_select]

   quality_list = get_quality_from_id(ham_id_list)

   data = {
    '编号': ham_id_list,
    '评级': quality_list,
    '销售': user_list,
    '时间': ham_time_list,
    '地点': ham_place_list,
    '状态': ham_state_list
   }
   df = pd.DataFrame(data)
   sl.table(df)

   for_return = ham_id_list
   sl.markdown('---')

   # after table
   sl.subheader('已售出的火腿')
   ham_id_list = [x[0] for x in bought_select]
   user_list = [x[1] for x in bought_select]
   ham_time_list = [x[2] for x in bought_select]
   ham_place_list = [x[3] for x in bought_select]
   ham_state_list = [x[4] for x in bought_select]

   quality_list = get_quality_from_id(ham_id_list)

   data = {
    '编号': ham_id_list,
    '评级': quality_list,
    '销售': user_list,
    '时间': ham_time_list,
    '地点': ham_place_list,
    '状态': ham_state_list
   }
   df = pd.DataFrame(data)
   sl.table(df)

   return for_return


if __name__ == '__main__':

   page_name = 'Salesperson · Gold medal ham'
   page_icon = '🍗'
   sl.set_page_config(page_name, page_icon)

   set_background('image/salesperson_background_2.png')

   username = get_information_section()

   title_section(username)
   sl.markdown('---')
   storage_ham_id_list = show_table_section()

   sidebar_section(username, storage_ham_id_list)
   
   