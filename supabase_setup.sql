-- Run this in Supabase SQL Editor to add user_id support

-- Add user_id column to all tables
ALTER TABLE portfolio ADD COLUMN IF NOT EXISTS user_id TEXT DEFAULT 'default';
ALTER TABLE savings_goals ADD COLUMN IF NOT EXISTS user_id TEXT DEFAULT 'default';
ALTER TABLE user_settings ADD COLUMN IF NOT EXISTS user_id TEXT DEFAULT 'default';
ALTER TABLE payslip_history ADD COLUMN IF NOT EXISTS user_id TEXT DEFAULT 'default';

-- Update the unique constraint on user_settings to include user_id
-- Drop old constraint first (key was unique before, now key+user_id should be unique)
ALTER TABLE user_settings DROP CONSTRAINT IF EXISTS user_settings_key_key;
ALTER TABLE user_settings ADD CONSTRAINT user_settings_key_user_id_unique UNIQUE (key, user_id);
