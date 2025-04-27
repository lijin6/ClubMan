<template>
  <div class="chat-container">
    <h1>活动策划助手</h1>
    <div class="chat-box" ref="chatBox">
      <div v-for="(message, index) in chatHistory" :key="index" :class="['message', message.role]">
        <strong>{{ message.role === 'user' ? '你' : '助手' }}:</strong>
        <p>
          <span v-if="message.role === 'assistant' && !message.isComplete" class="typing-cursor">|</span>
          <span v-html="message.displayContent || markedContent(message.content)"></span>
        </p>
      </div>
    </div>
    <div class="input-box">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="请输入你的问题或请求..."
      />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
import OpenAI from "openai";
import { marked } from "marked"; // 使用命名导出

export default {
  data() {
    return {
      userInput: "",
      chatHistory: [],
      openai: null,
    };
  },
  created() {
    // 初始化 OpenAI 客户端
    this.openai = new OpenAI({
      
      apiKey: "sk-328f437af70448b4b6a32a2e8a72f9c4", // 替换为你的 API Key
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
      dangerouslyAllowBrowser: true,
    });

    // 自动发送第一条消息
    this.chatHistory.push({
      role: "assistant",
      content: "# 我是你的社团智能助手\n你可以问我任何关于活动策划的问题！",
      isComplete: true, // 标记为完整消息
    });
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim()) return;

      // 将用户输入添加到聊天记录中
      this.chatHistory.push({ role: "user", content: this.userInput });

      try {
        let fullReply = "";

        const completion = await this.openai.chat.completions.create({
          model: "qwen-omni-turbo",
          messages: [
            { role: "system", content: "You are a helpful assistant." },
            ...this.chatHistory
              .slice(-5) // 只保留最近 5 条消息
              .filter((msg) => msg.content && msg.content.trim() !== "") // 过滤掉无效消息
              .map((msg) => ({
                role: msg.role,
                content: msg.content, // 确保只传递纯文本内容
              })),
            { role: "user", content: this.userInput },
          ],
          stream: true, // 启用流式传输
          stream_options: {
            include_usage: true,
          },
          modalities: ["text"],
        });

        // 创建一个临时的助手消息对象用于显示
        const assistantMessage = { role: "assistant", content: "", displayContent: "", isComplete: false };
        this.chatHistory.push(assistantMessage);

        for await (const chunk of completion) {
          if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
            const delta = chunk.choices[0].delta?.content || "";
            fullReply += delta;

            // 动态更新助手消息的显示内容（逐字显示）
            assistantMessage.displayContent = this.markedContent(fullReply);
          } else {
            console.log(chunk.usage); // 打印使用情况
          }
        }

        // 流式传输完成后，标记消息为完整
        assistantMessage.isComplete = true;
        assistantMessage.content = fullReply;
      } catch (error) {
        console.error("Error communicating with the API:", error);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
        this.chatHistory.push({
          role: "assistant",
          content: "抱歉，我无法处理你的请求，请稍后再试。",
          isComplete: true,
        });
      }

      // 清空输入框
      this.userInput = "";

      // 滚动到底部
      this.$nextTick(() => {
        this.$refs.chatBox.scrollTop = this.$refs.chatBox.scrollHeight;
      });
    },
    markedContent(content) {
      // 使用 marked 库将 Markdown 转换为 HTML
      return marked.parse(content || "");
    },
  },
};
</script>

<style scoped>
/* 全局样式 */
body {
  margin: 0;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8fafc;
}

/* 主容器 */
.chat-container {
  max-width: 900px; /* 增加宽度 */
  height: auto;
  margin: 20px auto;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, #ffffff, #eef2ff);
  animation: fadeIn 0.5s ease-in-out;
}

/* 标题 */
h1 {
  text-align: center;
  color: #4a5568;
  margin-bottom: 20px;
  font-size: 28px;
  font-weight: bold;
  letter-spacing: 1px;
}

/* 聊天框 */
.chat-box {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 15px;
  height: 500px; /* 增加高度 */
  overflow-y: auto;
  background-color: #ffffff;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
  scroll-behavior: smooth;
}

/* 自定义滚动条 */
.chat-box::-webkit-scrollbar {
  width: 8px;
}
.chat-box::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 10px;
}
.chat-box::-webkit-scrollbar-track {
  background: #f7fafc;
}

/* 消息样式 */
.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 8px;
  transition: transform 0.2s ease-in-out;
}
.message:hover {
  transform: scale(1.02);
}

.message.user {
  text-align: right;
  color: #fff;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  align-self: flex-end;
}

.message.assistant {
  text-align: left;
  color: #333;
  background: #f1f5f9;
  align-self: flex-start;
}

.message p {
  line-height: 1.6;
  margin: 0;
  word-break: break-word;
  position: relative;
}

/* 文字逐字显示动画 */
.typing-cursor {
  animation: blink-caret 0.75s step-end infinite;
  margin-left: 2px;
}

@keyframes blink-caret {
  from, to {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

/* 输入框 */
.input-box {
  display: flex;
  margin-top: 20px;
}

.input-box input {
  flex: 1;
  padding: 12px;
  border: 2px solid #cbd5e0;
  border-radius: 8px;
  margin-right: 10px;
  font-size: 16px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.input-box input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.2);
  outline: none;
}

.input-box button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s ease, transform 0.2s ease;
}
.input-box button:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: scale(1.05);
}
.input-box button:active {
  transform: scale(0.98);
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>