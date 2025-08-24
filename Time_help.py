import openai
import requests
import json
import datetime


api = "sk-90d6dcbb0a4f4f418d7bb97088eec077"

# 获取用户所在地天气
def Get_Weather(city1,city2):
    
    # 进程播报
    print(f"正在通过API接口获取{city1}{city2}的天气状况...")

    # 获取当地天气
    response = requests.get(url=f"https://cn.apihz.cn/api/tianqi/tqyb.php?id=88888888&key=88888888&sheng={city1}&place={city2}")


    # 调用错误处理:
    print(response)
    if (response.ok):
        pass
    else:
        print("天气获取失败！将生成不考虑天气影响的安排。")


    # 转化为json
    data = response.json()

    # 获取天气
    weather = data.get("weather1")

    if weather == None:
        print("天气获取失败！将生成不考虑天气影响的安排。")


    # 返回当地天气
    return weather


# 当前时间获取
def Get_time():
    time = datetime.datetime.now()

    

    # 返回当前时间
    return time


# 调用大模型
def llm(weather,time,tasks):

    # 初始化
    client = openai.OpenAI(
        
        api_key = api,
        base_url = "https://api.deepseek.com/v1"
        )

    # 构建prompt
    prompt = f"""
    你是一个时间管理助手，请根据以下信息为用户生成高效的时间安排建议：
    - 天气{weather}
    - 当前时间{time}
    - 用户的任务{tasks} 

    要求：
    - 1.分配任务到合理时段
    - 2.考虑天气对户外活动的影响
    - 3.包含休息时间建议
    - 4.输出为清晰的时间表格式
    - 5.你仅可输出高效的时间安排建议
    - 6.输出信息开头需包含（天气、当前时间、用户任务）如：
        天气 : {weather}   当前时间:{time}    行程 : {tasks}
        ===============已经为您生成智能行程安排===============
        
        ......

        




    """

    # 进程播报
    print("正在生成行程安排...")


    # 尝试发送请求
    response = client.chat.completions.create(


    # 指定模型
    model = "deepseek-chat",


    messages = [{"role":"user","content":prompt}],


    # 文本随机性
    temperature = 0.7,


    # 关闭流式传输
    stream = False 

    )


    return response.choices[0].message.content.strip()

# 生成记录保存
def save_log(tasks,response):

    # 生成的时间
    time = datetime.datetime.now().isoformat()  # 使用iso格式时间戳（YYYY-MM-DDTHH:MM:SSZ）

    # 创建记录字典：
    history = {

        # 生成时间
        "date" : time,

        # 用户行程
        "tasks" : tasks,

        # 模型生成

        "response" : response

    }

    with open("history.json" , "a" , encoding = "utf-8") as f:      # "a"追加模式

        # ensure_ascii=False  允许非ASCII码直接保存
        f.write(json.dumps(history,ensure_ascii = False) + "\n" )   
        






# 主程序
if __name__ == "__main__":
    print("======欢迎使用智能日程安排系统======")
    print()
    tasks = input("请输入您今天的安排(打球/买菜/购物...):")

    # 开始执行程序

    # 获取当前时间：
    time = Get_time()

    # 获取地址
    c1 = input("1")
    c2 = input("2")

    try:

        # 获取天气
        weather = Get_Weather(c1,c2)
     


        # 调用大模型
        response = llm(weather,time,tasks)

    
    # 错误显示
    except Exception as e:

        print( f"API调用失败，无法生成日志:{e}")



    print(response)

    # 保存记录
    save_log(tasks,response)











    
