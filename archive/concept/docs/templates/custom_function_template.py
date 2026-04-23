import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

# Environment Configuration
class EnvironmentConfig(BaseModel):
    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field("gpt-4-1106-preview", description="Model to use for function calling")
    temperature: float = Field(0.7, description="Model temperature (0-2)")
    max_tokens: int = Field(4000, description="Maximum tokens to generate")

# Core Data Models
class Timeframe(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    milestones: List[Dict[str, str]] = []

class Governance(BaseModel):
    structure: List[Dict[str, Any]] = []
    decision_making_process: Optional[str] = None
    escalation_path: List[str] = []

class MVPScope(BaseModel):
    core_features: List[str] = []
    success_metrics: Dict[str, str] = {}
    out_of_scope: List[str] = []

class BargainDetails(BaseModel):
    context: str
    terms: Dict[str, str] = {}
    timeframes: Timeframe = Timeframe()
    mvp: MVPScope = MVPScope()
    governance: Governance = Governance()
    arguments: Dict[str, Any] = {}

# Function Definitions
class FunctionCallTemplate:
    def __init__(self, config: EnvironmentConfig):
        self.config = config
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

    def get_system_prompt(self) -> str:
        return """You are a sophisticated AI assistant specialized in analyzing and structuring complex agreements and requirements. 
        Your task is to extract, validate, and structure information about initiatives, ensuring all critical aspects are captured."""

    def get_functions_schema(self) -> List[Dict]:
        return [
            {
                "name": "extract_bargain_details",
                "description": "Extract and structure all critical details from a bargain or agreement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "context": {
                            "type": "string",
                            "description": "Background and purpose of the agreement"
                        },
                        "terms": {
                            "type": "object",
                            "description": "Key terms and conditions",
                            "additionalProperties": {"type": "string"}
                        },
                        "timeframes": {
                            "type": "object",
                            "properties": {
                                "start_date": {"type": "string", "format": "date"},
                                "end_date": {"type": "string", "format": "date"},
                                "milestones": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "date": {"type": "string"},
                                            "description": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "mvp": {
                            "type": "object",
                            "properties": {
                                "core_features": {"type": "array", "items": {"type": "string"}},
                                "success_metrics": {"type": "object", "additionalProperties": {"type": "string"}},
                                "out_of_scope": {"type": "array", "items": {"type": "string"}}
                            }
                        },
                        "governance": {
                            "type": "object",
                            "properties": {
                                "structure": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "role": {"type": "string"},
                                            "responsibilities": {"type": "array", "items": {"type": "string"}}
                                        }
                                    }
                                },
                                "decision_making_process": {"type": "string"},
                                "escalation_path": {"type": "array", "items": {"type": "string"}}
                            }
                        },
                        "arguments": {
                            "type": "object",
                            "description": "Key arguments and rationale",
                            "additionalProperties": {}
                        }
                    },
                    "required": ["context"]
                }
            }
        ]

    def make_api_call(self, messages: List[Dict]) -> Dict:
        payload = {
            "model": self.config.model,
            "messages": messages,
            "functions": self.get_functions_schema(),
            "function_call": {"name": "extract_bargain_details"},
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request failed: {e}")
            raise

    def process_input(self, input_text: str) -> BargainDetails:
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": input_text}
        ]
        
        response = self.make_api_call(messages)
        
        try:
            function_call = response["choices"][0]["message"]["function_call"]
            if function_call["name"] == "extract_bargain_details":
                args = json.loads(function_call["arguments"])
                
                # Provide defaults for missing optional fields
                defaults = {
                    "terms": {},
                    "timeframes": {
                        "start_date": "",
                        "end_date": "",
                        "milestones": []
                    },
                    "mvp": {
                        "core_features": [],
                        "success_metrics": {},
                        "out_of_scope": []
                    },
                    "governance": {
                        "structure": [],
                        "decision_making_process": "",
                        "escalation_path": []
                    },
                    "arguments": {}
                }
                
                # Merge args with defaults
                for key, value in defaults.items():
                    if key not in args:
                        args[key] = value
                
                return BargainDetails(**args)
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error processing response: {e}")
            raise

# Example Usage
if __name__ == "__main__":
    # Initialize configuration
    config = EnvironmentConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4-1106-preview"
    )
    
    # Sample input text (replace with actual content)
    input_text = """
    We are launching a new research initiative on Temporal Resonance with the following details:
    - Duration: 6 months starting 2025-01-01
    - Key Milestones: 
      - Proposal submission by 2025-01-15
      - Initial findings by 2025-03-01
      - Final report by 2025-06-30
    - MVP: Focus on theoretical framework and initial experiments
    - Governance: Led by a steering committee with monthly reviews
    """
    
    # Process the input
    try:
        processor = FunctionCallTemplate(config)
        result = processor.process_input(input_text)
        
        # Print structured output
        print("\n=== Structured Output ===")
        print(json.dumps(result.model_dump(), indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")
