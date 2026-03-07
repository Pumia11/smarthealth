import { useState } from 'react';
import { useAuthStore } from '../stores/authStore';
import { authAPI } from '../utils/api';
import { useNavigate } from 'react-router-dom';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const login = useAuthStore((state) => state.login);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login({ email, password });
      const { user, access_token } = response.data;
      login(user, access_token);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.error || '登录失败，请检查邮箱和密码');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block font-pixel text-sm text-pixel-text mb-2">
          邮箱
        </label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-3 font-pixel text-pixel-text bg-pixel-bg border-2 border-pixel-border shadow-pixel-inset focus:outline-none focus:border-pixel-accent placeholder:text-pixel-muted"
          placeholder="请输入邮箱"
          required
        />
      </div>

      <div>
        <label className="block font-pixel text-sm text-pixel-text mb-2">
          密码
        </label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-3 font-pixel text-pixel-text bg-pixel-bg border-2 border-pixel-border shadow-pixel-inset focus:outline-none focus:border-pixel-accent placeholder:text-pixel-muted"
          placeholder="请输入密码"
          required
        />
      </div>

      {error && (
        <div className="p-3 bg-pixel-secondary/20 border-2 border-pixel-secondary font-pixel text-sm text-pixel-secondary">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full px-6 py-3 font-pixel text-pixel-text bg-pixel-primary border-2 border-pixel-border shadow-pixel transition-all duration-100 cursor-pointer hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-pixel-lg active:translate-x-[2px] active:translate-y-[2px] active:shadow-pixel-sm disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-x-0 disabled:hover:translate-y-0 disabled:hover:shadow-pixel"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="animate-pixel-pulse">●</span>
            <span>登录中...</span>
          </span>
        ) : (
          '登录'
        )}
      </button>
    </form>
  );
}
