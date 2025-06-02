#!/usr/bin/env python3
"""
Social Media Dashboard
Comprehensive social media management and analytics dashboard.
"""

from flask import Flask, render_template_string, jsonify, request
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

app = Flask(__name__)

# Mock social media data
class SocialMediaData:
    def __init__(self):
        self.platforms = ['Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'TikTok']
        self.generate_mock_data()
    
    def generate_mock_data(self):
        """Generate mock social media data."""
        self.accounts = {
            'Facebook': {
                'followers': 15420,
                'engagement_rate': 3.2,
                'posts_today': 2,
                'reach': 8500,
                'color': '#1877F2'
            },
            'Instagram': {
                'followers': 23150,
                'engagement_rate': 4.8,
                'posts_today': 3,
                'reach': 12300,
                'color': '#E4405F'
            },
            'Twitter': {
                'followers': 8930,
                'engagement_rate': 2.1,
                'posts_today': 5,
                'reach': 5200,
                'color': '#1DA1F2'
            },
            'LinkedIn': {
                'followers': 5670,
                'engagement_rate': 5.2,
                'posts_today': 1,
                'reach': 3400,
                'color': '#0A66C2'
            },
            'TikTok': {
                'followers': 45200,
                'engagement_rate': 7.8,
                'posts_today': 2,
                'reach': 28900,
                'color': '#000000'
            }
        }
        
        # Generate analytics data for the last 30 days
        self.analytics_data = []
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            for platform in self.platforms:
                self.analytics_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'platform': platform,
                    'followers': self.accounts[platform]['followers'] + random.randint(-50, 100),
                    'engagement': random.uniform(1, 10),
                    'reach': random.randint(1000, 30000),
                    'posts': random.randint(0, 5)
                })
        
        # Generate recent posts
        self.recent_posts = []
        for i in range(20):
            platform = random.choice(self.platforms)
            self.recent_posts.append({
                'id': i + 1,
                'platform': platform,
                'content': f"Sample post content for {platform} #{i+1}",
                'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat(),
                'likes': random.randint(10, 500),
                'comments': random.randint(2, 50),
                'shares': random.randint(1, 25),
                'engagement_rate': random.uniform(2, 8)
            })
        
        self.recent_posts.sort(key=lambda x: x['timestamp'], reverse=True)

