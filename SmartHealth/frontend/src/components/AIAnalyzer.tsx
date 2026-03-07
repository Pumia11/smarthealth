import { useState } from 'react';
import { aiAPI } from '../utils/api';

interface AnalysisResult {
  health_score: number;
  risks: string[];
  nutrition_analysis: {
    total_calories: number;
    protein_status: string;
    carbs_status: string;
    fat_status: string;
    suggestions: string[];
  };
  exercise_analysis: {
    total_duration: number;
    total_calories: number;
    exercise_frequency: string;
    suggestions: string[];
  };
  indicator_analysis: {
    [key: string]: {
      current_value: number;
      status: string;
      trend: string;
      suggestion: string;
    };
  };
  recommendations: string[];
}

export default function AIAnalyzer() {
  const [days, setDays] = useState(7);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await aiAPI.analyze(days);
      setResult(response.data.analysis);
    } catch (err: any) {
      setError(err.response?.data?.error || '分析失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-pixel-success';
    if (score >= 60) return 'text-pixel-warning';
    return 'text-pixel-secondary';
  };

  const getScoreEmoji = (score: number) => {
    if (score >= 80) return '😊';
    if (score >= 60) return '😐';
    return '😟';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <select
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          className="px-4 py-2 font-pixel text-pixel-text bg-pixel-bg border-2 border-pixel-border shadow-pixel-inset focus:outline-none focus:border-pixel-accent"
        >
          <option value={7}>近 7 天</option>
          <option value={14}>近 14 天</option>
          <option value={30}>近 30 天</option>
        </select>
        
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="px-6 py-2 font-pixel text-pixel-text bg-pixel-primary border-2 border-pixel-border shadow-pixel transition-all duration-100 cursor-pointer hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-pixel-lg active:translate-x-[2px] active:translate-y-[2px] active:shadow-pixel-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <span className="animate-pixel-pulse">●</span>
              <span>分析中...</span>
            </span>
          ) : (
            '🔍 开始分析'
          )}
        </button>
      </div>

      {error && (
        <div className="p-4 bg-pixel-secondary/20 border-2 border-pixel-secondary font-pixel text-sm text-pixel-secondary">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-6 animate-pixel-fade-in">
          <div className="text-center p-8 bg-pixel-bg border-2 border-pixel-border">
            <div className="text-6xl mb-4">{getScoreEmoji(result.health_score)}</div>
            <div className={`font-pixel text-5xl mb-2 ${getScoreColor(result.health_score)}`}>
              {result.health_score}
            </div>
            <div className="font-pixel text-sm text-pixel-muted">
              综合健康评分
            </div>
          </div>

          {result.risks.length > 0 && (
            <div className="p-4 bg-pixel-secondary/10 border-2 border-pixel-secondary">
              <h3 className="font-pixel text-sm text-pixel-secondary mb-3">
                ⚠️ 健康风险提示
              </h3>
              <ul className="space-y-2">
                {result.risks.map((risk, index) => (
                  <li key={index} className="font-pixel text-sm text-pixel-text">
                    • {risk}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-pixel-bg border-2 border-pixel-border">
              <h3 className="font-pixel text-sm text-pixel-accent mb-3">
                🍎 营养摄入分析
              </h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="font-pixel text-pixel-muted">总热量</span>
                  <span className="font-pixel text-pixel-accent">
                    {result.nutrition_analysis.total_calories} kcal
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="font-pixel text-pixel-muted">蛋白质</span>
                  <span className="font-pixel text-pixel-text">
                    {result.nutrition_analysis.protein_status}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="font-pixel text-pixel-muted">碳水化合物</span>
                  <span className="font-pixel text-pixel-text">
                    {result.nutrition_analysis.carbs_status}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="font-pixel text-pixel-muted">脂肪</span>
                  <span className="font-pixel text-pixel-text">
                    {result.nutrition_analysis.fat_status}
                  </span>
                </div>
              </div>
            </div>

            <div className="p-4 bg-pixel-bg border-2 border-pixel-border">
              <h3 className="font-pixel text-sm text-pixel-accent mb-3">
                🏃 运动情况分析
              </h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="font-pixel text-pixel-muted">总时长</span>
                  <span className="font-pixel text-pixel-accent">
                    {result.exercise_analysis.total_duration} 分钟
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="font-pixel text-pixel-muted">消耗热量</span>
                  <span className="font-pixel text-pixel-accent">
                    {result.exercise_analysis.total_calories} kcal
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="font-pixel text-pixel-muted">运动频率</span>
                  <span className="font-pixel text-pixel-text">
                    {result.exercise_analysis.exercise_frequency}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="p-4 bg-pixel-bg border-2 border-pixel-border">
            <h3 className="font-pixel text-sm text-pixel-accent mb-3">
              💡 健康建议
            </h3>
            <ul className="space-y-2">
              {result.recommendations.map((rec, index) => (
                <li key={index} className="font-pixel text-sm text-pixel-text">
                  • {rec}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {!result && !loading && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🤖</div>
          <p className="font-pixel text-pixel-muted">
            选择分析周期，点击开始分析
          </p>
          <p className="font-pixel text-sm text-pixel-muted mt-2">
            AI 将根据您的健康数据生成个性化分析报告
          </p>
        </div>
      )}
    </div>
  );
}
