<template>
  <a-spin :spinning="showSpin">
    <div class="chat-container">
      <h2 class="chat-title">AI辅助活动策划</h2>
      <div class="chat-box">
        <div v-for="(msg, index) in chatHistory" :key="index" class="chat-message">
          <div v-if="msg.role === 'user'" class="user-message">
            <div class="message-bubble user-bubble">
              <p>{{ msg.content }}</p>
            </div>
          </div>
          <div v-if="msg.role === 'assistant'" class="assistant-message">
            <div class="message-bubble assistant-bubble">
              <p>{{ msg.content }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="input-container">
        <a-input
          v-model="userMessage"
          placeholder="请输入您的问题"
          @pressEnter="sendMessage"
          :disabled="showSpin"
          class="chat-input"
        />
        <a-button
          type="primary"
          @click="sendMessage"
          :disabled="showSpin || !userMessage.trim()"
          class="send-button"
        >
          发送
        </a-button>
      </div>
    </div>
  </a-spin>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import OpenAI from 'openai';

// 定义消息类型
interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

// 定义状态
const showSpin = ref(false); // 控制加载状态
const userMessage = ref(''); // 用户输入的消息
const chatHistory = ref<ChatMessage[]>([]); // 聊天记录

// 初始化 OpenAI 客户端
const openai = new OpenAI({
  baseURL: 'https://api.deepseek.com', // DeepSeek API 地址
  apiKey: 'sk-6a593b0defd94aa2b3e4402d3fb20997', // 替换为你的 DeepSeek API 密钥
  dangerouslyAllowBrowser: true, // 允许在浏览器中使用
});

// 发送消息函数
const sendMessage = async () => {
  const message = userMessage.value.trim();
  if (!message) return; // 如果消息为空，直接返回

  showSpin.value = true; // 显示加载状态
  chatHistory.value.push({ role: 'user', content: message }); // 将用户消息添加到聊天记录

  try {
    // 调用 DeepSeek API
    const completion = await openai.chat.completions.create({
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' }, // 系统提示
        ...chatHistory.value.map((msg) => ({ role: msg.role, content: msg.content })), // 历史消息
      ],
      model: 'deepseek-chat', // 使用的模型
    });

    // 处理 DeepSeek 的响应
    if (completion.choices && completion.choices.length > 0) {
      const aiReply = completion.choices[0].message.content; // 获取 AI 的回复
      chatHistory.value.push({ role: 'assistant', content: aiReply }); // 将 AI 回复添加到聊天记录
    } else {
      chatHistory.value.push({ role: 'assistant', content: '抱歉，我没有理解您的问题。' }); // 处理空回复
    }
  } catch (error) {
    console.error('请求失败:', error);
    chatHistory.value.push({ role: 'assistant', content: '发生了错误，请稍后再试。' }); // 处理错误
  } finally {
    showSpin.value = false; // 隐藏加载状态
    userMessage.value = ''; // 清空输入框
  }
};
</script>

<style lang="less" scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 700px;
  margin: auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chat-title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #1890ff;
  margin-bottom: 20px;
}

.chat-box {
  overflow-y: auto;
  height: 400px; /* 增加高度 */
  margin-bottom: 15px;
  padding: 15px;
  background-color: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
}

.chat-message {
  margin-bottom: 15px;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-bubble {
  display: inline-block;
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 20px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-bubble {
  background-color: #1890ff;
  color: #ffffff;
  text-align: left;
  border-radius: 20px 20px 0 20px;
}

.assistant-bubble {
  background-color: #f0f5ff;
  color: #1890ff;
  text-align: right;
  border-radius: 20px 20px 20px 0;
}

.input-container {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  align-items: center; /* 确保输入框和按钮垂直居中 */
}

.chat-input {
  flex-grow: 1;
  border-radius: 30px;
  background-color: #f5f8fd;
  border: 1px solid #e8e8e8;
  padding: 10px 16px;
  height: 40px; /* 设置固定高度 */
  line-height: 40px; /* 确保文本垂直居中 */
}

.send-button {
  border-radius: 30px;
  padding: 0 20px; /* 调整内边距 */
  height: 40px; /* 设置与输入框相同的高度 */
  background-color: #1890ff;
  color: #ffffff;
  border: none;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center; /* 确保按钮内容垂直居中 */
  justify-content: center; /* 确保按钮内容水平居中 */
}

.send-button:hover {
  background-color: #40a9ff;
}

.a-input,
.a-button {
  font-size: 14px;
}

.a-spin {
  display: flex;
  justify-content: center;
}
</style>