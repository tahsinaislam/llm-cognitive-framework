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
    
    async def run_comparative_assessment(self, task_category: str = None, save_partial: bool = True) -> Dict:
        """Run assessment for all models and compare

        Args:
            task_category: Optional category to filter tasks
            save_partial: If True, save results after each successful model
        """
        all_metrics = {}

        for model_name in self.models.keys():
            try:
                metrics = await self.run_assessment(model_name, task_category)
                all_metrics[model_name] = metrics

                # Save partial results after each successful model
                if save_partial and self.results:
                    logger.info(f"Saving partial results after {model_name}")
                    self._save_partial_results()

            except Exception as e:
                logger.error(f"Failed assessment for {model_name}: {e}")
                continue  # Continue with next model even if this one fails

        # Only generate comparison if we have at least one successful model
        if all_metrics:
            # Generate comparative analysis
            comparison = self.metric_calculator.compare_models(all_metrics)

            # Create visualizations
            try:
                self.visualizer.create_comparative_plots(all_metrics, comparison)
            except Exception as e:
                logger.error(f"Failed to create visualizations: {e}")
                comparison['visualization_error'] = str(e)
        else:
            comparison = {'error': 'No models completed successfully'}
            logger.error("No models completed successfully - no results to compare")

        return {
            'individual_metrics': all_metrics,
            'comparison': comparison
        }

    def _save_partial_results(self, output_dir: str = "results"):
        """Save partial results as backup during assessment"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Save with 'partial' prefix to distinguish from final results
        with open(output_path / "partial_results.json", 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        metrics_summary = {
            model: results['metrics']
            for model, results in self.results.items()
        }
        with open(output_path / "partial_metrics.json", 'w') as f:
            json.dump(metrics_summary, f, indent=2)

        logger.info(f"Partial results saved to {output_path}")
    
    def save_results(self, output_dir: str = "results", report_format: str = "research"):
        """Save all results to files

        Args:
            output_dir: Directory to save results
            report_format: 'standard', 'research', or 'latex'
        """
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

        # Generate and save standard report
        report = self.generate_report(report_format)
        report_filename = f"report_{timestamp}.md"
        with open(output_path / report_filename, 'w') as f:
            f.write(report)

        # Always generate LaTeX tables for research use
        if report_format == "research":
            latex_tables = self.generate_report("latex")
            with open(output_path / f"tables_{timestamp}.tex", 'w') as f:
                f.write(latex_tables)
            logger.info(f"LaTeX tables saved to {output_path}/tables_{timestamp}.tex")

        logger.info(f"Results saved to {output_path}")
        logger.info(f"Report format: {report_format}")

        # Print summary to console
        print(f"\n{'='*60}")
        print("RESULTS SAVED")
        print(f"{'='*60}")
        print(f"Directory: {output_path}")
        print(f"Files generated:")
        print(f"  - results_{timestamp}.json (raw data)")
        print(f"  - metrics_{timestamp}.json (metrics summary)")
        print(f"  - {report_filename} (report)")
        if report_format == "research":
            print(f"  - tables_{timestamp}.tex (LaTeX tables)")
        print(f"{'='*60}\n")
    
    def generate_report(self, format_type: str = "standard") -> str:
        """Generate a markdown report of results

        Args:
            format_type: 'standard', 'research', or 'latex'
        """
        if format_type == "research":
            return self._generate_research_report()
        elif format_type == "latex":
            return self._generate_latex_tables()
        else:
            return self._generate_standard_report()

    def _generate_standard_report(self) -> str:
        """Generate standard markdown report"""
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

    def _generate_research_report(self) -> str:
        """Generate comprehensive research paper-ready report"""
        report = []

        # Title and metadata
        report.append("# Comparative Cognitive Profile Analysis of Large Language Models\n\n")
        report.append(f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n\n")
        report.append(f"**Models Evaluated:** {', '.join(self.results.keys())}\n\n")

        # Abstract
        report.append("## Abstract\n\n")
        report.append(self._generate_abstract())
        report.append("\n\n")

        # Methodology
        report.append("## Methodology\n\n")
        report.append(self._generate_methodology_section())
        report.append("\n\n")

        # Results Summary Table
        report.append("## Results\n\n")
        report.append("### Comparative Metrics Summary\n\n")
        report.append(self._generate_metrics_table())
        report.append("\n\n")

        # Detailed Results per Model
        report.append("### Detailed Model Profiles\n\n")
        for model_name, results in self.results.items():
            report.append(self._generate_model_section(model_name, results))

        # Statistical Analysis
        if len(self.results) > 1:
            report.append("### Statistical Comparison\n\n")
            report.append(self._generate_statistical_section())
            report.append("\n\n")

        # Key Findings
        report.append("## Key Findings\n\n")
        report.append(self._generate_key_findings())
        report.append("\n\n")

        # Discussion Points
        report.append("## Discussion\n\n")
        report.append(self._generate_discussion_points())
        report.append("\n\n")

        # Limitations
        report.append("## Limitations\n\n")
        report.append("- Results reflect model behavior under specific prompting conditions\n")
        report.append("- Cognitive metrics are approximations based on response patterns\n")
        report.append("- Task battery may not capture all cognitive dimensions\n")
        report.append("- Model responses may vary with temperature and sampling settings\n\n")

        return ''.join(report)

    def _generate_abstract(self) -> str:
        """Generate abstract summarizing findings"""
        if not self.results:
            return "No results available."

        models = list(self.results.keys())

        # Find best performers
        best_wmi = max(self.results.items(), key=lambda x: x[1]['metrics'].get('wmi', 0))
        best_efs = max(self.results.items(), key=lambda x: x[1]['metrics'].get('efs', 0))

        abstract = (
            f"This study presents a comparative cognitive profile analysis of {len(models)} "
            f"large language models ({', '.join(models)}) using a battery of {self.config.get('tasks', {}).get('tasks_per_category', 30) * 5} "
            f"cognitive assessment tasks spanning five dimensions: working memory, executive function, "
            f"reasoning, integration, and meta-cognition. "
            f"Results indicate that {best_wmi[0]} demonstrated the highest Working Memory Index "
            f"(WMI={best_wmi[1]['metrics'].get('wmi', 0):.3f}), while {best_efs[0]} showed superior "
            f"Executive Function performance (EFS={best_efs[1]['metrics'].get('efs', 0):.3f}). "
            f"Models exhibited distinct reasoning style preferences and integration patterns, "
            f"suggesting architecture-specific cognitive processing characteristics."
        )
        return abstract

    def _generate_methodology_section(self) -> str:
        """Generate methodology description"""
        tasks_per_cat = self.config.get('tasks', {}).get('tasks_per_category', 30)
        categories = self.config.get('tasks', {}).get('categories', [])

        methodology = f"""### Assessment Battery

