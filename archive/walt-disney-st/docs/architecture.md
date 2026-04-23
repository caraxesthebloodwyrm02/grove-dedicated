# Architecture Diagrams

This document contains three architecture diagrams that illustrate different aspects of the Python→Rust contract pipeline.

## Diagram 1: Code-Accurate Pipeline (Artifact Contract Mode)

This diagram shows the complete pipeline flow from Python AST parsing through validation to Rust execution.

```mermaid
flowchart TD
    subgraph contract["Contract Surface"]
        pyDataclasses["Python dataclasses<br/>artifact_generator.py<br/>FunctionArtifact/ClassArtifact/ModuleArtifact"]
        rustStructs["Rust structs<br/>rust/grid-core/src/lib.rs<br/>serde Serialize/Deserialize"]
        pyDataclasses -->|"defines contract"| rustStructs
    end

    subgraph orchestration["Orchestration"]
        shellScript["run_pipeline.sh<br/>ARTIFACT, RUST_FILE, RUST_ROOT,<br/>BIN, MODE, SKIP_RUN"]
        pyBridge["application_bridge.py<br/>--artifact --rust-file --bin --skip-run"]
        shellScript -->|"invokes"| pyBridge
    end

    subgraph tooling["Python Tooling"]
        artifactGen["artifact_generator.py<br/>AST to ModuleArtifact/ClassArtifact/FunctionArtifact"]
        schemaVal["schema_validator.py<br/>handwritten structural checks<br/>OR jsonschema validation"]
        typeVal["type_validator.py<br/>field-name matching<br/>Python vs Rust structs"]
        toolchainVal["toolchain_validator.py<br/>rustc/cargo availability"]
        buildVal["build_validator.py<br/>cargo build"]
        runtimeExec["runtime_executor.py<br/>cargo run --bin ..."]

        pyBridge --> artifactGen
        artifactGen -->|"generates"| pyDataclasses
        pyBridge --> schemaVal
        pyBridge --> typeVal
        pyDataclasses --> typeVal
        rustStructs --> typeVal
        typeVal --> toolchainVal
        toolchainVal --> buildVal
        buildVal --> runtimeExec
    end

    artifactJson["artifact.json<br/>artifact_version + modules array"]
    pyDataclasses -->|"serializes to"| artifactJson
    artifactJson -->|"deserializes from"| rustStructs
    artifactJson --> schemaVal

    runtimeExec -->|"executes"| rustApp["rust/my-app<br/>reads artifact.json<br/>deserializes & processes"]
    artifactJson --> rustApp
```

## Diagram 2: Runtime Consumption Loop

This diagram illustrates how the Rust binary consumes the artifact and produces outputs.

```mermaid
flowchart LR
    artifactJson["artifact.json"] -->|"read file"| serdeParse["serde_json::from_str"]
    serdeParse -->|"deserialize"| moduleArtifact["grid-core::ModuleArtifact"]
    moduleArtifact -->|"process"| businessLogic["Business logic in my-app<br/>metrics, analysis,<br/>codegen, policy checks"]
    businessLogic -->|"emit"| outputs["Outputs<br/>report, diffs, generated<br/>code, CI annotations"]
```

## Diagram 3: Continuous Groundedness Loop

This diagram shows the feedback loop between claims/guarantees and reality/evidence, ensuring continuous validation.

```mermaid
flowchart TD
    subgraph claims["Claims/Guarantees"]
        contract["Contract: dataclasses + Rust structs"]
        validators["Validators + tests<br/>schema/type/build/run"]
        benchmarks["Benchmarks/perf sweeps<br/>perf/run_sweep.*"]

        contract --> validators
        contract --> benchmarks
    end

    subgraph reality["Reality/Evidence"]
        sourceCode["Source code + commits"]
        runtimeOutputs["Observed runtime outputs<br/>cargo run, perf sweeps"]
        ciLogs["CI logs + artifacts"]

        sourceCode --> runtimeOutputs
        runtimeOutputs --> ciLogs
    end

    validators -->|"validates"| ciLogs
    benchmarks -->|"produces"| runtimeOutputs
    sourceCode -->|"implements"| contract
    runtimeOutputs -->|"feedback"| sourceCode
    ciLogs -->|"feedback"| sourceCode
```

## Key Concepts

### Contract Surface
The contract is defined by:
- **Python dataclasses** in `artifact_generator.py` (source of truth for structure)
- **Rust structs** in `rust/grid-core/src/lib.rs` (must match Python structure)
- **artifact.json** is the wire format (serialized from Python, deserialized by Rust)

### Validation Pipeline
1. **Schema validation**: Ensures JSON structure matches expected format
2. **Type validation**: Ensures Python and Rust field names match
3. **Toolchain validation**: Ensures Rust toolchain is available
4. **Build validation**: Ensures Rust code compiles
5. **Runtime validation**: Ensures Rust binary can execute and process artifacts

### Continuous Groundedness
Every claim about interoperability is backed by:
- An artifact (artifact.json)
- A validator (schema/type/build/run checks)
- Reproducible evidence (CI logs, build outputs)

This ensures that the contract remains valid as the codebase evolves.

