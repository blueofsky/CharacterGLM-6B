import itertools
from dotenv import load_dotenv
load_dotenv()
from api import get_characterglm_response

class ChatGroup:
    def __init__(self,messages):
        self.role_infos={}
        self.history_messages=messages
    def export_history(self, file_name: str):
        with open(file_name, 'w', encoding='utf-8') as file:
            for index, msg in enumerate(self.history_messages):
                file.write(f"{msg['role']}: {msg['content']}\n")
                if index>0 and (index + 1) % 2 == 0:
                    file.write("\n")
class Role:
    def __init__(self,role_name: str,role_info: str,chat_group: ChatGroup):
        self.role_name=role_name
        self.role_info=role_info
        self.chat_group = chat_group
        self.chat_group.role_infos[self.role_name]=self.role_info
    
    def chat_with(self,other_role_name:str):
        character_meta = {
            "user_info": self.chat_group.role_infos[other_role_name],
            "bot_info": self.role_info,
            "user_name": other_role_name,
            "bot_name": self.role_name,
        }
        
        messages = []
        for msg in self.chat_group.history_messages[-3:]:
           messages.append({"role": "user" if msg['role'] == other_role_name else "assistant", "content": msg['content']})
        content = ""
        for content in itertools.accumulate(get_characterglm_response(messages, meta=character_meta)):
            pass
        self.chat_group.history_messages.append({"role": self.role_name,"content": content})
        return content

def launch_chat_ui():
    pass

if __name__ == "__main__":
    chatgroup=ChatGroup([
        {"role": "郭襄","content": "（旁白：郭襄在寻找杨过的过程中，经历了许多艰难险阻，最终在华山之巅与杨过和小龙女相遇。）杨大哥，我可找到你们了。"},
        {"role": "杨过","content": "郭姑娘，这些年你四处奔波，真是辛苦了。"},
    ])
    yangguo=Role("杨过",
                 """
                 杨康与穆念慈之子，神雕侠。
                 聪明机智，善于观察和分析。
                 性格独立，不拘泥于传统礼教。
                 情感丰富，对爱情忠贞不渝。
                 有时显得孤傲，但内心深处渴望被理解和接纳。
                 师从黄药师、欧阳锋、洪七公等多位武林高手，精通多种武功。
                 从小失去父母，历经坎坷，最终成为一代大侠。
                 """,chatgroup)
    guoxiang=Role("郭襄",
                """
                郭靖与黄蓉之女，峨眉派创始人。
                活泼开朗，不拘小节。善良纯真，乐于助人。
                聪明伶俐，具有较高的武学天赋。情感真挚，对杨过怀有深厚的感情，但最终选择放下。
                继承了父母和师祖的武学，精通峨眉剑法。
                在寻找杨过的过程中，历经江湖风波，最终创立峨眉派，成为一代宗师。
                """,chatgroup)
    
    rounds=10 # 轮数
    print("---聊天开始---")
    for msg in chatgroup.history_messages:
        print(f'{msg["role"]}: {msg["content"]}')
    print()
    for i in range(rounds):        
        print(f'郭襄: {guoxiang.chat_with("杨过")}')
        print(f'杨过: {yangguo.chat_with("郭襄")}')
        print()
    print("---聊天结束---")

    print("---导出聊天记录开始---")
    chatgroup.export_history("chat.log")
    print("---导出聊天记录结束---")