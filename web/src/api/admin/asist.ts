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
  apiKey: "sk-6a593b0defd94aa2b3e4402d3fb20997", // 替换为你的 DeepSeek API 密钥
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
        { role: 'user', content: message }, // 用户当前消息
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