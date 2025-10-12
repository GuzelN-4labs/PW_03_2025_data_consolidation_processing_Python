-- Создание базы данных для анализа освоенного бюджета каждой партнерской компании
-- Задание 16: Партнеры, Проекты, Бюджет, процент выполнения работ - расчет освоенного бюджета для каждого партнера

-- Таблица партнерских компаний
CREATE TABLE IF NOT EXISTS partners (
    partner_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Таблица проектов 
CREATE TABLE IF NOT EXISTS projects (
    project_id SERIAL PRIMARY KEY,
    partner_id INTEGER REFERENCES partners(partner_id),
    project_type VARCHAR(20) NOT NULL,
    budget INTEGER  CHECK (passengers_count >= 0)
);

-- Таблица уровня выполнения работ
CREATE TABLE IF NOT EXISTS completion (
    project_id SERIAL PRIMARY KEY REFERENCES projects(project_id),
    completion_percent DECIMAL (10,2) CHECK (completion_percent>=0)
);

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_partners_partner_id ON partners(partner_id);
CREATE INDEX IF NOT EXISTS idx_projects_project_id ON projects(project_id);
CREATE INDEX IF NOT EXISTS idx_projects_partner_id ON projects(partner_id);
CREATE INDEX IF NOT EXISTS idx_completion_project_id ON completion(project_id);

-- Представление для расчета выручки авиакомпаний
CREATE OR REPLACE VIEW budget_execution AS
SELECT 
    p.partner_id,
    p.name AS partner_name,
    COUNT(DISTINCT pr.project_id) AS total_projects,
    SUM(pr.budget) AS total_budget,
    SUM(pr.budget * c.completion_percent)/SUM(pr.budget) AS avg_completion_percent,
    SUM(pr.budget * c.completion_percent) AS total_budget_executed
FROM partners p
LEFT JOIN projects pr ON p.partner_id = pr.partner_id
LEFT JOIN completion c ON pr.project_id = c.ptoject_id
GROUP BY a.airline_id, a.name, a.country
ORDER BY avg_completion_percent DESC NULLS LAST;
