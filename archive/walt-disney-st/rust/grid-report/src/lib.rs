use grid_core::ModuleArtifact;
use serde::Serialize;
use std::collections::HashMap;
use std::fs;
use std::path::Path;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("JSON deserialization error: {0}")]
    Json(#[from] serde_json::Error),
    #[error("Invalid artifact format")]
    InvalidFormat,
}

#[derive(Serialize)]
pub struct Report {
    pub total_modules: usize,
    pub total_functions: usize,
    pub total_classes: usize,
    pub total_methods: usize,
    pub docstring_coverage: DocstringStats,
    pub import_summary: ImportSummary,
    pub class_method_counts: Vec<ClassMethodCount>,
}

#[derive(Serialize)]
pub struct DocstringStats {
    pub modules_with_docs: usize,
    pub modules_without_docs: usize,
    pub functions_with_docs: usize,
    pub functions_without_docs: usize,
    pub classes_with_docs: usize,
    pub classes_without_docs: usize,
    pub methods_with_docs: usize,
    pub methods_without_docs: usize,
    pub overall_coverage_percent: f64,
}

#[derive(Serialize)]
pub struct ImportSummary {
    pub unique_imports: usize,
    pub most_common_imports: Vec<(String, usize)>,
}

#[derive(Serialize, Clone)]
pub struct ClassMethodCount {
    pub class_name: String,
    pub module_path: String,
    pub method_count: usize,
}

/// Load artifact from file, supporting both legacy array format and new object format.
pub fn load_artifact(path: &Path) -> Result<Vec<ModuleArtifact>, Error> {
    let content = fs::read_to_string(path)?;

    let json_value: serde_json::Value = serde_json::from_str(&content)?;

    // Handle both legacy array format and new format with artifact_version
    if let Some(obj) = json_value.as_object() {
        if obj.contains_key("artifact_version") && obj.contains_key("modules") {
            // New format: extract modules array
            if let Some(modules_value) = obj.get("modules") {
                let modules: Vec<ModuleArtifact> = serde_json::from_value(modules_value.clone())?;
                Ok(modules)
            } else {
                Err(Error::InvalidFormat)
            }
        } else {
            // Try to deserialize entire object as array (shouldn't happen, but handle gracefully)
            Err(Error::InvalidFormat)
        }
    } else if json_value.is_array() {
        // Legacy array format
        let modules: Vec<ModuleArtifact> = serde_json::from_value(json_value)?;
        Ok(modules)
    } else {
        Err(Error::InvalidFormat)
    }
}