social_data = SocialMediaData()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #7f8c8d;
            font-size: 1.1rem;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--platform-color);
        }
        
        .platform-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        
        .platform-name {
            font-size: 1.2rem;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .platform-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--platform-color);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .metric {
            margin-bottom: 15px;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .metric-change {
            font-size: 0.8rem;
            margin-left: 10px;
        }
        
        .positive { color: #27ae60; }
        .negative { color: #e74c3c; }
        
        .charts-section {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .chart-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .posts-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .post-item {
            border-bottom: 1px solid #ecf0f1;
            padding: 20px 0;
            transition: background 0.3s ease;
        }
        
        .post-item:hover {
            background: #f8f9fa;
            border-radius: 10px;
            margin: 0 -10px;
            padding: 20px 10px;
        }
        
        .post-header {
            display: flex;
            align-items: center;
            justify-content: between;
            margin-bottom: 10px;
        }
        
        .post-platform {
            background: var(--platform-color);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .post-time {
            color: #7f8c8d;
            font-size: 0.9rem;
            margin-left: auto;
        }
        
        .post-content {
            color: #2c3e50;
            margin-bottom: 15px;
            line-height: 1.5;
        }
        
        .post-metrics {
            display: flex;
            gap: 20px;
            font-size: 0.9rem;
            color: #7f8c8d;
        }
        
        .controls {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 500;
            transition: transform 0.3s ease;
            margin-right: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .charts-section {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>📱 Social Media Dashboard</h1>
            <p>Monitor and manage your social media presence across all platforms</p>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="refreshData()">🔄 Refresh Data</button>
            <button class="btn" onclick="exportReport()">📊 Export Report</button>
            <button class="btn" onclick="schedulePost()">📝 Schedule Post</button>
        </div>
        
        <div class="stats-grid" id="statsGrid">
            <!-- Platform stats will be loaded here -->
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <h3 class="chart-title">📈 Engagement Trends (Last 7 Days)</h3>
                <canvas id="engagementChart"></canvas>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">🎯 Platform Distribution</h3>
                <canvas id="platformChart"></canvas>
            </div>
        </div>
        
        <div class="posts-section">
            <h3 class="chart-title">📋 Recent Posts</h3>
            <div id="recentPosts">
                <!-- Recent posts will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        let engagementChart, platformChart;
        
        async function loadDashboard() {
            await loadStats();
            await loadCharts();
            await loadRecentPosts();
        }
        
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                const statsGrid = document.getElementById('statsGrid');
                statsGrid.innerHTML = '';
                
                Object.entries(data).forEach(([platform, stats]) => {
                    const card = document.createElement('div');
                    card.className = 'stat-card';
                    card.style.setProperty('--platform-color', stats.color);
                    
                    card.innerHTML = `
                        <div class="platform-header">
                            <div class="platform-name">${platform}</div>
                            <div class="platform-icon">${platform[0]}</div>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">Followers</div>
                            <div class="metric-value">
                                ${stats.followers.toLocaleString()}
                                <span class="metric-change positive">+${Math.floor(Math.random() * 100)}</span>
                            </div>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">Engagement Rate</div>
                            <div class="metric-value">${stats.engagement_rate}%</div>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">Posts Today</div>
                            <div class="metric-value">${stats.posts_today}</div>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">Reach</div>
                            <div class="metric-value">${stats.reach.toLocaleString()}</div>
                        </div>
                    `;
                    
                    statsGrid.appendChild(card);
                });
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function loadCharts() {
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();
                
                // Engagement Chart
                const ctx1 = document.getElementById('engagementChart').getContext('2d');
                if (engagementChart) engagementChart.destroy();
                
                engagementChart = new Chart(ctx1, {
                    type: 'line',
                    data: {
                        labels: data.dates,
                        datasets: data.platforms.map((platform, index) => ({
                            label: platform.name,
                            data: platform.engagement,
                            borderColor: platform.color,
                            backgroundColor: platform.color + '20',
                            tension: 0.4
                        }))
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
                
                // Platform Distribution Chart
                const ctx2 = document.getElementById('platformChart').getContext('2d');
                if (platformChart) platformChart.destroy();
                
                platformChart = new Chart(ctx2, {
                    type: 'doughnut',
                    data: {
                        labels: data.platforms.map(p => p.name),
                        datasets: [{
                            data: data.platforms.map(p => p.followers),
                            backgroundColor: data.platforms.map(p => p.color),
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
                
            } catch (error) {
                console.error('Error loading charts:', error);
            }
        }
        
        async function loadRecentPosts() {
            try {
                const response = await fetch('/api/posts');
                const posts = await response.json();
                
                const postsContainer = document.getElementById('recentPosts');
                postsContainer.innerHTML = '';
                
                posts.forEach(post => {
                    const postElement = document.createElement('div');
                    postElement.className = 'post-item';
                    
                    const platformColors = {
                        'Facebook': '#1877F2',
                        'Instagram': '#E4405F',
                        'Twitter': '#1DA1F2',
                        'LinkedIn': '#0A66C2',
                        'TikTok': '#000000'
                    };
                    
                    postElement.innerHTML = `
                        <div class="post-header">
                            <span class="post-platform" style="background: ${platformColors[post.platform]}">${post.platform}</span>
                            <span class="post-time">${new Date(post.timestamp).toLocaleString()}</span>
                        </div>
                        <div class="post-content">${post.content}</div>
                        <div class="post-metrics">
                            <span>❤️ ${post.likes} likes</span>
                            <span>💬 ${post.comments} comments</span>
                            <span>🔄 ${post.shares} shares</span>
                            <span>📊 ${post.engagement_rate.toFixed(1)}% engagement</span>
                        </div>
                    `;
                    
                    postsContainer.appendChild(postElement);
                });
                
            } catch (error) {
                console.error('Error loading posts:', error);
            }
        }
        
        function refreshData() {
            loadDashboard();
        }
        
        function exportReport() {
            alert('Report export functionality would be implemented here');
        }
        
        function schedulePost() {
            alert('Post scheduling functionality would be implemented here');
        }
        
        // Load dashboard on page load
        loadDashboard();
        
        // Auto-refresh every 5 minutes
        setInterval(loadDashboard, 300000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    """Get platform statistics."""
    return jsonify(social_data.accounts)

@app.route('/api/analytics')
def get_analytics():
    """Get analytics data for charts."""
    # Process data for charts
    df = pd.DataFrame(social_data.analytics_data)
    
    # Get last 7 days
    recent_dates = pd.date_range(end=datetime.now().date(), periods=7).strftime('%m/%d').tolist()
    
    platforms_data = []
    for platform in social_data.platforms:
        platform_data = df[df['platform'] == platform].tail(7)
        platforms_data.append({
            'name': platform,
            'color': social_data.accounts[platform]['color'],
            'engagement': platform_data['engagement'].tolist(),
            'followers': social_data.accounts[platform]['followers']
        })
    
    return jsonify({
        'dates': recent_dates,
        'platforms': platforms_data
    })

@app.route('/api/posts')
def get_posts():
    """Get recent posts."""
    return jsonify(social_data.recent_posts[:10])

def main():
    """Main execution function."""
    print("Social Media Dashboard")
    print("=" * 25)
    
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

