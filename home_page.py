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
      .st-emotion-cache-10trblm.e1nzilvr1 {
         color: white;
      }
      .st-emotion-cache-eqffof.e1nzilvr5 {
         color: white;
      }
      </style>
      """, unsafe_allow_html=True)

   column = sl.columns([4, 6])
   with column[0]:
      sl.markdown('<br>', unsafe_allow_html= True)
      sl.header('优质牧场')
      sl.markdown('<br>', unsafe_allow_html= True)
      sl.write('宣威特殊的地域气候环境条件，带来独属于金牌宣威火腿的风味。形似琵琶，脚细直伸，皮薄肉嫩；皮面呈棕色或淡黄色，切面肌肉呈玫瑰色，骨呈深红色，好似一股血气凝聚在内，油润有光泽，脂肪呈乳白色或微红色；食之酥脆，香而甜，油而不腻，咸淡适中。肉质弹性滋嫩，质感油而不腻，香味浓郁飘远。')
   with column[1]:
      sl.image('image/introduction_ham.png')
   
   column = sl.columns([4, 6])
   with column[0]:
      sl.markdown('<br>', unsafe_allow_html= True)
      sl.header('先进工艺')
      sl.markdown('<br>', unsafe_allow_html= True)
      sl.write('金牌宣威火腿腌制时只用食用盐，不加任何食品添加剂，其理化指标优于国标，特别是亚硝酸盐含量很低，成为宣腿的一特异性。')
      sl.write('金牌宣威火腿的精加工产品美观大方，营养丰富，风味独特，质量上乘，食用方便。宣威人民根据其特定的生产环境不断总结完善，让火腿在保持传统风味的同时，更加精美。')
   with column[1]:
      sl.image('image/introduction_craft.png')
   
   column = sl.columns([4, 6])
   with column[0]:
      sl.markdown('<br>', unsafe_allow_html= True)
      sl.header('品质监管')
      sl.markdown('<br>', unsafe_allow_html= True)
      sl.write('来自中国农业大学的“智慧云腿”北京市级创业项目团队，基于“物联网+”搭建火腿生产溯源系统。系统通过记录畜牧养殖、火腿加工、物流运输等环节信息，为消费者提供查询生产来源的可靠平台，保障金牌宣威火腿产业食品安全与健康。')
   with column[1]:
      sl.image('image/introduction_supervise.png')
   

def function_section():

   sl.markdown("""
      <center>
      <h1 class='title'>溯源系统能做什么</h1>
      <p class='describe'>先进的物联网+技术，让每一份金牌宣威火腿都安全可靠</p>
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
   
   # customer
   sl.markdown("""
      <center>
      <br>
      <h3 class='title'>我是顾客</h3>
      <p class='describe'>享美食，更放心。扫描火腿包装上的二维码，轻松查询火腿品质评级及生产来源</p>
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
   
   sl.image('image/function_customer.png')

   # farmer
   sl.markdown("""
      <center>
      <br>
      <h3 class='title'>我是养殖户</h3>
      <p class='describe'>动态录入火腿产品信息，申请金牌宣威火腿品牌认证，收获丰富利润</p>
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
   
   sl.image('image/function_farmer.png')

   # supervisor
   sl.markdown("""
      <center>
      <br>
      <h3 class='title'>我是监管员</h3>
      <p class='describe'>高效检测每一份火腿品质，保证金牌宣威火腿品牌质量</p>
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
   
   sl.image('image/function_supervisor.png')

   # salesperson
   sl.markdown("""
      <center>
      <br>
      <h3 class='title'>我是零售商</h3>
      <p class='describe'>查询进货火腿品质，合理管理产品品质分级销售，保障商家权益</p>
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
   
   sl.image('image/function_salesperson.png')


def bottom_section():

   column = sl.columns([0.2, 1, 1, 1, 1])

   with column[1]:
      sl.subheader('SITE')
      sl.write('Home & Log in')
      sl.write('Farmer')
      sl.write('Supervisor')
      sl.write('Salesperson')
      sl.write('Customer')
      
   with column[2]:
      sl.subheader('TECH')
      sl.write('Streamlit')
      sl.write('Python 3')
      sl.write('MySQL')
      sl.write('Keynote')
   
   with column[3]:
      sl.subheader('TEAM')
      sl.write('Chenxi Zhao')
      sl.write('Jina Lee')
      sl.write('Na Liu')
      sl.write('Weihong Zhu')
      sl.write('Xiaobei Zhao')

   with column[4]:
      sl.subheader('SOCIAL')
      sl.write('GitHub')
      sl.write('CAU')
      sl.write('Xuanwei City')

   sl.markdown('---')

   sl.markdown("""
      <center>
      <h4 class='title'>金牌宣威火腿溯源系统</h4>
      <p class='describe'>— 中国农业大学“智慧云腿”北京市级大学生创业项目作品 —</p>
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
   sl.markdown('<br>', unsafe_allow_html=True)
   username = login_section()
   if username != None:
      goto_next_page_section(username)
   # sl.markdown('---')
   introduction_section()
   sl.markdown('---')
   function_section()
   sl.markdown('---')
   bottom_section()
