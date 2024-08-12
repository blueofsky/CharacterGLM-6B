import itertools
import io
from dotenv import load_dotenv
load_dotenv()
from api import get_characterglm_response
import streamlit as st
from data_types import TextMsg

if "history" not in st.session_state:
    print("=========")
    st.session_state["history"] = []
    st.session_state["history_message"] = ""    
if "meta" not in st.session_state:
    st.session_state["meta"] = {}


def chat_with(role_name,role_info,other_role_name:str,other_role_info:str):
    character_meta = {
        "user_info": other_role_info,
        "bot_info": role_info,
        "user_name": other_role_name,
        "bot_name": role_name,
    }
    
    messages = []
    for msg in st.session_state["history"][-3:]:
        messages.append({"role": "user" if msg['role'] == other_role_name else "assistant", "content": msg['content']})
    # print(messages)
    content = ""
    for content in itertools.accumulate(get_characterglm_response(messages, meta=character_meta)):
        pass
    st.session_state["history"].append(TextMsg({"role": role_name,"content": content}))
    st.session_state["history_message"]+=f"{role_name}: {content}\n"
    # print("==",st.session_state["history_message"])
    # print(role_name,':',content)
    return content

# ui 
st.set_page_config(page_title="角色扮演", page_icon="🤖", layout="wide")

# 2x2 layout
with st.container():    
    st.subheader("角色信息: ")
    col1, col2 = st.columns(2)
    with col1:
        bot_name_a=st.text_input(label="角色名(甲方)", 
                    key="bot_name_a", 
                    value="郭襄", 
                    help="模型所扮演的角色的名字，不可以为空")
        bot_info_a=st.text_area(label="角色人设(甲方)", 
                    key="bot_info_a", 
                    height=120,
                    value="郭靖与黄蓉之女，峨眉派创始人。活泼开朗，不拘小节。善良纯真，乐于助人。聪明伶俐，具有较高的武学天赋。情感真挚，对杨过怀有深厚的感情，但最终选择放下。继承了父母和师祖的武学，精通峨眉剑法。在寻找杨过的过程中，历经江湖风波，最终创立峨眉派，成为一代宗师。",
                    help="角色的详细人设信息，不可以为空")
        bot_chat_a=st.text_input(label="初始聊天消息(甲方)", 
                    key="bot_chat_a", 
                    value="（旁白：郭襄在寻找杨过的过程中，经历了许多艰难险阻，最终在华山之巅与杨过和小龙女相遇。）杨大哥，我可找到你们了。",
                    help="角色的初始聊天信息，不可以为空")
        
    with col2:
        bot_name_b=st.text_input(label="角色名(乙方)", 
                    key="bot_name_b", 
                    value="杨过", 
                    help="模型所扮演的角色的名字，不可以为空")
        bot_info_b=st.text_area(label="角色人设(乙方)", 
                    key="bot_info_b", 
                    height=120,
                    value="杨康与穆念慈之子，神雕侠。聪明机智，善于观察和分析。性格独立，不拘泥于传统礼教。情感丰富，对爱情忠贞不渝。有时显得孤傲，但内心深处渴望被理解和接纳。师从黄药师、欧阳锋、洪七公等多位武林高手，精通多种武功。从小失去父母，历经坎坷，最终成为一代大侠。",
                    help="角色的详细人设信息，不可以为空")
        bot_chat_b=st.text_input(label="初始聊天消息(乙方)", 
                    key="bot_chat_b", 
                    value="（深沉的语气）郭姑娘，这些年你四处奔波，真是辛苦了。",
                    help="角色的初始聊天信息，不可以为空")  

if not st.session_state["history"]:
    print("init: {st.session_state['history']}")
    st.session_state["history"].append(TextMsg({"role": bot_name_a,"content": bot_chat_a}))
    st.session_state["history"].append(TextMsg({"role": bot_name_b,"content": bot_chat_b}))
    st.session_state["history_message"]+=f"{bot_name_a}: {bot_chat_a}\n"
    st.session_state["history_message"]+=f"{bot_name_b}: {bot_chat_b}\n"

def get_download_data():
    download_data=""
    for msg in st.session_state["history"]:
        download_data += f"{msg['role']}: {msg['content']}\n"
    print(f"download_data: {download_data}")
    return download_data

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        generate_chat = st.button("生成对话")
    with col2:
        st.download_button(label="导出聊天记录",
                           data=io.StringIO(get_download_data()).getvalue().encode('utf-8'),  # 动态获取数据
                           file_name="chatgroup.txt"
                        )
                 
with st.container():
    st.subheader("聊天记录: ")
    with st.chat_message(name="user", avatar="user"):
        st.markdown(f"{bot_name_a}: {bot_chat_a}")
    with st.chat_message(name="assistant", avatar="assistant"):
        st.markdown(f"{bot_name_b}: {bot_chat_b}")
    if generate_chat:
         for i in range(2):
            with st.chat_message(name="user", avatar="user"):
                st.markdown(f"{bot_name_a}: {chat_with(bot_name_a,bot_info_a,bot_name_b,bot_info_b)}")
            with st.chat_message(name="assistant", avatar="assistant"):    
                st.markdown(f"{bot_name_b}: {chat_with(bot_name_b,bot_info_b,bot_name_a,bot_info_a)}")
