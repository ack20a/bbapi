# BlackBox AI API

这是一个 BlackBox AI API 的反向工程项目,提供了与官方 API 相同的功能接口。

⚠️ 警告:本项目仅供学习研究使用,请于下载后24小时内自觉删除,不得用于商业用途或其他违法用途!

## 功能特性

- 支持多种AI模型调用(GPT-4、Claude、Gemini等)
- 支持流式输出(SSE)和普通输出
- 支持网络搜索增强对话
- 完整的错误处理和日志记录
- 兼容 OpenAI API 格式
- 支持 CORS 跨域请求
- 内置请求缓存机制

## 支持的模型

- gpt-4o
- gemini-1.5-pro  
- claude-3-5-sonnet
- deepseek-v3
- deepseek-r1
- blackboxai
- blackboxai-pro
- blackboxai-search
- meta-llama/Llama-3.3-70B-Instruct-Turbo
- meta-llama/Meta-Llama-3.1-405B-Instruct-Lite-Pro
- Qwen/QwQ-32B-Preview

## 安装

1. 克隆项目
```bash
git clone [项目地址]
cd blackbox-api
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建 .env 文件并配置以下变量:
```
HOST=0.0.0.0
PORT=8001
DEBUG=False
WORKERS=1
LOG_LEVEL=INFO
PROXY_URL=https://www.blackbox.ai
APP_SECRET=your_secret_key
```

## 运行

```bash
python main.py
```

服务将在 http://localhost:8001 启动

## API 使用

### 认证
所有请求需要在 Header 中携带 Authorization Bearer Token:
```
Authorization: Bearer your_app_secret
```

### 聊天完成接口
```
POST /api/v1/chat/completions
```

请求体格式:
```json
{
    "model": "gpt-4o",
    "messages": [
        {"role": "user", "content": "你好"}
    ],
    "stream": true,
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 8192
}
```

## 注意事项

1. 本项目仅供学习研究使用
2. 请遵守相关法律法规
3. 下载后24小时内请自觉删除
4. 不得用于商业用途
5. 使用本项目造成的任何问题由使用者自行承担

## 许可证

MIT License (仅供学习研究使用)
