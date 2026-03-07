import { useState, useEffect } from 'react';
import { exerciseAPI } from '../utils/api';

interface ExerciseRecord {
  id: string;
  exercise: {
    id: string;
    name: string;
    mets: number;
  };
  duration: number;
  calories_burned: number;
  record_time: string;
  heart_rate_avg?: number;
  heart_rate_max?: number;
}

export default function ExerciseRecords() {
  const [records, setRecords] = useState<ExerciseRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const response = await exerciseAPI.getRecords({ start_date: `${today}T00:00:00`, end_date: `${today}T23:59:59` });
      setRecords(response.data.records);
    } catch (error) {
      console.error('Failed to load exercise records:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getExerciseIcon = (name: string) => {
    const icons: { [key: string]: string } = {
      '跑步': '🏃',
      '游泳': '🏊',
      '骑行': '🚴',
      '篮球': '🏀',
      '足球': '⚽',
      '羽毛球': '🏸',
      '瑜伽': '🧘',
      '健身': '💪',
      '跳绳': '🪢',
      '登山': '🧗',
    };
    return icons[name] || '🏃';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-48">
        <div className="animate-pixel-pulse text-pixel-accent font-pixel">
          加载中...
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {records.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🏃</div>
          <p className="font-pixel text-pixel-muted">今日暂无运动记录</p>
          <p className="font-pixel text-sm text-pixel-muted mt-2">
            点击上方按钮开始记录
          </p>
        </div>
      ) : (
        records.map((record) => (
          <div
            key={record.id}
            className="p-4 bg-pixel-bg border-2 border-pixel-border hover:border-pixel-accent transition-colors"
          >
            <div className="flex justify-between items-start">
              <div className="flex items-start gap-4">
                <div className="text-3xl">
                  {getExerciseIcon(record.exercise.name)}
                </div>
                <div>
                  <div className="font-pixel text-base mb-1">
                    {record.exercise.name}
                  </div>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="font-pixel text-pixel-accent">
                      🔥 {record.calories_burned} kcal
                    </span>
                    <span className="font-pixel text-pixel-muted">
                      ⏱️ {record.duration} 分钟
                    </span>
                  </div>
                  {record.heart_rate_avg && (
                    <div className="mt-2 font-pixel text-xs text-pixel-muted">
                      ❤️ 平均心率: {record.heart_rate_avg} bpm
                      {record.heart_rate_max && ` / 最高: ${record.heart_rate_max} bpm`}
                    </div>
                  )}
                </div>
              </div>
              <div className="text-right">
                <span className="font-pixel text-xs text-pixel-muted">
                  {formatTime(record.record_time)}
                </span>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
