from typing import Dict, Any
import json
from dataclasses import dataclass


@dataclass
class PromptTemplate:
    name: str
    system_prompt: str
    user_prompt_template: str
    response_schema: Dict[str, Any]


class PromptManager:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, PromptTemplate]:
        """从配置文件加载 Prompt 模板"""
        return {
            'health_analysis': PromptTemplate(
                name='health_analysis',
                system_prompt='你是一个专业的健康分析师，擅长分析用户的健康数据并提供个性化建议。请只返回JSON格式的结果，不要包含其他文字。',
                user_prompt_template="""请根据以下用户数据，提供全面的健康分析报告。

用户基本信息：
{user_profile}

健康指标记录（最近{days}天）：
{health_records}

饮食记录（最近{days}天）：
{diet_records}

运动记录（最近{days}天）：
{exercise_records}

请以JSON格式返回以下内容：
{response_schema}""",
                response_schema={
                    "health_score": "0-100的健康评分",
                    "risks": "识别的健康风险列表",
                    "nutrition_analysis": {
                        "calories_status": "热量摄入评价",
                        "protein_status": "蛋白质摄入评价",
                        "carbs_status": "碳水化合物摄入评价",
                        "fat_status": "脂肪摄入评价",
                        "suggestions": "营养建议列表"
                    },
                    "exercise_analysis": {
                        "total_duration": "总运动时长",
                        "total_calories": "总消耗热量",
                        "exercise_frequency": "运动频率评价",
                        "suggestions": "运动建议列表"
                    },
                    "indicator_analysis": {
                        "<指标名称>": {
                            "current_value": "当前值",
                            "status": "正常/偏高/偏低",
                            "trend": "上升/下降/稳定",
                            "suggestion": "建议"
                        }
                    },
                    "recommendations": "个性化健康建议列表"
                }
            )
        }
    
    def get_template(self, name: str) -> PromptTemplate:
        """获取指定名称的 Prompt 模板"""
        return self.templates.get(name)
    
    def render_prompt(self, template_name: str, **kwargs) -> str:
        """渲染 Prompt 模板"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")
        
        formatted_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, (dict, list)):
                formatted_kwargs[key] = json.dumps(value, ensure_ascii=False, indent=2)
            else:
                formatted_kwargs[key] = value
        
        formatted_kwargs['response_schema'] = json.dumps(
            template.response_schema, ensure_ascii=False, indent=2
        )
        
        return template.user_prompt_template.format(**formatted_kwargs)


prompt_manager = PromptManager()
