# Grid Master Workflow System

> **Unified governance and execution framework for GRID development with integrated guardrails and workflows.**

## System Overview

This master workflow system unifies all GRID development activities under a single governance framework, with rules serving as guardrails that constrain and guide all workflows. The system integrates:

- **Rules Layer**: Canonical governance, exhibit management, sensory layer standards
- **Workflow Layer**: Task execution, reporting, optimization, and development processes
- **Guardrail Enforcement**: Rules automatically applied as constraints on all workflows

---

## Core Principles

### 1. Rule-First Development
All workflows must respect the canonical rules:
- **Canon Policy**: Strict separation between immutable canon (📜) and mutable tooling (🪄)
- **Exhibit Governance**: Museum-style exhibit management with required files and schemas
- **Sensory Layers**: Standardized sound/vision layer definitions and integrations

### 2. Guardrail Enforcement
Rules are automatically enforced through:
- **Schema Validation**: Exhibit manifests, sensory layer schemas
- **Code Analysis**: Canon header requirements, citation discipline
- **Workflow Integration**: All workflows include rule compliance checks

### 3. Unified Execution Model
All development activities follow:
- **Structured Input Processing**: API validation, decision routing, EQ-enhanced processing
- **Action Recommendation Systems**: Test analysis, pattern recognition, task generation
- **Quality Gates**: Automated testing, linting, compliance checks

---

## Guardrails (Rules Layer)

### Primary Rules

#### 1. Canon Policy Guardrails (`grid-canon-policy.md`)
**Scope**: `light_of_the_seven/**`, `docs/**`, `*.md` files

**Enforced Rules**:
- **Two-Layer Architecture**: Canon (🏛️📜) vs Tooling (🪄🧪) separation
- **Citation Discipline**: `[Source, Chapter "Title"]` format required for canon claims
- **Header Requirements**: `NON-CANONICAL` disclaimers for tooling code
- **Immutability**: Canon content cannot be modified without governance approval

**Guardrail Application**:
- All workflows check for proper headers before file modifications
- Citation validation in documentation workflows
- Canon vs tooling classification in exhibit creation

#### 2. Exhibit Governance Guardrails (`grid-exhibit-governance.md`)
**Scope**: `**/visualizations/**`, `**/exhibits/**`

**Enforced Rules**:
- **Required Files**: `exhibit.json`, `README.md` for all exhibits
- **Schema Compliance**: Exhibit manifests must validate against schema
- **Workspace Icons**: 🏛️=Root, 📜=Canon, 🪄=Tools, 🧪=Tests
- **Bridge Requirements**: `grid_bridge.py` for interactive exhibits

**Guardrail Application**:
- Exhibit creation workflows enforce file requirements
- Schema validation integrated into all exhibit operations
- Icon consistency maintained across workspace

#### 3. Sensory Layer Guardrails (`grid-sensory-layers.md`)
**Scope**: `schemas/**`, `circuits/vision/**`, `circuits/sound/**`

**Enforced Rules**:
- **Sound Layer**: Pitch (Hz), Loudness (dB), Timbre (0-1 normalized)
- **Vision Layer**: Nodes (id, label, type), Edges (source, target, relationship)
- **Color Coding**: Supportive=#4CAF50, Neutral=#9E9E9E, Adversarial=#F44336
- **Schema Validation**: All sensory data must conform to defined schemas

**Guardrail Application**:
- Schema validation in data processing workflows
- Color consistency in visualization workflows
- Sound/vision layer separation maintained

---

## Integrated Workflows

### Core Workflows with Guardrails

#### 1. Exhibit Management (`grid-exhibit.md`)
**Guardrails Applied**:
- Canon Policy: Header requirements, citation validation
- Exhibit Governance: File requirements, schema compliance
- Sensory Layers: Proper layer integration

**Execution Phases**:
1. **Validation**: Check all guardrails before creation
2. **Creation**: Enforce required files and schemas
3. **Integration**: Verify sensory layer compliance
4. **Documentation**: Ensure canon policy adherence

#### 2. Repository Organization (`grid-organize.md`)
**Guardrails Applied**:
- Exhibit Governance: Exhibit file organization
- Canon Policy: Documentation classification
- Sensory Layers: Schema file placement

