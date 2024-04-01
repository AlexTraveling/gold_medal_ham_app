import streamlit as sl
import sys
import pandas as pd
import time
from st_aggrid import AgGrid

from to_database import get_user_identity, get_table, get_if_ham_exist, add_ham, select_from_table
from home_page import set_background


def get_information_section():

   index = sys.argv.index("information")
   information = sys.argv[index + 1]

   return information


def title_section(username):

   user_identity = get_user_identity(username)

   chinese_identity = {'farmer': '养殖户',
                       'supervisor': '监管员'}
   user_chinese_identity = chinese_identity[user_identity]

   sl.title(f'早上好，{user_chinese_identity} {username}')


def show_table_section(username):

   sl.subheader('已出炉的火腿')

   after_select = select_from_table('ham', f"ham_username = '{str(username)}' AND ham_state = 'made'")

   ham_id_list = [x[0] for x in after_select]
   ham_time_list = [x[2] for x in after_select]
   ham_place_list = [x[3] for x in after_select]
   ham_state_list = [x[4] for x in after_select]

   data = {
    '编号': ham_id_list,
    '时间': ham_time_list,
    '产地': ham_place_list,
    '状态': ham_state_list
   }

   df = pd.DataFrame(data)
   sl.table(df)
   # AgGrid(df)


def sidebar_section(username):

   sl.sidebar.header('新出炉的火腿')

   default_ham_id = 1000
   default_place = 'Xuanwei City'

   ham_id = sl.sidebar.text_input('编号', default_ham_id)
   ham_date = sl.sidebar.date_input('日期')
   ham_time = sl.sidebar.time_input('时间')
   ham_place = sl.sidebar.text_input('产地', default_place)

   if sl.sidebar.button('录入'):

      if get_if_ham_exist(ham_id, 'made'):
         sl.sidebar.warning('该火腿编号已存在')
      
      else:
         if add_ham(ham_id, username, f'{ham_date}-{ham_time}', ham_place, 'made') == 'success':
            sl.sidebar.success(f'火腿{ham_id}录入成功')
            time.sleep(1)
            sl.experimental_rerun()


if __name__ == '__main__':

   page_name = 'Farmer · Gold medal ham'
   page_icon = '🍗'
   sl.set_page_config(page_name, page_icon)

   set_background('image/farmer_background.png')

   username = get_information_section()

   title_section(username)
   sl.markdown('---')
   show_table_section(username)
   
   sidebar_section(username)

