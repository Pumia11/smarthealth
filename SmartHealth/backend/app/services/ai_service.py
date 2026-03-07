import os
import json
import requests
from typing import Dict, Any

DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

def analyze_health(data: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
    你是一个专业的健康分析师。请根据以下用户数据，提供全面的健康分析报告。
    
    用户基本信息：
    {json.dumps(data.get('user_profile', {}), ensure_ascii=False, indent=2)}
    
    健康指标记录（最近{data.get('analysis_period', {}).get('days', 7)}天）：
    {json.dumps(data.get('health_records', []), ensure_ascii=False, indent=2)}
    
    饮食记录（最近{data.get('analysis_period', {}).get('days', 7)}天）：
    {json.dumps(data.get('diet_records', []), ensure_ascii=False, indent=2)}
    
    运动记录（最近{data.get('analysis_period', {}).get('days', 7)}天）：
    {json.dumps(data.get('exercise_records', []), ensure_ascii=False, indent=2)}
    
    请以JSON格式返回以下内容：
    {{
        "health_score": <0-100的健康评分>,
        "risks": [<识别的健康风险列表>],
        "nutrition_analysis": {{
            "calories_status": "<热量摄入评价>",
            "protein_status": "<蛋白质摄入评价>",
            "carbs_status": "<碳水化合物摄入评价>",
            "fat_status": "<脂肪摄入评价>",
            "suggestions": [<营养建议列表>]
        }},
        "exercise_analysis": {{
            "total_duration": <总运动时长>,
            "total_calories": <总消耗热量>,
            "exercise_frequency": "<运动频率评价>",
            "suggestions": [<运动建议列表>]
        }},
        "indicator_analysis": {{
            "<指标名称>": {{
                "current_value": <当前值>,
                "status": "<正常/偏高/偏低>",
                "trend": "<上升/下降/稳定>",
                "suggestion": "<建议>"
            }}
        }},
        "recommendations": [<个性化健康建议列表>]
    }}
    """
    
    if not DEEPSEEK_API_KEY:
        return generate_mock_analysis(data)
    
    try:
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': '你是一个专业的健康分析师，擅长分析用户的健康数据并提供个性化建议。'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return json.loads(content)
        else:
            return generate_mock_analysis(data)
            
    except Exception as e:
        print(f"AI analysis error: {e}")
        return generate_mock_analysis(data)

def generate_mock_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    health_records = data.get('health_records', [])
    diet_records = data.get('diet_records', [])
    exercise_records = data.get('exercise_records', [])
    
    total_calories = sum(r.get('total_calories', 0) for r in diet_records)
    total_exercise_calories = sum(r.get('calories_burned', 0) for r in exercise_records)
    total_duration = sum(r.get('duration', 0) for r in exercise_records)
    
    health_score = 75
    if health_records:
        abnormal_count = sum(1 for r in health_records if r.get('is_abnormal'))
        health_score -= abnormal_count * 5
    
    return {
        'health_score': max(health_score, 0),
        'risks': [
            '建议增加运动频率',
            '注意饮食均衡'
        ],
        'nutrition_analysis': {
            'calories_status': f'日均摄入{total_calories/7:.0f}千卡',
            'protein_status': '蛋白质摄入适中',
            'carbs_status': '碳水化合物摄入适中',
            'fat_status': '脂肪摄入适中',
            'suggestions': [
                '建议增加蔬菜水果摄入',
                '控制油脂摄入量'
            ]
        },
        'exercise_analysis': {
            'total_duration': total_duration,
            'total_calories': total_exercise_calories,
            'exercise_frequency': '运动频率适中',
            'suggestions': [
                '建议每周运动3-5次',
                '每次运动30分钟以上'
            ]
        },
        'indicator_analysis': {
            '体重': {
                'current_value': data.get('user_profile', {}).get('weight', 0),
                'status': '正常',
                'trend': '稳定',
                'suggestion': '保持当前体重'
            }
        },
        'recommendations': [
            '保持规律作息',
            '多喝水，每天至少8杯',
            '定期进行健康体检',
            '保持心情愉悦'
        ]
    }
