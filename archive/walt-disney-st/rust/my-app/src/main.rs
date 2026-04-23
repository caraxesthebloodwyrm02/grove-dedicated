use clap::Parser;
use grid_report::{load_artifact, generate_report};
use serde_json;
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "my-app")]
#[command(about = "Process artifact.json and generate analysis report")]
struct Args {
    /// Path to artifact.json file
    #[arg(long, default_value = "../artifact.json")]
    artifact: PathBuf,

    /// Output report as JSON
    #[arg(long)]
    json: bool,
}

fn main() {
    let args = Args::parse();

    // Resolve workspace root (rust/) once to avoid borrowing temporaries.
    let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let workspace_root = manifest_dir
        .parent()
        .and_then(|p| p.parent())
        .map(PathBuf::from)
        .expect("Workspace root (rust/) should exist");

    // Read and deserialize artifact.json
    // Check environment variable first (set by runtime_executor.py)
    let artifact_path = if let Ok(env_path) = std::env::var("ARTIFACT_PATH") {
        let env_path_buf = PathBuf::from(env_path);
        if env_path_buf.is_absolute() {
            env_path_buf
        } else {
            // Resolve relative to workspace root (rust/)
            workspace_root.join(env_path_buf)
        }
    } else if args.artifact.is_absolute() {
        args.artifact.clone()
    } else {
        // Resolve relative to workspace root (rust/)
        workspace_root.join(&args.artifact)
    };

    // Load artifact using library function
    let modules = match load_artifact(&artifact_path) {
        Ok(m) => m,
        Err(e) => {
            eprintln!("Error loading artifact from {:?}: {}", artifact_path, e);
            std::process::exit(1);
        }
    };

    // Generate report using library function
    let report = generate_report(&modules);

    // Output report
    if args.json {
        match serde_json::to_string_pretty(&report) {
            Ok(json) => println!("{}", json),
            Err(e) => {
                eprintln!("Error serializing report to JSON: {}", e);
                std::process::exit(1);
            }
        }
    } else {
        print_human_readable_report(&report, &modules);
    }
}

fn print_human_readable_report(report: &grid_report::Report, _modules: &[grid_core::ModuleArtifact]) {
    println!("Artifact Analysis Report");
    println!("{}", "=".repeat(50));
    println!();

    println!("Summary:");
    println!("  Total modules: {}", report.total_modules);
    println!("  Total functions: {}", report.total_functions);
    println!("  Total classes: {}", report.total_classes);
    println!("  Total methods: {}", report.total_methods);
    println!();

    println!("Docstring Coverage:");
    println!("  Modules: {}/{} with docs ({:.1}%)",
        report.docstring_coverage.modules_with_docs,
        report.total_modules,
        if report.total_modules > 0 {
            (report.docstring_coverage.modules_with_docs as f64 / report.total_modules as f64) * 100.0
        } else { 0.0 }
    );
    println!("  Functions: {}/{} with docs ({:.1}%)",
        report.docstring_coverage.functions_with_docs,
        report.total_functions,
        if report.total_functions > 0 {
            (report.docstring_coverage.functions_with_docs as f64 / report.total_functions as f64) * 100.0
        } else { 0.0 }
    );
    println!("  Classes: {}/{} with docs ({:.1}%)",
        report.docstring_coverage.classes_with_docs,
        report.total_classes,
        if report.total_classes > 0 {
            (report.docstring_coverage.classes_with_docs as f64 / report.total_classes as f64) * 100.0
        } else { 0.0 }
    );
    println!("  Methods: {}/{} with docs ({:.1}%)",
        report.docstring_coverage.methods_with_docs,
        report.total_methods,
        if report.total_methods > 0 {
            (report.docstring_coverage.methods_with_docs as f64 / report.total_methods as f64) * 100.0
        } else { 0.0 }
    );
    println!("  Overall coverage: {:.1}%", report.docstring_coverage.overall_coverage_percent);
    println!();

    println!("Import Summary:");
    println!("  Unique imports: {}", report.import_summary.unique_imports);
    if !report.import_summary.most_common_imports.is_empty() {
        println!("  Most common imports:");
        for (import, count) in &report.import_summary.most_common_imports {
            println!("    {} (used {} times)", import, count);
        }
    }
    println!();

    if !report.class_method_counts.is_empty() {
        println!("Classes by Method Count:");
        let mut sorted_classes = report.class_method_counts.clone();
        sorted_classes.sort_by(|a, b| b.method_count.cmp(&a.method_count));
        for class_info in sorted_classes.iter().take(10) {
            println!("  {} ({} methods) - {}",
                class_info.class_name,
                class_info.method_count,
                class_info.module_path
            );
        }
    }
}
