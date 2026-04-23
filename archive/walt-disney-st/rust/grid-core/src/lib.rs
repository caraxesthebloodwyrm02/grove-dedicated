use serde::{Deserialize, Serialize};

/// Represents a function artifact as produced by the Python generator.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FunctionArtifact {
    pub name: String,
    pub lineno: usize,
    pub args: usize,
    pub has_doc: bool,
    pub is_async: bool,
}

/// Represents a class artifact with its methods.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ClassArtifact {
    pub name: String,
    pub lineno: usize,
    pub bases: Vec<String>,
    pub has_doc: bool,
    pub methods: Vec<FunctionArtifact>,
}

/// Top-level module artifact structure.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ModuleArtifact {
    pub path: String,
    pub has_doc: bool,
    pub imports: Vec<String>,
    pub total_lines: usize,
    pub functions: Vec<FunctionArtifact>,
    pub classes: Vec<ClassArtifact>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn roundtrip_module_artifact() {
        let artifact = ModuleArtifact {
            path: "example.py".into(),
            has_doc: true,
            imports: vec!["import os".into()],
            total_lines: 10,
            functions: vec![FunctionArtifact {
                name: "foo".into(),
                lineno: 1,
                args: 0,
                has_doc: false,
                is_async: false,
            }],
            classes: vec![ClassArtifact {
                name: "Bar".into(),
                lineno: 5,
                bases: vec!["object".into()],
                has_doc: true,
                methods: vec![],
            }],
        };

        let serialized = serde_json::to_string(&artifact).unwrap();
        let deserialized: ModuleArtifact = serde_json::from_str(&serialized).unwrap();
        assert_eq!(artifact, deserialized);
    }

    #[test]
    fn function_defaults_are_retained() {
        let fn_artifact = FunctionArtifact {
            name: "compute".into(),
            lineno: 10,
            args: 2,
            has_doc: true,
            is_async: false,
        };
        assert_eq!(fn_artifact.name, "compute");
        assert!(!fn_artifact.is_async);
        assert!(fn_artifact.has_doc);
    }

    #[test]
    fn class_with_methods_serializes() {
        let class = ClassArtifact {
            name: "Worker".into(),
            lineno: 20,
            bases: vec!["Base".into()],
            has_doc: false,
            methods: vec![FunctionArtifact {
                name: "run".into(),
                lineno: 21,
                args: 1,
                has_doc: false,
                is_async: true,
            }],
        };

        let json = serde_json::to_string(&class).unwrap();
        let back: ClassArtifact = serde_json::from_str(&json).unwrap();
        assert_eq!(class, back);
        assert_eq!(back.methods[0].name, "run");
        assert!(back.methods[0].is_async);
    }
}
