-- SmartHealth Database Schema for Supabase
-- Run this SQL in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Profiles Table (extends Supabase auth.users)
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,
    username VARCHAR(50),
    avatar VARCHAR(255),
    gender VARCHAR(10),
    birthday DATE,
    height DECIMAL(5,1),
    weight DECIMAL(5,1),
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Health Indicator Types
CREATE TABLE health_indicator_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(100),
    sort INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Health Indicators
CREATE TABLE health_indicators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    indicator_type_id INTEGER REFERENCES health_indicator_types(id),
    belong_user_id UUID REFERENCES auth.users(id),
    unit VARCHAR(20),
    normal_min DECIMAL(10,2),
    normal_max DECIMAL(10,2),
    threshold_desc VARCHAR(255),
    icon VARCHAR(100),
    is_common BOOLEAN DEFAULT false,
    sort INTEGER DEFAULT 0,
    status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Health Records
CREATE TABLE health_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    indicator_id UUID REFERENCES health_indicators(id) NOT NULL,
    value DECIMAL(10,2) NOT NULL,
    record_time TIMESTAMP WITH TIME ZONE NOT NULL,
    is_abnormal BOOLEAN DEFAULT false,
    remark TEXT,
    source VARCHAR(20) DEFAULT 'manual',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Food Types
CREATE TABLE food_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(100),
    sort INTEGER DEFAULT 0,
    status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Foods
CREATE TABLE foods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    food_type_id INTEGER REFERENCES food_types(id),
    cover_image VARCHAR(255),
    calories DECIMAL(10,2) NOT NULL,
    protein DECIMAL(10,2) DEFAULT 0,
    carbohydrates DECIMAL(10,2) DEFAULT 0,
    fat DECIMAL(10,2) DEFAULT 0,
    dietary_fiber DECIMAL(10,2) DEFAULT 0,
    sugar DECIMAL(10,2) DEFAULT 0,
    sodium DECIMAL(10,2) DEFAULT 0,
    sort INTEGER DEFAULT 0,
    status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Food Units
