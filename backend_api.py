"""
Flask API Backend for GuardianAI Dashboard
Provides endpoints for live transactions, fraud alerts, and analytics.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import random
import numpy as np
from collections import defaultdict, deque
from typing import Dict, List, Optional

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# In-memory data store
class DataStore:
    """In-memory store for transaction and analytics data."""
    
    def __init__(self):
        self.transactions = deque(maxlen=1000)  # Keep last 1000 transactions
        self.fraud_alerts = deque(maxlen=100)   # Keep last 100 alerts
        self.risk_scores = {}  # user_id -> risk_score
        self.fraud_statistics = {
            'hourly': defaultdict(int),
            'daily': defaultdict(int),
            'by_category': defaultdict(int),
            'by_pattern': defaultdict(int),
        }
    
    def add_transaction(self, transaction: Dict) -> None:
        """Add transaction to store."""
        self.transactions.append(transaction)
        
    def add_fraud_alert(self, alert: Dict) -> None:
        """Add fraud alert."""
        self.fraud_alerts.append(alert)
        
    def update_risk_score(self, user_id: int, score: float) -> None:
        """Update user risk score."""
        self.risk_scores[user_id] = {
            'score': max(0, min(100, score)),
            'timestamp': datetime.now().isoformat(),
            'level': self._score_to_level(score)
        }
    
    def _score_to_level(self, score: float) -> str:
        """Convert score to risk level."""
        if score < 20:
            return 'LOW'
        elif score < 50:
            return 'MEDIUM'
        elif score < 80:
            return 'HIGH'
        else:
            return 'CRITICAL'
    
    def get_recent_transactions(self, limit: int = 20) -> List[Dict]:
        """Get recent transactions."""
        return list(self.transactions)[-limit:][::-1]
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent fraud alerts."""
        return list(self.fraud_alerts)[-limit:][::-1]
    
    def get_risk_scores_top(self, limit: int = 10) -> List[Dict]:
        """Get top users by risk score."""
        users = sorted(
            self.risk_scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )[:limit]
        return [
            {
                'user_id': uid,
                **score_info
            }
            for uid, score_info in users
        ]
    
    def get_fraud_statistics(self) -> Dict:
        """Get fraud statistics."""
        return {
            'hourly': dict(self.fraud_statistics['hourly']),
            'daily': dict(self.fraud_statistics['daily']),
            'by_category': dict(self.fraud_statistics['by_category']),
            'by_pattern': dict(self.fraud_statistics['by_pattern']),
        }

# Initialize data store
store = DataStore()


# ============================================================================
# Transaction Generation (Simulates Real Data)
# ============================================================================

def generate_mock_transaction() -> Dict:
    """Generate a mock transaction for demonstration."""
    user_id = random.randint(1000, 5000)
    amount = round(random.lognormvariate(8.5, 1.5), 2)  # Realistic amount distribution
    
    merchants = ['Amazon', 'Flipkart', 'Uber', 'Swiggy', 'PayTM', 'PhonePe',
                 'HDFC Bank', 'ICICI', 'Local Grocery', 'Gas Station', 'Hospital']
    categories = ['shopping', 'food', 'transport', 'utility', 'entertainment', 'bank']
    
    is_fraud = random.random() < 0.02  # 2% fraud rate
    
    return {
        'transaction_id': f'TXN{random.randint(100000, 999999)}',
        'user_id': user_id,
        'timestamp': datetime.now().isoformat(),
        'amount': amount,
        'merchant': random.choice(merchants),
        'category': random.choice(categories),
        'location': random.choice(['New Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Pune']),
        'device_id': f'DEV{random.randint(1000, 9999)}',
        'is_fraud': is_fraud,
        'fraud_pattern': random.choice([
            'amount_anomaly', 'geographic_anomaly', 'velocity_fraud',
            'unusual_merchant', 'account_compromise', 'none'
        ]) if is_fraud else 'none',
        'confidence': round(random.uniform(0.7, 1.0), 2),
        'risk_score': round(random.uniform(0, 100), 1) if is_fraud else round(random.uniform(0, 30), 1),
    }


