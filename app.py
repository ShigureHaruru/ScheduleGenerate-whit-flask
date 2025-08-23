import os
import openai
import json
import datetime

from flask import Flask, g, request, jsonify, render_template  # Flask Web框架相关
from flask_cors import CORS                                 # 跨域请求支持
import logging

# 导入函数文件
from Time_help import Get_time,Get_Weather,llm                                           



# 创建Flask应用实例
app = Flask(__name__,template_folder="html")

# 启用CORS(跨域资源共享)，允许前端应用从不同域访问API
CORS(app)

# 配置日志系统，设置日志级别为INFO，记录重要操作信息
logging.basicConfig(level=logging.INFO)





@app.route("/")             # "当用户访问网站的根路径时，执行下面的函数"
def index():

    #当用户访问根目录时，渲染并返回主页
    # render_template会在templates文件夹中查找index.html文件
    return render_template('index.html')


# 定义API端点路由（/api/generate 生成任务）
@app.route("/api/generate",methods = ['POST'])      # methods=['POST'] 仅接受post请求
# 返回: JSON响应，包含生成的日程或错误信息
def generate():
    

    # 获取请求中的参数(使用flask的request.json)
    data = request.json



    # 获取参数并赋值
    city1 = data.get("province","")
    city2 = data.get("city","")
    tasks = data.get("tasks","")



    # 判断数值是否空
    if not tasks or not city1 or not city2:

        # 为空则以json格式向用户返回错误：
        return jsonify({"error":"缺少必要参数！"}),400




    # 调用函数获取必要数据
    weather = Get_Weather(city1,city2)

    time = Get_time()



    # 尝试调用大模型生成日程
    try:
        Re = llm(weather = weather , time = time , tasks = tasks)


    except Exception as e:

        # 输出日志
        print(f"调用失败：{e}")

        # 调用失败返回结果
        return jsonify({"error":"大模型调用失败，请稍后再试！"}),500
        
        


    # 调用成功返回结果
    return jsonify({"schedule":Re}),200



if __name__ == "__main__":
    # 确保代码只在直接运行此脚本时执行


    # 获取环境变量端口，失败则使用默认端口10001
    port = os.environ.get("PORT",10002)
    

    # 启动Flask开发服务器
    # debug=True启用调试模式，自动重新加载代码更改并提供详细错误页面
    # 生产环境应设置为False
    app.run(debug = True,port=port)
