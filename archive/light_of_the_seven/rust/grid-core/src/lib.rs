//! Grid Core - Shared type definitions matching Python contracts

/// Artifact representing a Python function
#[derive(Debug, Clone)]
pub struct FunctionArtifact {
    pub name: String,
    pub lineno: usize,
    pub args: usize,
    pub has_doc: bool,
    pub is_async: bool,
}

/// Artifact representing a Python class
#[derive(Debug, Clone)]
pub struct ClassArtifact {
    pub name: String,
    pub lineno: usize,
    pub bases: Vec<String>,
    pub has_doc: bool,
    pub methods: Vec<FunctionArtifact>,
}

/// Artifact representing a Python module
#[derive(Debug, Clone)]
pub struct ModuleArtifact {
    pub path: String,
    pub has_doc: bool,
    pub imports: Vec<String>,
    pub total_lines: usize,
    pub functions: Vec<FunctionArtifact>,
    pub classes: Vec<ClassArtifact>,
    pub component_type: Option<String>,           // 'schema', 'engine', 'tracker', etc.
    pub cognitive_metrics: std::collections::HashMap<String, f64>, // load, complexity, etc.
    pub dependencies: Vec<String>,                // other cognitive components
}
