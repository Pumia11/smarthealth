import { useState, useEffect } from 'react';
import { healthAPI } from '../utils/api';

interface HealthRecord {
  id: string;
  value: number;
  record_time: string;
  is_abnormal: boolean;
  remark: string;
  indicator: {
    id: string;
    name: string;
    unit: string;
  };
}

export default function HealthRecords() {
  const [records, setRecords] = useState<HealthRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    try {
      const response = await healthAPI.getRecords();
      setRecords(response.data.records);
    } catch (error) {
      console.error('Failed to load records:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
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
          <div className="text-6xl mb-4">📊</div>
          <p className="font-pixel text-pixel-muted">暂无健康记录</p>
          <p className="font-pixel text-sm text-pixel-muted mt-2">
            点击上方按钮开始记录
          </p>
        </div>
      ) : (
        records.map((record) => (
          <div
            key={record.id}
            className={`p-4 bg-pixel-bg border-2 border-pixel-border hover:border-pixel-accent transition-colors ${
              record.is_abnormal ? 'border-pixel-secondary' : ''
            }`}
          >
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-pixel text-sm text-pixel-accent">
                    {record.indicator.name}
                  </span>
                  {record.is_abnormal && (
                    <span className="pixel-tag pixel-tag-danger text-xs">
                      异常
                    </span>
                  )}
                </div>
                <div className="flex items-baseline gap-1">
                  <span
                    className={`font-pixel text-2xl ${
                      record.is_abnormal ? 'text-pixel-secondary' : 'text-pixel-text'
                    }`}
                  >
                    {record.value}
                  </span>
                  <span className="font-pixel text-sm text-pixel-muted">
                    {record.indicator.unit}
                  </span>
                </div>
                {record.remark && (
                  <p className="font-pixel text-xs text-pixel-muted mt-2">
                    {record.remark}
                  </p>
                )}
              </div>
              <div className="text-right">
                <span className="font-pixel text-xs text-pixel-muted">
                  {formatDate(record.record_time)}
                </span>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
