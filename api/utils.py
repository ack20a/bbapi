from datetime import datetime
from http.client import HTTPException
import json
from typing import Any, Dict, Optional
import uuid

import httpx
from api import validate
from api.auth import APP_SECRET
from api.config import get_settings
from fastapi import Depends, security
from fastapi.security import HTTPAuthorizationCredentials

from api.models import ChatRequest

from api.logger import setup_logger

logger = setup_logger(__name__)

settings = get_settings()
BASE_URL = settings.PROXY_URL
MODEL_MAPPING = settings.MODEL_MAPPING



def create_chat_completion_data(
    content: str, model: str, timestamp: int, finish_reason: Optional[str] = None
) -> Dict[str, Any]:
    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion.chunk",
        "created": timestamp,
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {"content": content, "role": "assistant"},
                "finish_reason": finish_reason,
            }
        ],
        "usage": None,
    }


def verify_app_secret(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != APP_SECRET:
        raise HTTPException(status_code=403, detail="Invalid APP_SECRET")
    return credentials.credentials


def message_to_dict(message):
    if isinstance(message.content, str):
        return {"role": message.role, "content": message.content}
    elif isinstance(message.content, list) and len(message.content) == 2:
        return {
            "role": message.role,
            "content": message.content[0]["text"],
            "data": {
                "imageBase64": message.content[1]["image_url"]["url"],
                "fileText": "",
                "title": "snapshoot",
            },
        }
    else:
        return {"role": message.role, "content": message.content}


async def process_streaming_response(request: ChatRequest):
    search_results = []  # 初始化搜索结果数组
    
    json_data = {
        "messages": [message_to_dict(msg) for msg in request.messages],
        "previewToken": None,
        "userId": None,
        "codeModelMode": True,
        "agentMode": {},
        "trendingAgentMode": {},
        "isMicMode": False,
        "userSystemPrompt": None,
        "maxTokens": request.max_tokens,
        "playgroundTopP": request.top_p,
        "playgroundTemperature": request.temperature,
        "isChromeExt": False,
        "githubToken": None,
        "clickedAnswer2": False,
        "clickedAnswer3": False,
        "clickedForceWebSearch": False,
        "visitFromDelta": False,
        "mobileClient": False,
        "userSelectedModel": MODEL_MAPPING.get(request.model),
        "validated": validate.getVid(),
        "webSearchModePrompt": True if request.model.endswith("-search") else False
    }

    async with httpx.AsyncClient() as client:
        try:
            async with client.stream(
                "POST",
                f"{BASE_URL}/api/chat",
                headers=settings.HEADERS,
                json=json_data,
                timeout=100,
            ) as response:
                response.raise_for_status()
                timestamp = int(datetime.now().timestamp())
                async for line in response.aiter_lines():
                    if line:
                        if line.startswith("$~~~$"):  # 处理搜索结果
                            try:
                                json_str = line[5:-5]  # 提取中间的JSON字符串
                                results = json.loads(json_str)
                                search_results = results  # 保存搜索结果
                                continue
                            except json.JSONDecodeError:
                                logger.error("Failed to parse search results")
                                continue
                        
                        if line == "**":
                            continue
                        content = line + "\n"
                        print(content)
                        if "https://www.blackbox.ai" in content:
                            validate.getVid(True)
                            content = "vid已刷新,重新对话即可\n"
                            yield f"data: {json.dumps(create_chat_completion_data(content, request.model, timestamp))}\n\n"
                            break
                        if content.startswith("$@$v=undefined-rv1$@$"):
                            yield f"data: {json.dumps(create_chat_completion_data(content[21:], request.model, timestamp))}\n\n"
                        else:
                            yield f"data: {json.dumps(create_chat_completion_data(content, request.model, timestamp))}\n\n"
                    elif line == "":
                        content = line + "\n\n"
                        print(content)
                        if "https://www.blackbox.ai" in content:
                            validate.getVid(True)
                            content = "vid已刷新,重新对话即可\n"
                            yield f"data: {json.dumps(create_chat_completion_data(content, request.model, timestamp))}\n\n"
                            break
                        if content.startswith("$@$v=undefined-rv1$@$"):
                            yield f"data: {json.dumps(create_chat_completion_data(content[21:], request.model, timestamp))}\n\n"
                        else:
                            yield f"data: {json.dumps(create_chat_completion_data(content, request.model, timestamp))}\n\n"
                if search_results:  # 在结束前输出引用来源
                    sources = "\n\n**引用来源**\n" + "\n".join([f"- [{r['title']}]({r['link']})" for r in search_results])
                    yield f"data: {json.dumps(create_chat_completion_data(sources, request.model, timestamp))}\n\n"
                    
                yield f"data: {json.dumps(create_chat_completion_data('', request.model, timestamp, 'stop'))}\n\n"
                yield "data: [DONE]\n\n"
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            logger.error(f"Error occurred during request: {e}")
            raise HTTPException(status_code=500, detail=str(e))


async def process_non_streaming_response(request: ChatRequest):
    json_data = {
        "messages": [message_to_dict(msg) for msg in request.messages],
        "previewToken": None,
        "userId": None,
        "codeModelMode": True,
        "agentMode": {},
        "trendingAgentMode": {},
        "isMicMode": False,
        "userSystemPrompt": None,
        "maxTokens": request.max_tokens,
        "playgroundTopP": request.top_p,
        "playgroundTemperature": request.temperature,
        "isChromeExt": False,
        "githubToken": None,
        "clickedAnswer2": False,
        "clickedAnswer3": False,
        "clickedForceWebSearch": False,
        "visitFromDelta": False,
        "mobileClient": False,
        "userSelectedModel": MODEL_MAPPING.get(request.model),
        "validated": validate.getVid(),
        "webSearchModePrompt": True if request.model.endswith("-search") else False
    }
    full_response = ""
    async with httpx.AsyncClient() as client:
        async with client.stream(
            method="POST", url=f"{BASE_URL}/api/chat", headers=settings.HEADERS, json=json_data
        ) as response:
            async for chunk in response.aiter_text():
                full_response += chunk
    if "https://www.blackbox.ai" in full_response:
        validate.getVid(True)
        full_response = "vid已刷新，重新对话即可"
    if full_response.startswith("$@$v=undefined-rv1$@$"):
        full_response = full_response[21:]
    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(datetime.now().timestamp()),
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": full_response},
                "finish_reason": "stop",
            }
        ],
        "usage": None,
    }
