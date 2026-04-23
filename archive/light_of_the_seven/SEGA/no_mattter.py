import matplotlib.pyplot as plt
import numpy as np

from core.tool_attributes import ToolProperty
from scripts.no_mattter import *  # noqa: F401,F403

TOOL_ATTRIBUTES = ToolProperty.read_simulate()


def identify_type(value):
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dict"
    else:
        return (
            "tuple"
            if isinstance(value, tuple)
            else (
                "set"
                if isinstance(value, set)
                else "bytes" if isinstance(value, bytes) else "unknown"
            )
        )


def process_data(data: list, threshold: float = 0.5) -> dict:
    """Process data and return filtered results."""
    return {"filtered": [x for x in data if x > threshold], "count": len(data)}


def calculate_statistics(values: list) -> dict:
    """Calculate mean, median, and std deviation."""
    return {"mean": np.mean(values), "median": np.median(values), "std": np.std(values)}


def plot_distribution(data: list, bins: int = 20, title: str = "Distribution") -> None:
    """Plot histogram of data distribution."""
    plt.hist(data, bins=bins)
    plt.title(title)
    plt.show()


def filter_by_type(data: list, target_type: str) -> list:
    """Filter list items by their identified type."""
    return [x for x in data if identify_type(x) == target_type]


def vectorize_domain_features(
    age: int,
    income: float,
    credit_score: int,
    employment_status: str,
    debt_to_income_ratio: float,
) -> np.ndarray:
    """Convert domain features to vector representation for domain identification."""
    employment_encoded = 1.0 if employment_status == "employed" else 0.0
    return np.array(
        [age, income, credit_score, employment_encoded, debt_to_income_ratio]
    )


def identify_domain(feature_vector: np.ndarray) -> str:
    """Identify the relevant domain based on feature vector."""
    age, income, credit_score, employment_encoded, debt_to_income_ratio = feature_vector

    if credit_score < 600 or debt_to_income_ratio > 0.43:
        return "high_risk_lending"
    elif credit_score >= 750 and income >= 75000:
        return "premium_lending"
    elif income < 30000:
        return "subprime_lending"
    else:
        return "standard_lending"


def _calculate_interest_rate(credit_score: int) -> float:
    """Calculate interest rate based on credit score."""
    if credit_score >= 750:
        return 3.5
    elif credit_score >= 700:
        return 4.2
    elif credit_score >= 650:
        return 5.5
    else:
        return 7.0


def _assess_risk_level(debt_to_income_ratio: float, credit_score: int) -> str:
    """Assess risk level based on financial metrics."""
    if debt_to_income_ratio > 0.43 or credit_score < 600:
        return "high"
    elif debt_to_income_ratio > 0.36 or credit_score < 650:
        return "medium"
    else:
        return "low"


def _determine_approval(
    age: int,
    income: float,
    credit_score: int,
    employment_status: str,
    debt_to_income_ratio: float,
) -> str:
    """Determine loan approval status."""
    loan_eligible = age >= 18 and income >= 30000 and credit_score >= 650
    employment_verified = employment_status == "employed" and income > 0
    risk_level = _assess_risk_level(debt_to_income_ratio, credit_score)

    return (
        "approved"
        if loan_eligible and employment_verified and risk_level != "high"
        else "denied"
    )


def create_loan_profile(
    age: int,
    income: float,
    credit_score: int,
    employment_status: str,
    debt_to_income_ratio: float,
) -> dict:
    """Create a comprehensive loan profile with all assessments."""
    feature_vector = vectorize_domain_features(
        age, income, credit_score, employment_status, debt_to_income_ratio
    )
    loan_eligible = age >= 18 and income >= 30000 and credit_score >= 650

    return {
        "age": age,
        "income": income,
        "credit_score": credit_score,
        "employment_status": employment_status,
        "debt_to_income_ratio": debt_to_income_ratio,
        "domain": identify_domain(feature_vector),
        "loan_eligible": loan_eligible,
        "loan_amount": min(income * 5, 250000) if loan_eligible else 0,
        "interest_rate": _calculate_interest_rate(credit_score),
        "employment_verified": employment_status == "employed" and income > 0,
        "risk_level": _assess_risk_level(debt_to_income_ratio, credit_score),
        "approval_status": _determine_approval(
            age, income, credit_score, employment_status, debt_to_income_ratio
        ),
    }


def vectorize_corridor_features(
    age_years: int,
    nominal_capacity: float,
    reliability_score: int,
    operational_status: str,
    load_factor: float,
) -> np.ndarray:
    """Convert corridor or communication channel features to a vector representation."""
    operational_encoded = 1.0 if operational_status == "operational" else 0.0
    return np.array(
        [
            age_years,
            nominal_capacity,
            reliability_score,
            operational_encoded,
            load_factor,
        ]
    )


def classify_corridor_domain(feature_vector: np.ndarray) -> str:
    """Classify a corridor or communication channel into an operational domain."""
    age_years, nominal_capacity, reliability_score, operational_encoded, load_factor = (
        feature_vector
    )

    if reliability_score < 80 or load_factor > 0.9:
        return "congested_or_unreliable_corridor"
    elif reliability_score >= 95 and nominal_capacity >= 120:
        return "priority_high_throughput_corridor"
    elif nominal_capacity < 40:
        return "fragile_low_capacity_branch_line"
    else:
        return "standard_mainline_corridor"


