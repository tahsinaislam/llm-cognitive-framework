"""
Profile Visualizer Module
Creates visualizations of cognitive profiles
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from pathlib import Path

class ProfileVisualizer:
    """Create visualizations of cognitive profiles"""
    
    def __init__(self):
        """Initialize the visualizer"""
        self.color_scheme = {
            'GPT-4': '#10B981',
            'Claude': '#8B5CF6', 
            'Gemini': '#3B82F6',
            'DeepSeek': '#F59E0B'
        }
        
        sns.set_theme(style="whitegrid")
    
    def create_comparative_plots(self, metrics: Dict[str, Dict], comparison: Dict) -> None:
        """Create all comparative visualizations"""
        output_dir = Path("visualizations")
        output_dir.mkdir(exist_ok=True)
        
        # Create individual plots
        self.create_radar_chart(metrics, output_dir)
        self.create_bar_comparison(metrics, output_dir)
        self.create_heatmap(metrics, output_dir)
        self.create_profile_dashboard(metrics, comparison, output_dir)
    
    def create_radar_chart(self, metrics: Dict[str, Dict], output_dir: Path) -> None:
        """Create radar chart comparing cognitive profiles"""
        
        categories = ['Working Memory', 'Executive Function', 'Flexibility', 
                     'Efficiency', 'Meta-Cognition']
        
        fig = go.Figure()
        
        for model_name, model_metrics in metrics.items():
            values = [
                model_metrics.get('wmi', 0),
                model_metrics.get('efs', 0),
                model_metrics.get('cognitive_flexibility', 0),
                model_metrics.get('processing_efficiency', 0),
                model_metrics.get('meta_cognitive_awareness', 0)
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=model_name,
                line_color=self.color_scheme.get(model_name, '#6B7280')
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Cognitive Profile Comparison",
            width=800,
            height=600
        )
        
        fig.write_html(str(output_dir / "cognitive_radar.html"))
        fig.write_image(str(output_dir / "cognitive_radar.png"))
    
    def create_bar_comparison(self, metrics: Dict[str, Dict], output_dir: Path) -> None:
        """Create grouped bar chart for metrics comparison"""
        
        # Prepare data
        data = []
        metric_names = {
            'wmi': 'Working Memory Index',
            'efs': 'Executive Function Score',
            'cognitive_flexibility': 'Cognitive Flexibility',
            'processing_efficiency': 'Processing Efficiency',
            'meta_cognitive_awareness': 'Meta-Cognitive Awareness'
        }
        
        for model_name, model_metrics in metrics.items():
            for metric_key, metric_label in metric_names.items():
                data.append({
                    'Model': model_name,
                    'Metric': metric_label,
                    'Score': model_metrics.get(metric_key, 0)
                })
        
        df = pd.DataFrame(data)
        
        # Create plotly figure
        fig = px.bar(df, x='Metric', y='Score', color='Model',
                    barmode='group',
                    title='Cognitive Metrics Comparison',
                    color_discrete_map=self.color_scheme)
        
        fig.update_layout(
            xaxis_tickangle=-45,
            width=1000,
            height=600,
            yaxis_range=[0, 1]
        )
        
        fig.write_html(str(output_dir / "metrics_comparison.html"))
        fig.write_image(str(output_dir / "metrics_comparison.png"))
    
    def create_heatmap(self, metrics: Dict[str, Dict], output_dir: Path) -> None:
        """Create heatmap of all metrics"""
        
        # Prepare data matrix
        metric_names = ['wmi', 'efs', 'cognitive_flexibility', 
                       'processing_efficiency', 'meta_cognitive_awareness']
        
        models = list(metrics.keys())
        data_matrix = []
        
        for model in models:
            row = [metrics[model].get(metric, 0) for metric in metric_names]
            data_matrix.append(row)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=data_matrix,
            x=['Working Memory', 'Executive Function', 'Flexibility', 
               'Efficiency', 'Meta-Cognition'],
            y=models,
            colorscale='Viridis',
            text=[[f'{val:.2f}' for val in row] for row in data_matrix],
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Score")
        ))
        
        fig.update_layout(
            title='Cognitive Metrics Heatmap',
            width=800,
            height=500
        )
        
        fig.write_html(str(output_dir / "metrics_heatmap.html"))
        fig.write_image(str(output_dir / "metrics_heatmap.png"))
    
    def create_profile_dashboard(self, metrics: Dict[str, Dict], 
                                comparison: Dict, output_dir: Path) -> None:
        """Create comprehensive dashboard with all visualizations"""
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Overall Scores', 'Reasoning Styles', 
                          'Integration Patterns', 'Error Profiles'),
            specs=[[{'type': 'bar'}, {'type': 'pie'}],
                  [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        models = list(metrics.keys())
        
        # 1. Overall scores
        overall_scores = [metrics[m].get('composite_profile', {}).get('overall_score', 0) 
                         for m in models]
        fig.add_trace(
            go.Bar(x=models, y=overall_scores, name='Overall Score',
                  marker_color=[self.color_scheme.get(m, '#6B7280') for m in models]),
            row=1, col=1
        )
        
        # 2. Reasoning styles distribution
        reasoning_styles = {}
        for model in models:
            style = metrics[model].get('reasoning_style', 'unknown')
            reasoning_styles[style] = reasoning_styles.get(style, 0) + 1
        
        fig.add_trace(
            go.Pie(labels=list(reasoning_styles.keys()), 
                  values=list(reasoning_styles.values()),
                  name='Reasoning Styles'),
            row=1, col=2
        )
        
        # 3. Integration patterns
        integration_data = []
        for model in models:
            pattern = metrics[model].get('integration_pattern', 'unknown')
            integration_data.append(pattern)
        
        pattern_counts = pd.Series(integration_data).value_counts()
        fig.add_trace(
            go.Bar(x=pattern_counts.index, y=pattern_counts.values,
                  name='Integration Patterns'),
            row=2, col=1
        )
        
        # 4. Error profiles
        error_rates = [metrics[m].get('error_profile', {}).get('error_rate', 0) 
                      for m in models]
        fig.add_trace(
            go.Bar(x=models, y=error_rates, name='Error Rate',
                  marker_color='indianred'),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Cognitive Profile Dashboard",
            showlegend=False,
            width=1400,
            height=800
        )
        
        fig.write_html(str(output_dir / "cognitive_dashboard.html"))
    
    def create_individual_profile(self, model_name: str, metrics: Dict, 
                                 output_dir: Path) -> None:
        """Create detailed profile for a single model"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Cognitive Metrics', 'Response Patterns', 
                          'Processing Style', 'Strengths & Weaknesses'),
            specs=[[{'type': 'bar'}, {'type': 'scatter'}],
                  [{'type': 'pie'}, {'type': 'bar'}]]
        )
        
        # Cognitive metrics bar
        metric_names = ['wmi', 'efs', 'cognitive_flexibility', 
                       'processing_efficiency', 'meta_cognitive_awareness']
        metric_labels = ['WMI', 'EFS', 'Flexibility', 'Efficiency', 'Meta-Cog']
        values = [metrics.get(m, 0) for m in metric_names]
        
        fig.add_trace(
            go.Bar(x=metric_labels, y=values, 
                  marker_color=self.color_scheme.get(model_name, '#6B7280')),
            row=1, col=1
        )
        
        # Add more visualizations based on available data
        
        fig.update_layout(
            title_text=f"Cognitive Profile: {model_name}",
            showlegend=False,
            width=1200,
            height=700
        )
        
        fig.write_html(str(output_dir / f"profile_{model_name.lower().replace(' ', '_')}.html"))
    
    def create_comparison_matrix(self, comparison: Dict, output_dir: Path) -> None:
        """Create comparison matrix visualization"""
        
        if 'statistical_tests' not in comparison:
            return
        
        stats = comparison['statistical_tests']
        
        # Create DataFrame for visualization
        data = []
        for metric, values in stats.items():
            data.append({
                'Metric': metric,
                'Mean': values['mean'],
                'Std Dev': values['std'],
                'CV': values['cv'],
                'Range': values['range']
            })
        
        df = pd.DataFrame(data)
        
        # Create figure
        fig = go.Figure()
        
        # Add bars for each statistic
        fig.add_trace(go.Bar(name='Mean', x=df['Metric'], y=df['Mean']))
        fig.add_trace(go.Bar(name='Std Dev', x=df['Metric'], y=df['Std Dev']))
        fig.add_trace(go.Bar(name='Range', x=df['Metric'], y=df['Range']))
        
        fig.update_layout(
            title='Statistical Comparison of Metrics',
            barmode='group',
            width=1000,
            height=600
        )
        
        fig.write_html(str(output_dir / "statistical_comparison.html"))
