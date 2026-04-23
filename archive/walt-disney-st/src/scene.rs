use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Scene {
    pub id: String,
    pub intent: Intent,
    pub narrative_mode: NarrativeMode,
    pub environment: Environment,
    pub structures: Structures,
    pub symbol: Symbol,
    pub traversal: Traversal,
    pub agent: Agent,
    pub aesthetics: Aesthetics,
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Intent {
    pub primary: String,
    pub secondary: String,
    pub constraints: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NarrativeMode {
    pub pacing: String,
    pub sound_profile: SoundProfile,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SoundProfile {
    pub ambient_db: String,
    pub sources: Vec<String>,
    pub prohibited: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Environment {
    pub r#type: String,
    pub time: String,
    pub lighting: Lighting,
    pub visibility: String,
    pub atmosphere: Atmosphere,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Lighting {
    pub global: String,
    pub local: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Atmosphere {
    pub dust: String,
    pub air: String,
    pub motion: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Structures {
    pub scaffolding: Scaffolding,
    pub cranes: Cranes,
    pub barrels: Barrels,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Scaffolding {
    pub density: String,
    pub state: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Cranes {
    pub count: u32,
    pub motion: String,
    pub lights: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Barrels {
    pub placement: String,
    pub purpose: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Symbol {
    pub rust_core: RustCore,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RustCore {
    pub form: String,
    pub state: String,
    pub illumination: String,
    pub meaning: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Traversal {
    pub vehicle: String,
    pub rails: Rails,
    pub speed: String,
    pub interaction: Interaction,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Rails {
    pub condition: String,
    pub curvature: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Interaction {
    pub allowed: Vec<String>,
    pub disallowed: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Agent {
    pub archetype: String,
    pub tone: String,
    pub reference: String,
    pub posture: String,
    pub focus: String,
    pub tools: Vec<String>,
    pub backpack: Backpack,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Backpack {
    pub contents: String,
    pub weight: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Aesthetics {
    pub style: String,
    pub palette: Palette,
    pub texture_density: String,
    pub composition: Composition,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Palette {
    pub primary: Vec<String>,
    pub accents: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Composition {
    pub center_weighted: bool,
    pub negative_space: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Metadata {
    pub abstraction_level: String,
    pub audience: String,
    pub reuse: Reuse,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Reuse {
    pub safe_for: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SceneConfig {
    pub scene: Scene,
}

impl Scene {
    pub fn load_from_file(path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let contents = fs::read_to_string(path)?;
        let config: SceneConfig = serde_yaml::from_str(&contents)?;
        Ok(config.scene)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Intent {
    pub primary: String,
    pub secondary: String,
    pub constraints: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NarrativeMode {
    pub pacing: String,
    pub sound_profile: SoundProfile,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SoundProfile {
    pub ambient_db: String,
    pub sources: Vec<String>,
    pub prohibited: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Environment {
    pub r#type: String,
    pub time: String,
    pub lighting: Lighting,
    pub visibility: String,
    pub atmosphere: Atmosphere,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Lighting {
    pub global: String,
    pub local: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Atmosphere {
    pub dust: String,
    pub air: String,
    pub motion: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Structures {
    pub scaffolding: Scaffolding,
    pub cranes: Cranes,
    pub barrels: Barrels,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Scaffolding {
    pub density: String,
    pub state: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Cranes {
    pub count: u32,
    pub motion: String,
    pub lights: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Barrels {
    pub placement: String,
    pub purpose: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Symbol {
    pub rust_core: RustCore,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RustCore {
    pub form: String,
    pub state: String,
    pub illumination: String,
    pub meaning: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Traversal {
    pub vehicle: String,
    pub rails: Rails,
    pub speed: String,
    pub interaction: Interaction,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Rails {
    pub condition: String,
    pub curvature: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Interaction {
    pub allowed: Vec<String>,
    pub disallowed: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Agent {
    pub archetype: String,
    pub tone: String,
    pub reference: String,
    pub posture: String,
    pub focus: String,
    pub tools: Vec<String>,
    pub backpack: Backpack,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Backpack {
    pub contents: String,
    pub weight: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Aesthetics {
    pub style: String,
    pub palette: Palette,
    pub texture_density: String,
    pub composition: Composition,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Palette {
    pub primary: Vec<String>,
    pub accents: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Composition {
    pub center_weighted: bool,
    pub negative_space: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Metadata {
    pub abstraction_level: String,
    pub audience: String,
    pub reuse: Reuse,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Reuse {
    pub safe_for: Vec<String>,
}
