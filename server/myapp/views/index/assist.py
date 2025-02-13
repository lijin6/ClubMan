from rest_framework.decorators import api_view
from myapp.handler import APIResponse
import openai
from myapp import utils

# 设置 OpenAI API 密钥
openai.api_key = "sk-6a593b0defd94aa2b3e4402d3fb20997"  # 替换为你的实际 API 密钥
base_url = "https://api.deepseek.com"  # 或者根据需要替换为 DeepSeek 的 URL

# 存储每个用户的对话历史
user_conversations = {}

# AI 模型请求函数
def generate_event_plan(event_details, user_id):
    client = openai.OpenAI(api_key=openai.api_key, base_url=base_url)
    
    # 如果用户有历史对话，传递上下文
    messages = [{"role": "system", "content": "You are an AI assistant that helps create event plans."}]
    
    if user_id in user_conversations:
        messages.extend(user_conversations[user_id])  # 添加历史对话

    # 添加当前消息
    messages.append({"role": "user", "content": event_details})
    
    # 调用 AI 模型生成回复
    response = client.chat.completions.create(
        model="deepseek-chat",  # 或者替换为正确的模型名称
        messages=messages,
        stream=False
    )
    
    # 获取 AI 回复
    reply = response.choices[0].message.content

    # 保存对话上下文
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    user_conversations[user_id].append({"role": "user", "content": event_details})
    user_conversations[user_id].append({"role": "assistant", "content": reply})

    return reply


@api_view(['POST'])
def generate_event_plan_view(request):
    """
    用于生成活动策划方案的交互式对话接口
    """
    try:
        # 从请求中获取活动的基本信息
        user_id = request.data.get("user_id", 1)  # 本地开发时，直接使用默认用户 ID
        event_details = request.data.get("event_details", "")
        
        if not event_details:
            return APIResponse(code=1, msg="活动详情不能为空")
        
        # 调用 AI 模型生成活动策划方案
        plan = generate_event_plan(event_details, user_id)
        
        # 返回生成的活动策划方案
        return APIResponse(code=0, msg="活动策划生成成功", data={"plan": plan})
    
    except Exception as e:
        utils.log_error(request, f"生成活动策划失败: {str(e)}")
        return APIResponse(code=1, msg="生成活动策划失败")
    
    
    