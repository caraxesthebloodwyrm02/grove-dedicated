#!/usr/bin/env python3
"""
IDE Recorder Variant Simulation Engine

Runs Monte Carlo simulations for different product variants to generate
concrete scenarios with metrics, timelines, and success probabilities.
"""

import random
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from enum import Enum

class Variant(Enum):
    YOUTUBE_TUTORIAL = "A: YouTube Tutorial Generator"
    DEV_JOURNAL = "B: Developer Daily Journal"
    TIMELINE_ANALYZER = "C: Timeline Analyzer"
    BUG_REPRODUCER = "D: Bug Reproduction Tool"

@dataclass
class SimulationParameters:
    """Parameters for variant simulation"""
    technical_feasibility: float  # 0-1
    market_size_factor: float     # 0-1
    competition_factor: float     # 0-1 (higher = more competition)
    implementation_complexity: float  # 0-1 (higher = more complex)
    viral_coefficient: float      # 0-1
    revenue_per_user: float       # dollars
    monthly_burn_rate: float      # dollars
    
@dataclass
class SimulationResult:
    """Results from a single simulation run"""
    variant: Variant
    months_to_product_market_fit: int
    total_users_12_months: int
    revenue_12_months: float
    technical_success: bool
    traction_success: bool
    sustainable_success: bool
    failure_reason: str = ""
    key_events: List[str] = None
    
    def __post_init__(self):
        if self.key_events is None:
            self.key_events = []
    
    @property
    def success(self) -> bool:
        """Overall success if any tier is achieved"""
        return self.technical_success or self.traction_success or self.sustainable_success

class VariantSimulation:
    """Simulates different product variants with realistic scenarios"""
    
    def __init__(self):
        self.variant_params = self._initialize_parameters()
        
    def _initialize_parameters(self) -> Dict[Variant, SimulationParameters]:
        """Initialize realistic parameters for each variant"""
        return {
            Variant.YOUTUBE_TUTORIAL: SimulationParameters(
                technical_feasibility=0.95,
                market_size_factor=0.7,
                competition_factor=0.6,
                implementation_complexity=0.2,
                viral_coefficient=0.3,
                revenue_per_user=5.0,
                monthly_burn_rate=500  # Lower burn rate for local-first
            ),
            Variant.DEV_JOURNAL: SimulationParameters(
                technical_feasibility=0.85,
                market_size_factor=0.5,
                competition_factor=0.4,
                implementation_complexity=0.3,
                viral_coefficient=0.2,
                revenue_per_user=8.0,
                monthly_burn_rate=800
            ),
            Variant.TIMELINE_ANALYZER: SimulationParameters(
                technical_feasibility=0.90,
                market_size_factor=0.4,
                competition_factor=0.8,
                implementation_complexity=0.7,
                viral_coefficient=0.1,
                revenue_per_user=50.0,
                monthly_burn_rate=2000  # Higher for enterprise features
            ),
            Variant.BUG_REPRODUCER: SimulationParameters(
                technical_feasibility=0.75,
                market_size_factor=0.3,
                competition_factor=0.9,
                implementation_complexity=0.8,
                viral_coefficient=0.15,
                revenue_per_user=100.0,
                monthly_burn_rate=3000  # Highest for enterprise/security
            )
        }
    
    def run_single_simulation(self, variant: Variant, random_seed: int = None) -> SimulationResult:
        """Run a single simulation for a variant"""
        if random_seed:
            random.seed(random_seed)
            
        params = self.variant_params[variant]
        
        # Technical feasibility check
        if random.random() > params.technical_feasibility:
            return SimulationResult(
                variant=variant,
                months_to_product_market_fit=3,
                total_users_12_months=0,
                revenue_12_months=0,
                technical_success=False,
                traction_success=False,
                sustainable_success=False,
                failure_reason="Technical implementation failed",
                key_events=["Month 1: Critical technical issues discovered", "Month 3: Project abandoned"]
            )
        
        # Simulate month-by-month growth
        users = 0
        revenue = 0
        events = []
        pmtf_reached = False
        pmtf_month = 12
        
        # Track tiered success
        technical_success = True  # Passed feasibility check above
        traction_success = False
        sustainable_success = False
        
        for month in range(1, 13):
            # Base growth rate affected by market size and competition
            base_growth = random.uniform(0.3, 1.5) * params.market_size_factor  # Increased from 0.1-0.5 to 0.3-1.5
            competition_drag = random.uniform(0.05, 0.15) * params.competition_factor  # Reduced from 0.05-0.2 to 0.05-0.15
            monthly_growth_rate = max(0.1, base_growth - competition_drag)  # Minimum 10% growth
            
            # Viral growth events (increased probability)
            if random.random() < params.viral_coefficient * 0.2:  # Increased from 0.1 to 0.2
                viral_multiplier = random.uniform(2, 5)
                monthly_growth_rate *= viral_multiplier
                events.append(f"Month {month}: Viral growth event ({viral_multiplier:.1f}x)")
            
            # Calculate new users
            if month == 1:
                new_users = random.randint(5, 20)  # Initial launch
            else:
                # Fixed growth calculation: users * (1 + growth_rate) not users * growth_rate
                new_users = int(users * monthly_growth_rate)
            
            users += new_users
            
            # Check traction success (25+ users for MVP)
            if users >= 25 and not traction_success:
                traction_success = True
                events.append(f"Month {month}: Traction milestone reached (25+ users)")
            
            # Revenue calculation
            if month >= 3:  # Start monetizing after 3 months
                paying_users = int(users * random.uniform(0.05, 0.15))
                monthly_revenue = paying_users * params.revenue_per_user
                revenue += monthly_revenue
                
                # Check for product-market fit
                if monthly_revenue > params.monthly_burn_rate and not pmtf_reached:
                    pmtf_reached = True
                    pmtf_month = month
                    events.append(f"Month {month}: Product-market fit achieved!")
                
                # Check sustainable success (revenue > burn rate for 3+ months)
                if monthly_revenue > params.monthly_burn_rate and month >= 6:
                    sustainable_success = True
                    events.append(f"Month {month}: Sustainable revenue achieved")
            
            # Random events
            event_roll = random.random()
            if event_roll < 0.1:
                events.append(f"Month {month}: Competitor launched similar product")
                params.competition_factor += 0.1
            elif event_roll < 0.2:
                events.append(f"Month {month}: Positive press coverage")
                params.viral_coefficient += 0.1
            elif event_roll < 0.25:
                events.append(f"Month {month}: Technical debt accumulation")
                params.technical_feasibility -= 0.05
        
        # Determine failure reason if no success
        failure_reason = ""
        if not (technical_success or traction_success or sustainable_success):
            if not technical_success:
                failure_reason = "Technical implementation failed"
            elif users < 25:
                failure_reason = "Failed to achieve user traction (25+ users)"
            else:
                failure_reason = "Revenue insufficient for sustainability"
        
        return SimulationResult(
            variant=variant,
            months_to_product_market_fit=pmtf_month if pmtf_reached else 12,
            total_users_12_months=users,
            revenue_12_months=revenue,
            technical_success=technical_success,
            traction_success=traction_success,
            sustainable_success=sustainable_success,
            failure_reason=failure_reason,
            key_events=events
        )
    
    def run_monte_carlo(self, variant: Variant, iterations: int = 1000) -> Dict:
        """Run Monte Carlo simulation for a variant"""
        results = []
        
        for i in range(iterations):
            result = self.run_single_simulation(variant, random_seed=i)
            results.append(result)
        
        # Calculate statistics for each tier
        overall_success_count = sum(1 for r in results if r.success)
        technical_success_count = sum(1 for r in results if r.technical_success)
        traction_success_count = sum(1 for r in results if r.traction_success)
        sustainable_success_count = sum(1 for r in results if r.sustainable_success)
        
        overall_success_rate = overall_success_count / iterations
        technical_success_rate = technical_success_count / iterations
        traction_success_rate = traction_success_count / iterations
        sustainable_success_rate = sustainable_success_count / iterations
        
        avg_users = sum(r.total_users_12_months for r in results) / iterations
        avg_revenue = sum(r.revenue_12_months for r in results) / iterations
        avg_pmtf = sum(r.months_to_product_market_fit for r in results if r.traction_success) / max(traction_success_count, 1)
        
        # Find best and worst cases
        best_case = max(results, key=lambda r: r.revenue_12_months)
        worst_case = min(results, key=lambda r: r.revenue_12_months)
        
        return {
            "variant": variant.value,
            "overall_success_rate": overall_success_rate,
            "technical_success_rate": technical_success_rate,
            "traction_success_rate": traction_success_rate,
            "sustainable_success_rate": sustainable_success_rate,
            "avg_users_12_months": avg_users,
            "avg_revenue_12_months": avg_revenue,
            "avg_months_to_pmtf": avg_pmtf,
            "best_case": asdict(best_case),
            "worst_case": asdict(worst_case)
        }
    
    def run_all_variants(self, iterations: int = 1000) -> Dict:
        """Run simulations for all variants"""
        results = {}
        
        for variant in Variant:
            print(f"Running simulation for {variant.value}...")
            results[variant.value] = self.run_monte_carlo(variant, iterations)
        
        return results
    
    def generate_scenarios(self, iterations: int = 100) -> List[SimulationResult]:
        """Generate specific scenarios for analysis"""
        scenarios = []
        
        for variant in Variant:
            # Generate 3 representative scenarios per variant
            for i in range(3):
                result = self.run_single_simulation(variant, random_seed=hash(f"{variant.value}_{i}") % 10000)
                scenarios.append(result)
        
        return scenarios

