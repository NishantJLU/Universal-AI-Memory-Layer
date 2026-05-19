-- Enable Row Level Security on the memory table
ALTER TABLE memory ENABLE ROW LEVEL SECURITY;

-- Create a policy that restricts access based on project_id
-- This policy assumes that the application sets a session variable 'app.current_project_id'
CREATE POLICY project_isolation_policy ON memory
    FOR ALL
    USING (project_id = current_setting('app.current_project_id', TRUE));

-- Note: The application must run 'SET app.current_project_id = 'your_project_id';' before querying