def _calculate_latency_penalty(reliability_score: int) -> float:
    """Calculate a latency or cost penalty factor based on corridor reliability."""
    if reliability_score >= 95:
        return 0.95
    elif reliability_score >= 90:
        return 1.0
    elif reliability_score >= 80:
        return 1.1
    else:
        return 1.25


def _assess_corridor_risk(load_factor: float, reliability_score: int) -> str:
    """Assess operational risk level for a corridor or communication channel."""
    if load_factor > 0.9 or reliability_score < 80:
        return "high"
    elif load_factor > 0.75 or reliability_score < 85:
        return "medium"
    else:
        return "low"


def _determine_route_status(
    age_years: int,
    nominal_capacity: float,
    reliability_score: int,
    operational_status: str,
    load_factor: float,
) -> str:
    """Determine whether a corridor is open for additional routing."""
    route_viable = (
        age_years < 120 and nominal_capacity >= 20 and reliability_score >= 80
    )
    operational_verified = operational_status == "operational"
    risk_level = _assess_corridor_risk(load_factor, reliability_score)

    return (
        "open"
        if route_viable and operational_verified and risk_level != "high"
        else "closed"
    )


def create_corridor_profile(
    age_years: int,
    nominal_capacity: float,
    reliability_score: int,
    operational_status: str,
    load_factor: float,
) -> dict:
    """Create a corridor or communication channel profile with risk and capacity assessments."""
    feature_vector = vectorize_corridor_features(
        age_years, nominal_capacity, reliability_score, operational_status, load_factor
    )
    route_viable = (
        age_years < 120 and nominal_capacity >= 20 and reliability_score >= 80
    )

    return {
        "age_years": age_years,
        "nominal_capacity": nominal_capacity,
        "reliability_score": reliability_score,
        "operational_status": operational_status,
        "load_factor": load_factor,
        "domain": classify_corridor_domain(feature_vector),
        "route_viable": route_viable,
        "max_throughput": nominal_capacity if route_viable else 0.0,
        "latency_penalty": _calculate_latency_penalty(reliability_score),
        "operational_verified": operational_status == "operational",
        "risk_level": _assess_corridor_risk(load_factor, reliability_score),
        "route_status": _determine_route_status(
            age_years,
            nominal_capacity,
            reliability_score,
            operational_status,
            load_factor,
        ),
    }


if __name__ == "__main__":
    age = 25
    income = 50000
    credit_score = 720
    employment_status = "employed"
    debt_to_income_ratio = 0.35

    profile = create_loan_profile(
        age, income, credit_score, employment_status, debt_to_income_ratio
    )

    print(f"{'='*60}")
    print(f"LOAN PROFILE ANALYSIS")
    print(f"{'='*60}")
    print(f"Applicant Age: {profile['age']}")
    print(f"Annual Income: ${profile['income']:,.2f}")
    print(f"Credit Score: {profile['credit_score']}")
    print(f"Employment Status: {profile['employment_status']}")
    print(f"Debt-to-Income Ratio: {profile['debt_to_income_ratio']:.2%}")
    print(f"\nDomain Classification: {profile['domain']}")
    print(f"Loan Eligible: {profile['loan_eligible']}")
    print(f"Max Loan Amount: ${profile['loan_amount']:,.2f}")
    print(f"Interest Rate: {profile['interest_rate']:.2f}%")
    print(f"Employment Verified: {profile['employment_verified']}")
    print(f"Risk Level: {profile['risk_level'].upper()}")
    print(f"{'='*60}")
    print(f"APPROVAL STATUS: {profile['approval_status'].upper()}")
    print(f"{'='*60}")

    corridor_age_years = 40
    nominal_capacity = 100.0
    reliability_score = 92
    operational_status = "operational"
    load_factor = 0.8

    corridor_profile = create_corridor_profile(
        corridor_age_years,
        nominal_capacity,
        reliability_score,
        operational_status,
        load_factor,
    )

    print(f"\n{'='*60}")
    print(f"CORRIDOR PROFILE ANALYSIS")
    print(f"{'='*60}")
    print(f"Corridor Age (years): {corridor_profile['age_years']}")
    print(f"Nominal Capacity: {corridor_profile['nominal_capacity']}")
    print(f"Reliability Score: {corridor_profile['reliability_score']}")
    print(f"Operational Status: {corridor_profile['operational_status']}")
    print(f"Load Factor: {corridor_profile['load_factor']:.0%}")
    print(f"\nDomain Classification: {corridor_profile['domain']}")
    print(f"Route Viable: {corridor_profile['route_viable']}")
    print(f"Max Throughput: {corridor_profile['max_throughput']}")
    print(f"Latency Penalty: {corridor_profile['latency_penalty']:.2f}")
    print(f"Operational Verified: {corridor_profile['operational_verified']}")
    print(f"Risk Level: {corridor_profile['risk_level'].upper()}")
    print(f"{'='*60}")
    print(f"ROUTE STATUS: {corridor_profile['route_status'].upper()}")
    print(f"{'='*60}")
