//! Cognitive test binary for validating cognitive types and calculating metrics

use grid_cognitive::*;
use std::env;

fn main() {
    println!("Cognitive Rust Test");

    // Test cognitive state creation
    let state = CognitiveState {
        load_estimate: 0.75,
        load_type: CognitiveLoadType::Intrinsic,
        working_memory_usage: 0.8,
        processing_mode: ProcessingMode::System2,
        mode_confidence: 0.9,
        mental_model_alignment: 0.85,
        decision_complexity: 0.6,
        time_pressure: 0.3,
    };

    println!("Cognitive State: load={}, mode={:?}", state.load_estimate, state.processing_mode);

    // Test user profile
    let profile = UserCognitiveProfile {
        user_id: "test_user".to_string(),
        username: Some("Test User".to_string()),
        expertise_level: ExpertiseLevel::Intermediate,
        working_memory_capacity: 0.7,
        decision_style: DecisionStyle::Balanced,
        satisficing_tendency: 0.6,
        risk_tolerance: 0.5,
        cognitive_load_tolerance: 0.6,
    };

    println!("User Profile: expertise={:?}, capacity={}", profile.expertise_level, profile.working_memory_capacity);

    // Test metrics
    let metrics = CognitiveMetrics::new(
        0.75,
        0.85,
        0.8,
        QuantizationLevel::Medium,
    );

    println!("Cognitive Metrics: load={}, decision={}, alignment={}, level={:?}",
             metrics.load_score,
             metrics.decision_quality,
             metrics.alignment_score,
             metrics.quantized_level);

    // Check if artifact file path is provided
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 {
        let artifact_path = &args[1];
        println!("Artifact path provided: {}", artifact_path);
        // Here you would load and validate artifacts
    }

    println!("Test completed successfully");
}