def generate_mock_alert() -> Optional[Dict]:
    """Generate a mock fraud alert."""
    if random.random() < 0.1:  # 10% chance of alert
        patterns = ['amount_anomaly', 'geographic_anomaly', 'velocity_fraud',
                   'unusual_merchant', 'account_compromise']
        return {
            'alert_id': f'ALERT{random.randint(100000, 999999)}',
            'transaction_id': f'TXN{random.randint(100000, 999999)}',
            'user_id': random.randint(1000, 5000),
            'timestamp': datetime.now().isoformat(),
            'pattern': random.choice(patterns),
            'confidence': round(random.uniform(0.75, 0.99), 2),
            'amount': round(random.uniform(1000, 50000), 2),
            'merchant': random.choice(['Anonymous', 'Unknown Vendor', 'Suspicious Shop']),
            'severity': random.choice(['MEDIUM', 'HIGH', 'CRITICAL']),
            'action': 'blocked' if random.random() < 0.7 else 'flagged'
        }
    return None


# ============================================================================
# API Endpoints
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'transactions_count': len(store.transactions),
        'alerts_count': len(store.fraud_alerts),
    })


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get recent transactions."""
    limit = request.args.get('limit', 20, type=int)
    transactions = store.get_recent_transactions(limit)
    return jsonify({
        'status': 'success',
        'data': transactions,
        'count': len(transactions),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/transactions/stream', methods=['GET'])
def stream_transactions():
    """Get streaming transaction data (for polling)."""
    # Generate new mock transactions
    for _ in range(random.randint(1, 3)):
        tx = generate_mock_transaction()
        store.add_transaction(tx)
        
        # Update fraud stats
        store.fraud_statistics['by_category'][tx['category']] += 1
        if tx['is_fraud']:
            store.fraud_statistics['by_pattern'][tx['fraud_pattern']] += 1
    
    transactions = store.get_recent_transactions(10)
    return jsonify({
        'status': 'success',
        'data': transactions,
        'count': len(transactions),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get recent fraud alerts."""
    limit = request.args.get('limit', 10, type=int)
    alerts = store.get_recent_alerts(limit)
    return jsonify({
        'status': 'success',
        'data': alerts,
        'count': len(alerts),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/alerts/stream', methods=['GET'])
def stream_alerts():
    """Get streaming alert data (for polling)."""
    # Generate new mock alerts
    for _ in range(random.randint(0, 2)):
        alert = generate_mock_alert()
        if alert:
            store.add_fraud_alert(alert)
    
    alerts = store.get_recent_alerts(5)
    return jsonify({
        'status': 'success',
        'data': alerts,
        'new_count': len(alerts),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/scoring/risk', methods=['GET'])
def get_risk_scores():
    """Get top users by risk score."""
    limit = request.args.get('limit', 10, type=int)
    
    # Update risk scores with random users
    for _ in range(5):
        user_id = random.randint(1000, 5000)
        risk_score = random.uniform(0, 100)
        store.update_risk_score(user_id, risk_score)
    
    top_users = store.get_risk_scores_top(limit)
    return jsonify({
        'status': 'success',
        'data': top_users,
        'count': len(top_users),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/scoring/risk/<int:user_id>', methods=['GET'])
def get_user_risk_score(user_id: int):
    """Get risk score for specific user."""
    if user_id not in store.risk_scores:
        store.update_risk_score(user_id, random.uniform(0, 100))
    
    score_info = store.risk_scores[user_id]
    return jsonify({
        'status': 'success',
        'user_id': user_id,
        'data': score_info,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Get comprehensive dashboard analytics."""
    total_transactions = len(store.transactions)
    total_alerts = len(store.fraud_alerts)
    fraud_transactions = sum(1 for tx in store.transactions if tx.get('is_fraud'))
    
    fraud_rate = (fraud_transactions / total_transactions * 100) if total_transactions > 0 else 0
    alert_rate = (total_alerts / total_transactions * 100) if total_transactions > 0 else 0
    
    return jsonify({
        'status': 'success',
        'summary': {
            'total_transactions': total_transactions,
            'total_alerts': total_alerts,
            'fraud_count': fraud_transactions,
            'fraud_rate': round(fraud_rate, 2),
            'alert_rate': round(alert_rate, 2),
        },
        'top_users_by_risk': store.get_risk_scores_top(5),
        'fraud_by_category': dict(store.fraud_statistics['by_category']),
        'fraud_by_pattern': dict(store.fraud_statistics['by_pattern']),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/analytics/trends', methods=['GET'])
def get_fraud_trends():
    """Get fraud trends for charting."""
    time_period = request.args.get('period', 'hourly', type=str)
    
    # Generate hourly trend data for last 24 hours
    trend_data = []
    for hours_ago in range(24, 0, -1):
        timestamp = datetime.now() - timedelta(hours=hours_ago)
        hour_key = timestamp.strftime('%Y-%m-%d %H:00')
        
        # Simulate trend data
        fraud_count = random.randint(0, 10)
        transaction_count = random.randint(50, 200)
        
        trend_data.append({
            'timestamp': hour_key,
            'fraud_count': fraud_count,
            'transaction_count': transaction_count,
            'fraud_rate': round((fraud_count / transaction_count * 100), 2) if transaction_count > 0 else 0,
            'alert_count': random.randint(0, 5),
        })
    
    return jsonify({
        'status': 'success',
        'period': time_period,
        'data': trend_data,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/analytics/risk-distribution', methods=['GET'])
def get_risk_distribution():
    """Get risk score distribution."""
    # Generate mock distribution
    distribution = {
        'LOW': random.randint(3000, 4000),
        'MEDIUM': random.randint(500, 1000),
        'HIGH': random.randint(100, 300),
        'CRITICAL': random.randint(10, 50),
    }
    
    total = sum(distribution.values())
    distribution_percentage = {
        level: round((count / total * 100), 2)
        for level, count in distribution.items()
    }
    
    return jsonify({
        'status': 'success',
        'distribution': distribution,
        'percentage': distribution_percentage,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/analytics/performance', methods=['GET'])
def get_performance_metrics():
    """Get system performance metrics."""
    return jsonify({
        'status': 'success',
        'metrics': {
            'api_response_time_ms': round(random.uniform(50, 150), 2),
            'model_detection_time_ms': round(random.uniform(10, 50), 2),
            'database_query_time_ms': round(random.uniform(5, 30), 2),
            'false_positive_rate': round(random.uniform(0.1, 5), 2),
            'true_positive_rate': round(random.uniform(85, 98), 2),
            'system_uptime_percentage': round(random.uniform(99.5, 99.99), 2),
        },
        'timestamp': datetime.now().isoformat()
    })


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'error': str(error)
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'error': str(error)
    }), 500

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'error': str(error)
    }), 500


# =========================
# OPENENV REQUIRED ENDPOINTS
# =========================

@app.route('/reset', methods=['POST'])
def reset_environment():
    global store
    store = DataStore()
    return jsonify({
        "status": "reset",
        "state": {
            "step": 0,
            "transactions_processed": 0,
            "fraud_detected": 0
        }
    })


@app.route('/state', methods=['GET'])
def get_state():
    return jsonify({
        "state": {
            "transactions": len(store.transactions),
            "alerts": len(store.fraud_alerts)
        }
    })


@app.route('/step', methods=['POST'])
def step_environment():
    action = request.json.get("action", "scan")

    tx = generate_mock_transaction()
    store.add_transaction(tx)

    reward = 1.0 if tx["is_fraud"] else 0.0

    return jsonify({
        "reward": reward,
        "done": False,
        "info": {
            "transaction_id": tx["transaction_id"],
            "fraud": tx["is_fraud"]
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)