**Execution Phases**:
1. **Analysis**: Semantic file classification with rule awareness
2. **Organization**: Rule-compliant file placement
3. **Validation**: Guardrail verification of new structure
4. **Documentation**: Update organization docs with canon references

#### 3. Performance Optimization (`grid-optimize-performance.md`)
**Guardrails Applied**:
- Sensory Layers: Performance impact on audio/video processing
- Canon Policy: Performance claims must be cited
- Exhibit Governance: Optimization doesn't break exhibit functionality

**Execution Phases**:
1. **Baseline**: Measure current performance with guardrail compliance
2. **Analysis**: Identify bottlenecks respecting sensory layer rules
3. **Optimization**: Apply changes without violating canon policies
4. **Validation**: Verify performance gains and rule compliance

#### 4. Code Quality & Reporting (`grid-report.md`, `grid-grep-unix.md`)
**Guardrails Applied**:
- All rules: Comprehensive compliance checking
- Canon Policy: Report generation follows citation discipline
- Exhibit Governance: Exhibit status reporting
- Sensory Layers: Schema validation reporting

**Execution Phases**:
1. **Health Check**: Repository status with rule compliance
2. **Pattern Analysis**: Code patterns respecting guardrails
3. **Report Generation**: Structured output with canon references
4. **Action Items**: Prioritized tasks following governance rules

#### 5. Task Execution (`grid-run-tasks.md`)
**Guardrails Applied**:
- Canon Policy: Task execution respects tooling boundaries
- Exhibit Governance: Tasks maintain exhibit integrity
- Sensory Layers: Tasks don't violate schema constraints

**Execution Phases**:
1. **Environment Setup**: Virtual environment with rule-compliant paths
2. **Dependency Management**: Package installation respecting constraints
3. **Task Execution**: Run tasks within guardrail boundaries
4. **Validation**: Verify execution didn't violate rules

#### 6. Advanced Git Grep Operations (`grid-grep-unix.md`)
**Guardrails Applied**:
- Canon Policy: Search results respect canon/tooling separation
- Exhibit Governance: Exhibit file searches follow governance rules
- Sensory Layers: Pattern searches maintain schema integrity

**WSL-Enhanced Git Grep Workflow**:

**Core Search Patterns**:
```bash
# Basic pattern search with Unix pipeline
git grep -n "pattern" -- grid/ | sort -t: -k1,1 -k2,2n

# Boolean logic for complex searches
git grep -e "function.*def" --and -e "async" -- "*.py" | head -20

# Function context for better understanding
git grep -W "class.*Model" -- circuits/models/ | less -R

# Search with depth control to avoid OS errors
git grep --max-depth=3 "TODO" -- grid/ tests/
```

**Advanced WSL Integration**:
```bash
# Combine with Unix tools for powerful analysis
git grep -l "import.*pytest" -- tests/ | xargs wc -l | sort -n

# Parallel processing with xargs
git grep -l "def test_" -- tests/ | xargs -P4 -I {} python -m pytest {}

# Process substitution for pattern files
git grep -f <(printf "error\nexception\nfail") -- grid/ --count

# Perl regex for complex patterns
git grep -P "(?<=def\s)\w+(?=\s*\()" -- grid/ | cut -d: -f2 | sort | uniq -c
```

**Safety Scoping**:
```bash
# Avoid problematic paths (memory warning)
git grep "pattern" -- grid/ tests/  # Exclude light_of_the_seven/

# Use pathspecs for precise targeting
git grep "exhibit" -- ':(glob)**/visualizations/**' ':(glob)**/exhibits/**'

# Exclude binary and generated files
git grep --textconv "config" -- ':!*.png' ':!*.min.js'
```

**Execution Phases**:
1. **Pattern Definition**: Create search patterns respecting rule boundaries
2. **Scoped Search**: Execute searches within safe path boundaries
3. **Unix Integration**: Pipe results through Unix toolchain for analysis
4. **Result Validation**: Ensure findings comply with all guardrails

#### 7. Performance-Optimized Analysis (`grid-grep-performance-report.md`)
**Guardrails Applied**:
- Canon Policy: Performance claims must be cited with measured data
- Exhibit Governance: Analysis doesn't disrupt exhibit functionality
- Sensory Layers: Performance metrics respect schema definitions

**Performance Best Practices**:

