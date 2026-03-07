import { useState, useEffect } from 'react';
import { dietAPI } from '../utils/api';

interface DietRecord {
  id: string;
  food: {
    id: string;
    name: string;
    calories: number;
    protein: number;
    carbohydrates: number;
    fat: number;
  };
  meal_type: string;
  weight: number;
  total_calories: number;
  record_time: string;
}

export default function DietRecords() {
  const [records, setRecords] = useState<DietRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const response = await dietAPI.getRecords({ start_date: `${today}T00:00:00`, end_date: `${today}T23:59:59` });
      setRecords(response.data.records);
    } catch (error) {
      console.error('Failed to load diet records:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMealIcon = (mealType: string) => {
    const icons: { [key: string]: string } = {
      'breakfast': '🌅',
      'lunch': '☀️',
      'dinner': '🌙',
      'snack': '🍎',
    };
    return icons[mealType] || '🍽️';
  };

  const getMealName = (mealType: string) => {
    const names: { [key: string]: string } = {
      'breakfast': '早餐',
      'lunch': '午餐',
      'dinner': '晚餐',
      'snack': '加餐',
    };
    return names[mealType] || mealType;
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit',
    });
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
          <div className="text-6xl mb-4">🍽️</div>
          <p className="font-pixel text-pixel-muted">今日暂无饮食记录</p>
          <p className="font-pixel text-sm text-pixel-muted mt-2">
            点击上方按钮添加饮食
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
                  {getMealIcon(record.meal_type)}
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-pixel text-sm text-pixel-accent">
                      {getMealName(record.meal_type)}
                    </span>
                    <span className="font-pixel text-xs text-pixel-muted">
                      {formatTime(record.record_time)}
                    </span>
                  </div>
                  <div className="font-pixel text-base mb-1">
                    {record.food.name}
                  </div>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="font-pixel text-pixel-accent">
                      {record.total_calories} kcal
                    </span>
                    <span className="font-pixel text-pixel-muted">
                      {record.weight}g
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