The cognitive assessment battery consisted of {tasks_per_cat * len(categories)} tasks distributed across {len(categories)} cognitive categories:

| Category | Tasks | Description |
|----------|-------|-------------|
| Working Memory | {tasks_per_cat} | Information retention, sequential processing, concurrent handling |
| Executive Function | {tasks_per_cat} | Task switching, inhibition, updating, planning |
| Reasoning | {tasks_per_cat} | Deductive, inductive, analogical, and causal reasoning |
| Integration | {tasks_per_cat} | Cross-domain synthesis and connection-making |
| Meta-Cognitive | {tasks_per_cat} | Self-monitoring, strategy selection, confidence calibration |

### Metrics Calculated

- **Working Memory Index (WMI):** Composite score (0-1) measuring sequential processing, information retention, concurrent processing, and chunking ability
- **Executive Function Score (EFS):** Composite score (0-1) measuring task switching, inhibition, updating, and planning
- **Cognitive Flexibility:** Measure of reasoning style variety and adaptive switching
- **Processing Efficiency:** Balance of response appropriateness and error rate
- **Meta-Cognitive Awareness:** Self-monitoring and strategy verbalization

### Experimental Parameters

- Temperature: {self.config.get('models', {}).get(list(self.results.keys())[0] if self.results else '', {}).get('temperature', 0.7)}
- Max Tokens: {self.config.get('models', {}).get(list(self.results.keys())[0] if self.results else '', {}).get('max_tokens', 1000)}
- Tasks randomized: {self.config.get('tasks', {}).get('randomize', True)}
"""
        return methodology

    def _generate_metrics_table(self) -> str:
        """Generate comparative metrics table in markdown"""
        if not self.results:
            return "No results available."

        # Header
        table = "| Model | WMI | EFS | Flexibility | Efficiency | Meta-Cog | Overall | Profile Type |\n"
        table += "|-------|-----|-----|-------------|------------|----------|---------|-------------|\n"

        # Data rows
        for model_name, results in self.results.items():
            metrics = results['metrics']
            profile = metrics.get('composite_profile', {})
            table += (
                f"| {model_name} "
                f"| {metrics.get('wmi', 0):.3f} "
                f"| {metrics.get('efs', 0):.3f} "
                f"| {metrics.get('cognitive_flexibility', 0):.3f} "
                f"| {metrics.get('processing_efficiency', 0):.3f} "
                f"| {metrics.get('meta_cognitive_awareness', 0):.3f} "
                f"| {profile.get('overall_score', 0):.3f} "
                f"| {profile.get('type', 'N/A')} |\n"
            )

        return table

    def _generate_model_section(self, model_name: str, results: Dict) -> str:
        """Generate detailed section for a single model"""
        metrics = results['metrics']
        analysis = results.get('analysis', {})
        profile = metrics.get('composite_profile', {})
        error_profile = metrics.get('error_profile', {})

        section = f"""#### {model_name}

