# Role Play 对话数据生成工具

包含下列功能：

- 基于一段文本（自己找一段文本，复制到提示词就可以了，比如你可以从小说中选取一部分文本，注意文本要用 markdown 格式）生成角色人设，可借助 ChatGLM 实现。
- 给定两个角色的人设，调用 CharacterGLM 交替生成他们的回复。
- 将生成的对话数据保存到文件中。

运行方式：
```bash
# 1.安装依赖
pip install -r requirements.txt
# 2.修改.env 文件，配置CharacterGLM模型的API_KEY
# vi .env
# 3.启动 Streamlit，聊天并导出聊天记录到caht.log
streamlit run main.py

```