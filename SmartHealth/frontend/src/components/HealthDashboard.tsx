import { useEffect, useState } from 'react';
import { healthAPI } from '../utils/api';

interface HealthStats {
  [key: string]: {
    latest: number;
    unit: string;
    is_abnormal: boolean;
    record_time: string;
  };
}

export default function HealthDashboard() {
  const [stats, setStats] = useState<HealthStats>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await healthAPI.getStats();
      setStats(response.data.stats);
    } catch (error) {
      console.error('Failed to load health stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const getIndicatorIcon = (name: string) => {
    const icons: { [key: string]: string } = {
      '体重': '⚖️',
      '身高': '📏',
      'BMI': '📊',
      '收缩压': '❤️',
      '舒张压': '💙',
      '心率': '💓',
      '空腹血糖': '🩸',
      '餐后血糖': '🍬',
      '体温': '🌡️',
      '血氧': '💨',
      '睡眠时长': '😴',
    };
    return icons[name] || '📋';
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
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {Object.entries(stats).map(([name, data]) => (
        <div
          key={name}
          className={`p-4 border-2 border-pixel-border shadow-pixel-sm ${
            data.is_abnormal ? 'bg-pixel-secondary/20' : 'bg-pixel-bg'
          }`}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">{getIndicatorIcon(name)}</span>
            <span className="font-pixel text-sm text-pixel-muted">{name}</span>
          </div>
          <div className="flex items-baseline gap-1">
            <span
              className={`font-pixel text-2xl ${
                data.is_abnormal ? 'text-pixel-secondary' : 'text-pixel-accent'
              }`}
            >
              {data.latest}
            </span>
            <span className="font-pixel text-sm text-pixel-muted">{data.unit}</span>
          </div>
          {data.is_abnormal && (
            <div className="mt-2 pixel-tag pixel-tag-danger text-xs">
              异常
            </div>
          )}
        </div>
      ))}
      {Object.keys(stats).length === 0 && (
        <div className="col-span-full text-center py-8">
          <p className="font-pixel text-pixel-muted">暂无健康数据</p>
          <p className="font-pixel text-sm text-pixel-muted mt-2">
            开始记录您的健康指标吧！
          </p>
        </div>
      )}
    </div>
  );
}
