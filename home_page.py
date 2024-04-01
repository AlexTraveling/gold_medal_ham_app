import streamlit as sl
import base64
import subprocess

from to_database import get_if_user_exist, get_user_identity


def set_background(main_bg):
   main_bg_ext = "png"
   sl.markdown(
      f"""
      <style>
      .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover
      }}
      </style>
      """,
      unsafe_allow_html=True
   )


def title_section():
   
   sl.markdown("""
               <center>
               <h1 class='title'>金牌宣威火腿</h1>
               <p class='describe'>优中选优的宣威火腿，更好的品质，更好的火腿</p>
               </center>

               <style>
               .title {
                  color: white;
               }
               .describe {
                  color: white;
               }
               </style>
               """, unsafe_allow_html=True)


def login_section():

   with sl.form('login'):
      username = sl.text_input('用户名')
      password = sl.text_input('密码', type='password')
      
      sl.markdown('''
      <style>       
      .st-emotion-cache-7ym5gk.ef3psqc7 {
         # width: 100%;
      }         
      .st-emotion-cache-ue6h4q.e1y5xkzn3 {
         color: white;
      }
      <style>
      ''', unsafe_allow_html=True)

      if sl.form_submit_button('登录'):

         if_user_exist, real_password = get_if_user_exist(username)
         if if_user_exist:
            if password == real_password:
               sl.success('登录成功')
               return username
            else:
               sl.warning('密码错误')
         else:
            sl.warning('不存在该用户')

   return None


def goto_next_page_section(username):

   user_identity = get_user_identity(username)

   # sl.info('goto')
   # sl.info(user_identity)

   subprocess.Popen(["streamlit", 
                     "run", 
                     f"{user_identity}_page.py", 
                     "information", 
                     f"{username}"])


def introduction_section():

   sl.markdown("""
               <center>
               <h1 class='title'>为什么选择我们</h1>
               <p class='describe'>简单朴素的三个原因</p>
               </center>

               <style>
               .title {
                  color: white;
               }
               .describe {
                  color: white;
               }
               </style>
               """, unsafe_allow_html=True)
   

if __name__ == '__main__':
   
   page_name = 'Home · Gold medal ham'
   page_icon = '🍗'
   sl.set_page_config(page_name, page_icon)

   set_background('./image/ham_2_mask.jpg')
    
   title_section()
   username = login_section()
   if username != None:
      goto_next_page_section(username)
   introduction_section()