def main():
    """Main simulation runner"""
    print("IDE Recorder Variant Simulation Engine")
    print("=" * 50)
    
    sim = VariantSimulation()
    
    # Run Monte Carlo simulations
    print("\nRunning Monte Carlo simulations (1000 iterations each)...")
    monte_carlo_results = sim.run_all_variants(iterations=1000)
    
    # Display results
    print("\nMONTE CARLO RESULTS:")
    print("-" * 50)
    
    for variant_name, result in monte_carlo_results.items():
        print(f"\n{variant_name}:")
        print(f"  Overall Success Rate: {result['overall_success_rate']:.1%}")
        print(f"  Technical Success Rate: {result['technical_success_rate']:.1%}")
        print(f"  Traction Success Rate: {result['traction_success_rate']:.1%}")
        print(f"  Sustainable Success Rate: {result['sustainable_success_rate']:.1%}")
        print(f"  Avg Users (12mo): {result['avg_users_12_months']:.0f}")
        print(f"  Avg Revenue (12mo): ${result['avg_revenue_12_months']:,.0f}")
        print(f"  Avg Time to Traction: {result['avg_months_to_pmtf']:.1f} months")
    
    # Generate specific scenarios
    print("\nGenerating detailed scenarios...")
    scenarios = sim.generate_scenarios(iterations=100)
    
    # Save detailed results
    output = {
        "monte_carlo": monte_carlo_results,
        "scenarios": [asdict(s) for s in scenarios],
        "generated_at": datetime.now().isoformat()
    }
    
    with open("simulation_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\nSimulation complete! Results saved to simulation_results.json")
    
    # Return scenarios for immediate display
    return scenarios

if __name__ == "__main__":
    scenarios = main()
