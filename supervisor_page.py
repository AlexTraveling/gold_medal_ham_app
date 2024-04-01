import streamlit as sl
import sys
from st_aggrid import AgGrid
import pandas as pd
import time

from to_database import get_user_identity, select_from_table, add_ham, get_if_ham_exist, add_evaluate, get_quality_from_id
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

   sl.title(f'中午好，{user_chinese_identity} {username}')


def evaluate_sidebar_section(username, ham_id_list):

   sl.sidebar.header('开始评级')

   default_place = 'Kunming City'
   quality_option = ['gold_medal', 'regular', 'bad']

   ham_id = sl.sidebar.selectbox('编号', ham_id_list)
   quality = sl.sidebar.radio('品质', quality_option)
   ham_date = sl.sidebar.date_input('日期')
   ham_time = sl.sidebar.time_input('时间')
   ham_place = sl.sidebar.text_input('评级地点', default_place)

   if sl.sidebar.button('录入'):

      # to evaluate table
      if add_evaluate(ham_id, quality) == 'success':

         # to ham table
         if add_ham(ham_id, username, f'{ham_date}-{ham_time}', ham_place, 'evaluated') == 'success':
            sl.sidebar.success(f'火腿{ham_id}评级成功')
            time.sleep(1)
            sl.experimental_rerun()


def evaluate_show_table_section():

   # split
   all_select = select_from_table('ham', f"ham_state = 'made'")
   after_select = select_from_table('ham', f"ham_state = 'evaluated'")
   after_ham_id_list = [x[0] for x in after_select]
   
   # before = all - after
   before_select = []
   for single in all_select:
      if single[0] not in after_ham_id_list:
         before_select.append(single)

   # before table
   sl.subheader('待评级的火腿')
   ham_id_list = [x[0] for x in before_select]
   user_list = [x[1] for x in before_select]
   ham_time_list = [x[2] for x in before_select]
   ham_place_list = [x[3] for x in before_select]
   ham_state_list = [x[4] for x in before_select]

   data = {
    '编号': ham_id_list,
    '农户': user_list,
    '时间': ham_time_list,
    '产地': ham_place_list,
    '状态': ham_state_list
   }
   df = pd.DataFrame(data)
   sl.table(df)

   for_return = ham_id_list
   sl.markdown('---')

   # after table
   sl.subheader('已评级的火腿')
   ham_id_list = [x[0] for x in after_select]
   user_list = [x[1] for x in after_select]
   ham_time_list = [x[2] for x in after_select]
   ham_place_list = [x[3] for x in after_select]
   ham_state_list = [x[4] for x in after_select]

   quality_list = get_quality_from_id(ham_id_list)

   data = {
    '编号': ham_id_list,
    '评级': quality_list,
    '监管': user_list,
    '时间': ham_time_list,
    '地点': ham_place_list,
    '状态': ham_state_list
   }
   df = pd.DataFrame(data)
   sl.table(df)

   return for_return


def trace_side_section(username):

   sl.sidebar.header('开始追溯')




if __name__ == '__main__':

   page_name = 'Supervisor · Gold medal ham'
   page_icon = '🍗'
   sl.set_page_config(page_name, page_icon)

   # set_background('image/supervisor_background.jpg')

   username = get_information_section()

   title_section(username)
   sl.markdown('---')
   
   sl.sidebar.header('工作模式')
   options = ["评级模式", "追溯模式"]
   work_mode = sl.sidebar.radio('', options=options)
   sl.sidebar.markdown('---')

   if work_mode == '评级模式':
      ham_id_list = evaluate_show_table_section()
      evaluate_sidebar_section(username, ham_id_list)

   else:
      trace_side_section(username)

   