CREATE TABLE food_units (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    food_id UUID REFERENCES foods(id) ON DELETE CASCADE,
    unit_name VARCHAR(20) NOT NULL,
    unit_weight DECIMAL(10,2) NOT NULL,
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Diet Records
CREATE TABLE diet_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    food_id UUID REFERENCES foods(id) NOT NULL,
    meal_type VARCHAR(20) NOT NULL,
    weight DECIMAL(10,2) NOT NULL,
    total_calories DECIMAL(10,2) NOT NULL,
    total_protein DECIMAL(10,2) DEFAULT 0,
    total_carbs DECIMAL(10,2) DEFAULT 0,
    total_fat DECIMAL(10,2) DEFAULT 0,
    record_time TIMESTAMP WITH TIME ZONE NOT NULL,
    image_url VARCHAR(255),
    remark TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Exercise Types
CREATE TABLE exercise_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(100),
    sort INTEGER DEFAULT 0,
    status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Exercises
CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    exercise_type_id INTEGER REFERENCES exercise_types(id),
    cover_image VARCHAR(255),
    mets DECIMAL(10,2) NOT NULL,
    description TEXT,
    calories_per_hour DECIMAL(10,2),
    sort INTEGER DEFAULT 0,
    status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Exercise Records
CREATE TABLE exercise_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    exercise_id UUID REFERENCES exercises(id) NOT NULL,
    duration INTEGER NOT NULL,
    calories_burned DECIMAL(10,2) NOT NULL,
    record_time TIMESTAMP WITH TIME ZONE NOT NULL,
    heart_rate_avg INTEGER,
    heart_rate_max INTEGER,
    remark TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Article Types
CREATE TABLE article_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(100),
    sort INTEGER DEFAULT 0,
    status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Health Articles
CREATE TABLE health_articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    article_type_id INTEGER REFERENCES article_types(id),
    author_id UUID REFERENCES auth.users(id),
    cover_image VARCHAR(255),
    content TEXT NOT NULL,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    collect_count INTEGER DEFAULT 0,
    publish_status VARCHAR(20) DEFAULT 'draft',
    audit_status VARCHAR(20) DEFAULT 'pending',
    audit_time TIMESTAMP WITH TIME ZONE,
    audit_reply TEXT,
    publish_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Recipes
CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    author_id UUID REFERENCES auth.users(id),
    cover_image VARCHAR(255),
    content TEXT NOT NULL,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    collect_count INTEGER DEFAULT 0,
    publish_status VARCHAR(20) DEFAULT 'draft',
    audit_status VARCHAR(20) DEFAULT 'pending',
    audit_time TIMESTAMP WITH TIME ZONE,
    audit_reply TEXT,
    publish_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Collects
CREATE TABLE user_collects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    collect_type VARCHAR(50) NOT NULL,
    article_id UUID,
    recipe_id UUID REFERENCES recipes(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Likes
CREATE TABLE user_likes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    like_type VARCHAR(50) NOT NULL,
    article_id UUID,
    recipe_id UUID REFERENCES recipes(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Health Reports (AI Analysis)
CREATE TABLE health_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,
    analysis_period_days INTEGER NOT NULL,
    health_score INTEGER,
    risks JSONB,
    nutrition_analysis JSONB,
    exercise_analysis JSONB,
    indicator_analysis JSONB,
    recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Reminder Tasks
CREATE TABLE reminder_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    task_title VARCHAR(100) NOT NULL,
    task_content TEXT,
    task_type VARCHAR(20) NOT NULL,
    remind_type VARCHAR(20) NOT NULL,
    cron_expression VARCHAR(50),
    remind_time TIME NOT NULL,
    repeat_type VARCHAR(20) DEFAULT 'daily',
    is_active BOOLEAN DEFAULT true,
    last_remind_time TIMESTAMP WITH TIME ZONE,
    next_remind_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Message Notices
CREATE TABLE message_notices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create Indexes
CREATE INDEX idx_health_records_user ON health_records(user_id);
CREATE INDEX idx_health_records_indicator ON health_records(indicator_id);
CREATE INDEX idx_health_records_time ON health_records(record_time);

CREATE INDEX idx_diet_records_user ON diet_records(user_id);
CREATE INDEX idx_diet_records_time ON diet_records(record_time);

CREATE INDEX idx_exercise_records_user ON exercise_records(user_id);
CREATE INDEX idx_exercise_records_time ON exercise_records(record_time);

CREATE INDEX idx_health_articles_status ON health_articles(publish_status, audit_status);
CREATE INDEX idx_health_articles_author ON health_articles(author_id);

CREATE INDEX idx_reminder_tasks_user ON reminder_tasks(user_id, is_active);
CREATE INDEX idx_reminder_tasks_next ON reminder_tasks(next_remind_time);

-- Insert Default Data

-- Health Indicator Types
INSERT INTO health_indicator_types (name, icon, sort) VALUES
('血糖指标', '🩸', 1),
('基础体征', '📏', 2),
('血压指标', '❤️', 3),
('血脂指标', '💉', 4),
('心率指标', '💓', 5),
('肝功能', '🫀', 6),
('肾功能', '🫘', 7),
('血常规', '🩸', 8),
('呼吸功能', '💨', 9);

-- Common Health Indicators
INSERT INTO health_indicators (name, indicator_type_id, unit, normal_min, normal_max, is_common, sort) VALUES
('体重', 2, 'kg', 40, 100, true, 1),
('身高', 2, 'cm', 100, 220, true, 2),
('BMI', 2, '', 18.5, 24, true, 3),
('收缩压', 3, 'mmHg', 90, 140, true, 4),
('舒张压', 3, 'mmHg', 60, 90, true, 5),
('心率', 5, 'bpm', 60, 100, true, 6),
('空腹血糖', 1, 'mmol/L', 3.9, 6.1, true, 7),
('餐后血糖', 1, 'mmol/L', 3.9, 7.8, true, 8),
('体温', 2, '℃', 36.0, 37.5, true, 9),
('血氧', 9, '%', 95, 100, true, 10),
('睡眠时长', 2, '小时', 7, 9, true, 11);

-- Food Types
INSERT INTO food_types (name, icon, sort) VALUES
('谷物', '🌾', 1),
('蔬菜', '🥬', 2),
('水果', '🍎', 3),
('肉类', '🥩', 4),
('蛋奶', '🥚', 5),
('豆类', '🫘', 6),
('坚果', '🥜', 7),
('饮品', '🥤', 8);

-- Exercise Types
INSERT INTO exercise_types (name, icon, sort) VALUES
('有氧运动', '🏃', 1),
('无氧运动', '💪', 2),
('柔韧性训练', '🧘', 3),
('平衡训练', '⚖️', 4),
('竞技运动', '⚽', 5);

-- Article Types
INSERT INTO article_types (name, icon, sort) VALUES
('营养饮食', '🥗', 1),
('运动健身', '🏃', 2),
('疾病预防', '🏥', 3),
('心理健康', '🧠', 4),
('睡眠健康', '😴', 5),
('中医养生', '🌿', 6),
('健康资讯', '📰', 7),
('健康食谱', '👨‍🍳', 8);

-- Row Level Security (RLS) Policies
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE diet_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercise_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE reminder_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE message_notices ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_collects ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_likes ENABLE ROW LEVEL SECURITY;

-- User Profiles Policies
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON user_profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Health Records Policies
CREATE POLICY "Users can view own health records" ON health_records
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own health records" ON health_records
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own health records" ON health_records
    FOR DELETE USING (auth.uid() = user_id);

-- Diet Records Policies
CREATE POLICY "Users can view own diet records" ON diet_records
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own diet records" ON diet_records
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own diet records" ON diet_records
    FOR DELETE USING (auth.uid() = user_id);

-- Exercise Records Policies
CREATE POLICY "Users can view own exercise records" ON exercise_records
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own exercise records" ON exercise_records
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own exercise records" ON exercise_records
    FOR DELETE USING (auth.uid() = user_id);

-- Health Reports Policies
CREATE POLICY "Users can view own health reports" ON health_reports
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own health reports" ON health_reports
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Reminder Tasks Policies
CREATE POLICY "Users can view own reminder tasks" ON reminder_tasks
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own reminder tasks" ON reminder_tasks
    FOR ALL USING (auth.uid() = user_id);

-- Message Notices Policies
CREATE POLICY "Users can view own messages" ON message_notices
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own messages" ON message_notices
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own messages" ON message_notices
    FOR UPDATE USING (auth.uid() = user_id);

-- User Collects Policies
CREATE POLICY "Users can view own collects" ON user_collects
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own collects" ON user_collects
    FOR ALL USING (auth.uid() = user_id);

-- User Likes Policies
CREATE POLICY "Users can view own likes" ON user_likes
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own likes" ON user_likes
    FOR ALL USING (auth.uid() = user_id);

-- Create function to handle user creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.user_profiles (user_id, username, avatar)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
        NEW.raw_user_meta_data->>'avatar'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for new user creation
CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