**Cognitive Profile Type:** {profile.get('type', 'N/A')}

**Primary Metrics:**
| Metric | Score | Interpretation |
|--------|-------|----------------|
| Working Memory Index | {metrics.get('wmi', 0):.3f} | {self._interpret_score(metrics.get('wmi', 0), 'wmi')} |
| Executive Function | {metrics.get('efs', 0):.3f} | {self._interpret_score(metrics.get('efs', 0), 'efs')} |
| Cognitive Flexibility | {metrics.get('cognitive_flexibility', 0):.3f} | {self._interpret_score(metrics.get('cognitive_flexibility', 0), 'flex')} |
| Processing Efficiency | {metrics.get('processing_efficiency', 0):.3f} | {self._interpret_score(metrics.get('processing_efficiency', 0), 'eff')} |
| Meta-Cognitive Awareness | {metrics.get('meta_cognitive_awareness', 0):.3f} | {self._interpret_score(metrics.get('meta_cognitive_awareness', 0), 'meta')} |

**Reasoning Style:** {metrics.get('reasoning_style', 'N/A')}

**Integration Pattern:** {metrics.get('integration_pattern', 'N/A')}

**Error Profile:** {error_profile.get('tendency', 'N/A')} (error rate: {error_profile.get('error_rate', 0):.1%})

"""
        return section

    def _interpret_score(self, score: float, metric_type: str) -> str:
        """Provide interpretation of metric scores"""
        if score >= 0.8:
            return "High"
        elif score >= 0.6:
            return "Moderate-High"
        elif score >= 0.4:
            return "Moderate"
        elif score >= 0.2:
            return "Low-Moderate"
        else:
            return "Low"

    def _generate_statistical_section(self) -> str:
        """Generate statistical comparison section"""
        if len(self.results) < 2:
            return "Insufficient models for statistical comparison.\n"

        import numpy as np

        metrics_list = ['wmi', 'efs', 'cognitive_flexibility', 'processing_efficiency', 'meta_cognitive_awareness']

        section = "| Metric | Mean | Std Dev | Range | CV |\n"
        section += "|--------|------|---------|-------|----|\n"

        for metric in metrics_list:
            scores = [r['metrics'].get(metric, 0) for r in self.results.values()]
            mean = np.mean(scores)
            std = np.std(scores)
            range_val = max(scores) - min(scores)
            cv = std / mean if mean > 0 else 0

            metric_name = metric.replace('_', ' ').title()
            section += f"| {metric_name} | {mean:.3f} | {std:.3f} | {range_val:.3f} | {cv:.2f} |\n"

        return section

    def _generate_key_findings(self) -> str:
        """Generate key findings bullet points"""
        if not self.results:
            return "No results available."

        findings = []

        # Find best/worst performers for each metric
        metrics_to_check = ['wmi', 'efs', 'cognitive_flexibility', 'processing_efficiency']
        metric_names = {
            'wmi': 'Working Memory',
            'efs': 'Executive Function',
            'cognitive_flexibility': 'Cognitive Flexibility',
            'processing_efficiency': 'Processing Efficiency'
        }

        for metric in metrics_to_check:
            best = max(self.results.items(), key=lambda x: x[1]['metrics'].get(metric, 0))
            findings.append(
                f"- **{metric_names[metric]}:** {best[0]} demonstrated the highest performance "
                f"({best[1]['metrics'].get(metric, 0):.3f})"
            )

        # Reasoning style diversity
        styles = set()
        for r in self.results.values():
            styles.add(r['metrics'].get('reasoning_style', 'unknown'))
        findings.append(f"- **Reasoning Diversity:** {len(styles)} distinct reasoning styles observed across models")

        # Overall patterns
        profile_types = [r['metrics'].get('composite_profile', {}).get('type', 'unknown') for r in self.results.values()]
        findings.append(f"- **Profile Distribution:** Models classified as: {', '.join(set(profile_types))}")

        return '\n'.join(findings)

    def _generate_discussion_points(self) -> str:
        """Generate discussion points for research paper"""
        return """The observed differences in cognitive profiles suggest that LLM architectures
