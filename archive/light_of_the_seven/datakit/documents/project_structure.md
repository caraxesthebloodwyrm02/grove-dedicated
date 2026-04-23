# Project Structure Diagram

```mermaid
graph TD
    A[DataKit] --> B[core/]
    A --> C[data/]
    A --> D[examples/]
    A --> E[scripts/]
    A --> F[templates/]
    A --> G[visualizations/]
    
    B --> B1[Core functionality modules]
    C --> C1[Data storage and processing]
    D --> D1[Example usage and demos]
    E --> E1[Utility scripts]
    F --> F1[Template files]
    G --> G1[Visualization components]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333
    style C fill:#bbf,stroke:#333
    style D fill:#bbf,stroke:#333
    style E fill:#bbf,stroke:#333
    style F fill:#bbf,stroke:#333
    style G fill:#bbf,stroke:#333
```

## Directory Structure

```
full_datakit/
├── core/           # Core functionality and main logic
├── data/           # Data storage and processing
├── examples/       # Example usage and demos
├── scripts/        # Utility scripts
├── templates/      # Template files
├── visualizations/ # Visualization components
└── datakit.py      # Main package entry point
```

## Key Components

- **core/**: Contains the main business logic and core functionality
- **data/**: Handles data storage, loading, and preprocessing
- **examples/**: Example scripts and notebooks demonstrating usage
- **scripts/**: Utility and helper scripts
- **templates/**: Template files for various use cases
- **visualizations/**: Components for data visualization
- **datakit.py**: Main package entry point and public API
