import streamlit as sl
import sys

from to_database import get_user_identity


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

   sl.title(f'中午好，{user_chinese_identity} {username}')


def sidebar_section():
   
   sl.sidebar.header('新的进货')

   sl.sidebar.markdown('---')

   sl.sidebar.header('新的售出')


if __name__ == '__main__':

   page_name = 'Salesperson · Gold medal ham'
   page_icon = '🍗'
   sl.set_page_config(page_name, page_icon)

   username = get_information_section()

   title_section(username)
   sl.markdown('---')

   sidebar_section()
   
   