//! Grid Cognitive - Rust type definitions for cognitive layer integration

use serde::{Deserialize, Serialize};

/// Processing mode (System 1 or System 2)
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ProcessingMode {
    #[serde(rename = "system_1")]
    System1, // Fast, automatic, intuitive
    #[serde(rename = "system_2")]
    System2, // Slow, deliberate, analytical
}

/// Cognitive load type
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum CognitiveLoadType {
    #[serde(rename = "intrinsic")]
    Intrinsic, // Inherent difficulty
    #[serde(rename = "extrinsic")]
    Extrinsic, // Poor design
    #[serde(rename = "germane")]
    Germane, // Schema construction
}

/// Cognitive state representation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CognitiveState {
    pub load_estimate: f64,
    pub load_type: CognitiveLoadType,
    pub working_memory_usage: f64,
    pub processing_mode: ProcessingMode,
    pub mode_confidence: f64,
    pub mental_model_alignment: f64,
    pub decision_complexity: f64,
    pub time_pressure: f64,
}

/// Expertise level
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ExpertiseLevel {
    #[serde(rename = "novice")]
    Novice,
    #[serde(rename = "beginner")]
    Beginner,
    #[serde(rename = "intermediate")]
    Intermediate,
    #[serde(rename = "advanced")]
    Advanced,
    #[serde(rename = "expert")]
    Expert,
}

/// Decision style
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum DecisionStyle {
    #[serde(rename = "quick")]
    Quick,
    #[serde(rename = "deliberate")]
    Deliberate,
    #[serde(rename = "balanced")]
    Balanced,
    #[serde(rename = "risk_averse")]
    RiskAverse,
    #[serde(rename = "risk_taking")]
    RiskTaking,
}

/// User cognitive profile
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserCognitiveProfile {
    pub user_id: String,
    pub username: Option<String>,
    pub expertise_level: ExpertiseLevel,
    pub working_memory_capacity: f64,
    pub decision_style: DecisionStyle,
    pub satisficing_tendency: f64,
    pub risk_tolerance: f64,
    pub cognitive_load_tolerance: f64,
}

/// Decision type
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum DecisionType {
    #[serde(rename = "routine")]
    Routine,
    #[serde(rename = "strategic")]
    Strategic,
    #[serde(rename = "tactical")]
    Tactical,
    #[serde(rename = "exploratory")]
    Exploratory,
}

/// Decision urgency
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum DecisionUrgency {
    #[serde(rename = "low")]
    Low,
    #[serde(rename = "medium")]
    Medium,
    #[serde(rename = "high")]
    High,
    #[serde(rename = "critical")]
    Critical,
}

/// Decision context
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DecisionContext {
    pub decision_id: String,
    pub decision_type: DecisionType,
    pub description: String,
    pub urgency: DecisionUrgency,
    pub complexity: f64,
    pub familiarity: f64,
    pub stakes: f64,
    pub time_constraint: Option<f64>,
    pub information_available: f64,
    pub satisficing_threshold: f64,
    pub max_search_depth: Option<usize>,
}

/// Quantization level
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum QuantizationLevel {
    #[serde(rename = "coarse")]
    Coarse,
    #[serde(rename = "medium")]
    Medium,
    #[serde(rename = "fine")]
    Fine,
    #[serde(rename = "ultra_fine")]
    UltraFine,
}

/// Cognitive metrics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CognitiveMetrics {
    pub load_score: f64,
    pub decision_quality: f64,
    pub alignment_score: f64,
    pub quantized_level: QuantizationLevel,
}

impl CognitiveMetrics {
    /// Create new cognitive metrics
    pub fn new(load_score: f64, decision_quality: f64, alignment_score: f64, quantized_level: QuantizationLevel) -> Self {
        Self {
            load_score,
            decision_quality,
            alignment_score,
            quantized_level,
        }
    }
}