may develop distinct information processing strategies during training. The variation in
Working Memory Index scores indicates differential capacity for maintaining and manipulating
information across context windows. Executive Function differences may reflect varying
approaches to task decomposition and response organization.

The diversity in reasoning styles (sequential-deductive vs. pattern-inductive) aligns with
theoretical predictions about how different training objectives and data compositions might
shape emergent cognitive-like behaviors. Models showing higher meta-cognitive awareness
scores tended to provide more explicit reasoning chains and uncertainty calibration.

These findings have implications for:
1. **Model Selection:** Task-specific cognitive requirements should guide model choice
2. **Prompt Engineering:** Strategies should account for model-specific processing patterns
3. **Evaluation Frameworks:** Cognitive profiling offers complementary insights to benchmark performance
"""

    def _generate_latex_tables(self) -> str:
        """Generate LaTeX-formatted tables for direct paper inclusion"""
        if not self.results:
            return "% No results available"

        latex = []
        latex.append("% LaTeX Tables for Research Paper")
        latex.append("% Copy these directly into your paper\n")

        # Main results table
        latex.append("\\begin{table}[htbp]")
        latex.append("\\centering")
        latex.append("\\caption{Comparative Cognitive Metrics Across LLMs}")
        latex.append("\\label{tab:cognitive_metrics}")
        latex.append("\\begin{tabular}{lccccc}")
        latex.append("\\toprule")
        latex.append("Model & WMI & EFS & Flexibility & Efficiency & Meta-Cog \\\\")
        latex.append("\\midrule")

        for model_name, results in self.results.items():
            metrics = results['metrics']
            latex.append(
                f"{model_name} & "
                f"{metrics.get('wmi', 0):.3f} & "
                f"{metrics.get('efs', 0):.3f} & "
                f"{metrics.get('cognitive_flexibility', 0):.3f} & "
                f"{metrics.get('processing_efficiency', 0):.3f} & "
                f"{metrics.get('meta_cognitive_awareness', 0):.3f} \\\\"
            )

        latex.append("\\bottomrule")
        latex.append("\\end{tabular}")
        latex.append("\\end{table}\n")

        # Reasoning styles table
        latex.append("\\begin{table}[htbp]")
        latex.append("\\centering")
        latex.append("\\caption{Reasoning Styles and Integration Patterns}")
        latex.append("\\label{tab:reasoning_patterns}")
        latex.append("\\begin{tabular}{lll}")
        latex.append("\\toprule")
        latex.append("Model & Reasoning Style & Integration Pattern \\\\")
        latex.append("\\midrule")

        for model_name, results in self.results.items():
            metrics = results['metrics']
            latex.append(
                f"{model_name} & "
                f"{metrics.get('reasoning_style', 'N/A')} & "
                f"{metrics.get('integration_pattern', 'N/A')} \\\\"
            )

        latex.append("\\bottomrule")
        latex.append("\\end{tabular}")
        latex.append("\\end{table}")

        return '\n'.join(latex)

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
    parser.add_argument('--report-format', type=str, default='research',
                       choices=['standard', 'research', 'latex'],
                       help='Report format: standard (basic), research (paper-ready), latex (tables only)')

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

        # Save results with specified report format
        framework.save_results(args.output, args.report_format)

    except Exception as e:
        logger.error(f"Framework execution failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
