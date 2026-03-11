import re
import json
from typing import Optional


def is_valid_json(json_str: str) -> bool:
    """验证字符串是否为有效的 JSON"""
    try:
        json.loads(json_str)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def extract_json(content: str) -> Optional[str]:
    """
    从 AI 响应中提取 JSON 字符串
    
    支持以下格式：
    1. Markdown 代码块：```json ... ```
    2. 纯 JSON：{ ... }
    3. JSON 前后有其他文字
    
    Args:
        content: AI 返回的原始内容
        
    Returns:
        提取的 JSON 字符串，如果提取失败则返回 None
    """
    markdown_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    markdown_match = re.search(markdown_pattern, content)
    if markdown_match:
        json_str = markdown_match.group(1).strip()
        if is_valid_json(json_str):
            return json_str
    
    stack = []
    start_idx = -1
    
    for i, char in enumerate(content):
        if char == '{':
            if not stack:
                start_idx = i
            stack.append(char)
        elif char == '}':
            if stack:
                stack.pop()
                if not stack and start_idx != -1:
                    json_str = content[start_idx:i+1]
                    if is_valid_json(json_str):
                        return json_str
    
    if is_valid_json(content.strip()):
        return content.strip()
    
    return None
