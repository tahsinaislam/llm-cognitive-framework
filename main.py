"""
LLM Cognitive Profiling Framework
Main execution script for running cognitive assessments on LLMs
"""

import asyncio
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from src.models.model_interface import ModelInterface
from src.tasks.task_generator import TaskGenerator
from src.analysis.cognitive_analyzer import CognitiveAnalyzer
from src.metrics.metric_calculator import MetricCalculator
from src.visualization.profile_visualizer import ProfileVisualizer
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class CognitiveFramework:
    """Main framework for cognitive profiling of LLMs"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the framework with configuration"""
        self.config = Config(config_path)
        self.models = self._initialize_models()
        self.task_generator = TaskGenerator(self.config)
        self.analyzer = CognitiveAnalyzer()
        self.metric_calculator = MetricCalculator()
        self.visualizer = ProfileVisualizer()
        self.results = {}
        
    def _initialize_models(self) -> Dict[str, ModelInterface]:
        """Initialize all model interfaces"""
        models = {}
        for model_name in self.config.get("models", {}).keys():
            try:
                models[model_name] = ModelInterface(model_name, self.config)
                logger.info(f"Initialized {model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize {model_name}: {e}")
        return models
    
    async def run_assessment(self, model_name: str, task_category: str = None) -> Dict:
        """Run cognitive assessment for a specific model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not initialized")
        
        logger.info(f"Starting assessment for {model_name}")
        model = self.models[model_name]
        
        # Generate tasks
        tasks = self.task_generator.generate_tasks(task_category)
        logger.info(f"Generated {len(tasks)} tasks")
        
        # Collect responses
        responses = []
        for i, task in enumerate(tasks):
            try:
                response = await model.get_response(task)
                responses.append({
                    'task_id': task['id'],
                    'task_type': task['type'],
                    'prompt': task['prompt'],
                    'response': response,
                    'timestamp': datetime.now().isoformat()
                })
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Completed {i + 1}/{len(tasks)} tasks")
                    
            except Exception as e:
                logger.error(f"Error on task {task['id']}: {e}")
                responses.append({
                    'task_id': task['id'],
                    'error': str(e)
                })
        
        # Analyze responses
        analysis_results = self.analyzer.analyze_responses(responses)
        
        # Calculate metrics
        metrics = self.metric_calculator.calculate_metrics(analysis_results)
        
        # Store results
        self.results[model_name] = {
            'responses': responses,
            'analysis': analysis_results,
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Assessment complete for {model_name}")
        return metrics
    
    async def run_comparative_assessment(self, task_category: str = None) -> Dict:
        """Run assessment for all models and compare"""
        all_metrics = {}
        
        for model_name in self.models.keys():
            try:
                metrics = await self.run_assessment(model_name, task_category)
                all_metrics[model_name] = metrics
            except Exception as e:
                logger.error(f"Failed assessment for {model_name}: {e}")
        
        # Generate comparative analysis
        comparison = self.metric_calculator.compare_models(all_metrics)
        
        # Create visualizations
        self.visualizer.create_comparative_plots(all_metrics, comparison)
        
        return {
            'individual_metrics': all_metrics,
            'comparison': comparison
        }
    
    def save_results(self, output_dir: str = "results"):
        """Save all results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save raw results
        with open(output_path / f"results_{timestamp}.json", 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save metrics summary
        metrics_summary = {
            model: results['metrics'] 
            for model, results in self.results.items()
        }
        with open(output_path / f"metrics_{timestamp}.json", 'w') as f:
            json.dump(metrics_summary, f, indent=2)
        
        # Generate and save report
        report = self.generate_report()
        with open(output_path / f"report_{timestamp}.md", 'w') as f:
            f.write(report)
        
        logger.info(f"Results saved to {output_path}")
    
    def generate_report(self) -> str:
        """Generate a markdown report of results"""
        report = ["# Cognitive Profiling Results\n"]
        report.append(f"Generated: {datetime.now().isoformat()}\n")
        
        for model_name, results in self.results.items():
            report.append(f"\n## {model_name}\n")
            
            metrics = results['metrics']
            report.append("### Cognitive Metrics\n")
            report.append(f"- Working Memory Index: {metrics.get('wmi', 'N/A'):.3f}\n")
            report.append(f"- Executive Function Score: {metrics.get('efs', 'N/A'):.3f}\n")
            report.append(f"- Reasoning Profile: {metrics.get('reasoning_style', 'N/A')}\n")
            report.append(f"- Integration Pattern: {metrics.get('integration_pattern', 'N/A')}\n")
            
            if 'analysis' in results:
                report.append("\n### Key Patterns\n")
                patterns = results['analysis'].get('patterns', {})
                for pattern, count in patterns.items():
                    report.append(f"- {pattern}: {count} occurrences\n")
        
        return ''.join(report)

async def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='LLM Cognitive Profiling Framework')
    parser.add_argument('--config', type=str, default='config/config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--model', type=str, help='Specific model to assess')
    parser.add_argument('--category', type=str, help='Task category to run')
    parser.add_argument('--compare', action='store_true', 
                       help='Run comparative assessment')
    parser.add_argument('--output', type=str, default='results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = CognitiveFramework(args.config)
    
    try:
        if args.compare:
            # Run comparative assessment
            logger.info("Running comparative assessment")
            await framework.run_comparative_assessment(args.category)
        elif args.model:
            # Run single model assessment
            logger.info(f"Running assessment for {args.model}")
            await framework.run_assessment(args.model, args.category)
        else:
            # Default: run all models
            logger.info("Running assessment for all models")
            await framework.run_comparative_assessment(args.category)
        
        # Save results
        framework.save_results(args.output)
        
    except Exception as e:
        logger.error(f"Framework execution failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