**1. Use Native Linux Paths for Intensive Analysis**
```bash
# 5.15x faster than /mnt/ paths (measured)
rsync -av --exclude=".git" /mnt/e/grid/ ~/grid/
cd ~/grid && git grep "pattern" -- grid/ tests/

# Path comparison results:
# /mnt/e/grid (Windows): 0.067s baseline
# ~/grid (Linux native): 0.013s (5.15x faster)
```

**2. Always Scope Searches to Safe Directories**
```bash
# REQUIRED: Scope to grid/ and tests/ to avoid OS errors
git grep "pattern" -- grid/ tests/

# AVOID: Full repo search hits problematic paths
# git grep "pattern" -- .  # May cause OS error 1

# Known problematic path:
# light_of_the_seven/full_datakit/visualizations/Hogwarts/great_hall/nul
```

**3. Choose Appropriate Pattern Types**
```bash
# Fixed strings (fastest) - use for literal matches
git grep -F "def __init__" -- "*.py"  # 0.026s

# Extended regex - use for moderate patterns
git grep -E "class\s+\w+Model" -- "*.py"  # 0.036s

# Boolean logic - use for complex multi-pattern searches
git grep -e "async" --and -e "def " -- "*.py"  # 0.234s

# Perl regex - use for advanced lookbehind/lookahead
git grep -P "(?<=def\s)\w+(?=\s*\()" -- "*.py"  # 0.026s
```

**4. Leverage Unix Pipelines for Complex Analysis**
```bash
# Efficient file counting with parallel processing
git grep -l "import" -- grid/ tests/ | xargs -P4 wc -l | sort -n

# Sorted results with line numbers
git grep -n "TODO" -- grid/ tests/ | sort -t: -k1,1 -k2,2n

# Pattern frequency analysis
git grep -c "def test_" -- tests/ | sort -t: -k2 -nr | head -10

# Multi-pattern search with process substitution
git grep -f <(printf "error\nexception\nfail") -- grid/ --count
```

**Performance Metrics Reference**:
| Operation | Execution Time | Use Case |
|-----------|----------------|----------|
| Simple pattern | <0.04s | Quick searches |
| Scoped search | 0.067s | Targeted analysis |
| Boolean logic | 0.234s | Complex patterns |
| Function context | 0.029s | Code understanding |
| Perl regex | 0.026s | Advanced patterns |

**Execution Phases**:
1. **Environment Setup**: Use native Linux paths when possible
2. **Scope Definition**: Define safe search boundaries (grid/, tests/)
3. **Pattern Selection**: Choose optimal pattern type for task
4. **Pipeline Construction**: Build Unix pipelines for analysis
5. **Performance Validation**: Verify execution times meet expectations

---

## Unified Execution Pipeline

### Input Processing Chain

```
Raw Input → API Validation → Decision Routing → EQ Processing → Task Generation
    ↓           ↓              ↓             ↓              ↓
Guardrails → Sanitization → Rule Checking → Compliance → Action Validation
```

### Guardrail Integration Points

1. **Input Validation**: All inputs checked against canon policy and exhibit rules
2. **Processing**: Sensory layer schemas enforced during data processing
3. **Output Generation**: Results validated for canon compliance and proper citations
4. **Task Creation**: Generated tasks respect exhibit governance and tooling boundaries

---

## Quality Gates & Enforcement

### Automated Gates

#### Pre-Commit Hooks
- **Canon Headers**: Check for NON-CANONICAL headers in new files
- **Schema Validation**: Validate exhibit manifests and sensory schemas
- **Citation Check**: Verify citations in documentation changes

#### CI/CD Integration
- **Rule Compliance**: Automated checking of all guardrails
- **Exhibit Validation**: Schema validation for all exhibit changes
- **Sensory Testing**: Sound/vision layer integration tests

#### Development Workflow
- **VS Code Integration**: Editor shows rule violations inline
- **Workflow Guards**: All workflows include guardrail checks
- **Review Requirements**: Human verification for canon changes

### Manual Enforcement

#### Code Reviews
- **Canon Claims**: Verify citations and header requirements
- **Exhibit Changes**: Check governance compliance
- **Sensory Modifications**: Validate against layer schemas

#### Periodic Audits
- **Full Compliance Scan**: Monthly comprehensive rule checking
- **Documentation Review**: Quarterly canon content validation
- **Exhibit Inventory**: Regular exhibit status and compliance review

