-- Run this in Supabase SQL Editor to add the payslip history table

CREATE TABLE IF NOT EXISTS payslip_history (
    id SERIAL PRIMARY KEY,
    calculated_at TIMESTAMPTZ DEFAULT NOW(),
    employment_type TEXT NOT NULL,
    hourly_rate FLOAT NOT NULL,
    total_hours FLOAT NOT NULL,
    overtime_hours FLOAT NOT NULL DEFAULT 0,
    total_pay FLOAT NOT NULL,
    shifts_data JSONB NOT NULL DEFAULT '[]'
);
