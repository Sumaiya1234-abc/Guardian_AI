"""
Configuration file for GuardianAI environment defaults and settings.
"""

# Environment Defaults
DEFAULT_ENV_CONFIG = {
    "num_accounts": 100,
    "num_merchants": 1000,
    "fraud_rate": 0.05,
    "difficulty": "medium",
    "reward_scheme": "balanced",
    "max_episode_length": 1000,
}

# Difficulty Level Configurations
DIFFICULTY_CONFIGS = {
    "easy": {
        "amount_multiplier_range": (5, 20),    # 5-20x normal
        "velocity_threshold": 20,               # Easy to detect
        "geographic_change_frequency": 0.8,    # Frequent
        "merchant_change_frequency": 0.7,      # Common
        "fraud_subtlety": 0.1,                 # Obvious
    },
    "medium": {
        "amount_multiplier_range": (3, 10),    # 3-10x normal
        "velocity_threshold": 10,               # Moderate
        "geographic_change_frequency": 0.4,    # Occasional
        "merchant_change_frequency": 0.3,      # Less common
        "fraud_subtlety": 0.5,                 # Moderate
    },
    "hard": {
        "amount_multiplier_range": (1.5, 3),   # 1.5-3x normal
        "velocity_threshold": 5,                # Hard to detect
        "geographic_change_frequency": 0.2,    # Rare
        "merchant_change_frequency": 0.15,     # Very rare
        "fraud_subtlety": 0.9,                 # Subtle
    },
}

# Reward Schemes
REWARD_SCHEMES = {
    "balanced": {
        "fraud_detected_correct": 10.0,
        "legitimate_correct": 2.0,
        "fraud_missed": -10.0,
        "false_positive": -5.0,
        "fraud_bonus_multiplier": 1.0,
        "legitimate_bonus_multiplier": 1.0,
    },
    "conservative": {
        "fraud_detected_correct": 10.0,
        "legitimate_correct": 2.0,
        "fraud_missed": -10.0,
        "false_positive": -8.0,  # Heavier penalty
        "fraud_bonus_multiplier": 1.0,
        "legitimate_bonus_multiplier": 1.5,  # Reward right decisions more
    },
    "aggressive": {
        "fraud_detected_correct": 15.0,  # Higher reward
        "legitimate_correct": 2.0,
        "fraud_missed": -15.0,
        "false_positive": -3.0,  # Lighter penalty
        "fraud_bonus_multiplier": 1.5,  # Reward fraud detection more
        "legitimate_bonus_multiplier": 1.0,
    },
}

# Transaction Categories
TRANSACTION_TYPES = [
    "transfer",
    "payment", 
    "withdrawal",
    "deposit",
    "utility_bill",
    "shopping",
    "subscription",
]

MERCHANT_CATEGORIES = [
    "retail",
    "online",
    "utility",
    "transport",
    "food",
    "entertainment",
    "bank",
    "atm",
    "p2p",
]

HIGH_RISK_MERCHANT_CATEGORIES = [
    "cryptocurrency",
    "gambling",
    "wire_transfer",
    "unlicensed_lending",
    "suspicious",
]

# Feature Normalization
FEATURE_NORMALIZATION = {
    "amount_zscore": {"min": -10, "max": 10},
    "amount": {"min": 0, "max": 500000},
    "transactions_last_1h": {"min": 0, "max": 100},
    "new_merchant": {"min": 0, "max": 1},
    "location_change": {"min": 0, "max": 1},
    "is_international": {"min": 0, "max": 1},
    "unique_merchants": {"min": 0, "max": 1000},
    "fraud_history_rate": {"min": 0, "max": 1},
    "device_changes": {"min": 0, "max": 10},
    "account_age_days": {"min": 0, "max": 3650},
}

# Fraud Pattern Probabilities (for "medium" difficulty)
FRAUD_PATTERN_PROBABILITIES = {
    "amount_anomaly": 0.15,
    "geographic_anomaly": 0.10,
    "velocity_fraud": 0.12,
    "unusual_merchant": 0.11,
    "account_compromise": 0.18,
    "test_transaction": 0.08,
    "synthetic_identity": 0.09,
    "fraud_ring": 0.17,
}

# Agent Configuration Templates
AGENT_TEMPLATES = {
    "conservative": {
        "amount_zscore_threshold": 3.0,
        "velocity_threshold": 15,
        "new_merchant_international_weight": 0.8,
        "require_multiple_indicators": True,
    },
    "balanced": {
        "amount_zscore_threshold": 2.0,
        "velocity_threshold": 8,
        "new_merchant_international_weight": 0.5,
        "require_multiple_indicators": False,
    },
    "aggressive": {
        "amount_zscore_threshold": 1.5,
        "velocity_threshold": 5,
        "new_merchant_international_weight": 0.3,
        "require_multiple_indicators": False,
    },
}

# Performance Metrics Thresholds
PERFORMANCE_THRESHOLDS = {
    "excellent_accuracy": 0.85,
    "good_accuracy": 0.75,
    "acceptable_accuracy": 0.65,
    "excellent_precision": 0.90,
    "good_precision": 0.80,
    "excellent_recall": 0.80,
    "good_recall": 0.70,
}

# Default Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "guardianai.log",
}

# Environment Limits (for resource management)
ENVIRONMENT_LIMITS = {
    "max_accounts": 100000,
    "max_episodes": 10000,
    "max_transactions_per_episode": 10000,
    "max_history_per_account": 1000,
}

# Testing Configuration
TEST_CONFIG = {
    "num_test_episodes": 10,
    "num_test_transactions": 1000,
    "test_seed": 42,
    "test_difficulties": ["easy", "medium", "hard"],
}
