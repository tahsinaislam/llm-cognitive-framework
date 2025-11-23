"""
Metric Calculator Module
Calculates cognitive metrics from analysis results
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from scipy import stats
from sklearn.preprocessing import StandardScaler
import pandas as pd

class MetricCalculator:
    """Calculate cognitive metrics from analysis results"""
    
    def __init__(self):
        """Initialize the metric calculator"""
        self.metric_weights = {
            'wmi': {  # Working Memory Index weights
                'sequential_processing': 0.3,
                'information_retention': 0.3,
                'concurrent_processing': 0.2,
                'chunking_ability': 0.2
            },
            'efs': {  # Executive Function Score weights
                'task_switching': 0.25,
                'inhibition': 0.25,
                'updating': 0.25,
                'planning': 0.25
            }
        }
        
        self.scaler = StandardScaler()
    
    def calculate_metrics(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate cognitive metrics from analysis results"""
        metrics = {
            'wmi': self._calculate_working_memory_index(analysis_results),
            'efs': self._calculate_executive_function_score(analysis_results),
            'reasoning_style': self._determine_reasoning_style(analysis_results),
            'integration_pattern': self._analyze_integration_pattern(analysis_results),
            'cognitive_flexibility': self._calculate_flexibility(analysis_results),
            'processing_efficiency': self._calculate_efficiency(analysis_results),
            'error_profile': self._analyze_error_patterns(analysis_results),
            'meta_cognitive_awareness': self._calculate_meta_cognitive_score(analysis_results)
        }
        
        # Calculate composite cognitive profile
        metrics['composite_profile'] = self._calculate_composite_profile(metrics)
        
        return metrics
    
    def _calculate_working_memory_index(self, analysis: Dict) -> float:
        """Calculate Working Memory Index (WMI)"""
        wmi_components = {
            'sequential_processing': 0,
            'information_retention': 0,
            'concurrent_processing': 0,
            'chunking_ability': 0
        }
        
        patterns = analysis.get('patterns', {})
        structure_metrics = analysis.get('structure_metrics', [])
        
        # Sequential processing: based on sequential markers and structure
        if patterns.get('sequential_markers', 0) > 0:
            wmi_components['sequential_processing'] = min(patterns['sequential_markers'] / 10, 1.0)
        
        # Information retention: based on response completeness and accuracy
        # This would ideally compare against correct answers
        if structure_metrics:
            avg_response_length = np.mean([s['num_sentences'] for s in structure_metrics])
            wmi_components['information_retention'] = min(avg_response_length / 10, 1.0)
        
        # Concurrent processing: ability to handle multiple constraints
        complexity_scores = analysis.get('integration_complexity', [])
        if complexity_scores:
            avg_complexity = np.mean([c['noun_phrases'] for c in complexity_scores])
            wmi_components['concurrent_processing'] = min(avg_complexity / 5, 1.0)
        
        # Chunking ability
        if patterns.get('uses_chunking', 0) > 0:
            wmi_components['chunking_ability'] = min(patterns['uses_chunking'] / 5, 1.0)
        
        # Calculate weighted WMI
        wmi = sum(wmi_components[key] * self.metric_weights['wmi'][key] 
                 for key in wmi_components)
        
        return round(wmi, 3)
    
    def _calculate_executive_function_score(self, analysis: Dict) -> float:
        """Calculate Executive Function Score (EFS)"""
        efs_components = {
            'task_switching': 0,
            'inhibition': 0,
            'updating': 0,
            'planning': 0
        }
        
        patterns = analysis.get('patterns', {})
        
        # Task switching ability
        if patterns.get('explicit_switching', 0) > 0:
            efs_components['task_switching'] = min(patterns['explicit_switching'] / 5, 1.0)
        
        # Inhibition success
        if patterns.get('inhibition_success', 0) > 0:
            efs_components['inhibition'] = min(patterns['inhibition_success'] / 5, 1.0)
        
        # Updating ability (meta-cognitive awareness serves as proxy)
        meta_score = analysis.get('meta_cognitive_score', 0)
        num_responses = len(analysis.get('structure_metrics', [1]))  # Avoid division by zero
        efs_components['updating'] = min(meta_score / num_responses, 1.0)
        
        # Planning ability (based on structural organization)
        structure_metrics = analysis.get('structure_metrics', [])
        if structure_metrics:
            has_lists = sum(1 for s in structure_metrics if s.get('has_list') or s.get('has_numbered_list'))
            efs_components['planning'] = min(has_lists / len(structure_metrics), 1.0)
        
        # Calculate weighted EFS
        efs = sum(efs_components[key] * self.metric_weights['efs'][key] 
                 for key in efs_components)
        
        return round(efs, 3)
    
    def _determine_reasoning_style(self, analysis: Dict) -> str:
        """Determine dominant reasoning style"""
        reasoning_styles = analysis.get('reasoning_styles', {})
        
        if not reasoning_styles:
            return "mixed"
        
        # Get the most common reasoning style
        style_counts = dict(reasoning_styles)
        total = sum(style_counts.values())
        
        if total == 0:
            return "mixed"
        
        # Calculate percentages
        style_percentages = {style: count/total for style, count in style_counts.items()}
        
        # Determine if there's a dominant style (>40% usage)
        max_style = max(style_percentages, key=style_percentages.get)
        if style_percentages[max_style] > 0.4:
            style_map = {
                'deductive': 'sequential-deductive',
                'inductive': 'pattern-inductive',
                'analogical': 'associative-analogical',
                'causal': 'causal-mechanistic'
            }
            return style_map.get(max_style, max_style)
        else:
            return "mixed-flexible"
    
    def _analyze_integration_pattern(self, analysis: Dict) -> str:
        """Analyze information integration patterns"""
        patterns = analysis.get('patterns', {})
        complexity_metrics = analysis.get('integration_complexity', [])
        
        if not complexity_metrics:
            return "unknown"
        
        # Calculate integration metrics
        avg_connections = patterns.get('makes_connections', 0) / max(len(complexity_metrics), 1)
        avg_synthesis = patterns.get('synthesis_depth', 0) / max(len(complexity_metrics), 1)
        avg_lexical_div = np.mean([c['lexical_diversity'] for c in complexity_metrics])
        
        # Determine pattern based on metrics
        if avg_connections > 2 and avg_lexical_div > 0.6:
            return "web-like-associative"
        elif avg_synthesis > 2 and avg_lexical_div > 0.5:
            return "deep-hierarchical"
        elif avg_connections > 1 or avg_synthesis > 1:
            return "moderate-structured"
        else:
            return "linear-sequential"
    
    def _calculate_flexibility(self, analysis: Dict) -> float:
        """Calculate cognitive flexibility score"""
        reasoning_styles = analysis.get('reasoning_styles', {})
        patterns = analysis.get('patterns', {})
        
        # Flexibility indicated by:
        # 1. Variety in reasoning styles
        # 2. Ability to switch between approaches
        # 3. Meta-cognitive awareness
        
        style_variety = len([s for s in reasoning_styles.values() if s > 0])
        switching_ability = patterns.get('explicit_switching', 0)
        meta_score = analysis.get('meta_cognitive_score', 0)
        
        flexibility = (
            (style_variety / 4) * 0.4 +  # Max 4 reasoning styles
            min(switching_ability / 5, 1.0) * 0.3 +
            min(meta_score / len(analysis.get('structure_metrics', [1])), 1.0) * 0.3
        )
        
        return round(flexibility, 3)
    
    def _calculate_efficiency(self, analysis: Dict) -> float:
        """Calculate processing efficiency"""
        structure_metrics = analysis.get('structure_metrics', [])
        error_patterns = analysis.get('error_patterns', {})
        
        if not structure_metrics:
            return 0.0
        
        # Efficiency based on:
        # 1. Conciseness (not overly verbose)
        # 2. Low error rate
        # 3. Appropriate complexity for task
        
        avg_length = np.mean([s['num_sentences'] for s in structure_metrics])
        optimal_length = 5  # Assumed optimal response length
        length_efficiency = 1.0 - min(abs(avg_length - optimal_length) / optimal_length, 1.0)
        
        total_responses = len(structure_metrics)
        error_rate = sum(error_patterns.values()) / max(total_responses, 1)
        error_efficiency = 1.0 - error_rate
        
        complexity_metrics = analysis.get('integration_complexity', [])
        if complexity_metrics:
            avg_complexity = np.mean([c['dependency_depth'] for c in complexity_metrics])
            optimal_complexity = 3.5  # Assumed optimal complexity
            complexity_efficiency = 1.0 - min(abs(avg_complexity - optimal_complexity) / optimal_complexity, 1.0)
        else:
            complexity_efficiency = 0.5
        
        efficiency = (length_efficiency * 0.3 + 
                     error_efficiency * 0.4 + 
                     complexity_efficiency * 0.3)
        
        return round(efficiency, 3)
    
    def _analyze_error_patterns(self, analysis: Dict) -> Dict[str, Any]:
        """Analyze patterns in errors"""
        error_patterns = analysis.get('error_patterns', {})
        patterns = analysis.get('patterns', {})
        
        error_profile = {
            'error_rate': sum(error_patterns.values()) / max(len(analysis.get('structure_metrics', [1])), 1),
            'error_types': dict(error_patterns),
            'recovery_ability': patterns.get('self_correction', 0) / max(sum(error_patterns.values()), 1) if error_patterns else 1.0
        }
        
        # Classify error tendency
        if error_profile['error_rate'] < 0.1:
            error_profile['tendency'] = 'low-error-robust'
        elif error_profile['error_rate'] < 0.25:
            error_profile['tendency'] = 'moderate-error-recoverable'
        else:
            error_profile['tendency'] = 'high-error-fragile'
        
        return error_profile
    
    def _calculate_meta_cognitive_score(self, analysis: Dict) -> float:
        """Calculate meta-cognitive awareness score"""
        meta_score = analysis.get('meta_cognitive_score', 0)
        num_responses = len(analysis.get('structure_metrics', [1]))
        
        patterns = analysis.get('patterns', {})
        
        # Meta-cognitive awareness based on:
        # 1. Use of meta-cognitive markers
        # 2. Self-explanation
        # 3. Strategy awareness
        # 4. Confidence calibration
        
        base_score = meta_score / max(num_responses, 1)
        explanation_score = patterns.get('explains_thinking', 0) / max(num_responses, 1)
        strategy_score = patterns.get('explicit_strategy', 0) / max(num_responses, 1)
        evaluation_score = patterns.get('evaluates_answer', 0) / max(num_responses, 1)
        
        meta_cognitive_awareness = (
            base_score * 0.3 +
            explanation_score * 0.3 +
            strategy_score * 0.2 +
            evaluation_score * 0.2
        )
        
        return round(meta_cognitive_awareness, 3)
    
    def _calculate_composite_profile(self, metrics: Dict) -> Dict[str, Any]:
        """Calculate composite cognitive profile"""
        # Create a multi-dimensional profile
        profile = {
            'memory_processing': metrics['wmi'],
            'executive_control': metrics['efs'],
            'flexibility': metrics['cognitive_flexibility'],
            'efficiency': metrics['processing_efficiency'],
            'meta_awareness': metrics['meta_cognitive_awareness'],
            'primary_style': metrics['reasoning_style'],
            'integration_type': metrics['integration_pattern']
        }
        
        # Calculate overall cognitive score
        numerical_metrics = [
            metrics['wmi'],
            metrics['efs'],
            metrics['cognitive_flexibility'],
            metrics['processing_efficiency'],
            metrics['meta_cognitive_awareness']
        ]
        
        profile['overall_score'] = round(np.mean(numerical_metrics), 3)
        
        # Determine cognitive profile type
        if profile['overall_score'] > 0.7:
            if metrics['reasoning_style'].startswith('sequential'):
                profile['type'] = 'systematic-analytical'
            elif metrics['reasoning_style'].startswith('pattern'):
                profile['type'] = 'pattern-recognizer'
            else:
                profile['type'] = 'adaptive-generalist'
        elif profile['overall_score'] > 0.5:
            profile['type'] = 'balanced-processor'
        else:
            profile['type'] = 'developing'
        
        return profile
    
    def compare_models(self, all_metrics: Dict[str, Dict]) -> Dict[str, Any]:
        """Compare metrics across multiple models"""
        comparison = {
            'rankings': {},
            'statistical_tests': {},
            'relative_strengths': {},
            'clustering': None
        }
        
        # Create rankings for each metric
        metric_names = ['wmi', 'efs', 'cognitive_flexibility', 
                       'processing_efficiency', 'meta_cognitive_awareness']
        
        for metric in metric_names:
            scores = {model: metrics[metric] for model, metrics in all_metrics.items()}
            sorted_models = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            comparison['rankings'][metric] = [(model, score) for model, score in sorted_models]
        
        # Perform statistical tests if we have enough models
        if len(all_metrics) >= 3:
            comparison['statistical_tests'] = self._perform_statistical_tests(all_metrics)
        
        # Identify relative strengths
        for model in all_metrics:
            strengths = []
            for metric in metric_names:
                model_score = all_metrics[model][metric]
                other_scores = [all_metrics[m][metric] for m in all_metrics if m != model]
                if other_scores and model_score > np.mean(other_scores) + np.std(other_scores):
                    strengths.append(metric)
            comparison['relative_strengths'][model] = strengths
        
        return comparison
    
    def _perform_statistical_tests(self, all_metrics: Dict) -> Dict[str, Any]:
        """Perform statistical tests on metrics"""
        tests = {}
        
        metric_names = ['wmi', 'efs', 'cognitive_flexibility', 
                       'processing_efficiency', 'meta_cognitive_awareness']
        
        for metric in metric_names:
            scores = [metrics[metric] for metrics in all_metrics.values()]
            
            # Perform one-way ANOVA equivalent
            if len(set(scores)) > 1:  # Only if there's variation
                # Calculate coefficient of variation
                cv = np.std(scores) / np.mean(scores) if np.mean(scores) > 0 else 0
                tests[metric] = {
                    'mean': round(np.mean(scores), 3),
                    'std': round(np.std(scores), 3),
                    'cv': round(cv, 3),
                    'range': round(max(scores) - min(scores), 3)
                }
        
        return tests