---

## Error Handling & Recovery

### Guardrail Violations

#### Detection
- **Schema Errors**: Invalid exhibit manifests or sensory data
- **Header Missing**: NON-CANONICAL headers not present in tooling
- **Citation Issues**: Missing or malformed citations in canon content

#### Recovery Procedures
1. **Automatic Fixes**: Scripts to add missing headers or fix common issues
2. **Manual Correction**: Developer fixes for complex violations
3. **Governance Review**: Escalation for canon policy violations

### Workflow Failures

#### Common Issues
- **Rule Conflicts**: Workflows attempting operations that violate guardrails
- **Dependency Issues**: Changes that break exhibit or sensory dependencies
- **Documentation Gaps**: Missing canon references or header requirements

#### Recovery Strategies
1. **Rule Consultation**: Reference specific rule files for clarification
2. **Workflow Adjustment**: Modify workflow to comply with guardrails
3. **Escalation**: Governance review for blocking issues

---

## Monitoring & Continuous Improvement

### Metrics Tracking

#### Compliance Metrics
- **Header Coverage**: Percentage of files with correct NON-CANONICAL headers
- **Schema Compliance**: Pass rate for exhibit and sensory schema validation
- **Citation Accuracy**: Percentage of canon claims with proper citations

#### Process Metrics
- **Workflow Success**: Percentage of workflows completing without guardrail violations
- **Review Cycle Time**: Time from workflow completion to governance approval
- **Error Recovery**: Time to resolve guardrail violations

### Feedback Loops

#### Workflow Improvement
- **Violation Analysis**: Review common guardrail violations to improve workflows
- **Rule Updates**: Update rules based on practical development needs
- **Automation Opportunities**: Identify areas for automated guardrail enforcement

#### Team Learning
- **Training Updates**: Update developer training based on common violations
- **Documentation Enhancement**: Improve rule documentation based on confusion areas
- **Tool Integration**: Enhance IDE and workflow tool integration

---

## Emergency Procedures

### Guardrail Bypass (Restricted)
**Conditions**: Only for critical production issues where guardrails prevent necessary fixes

**Procedure**:
1. **Governance Approval**: Obtain explicit approval from project maintainers
2. **Temporary Bypass**: Document specific guardrails to bypass and duration
3. **Immediate Fix**: Apply necessary changes with minimal scope
4. **Post-Mortem**: Review incident and update guardrails if needed

### System Recovery
**Conditions**: Guardrail system itself fails or causes development blockage

**Procedure**:
1. **Manual Override**: Temporarily disable problematic guardrails
2. **Root Cause Analysis**: Identify why guardrails caused issues
3. **System Update**: Fix guardrail implementation or update rules
4. **Validation**: Test updated system before re-enabling

---

## Integration with AI Development

### Cascade Interaction Rules

#### Context Loading
- **Rule Files**: All `.windsurf/rules/*.md` files loaded as context
- **Workflow References**: Workflows include guardrail compliance steps
- **Exhibit Awareness**: AI understands exhibit vs canon distinctions

#### Response Guidelines
- **Rule Citation**: Reference specific rules when giving advice
- **Guardrail Respect**: Never suggest actions that violate guardrails
- **Escalation Clarity**: Clearly indicate when human governance review needed

### Workflow Automation

#### Guardrail Integration
- **Pre-execution Checks**: All workflows validate guardrails before proceeding
- **Error Handling**: Clear error messages referencing specific violated rules
- **Recovery Suggestions**: Automated suggestions for fixing common violations

---

## Future Evolution

### Rule Expansion
- **New Domains**: Additional rules for emerging development areas
- **Granular Control**: More specific rules for complex scenarios
- **Automation**: Increased automated enforcement capabilities

### Workflow Enhancement
- **Intelligence**: AI-assisted workflow optimization within guardrails
- **Integration**: Deeper integration with development tools and platforms
- **Metrics**: Enhanced monitoring and continuous improvement feedback

### Governance Maturity
- **Process Refinement**: Streamlined governance processes
- **Team Adoption**: Improved team understanding and compliance
- **Scalability**: Governance that scales with project growth

---

*"Through unified workflows and unwavering guardrails, GRID achieves both innovation and integrity. Rules guide creation; guardrails protect progress."*
