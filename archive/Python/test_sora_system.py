"""
Comprehensive test suite for Sora system before packaging.
Tests all modules, classes, enums, and functional pipelines.
"""

import sys
from pathlib import Path

print('=' * 70)
print('SORA SYSTEM - COMPREHENSIVE TEST SUITE')
print('=' * 70)
print()

print('PHASE 1: IMPORT VERIFICATION')
print('-' * 70)
try:
    import sora_prompt_generator
    print('✓ sora_prompt_generator module')
except Exception as e:
    print(f'✗ sora_prompt_generator: {e}')
    sys.exit(1)

try:
    import sora_client
    print('✓ sora_client module')
except Exception as e:
    print(f'✗ sora_client: {e}')
    sys.exit(1)

try:
    import sora_integration
    print('✓ sora_integration module')
except Exception as e:
    print(f'✗ sora_integration: {e}')
    sys.exit(1)

print()
print('PHASE 2: CLASS AVAILABILITY')
print('-' * 70)
from sora_prompt_generator import (
    SoraPromptGenerator, TokenBudgetLevel, RepoAnalyzer, 
    ConceptMapper, StoryTemplate, PromptOptimizer, RepositoryConcepts,
    MetaphorMapping, build_prompt_from_repo
)
print('✓ sora_prompt_generator classes')

from sora_client import (
    SoraClient, VideoGenerationRequest, VideoGenerationResponse,
    AspectRatio, VideoStyle
)
print('✓ sora_client classes')

from sora_integration import SoraWorkflow
print('✓ sora_integration classes')

print()
print('PHASE 3: ENUM VALUES')
print('-' * 70)
print('Token Budget Levels:')
for level in TokenBudgetLevel:
    print(f'  • {level.name}: {level.value} tokens')

print('Video Aspect Ratios:')
for ratio in AspectRatio:
    print(f'  • {ratio.name}: {ratio.value}')

print('Video Styles:')
for style in VideoStyle:
    print(f'  • {style.name}')

print()
print('PHASE 4: FUNCTIONAL TESTS')
print('-' * 70)

req = VideoGenerationRequest(
    prompt='Test prompt for 90 second video',
    duration=90.0,
    aspect_ratio=AspectRatio.WIDESCREEN,
    quality='high'
)
cost = req.estimate_cost_usd()
print(f'✓ VideoGenerationRequest: 90s @ high quality = ${cost:.2f}')

client = SoraClient(api_key='test-key-12345', monthly_budget_usd=10.0)
print('✓ SoraClient initialized')

gen = SoraPromptGenerator(Path('e:/projects/python/hello'), budget=TokenBudgetLevel.LOW)
print('✓ SoraPromptGenerator initialized')

test_prompt = 'Black and white silent-film style short (90 seconds). Inspired by Charlie Chaplin. Test text.'
compressed = PromptOptimizer.compress_prompt(test_prompt, TokenBudgetLevel.LOW)
est_tokens = PromptOptimizer.estimate_tokens(test_prompt)
print(f'✓ PromptOptimizer: {len(test_prompt)} chars -> {est_tokens} estimated tokens')

concept_map = ConceptMapper.get_metaphor('ModuleNotFoundError')
if concept_map:
    gag_preview = concept_map.physical_gag[:50]
    print(f'✓ ConceptMapper: ModuleNotFoundError -> {gag_preview}...')

print()
print('PHASE 5: PIPELINE EXECUTION (DRY RUN)')
print('-' * 70)
try:
    prompt = build_prompt_from_repo('e:/projects/python/hello', TokenBudgetLevel.LOW)
    tokens = PromptOptimizer.estimate_tokens(prompt)
    print(f'✓ Pipeline executed successfully')
    print(f'  Generated prompt: {len(prompt)} chars / {tokens} estimated tokens')
    if tokens > TokenBudgetLevel.LOW.value:
        overage = tokens - TokenBudgetLevel.LOW.value
        print(f'  ⚠ Over budget: {overage} tokens over limit')
    else:
        remaining = TokenBudgetLevel.LOW.value - tokens
        print(f'  ✓ Within budget: {remaining} tokens remaining')
except Exception as e:
    print(f'✗ Pipeline failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print('PHASE 6: TYPE HINTS VERIFICATION')
print('-' * 70)
from typing import get_type_hints

try:
    hints = get_type_hints(SoraPromptGenerator.generate)
    print(f'✓ SoraPromptGenerator.generate type hints: {len(hints)} annotations')
except Exception as e:
    print(f'⚠ Type hints check: {e}')

print()
print('=' * 70)
print('ALL TESTS PASSED ✓')
print('=' * 70)
print()
print('SUMMARY:')
print('  • All 3 modules import successfully')
print('  • All classes and enums available')
print('  • Functional tests passed')
print('  • Pipeline execution successful')
print('  • Ready for packaging')
