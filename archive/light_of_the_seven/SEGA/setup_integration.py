#!/usr/bin/env python3
"""
Setup Integration Script

Generates all integration artifacts:
- StreamSets pipeline JSON
- Kafka topics shell script
- CP4D authentication and scoring scripts
- Prometheus monitoring configuration
- GitHub Actions CI workflow
"""

import json
import os


def streamsets_pipeline():
    """Generate StreamSets pipeline JSON."""
    pipeline = {
        "pipelineId": "raw-events-to-features",
        "title": "Raw Events Validation Pipeline",
        "version": 1,
        "uuid": "pipeline-uuid-123",
        "description": "Validates raw events against JSON schema",
        "stages": [
            {
                "instanceName": "KafkaConsumer",
                "library": "streamsets-datacollector-apache-kafka_2_0-lib",
                "stageName": "com_streamsets_pipeline_stage_origin_kafka_KafkaDSource",
                "configuration": [{"name": "conf.topicList", "value": ["raw-events"]}],
            }
        ],
    }
    os.makedirs("streamsets/pipelines", exist_ok=True)
    with open("streamsets/pipelines/raw-events-to-features.json", "w") as f:
        json.dump(pipeline, f, indent=2)
    print("Generated StreamSets pipeline")


def kafka_topics():
    """Generate Kafka topics creation script."""
    script = """# Kafka CLI (replace with your bootstrap servers)
kafka-topics.sh --create --bootstrap-server $KAFKA_BOOTSTRAP --replication-factor 3 --partitions 6 --topic raw-events
kafka-topics.sh --create --bootstrap-server $KAFKA_BOOTSTRAP --replication-factor 3 --partitions 6 --topic features
kafka-topics.sh --create --bootstrap-server $KAFKA_BOOTSTRAP --replication-factor 3 --partitions 3 --topic predictions
kafka-topics.sh --create --bootstrap-server $KAFKA_BOOTSTRAP --replication-factor 3 --partitions 3 --topic raw-events-dlq

# Azure Event Hub CLI (replace with your namespace and resource group)
az eventhubs eventhub create --resource-group $RG --namespace-name $NS --name raw-events --message-retention-in-days 7 --partition-count 6
az eventhubs eventhub create --resource-group $RG --namespace-name $NS --name features --message-retention-in-days 7 --partition-count 6
az eventhubs eventhub create --resource-group $RG --namespace-name $NS --name predictions --message-retention-in-days 7 --partition-count 3
az eventhubs eventhub create --resource-group $RG --namespace-name $NS --name raw-events-dlq --message-retention-in-days 7 --partition-count 3
"""
    os.makedirs("infra", exist_ok=True)
    with open("infra/kafka-topics.sh", "w") as f:
        f.write(script)
    print("Generated Kafka topics script")


def cp4d_snippets():
    """Generate CP4D scripts."""
    auth_script = """# CP4D 4.6: Obtain Bearer token
export CPD_HOST=https://your-cpd-host
export CPD_USER=your-user
export CPD_PASS=your-pass
TOKEN=$(curl -sk -X POST "$CPD_HOST/icp4d-api/v1/authorize" \\
  -H "Content-Type: application/json" \\
  -d '{"username":"'"$CPD_USER"'","password":"'"$CPD_PASS"'"}' | jq -r '.token')
echo $TOKEN
"""
    scoring_script = """# Score a feature payload (example with embedding and a numeric feature)
curl -sk -X POST "$CPD_HOST/ml/v4/deployments/$DEPLOY_ID/predictions?version=2021-06-01" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "input_data": [{
      "fields": ["embedding", "x1"],
      "values": [
        [[0.12, -0.44, 0.98, 0.01, 0.23, 0.67, 0.45, -0.33, 0.78, -0.12], 3.14]
      ]
    }]
  }'
"""
    with open("infra/cp4d-auth.sh", "w") as f:
        f.write(auth_script)
    with open("infra/cp4d-scoring.sh", "w") as f:
        f.write(scoring_script)
    print("Generated CP4D scripts")


def monitoring_skeleton():
    """Generate Prometheus metrics configuration."""
    config = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'transformer'
    static_configs:
      - targets: ['transformer:8000']
    metrics_path: /metrics
    scrape_interval: 10s

  - job_name: 'streamsets'
    static_configs:
      - targets: ['streamsets:18630']
    metrics_path: /rest/v1/metrics/prometheus
    scrape_interval: 30s
"""
    os.makedirs("infra/monitoring", exist_ok=True)
    with open("infra/monitoring/prometheus.yml", "w") as f:
        f.write(config)
    print("Generated Prometheus config")


def ci_pipeline():
    """Generate GitHub Actions CI workflow."""
    workflow = """name: Integration CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r transformer/requirements.txt
      - name: Lint
        run: |
          flake8 transformer/
          black --check transformer/
      - name: Unit tests
        run: |
          pytest transformer/tests/
      - name: Build Docker image
        run: |
          docker build -t transformer:${{ github.sha }} ./transformer
      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker tag transformer:${{ github.sha }} your-registry/transformer:latest
          docker push your-registry/transformer:latest
"""
    os.makedirs(".github/workflows", exist_ok=True)
    with open(".github/workflows/ci.yml", "w") as f:
        f.write(workflow)
    print("Generated CI workflow")


def main():
    """Main function to generate all artifacts."""
    print("Setting up Grid Integration Pipeline...")

    streamsets_pipeline()
    kafka_topics()
    cp4d_snippets()
    monitoring_skeleton()
    ci_pipeline()

    print("All integration artifacts generated successfully!")


if __name__ == "__main__":
    main()
