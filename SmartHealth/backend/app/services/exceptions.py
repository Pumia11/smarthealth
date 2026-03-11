class AIServiceError(Exception):
    """AI 服务基础异常"""
    pass


class AIConfigurationError(AIServiceError):
    """配置错误（如 API 密钥缺失）"""
    pass


class AINetworkError(AIServiceError):
    """网络错误"""
    pass


class AIAPIError(AIServiceError):
    """API 调用错误"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API error {status_code}: {message}")


class AIResponseError(AIServiceError):
    """响应解析错误"""
    pass