/// Generate report from modules.
pub fn generate_report(modules: &[ModuleArtifact]) -> Report {
    let total_modules = modules.len();
    let mut total_functions = 0;
    let mut total_classes = 0;
    let mut total_methods = 0;

    let mut modules_with_docs = 0;
    let mut modules_without_docs = 0;
    let mut functions_with_docs = 0;
    let mut functions_without_docs = 0;
    let mut classes_with_docs = 0;
    let mut classes_without_docs = 0;
    let mut methods_with_docs = 0;
    let mut methods_without_docs = 0;

    let mut import_counts: HashMap<String, usize> = HashMap::new();
    let mut class_method_counts = Vec::new();

    for module in modules {
        // Module docstring stats
        if module.has_doc {
            modules_with_docs += 1;
        } else {
            modules_without_docs += 1;
        }

        // Count imports
        for import in &module.imports {
            *import_counts.entry(import.clone()).or_insert(0) += 1;
        }

        // Function stats
        total_functions += module.functions.len();
        for func in &module.functions {
            if func.has_doc {
                functions_with_docs += 1;
            } else {
                functions_without_docs += 1;
            }
        }

        // Class stats
        total_classes += module.classes.len();
        for class in &module.classes {
            if class.has_doc {
                classes_with_docs += 1;
            } else {
                classes_without_docs += 1;
            }

            // Method stats
            total_methods += class.methods.len();
            for method in &class.methods {
                if method.has_doc {
                    methods_with_docs += 1;
                } else {
                    methods_without_docs += 1;
                }
            }

            class_method_counts.push(ClassMethodCount {
                class_name: class.name.clone(),
                module_path: module.path.clone(),
                method_count: class.methods.len(),
            });
        }
    }

    // Calculate overall docstring coverage
    let total_docstring_opportunities = total_modules
        + total_functions
        + total_classes
        + total_methods;
    let total_with_docs = modules_with_docs
        + functions_with_docs
        + classes_with_docs
        + methods_with_docs;
    let overall_coverage_percent = if total_docstring_opportunities > 0 {
        (total_with_docs as f64 / total_docstring_opportunities as f64) * 100.0
    } else {
        0.0
    };

    // Get most common imports
    let unique_imports_count = import_counts.len();
    let mut import_vec: Vec<(String, usize)> = import_counts.into_iter().collect();
    import_vec.sort_by(|a, b| b.1.cmp(&a.1));
    let most_common_imports = import_vec.into_iter().take(10).collect();

    Report {
        total_modules,
        total_functions,
        total_classes,
        total_methods,
        docstring_coverage: DocstringStats {
            modules_with_docs,
            modules_without_docs,
            functions_with_docs,
            functions_without_docs,
            classes_with_docs,
            classes_without_docs,
            methods_with_docs,
            methods_without_docs,
            overall_coverage_percent,
        },
        import_summary: ImportSummary {
            unique_imports: unique_imports_count,
            most_common_imports,
        },
        class_method_counts,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use grid_core::{ClassArtifact, FunctionArtifact, ModuleArtifact};

    #[test]
    fn test_load_artifact_new_format() {
        let test_json = r#"{
            "artifact_version": "1.0",
            "modules": [
                {
                    "path": "test.py",
                    "has_doc": true,
                    "imports": ["import os"],
                    "total_lines": 10,
                    "functions": [],
                    "classes": []
                }
            ]
        }"#;

        let temp_file = std::env::temp_dir().join("test_artifact.json");
        fs::write(&temp_file, test_json).unwrap();

        let result = load_artifact(&temp_file);
        assert!(result.is_ok());
        let modules = result.unwrap();
        assert_eq!(modules.len(), 1);
        assert_eq!(modules[0].path, "test.py");

        fs::remove_file(&temp_file).ok();
    }

    #[test]
    fn test_load_artifact_legacy_format() {
        let test_json = r#"[
            {
                "path": "test.py",
                "has_doc": true,
                "imports": ["import os"],
                "total_lines": 10,
                "functions": [],
                "classes": []
            }
        ]"#;

        let temp_file = std::env::temp_dir().join("test_artifact_legacy.json");
        fs::write(&temp_file, test_json).unwrap();

        let result = load_artifact(&temp_file);
        assert!(result.is_ok());
        let modules = result.unwrap();
        assert_eq!(modules.len(), 1);

        fs::remove_file(&temp_file).ok();
    }

    #[test]
    fn test_generate_report() {
        let modules = vec![
            ModuleArtifact {
                path: "test.py".into(),
                has_doc: true,
                imports: vec!["import os".into()],
                total_lines: 10,
                functions: vec![
                    FunctionArtifact {
                        name: "foo".into(),
                        lineno: 1,
                        args: 0,
                        has_doc: true,
                        is_async: false,
                    }
                ],
                classes: vec![
                    ClassArtifact {
                        name: "Bar".into(),
                        lineno: 5,
                        bases: vec![],
                        has_doc: false,
                        methods: vec![],
                    }
                ],
            }
        ];

        let report = generate_report(&modules);
        assert_eq!(report.total_modules, 1);
        assert_eq!(report.total_functions, 1);
        assert_eq!(report.total_classes, 1);
        assert_eq!(report.docstring_coverage.modules_with_docs, 1);
        assert_eq!(report.docstring_coverage.functions_with_docs, 1);
        assert_eq!(report.docstring_coverage.classes_with_docs, 0);
    }
}

