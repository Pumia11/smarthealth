from typing import Dict, Any
from .exceptions import AIResponseError


def validate_analysis_result(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证 AI 返回的分析结果
    
    Args:
        data: AI 返回的原始数据
        
    Returns:
        验证后的数据，缺失字段会使用默认值
        
    Raises:
        AIResponseError: 如果数据格式严重错误
    """
    if not isinstance(data, dict):
        raise AIResponseError("Response must be a dictionary")
    
    health_score = data.get('health_score', 75)
    if not isinstance(health_score, (int, float)):
        health_score = 75
    else:
        health_score = max(0, min(100, int(health_score)))
    
    risks = data.get('risks', [])
    if not isinstance(risks, list):
        risks = []
    risks = [str(risk) for risk in risks if risk]
    
    nutrition_analysis = data.get('nutrition_analysis', {})
    if not isinstance(nutrition_analysis, dict):
        nutrition_analysis = {}
    
    validated_nutrition = {
        'calories_status': str(nutrition_analysis.get('calories_status', '未知')),
        'protein_status': str(nutrition_analysis.get('protein_status', '未知')),
        'carbs_status': str(nutrition_analysis.get('carbs_status', '未知')),
        'fat_status': str(nutrition_analysis.get('fat_status', '未知')),
        'suggestions': [
            str(s) for s in nutrition_analysis.get('suggestions', []) if s
        ]
    }
    
    exercise_analysis = data.get('exercise_analysis', {})
    if not isinstance(exercise_analysis, dict):
        exercise_analysis = {}
    
    validated_exercise = {
        'total_duration': int(exercise_analysis.get('total_duration', 0)),
        'total_calories': float(exercise_analysis.get('total_calories', 0)),
        'exercise_frequency': str(exercise_analysis.get('exercise_frequency', '未知')),
        'suggestions': [
            str(s) for s in exercise_analysis.get('suggestions', []) if s
        ]
    }
    
    indicator_analysis = data.get('indicator_analysis', {})
    if not isinstance(indicator_analysis, dict):
        indicator_analysis = {}
    
    validated_indicators = {}
    for key, value in indicator_analysis.items():
        if isinstance(value, dict):
            validated_indicators[str(key)] = {
                'current_value': value.get('current_value', 0),
                'status': str(value.get('status', '未知')),
                'trend': str(value.get('trend', '未知')),
                'suggestion': str(value.get('suggestion', ''))
            }
    
    recommendations = data.get('recommendations', [])
    if not isinstance(recommendations, list):
        recommendations = []
    recommendations = [str(rec) for rec in recommendations if rec]
    
    return {
        'health_score': health_score,
        'risks': risks,
        'nutrition_analysis': validated_nutrition,
        'exercise_analysis': validated_exercise,
        'indicator_analysis': validated_indicators,
        'recommendations': recommendations
    }
