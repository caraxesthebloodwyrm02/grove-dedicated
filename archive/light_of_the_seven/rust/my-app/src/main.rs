//! Example binary using grid-core types

use grid_core::FunctionArtifact;

fn main() {
    println!("Grid Rust Application");

    // Example usage of grid-core types
    let func = FunctionArtifact {
        name: "example_function".to_string(),
        lineno: 1,
        args: 2,
        has_doc: true,
        is_async: false,
    };

    println!("Function: {} (line {})", func.name, func.lineno);
}
