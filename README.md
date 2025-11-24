# LLM Cognitive Profiling Framework

A computational framework for characterizing and comparing the cognitive-like information processing patterns of Large Language Models.

## Supported Models

### Free Tier (Default)
| Model | Provider | Description |
|-------|----------|-------------|
| **Ollama-Llama3** | Ollama (local) | Llama 3.2 running locally - completely free |
| **Ollama-Mistral** | Ollama (local) | Mistral running locally - completely free |
| **Ollama-DeepSeek** | Ollama (local) | DeepSeek-R1 running locally - completely free |
| **Groq-Llama3** | Groq | Llama 3.3 70B via Groq's free API tier |
| **Groq-Mixtral** | Groq | Mixtral 8x7B via Groq's free API tier |
| **Gemini** | Google | Gemini 1.5 Flash via Google's free API tier |

### Paid Options (Optional)
GPT-4, Claude, and DeepSeek API are also supported but commented out by default.

## Overview

This framework applies cognitive science principles to systematically evaluate and profile how different LLM architectures process information. It assesses models across multiple cognitive dimensions including:

- **Working Memory** - Information retention and manipulation
- **Executive Function** - Task switching, inhibition, and updating
- **Reasoning Strategies** - Deductive, inductive, analogical, and causal reasoning
- **Integration Patterns** - Cross-domain synthesis and connections
- **Meta-Cognitive Awareness** - Self-monitoring and strategy selection

## Features

- Cognitive Assessment Battery: 150+ carefully designed tasks across 5 cognitive categories
- Automated Analysis: Pattern recognition and metric calculation
- Visualization Dashboard: Interactive charts and comparative profiles
- Multi-Model Support: Unified interface for Ollama, Groq, Gemini, and more
- Research-Ready Reports: Paper-ready markdown and LaTeX table output
- Free by Default: Uses free APIs and local models out of the box

## Installation

### Prerequisites

- Python 3.8 or higher
- API keys for the LLMs you want to test

### Method 1: Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/llm-cognitive-framework.git
cd llm-cognitive-framework
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. **Set up API keys**
```bash
cp .env .env
# Edit .env and add your API keys
```

### Method 2: Docker Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/llm-cognitive-framework.git
cd llm-cognitive-framework
```

2. **Set up API keys**
```bash
cp .env .env
# Edit .env and add your API keys
```

3. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

This will:
- Build the framework container
- Run the comparative assessment
- Start a web server on http://localhost:8080 for visualizations

## Usage

### Quick Start (Free Models)

**Run comparative assessment with Groq models:**
```bash
python main.py --compare
```

**Assess a specific model:**
```bash
python main.py --model Groq-Llama3
python main.py --model Ollama-Mistral
python main.py --model Gemini
```

**Run specific task category:**
```bash
python main.py --category working_memory
```

### Research Paper Output

**Generate research-ready report (default):**
```bash
python main.py --compare --report-format research
```

**Generate LaTeX tables only:**
```bash
python main.py --compare --report-format latex
```

**Specify output directory:**
```bash
python main.py --compare --output my_results
```

### Advanced Usage

**Custom configuration:**
```bash
python main.py --config custom_config.yaml
```

**Programmatic usage:**
```python
import asyncio
from src.models.model_interface import ModelInterface
from src.tasks.task_generator import TaskGenerator
from src.analysis.cognitive_analyzer import CognitiveAnalyzer
from src.metrics.metric_calculator import MetricCalculator

async def run_custom_assessment():
    # Initialize components
    model = ModelInterface("Groq-Llama3", config)
    task_gen = TaskGenerator(config)
    analyzer = CognitiveAnalyzer()
    calculator = MetricCalculator()

    # Generate and run tasks
    tasks = task_gen.generate_tasks("reasoning", count=10)
    responses = []
    for task in tasks:
        response = await model.get_response(task)
        responses.append(response)

    # Analyze and calculate metrics
    analysis = analyzer.analyze_responses(responses)
    metrics = calculator.calculate_metrics(analysis)

    return metrics

# Run assessment
metrics = asyncio.run(run_custom_assessment())
print(metrics)
```

## Configuration

Edit `config/config.yaml` to customize:

- **Model Settings**: Temperature, max tokens, rate limits
- **Task Parameters**: Categories, count, randomization
- **Analysis Options**: Batch size, parallelization, caching
- **Output Formats**: JSON, visualizations, reports

## API Keys Setup

### Free Options (Recommended)

1. **Ollama (Local - No API Key Required)**
   ```bash
   # Install Ollama
   brew install ollama  # macOS
   # or visit https://ollama.ai for other platforms

   # Download models
   ollama pull llama3.2
   ollama pull mistral
   ollama pull deepseek-r1:8b

   # Start the server
   ollama serve
   ```

2. **Groq (Free Tier)**
   - Get free API key from: https://console.groq.com
   - Set in `.env`: `GROQ_API_KEY=gsk_...`

3. **Google Gemini (Free Tier)**
   - Get free API key from: https://aistudio.google.com/apikey
   - Set in `.env`: `GOOGLE_API_KEY=...`

### Paid Options (Optional)

Uncomment in `config/config.yaml` to enable:

- **OpenAI (GPT-4)**: https://platform.openai.com/api-keys
- **Anthropic (Claude)**: https://console.anthropic.com/
- **DeepSeek**: https://platform.deepseek.com/

## Output Structure

```
results/
├── results_20240315_143022.json      # Raw response data
├── metrics_20240315_143022.json      # Calculated metrics
├── report_20240315_143022.md         # Research paper-ready report
└── tables_20240315_143022.tex        # LaTeX tables for paper

visualizations/
├── cognitive_radar.html              # Interactive radar chart
├── metrics_comparison.html           # Bar chart comparison
├── metrics_heatmap.html              # Heatmap visualization
└── cognitive_dashboard.html          # Comprehensive dashboard
```

### LaTeX Tables

The `tables_*.tex` file contains ready-to-use tables:
```latex
% Add to preamble: \usepackage{booktabs}
\begin{table}[htbp]
\centering
\caption{Comparative Cognitive Metrics Across LLMs}
\begin{tabular}{lccccc}
\toprule
Model & WMI & EFS & Flexibility & Efficiency & Meta-Cog \\
\midrule
...
\end{tabular}
\end{table}
```

## Project Structure

```
llm-cognitive-framework/
├── main.py                    # Main entry point
├── src/
│   ├── models/               # Model interfaces
│   │   └── model_interface.py
│   ├── tasks/                # Task generation
│   │   └── task_generator.py
│   ├── analysis/             # Response analysis
│   │   └── cognitive_analyzer.py
│   ├── metrics/              # Metric calculation
│   │   └── metric_calculator.py
│   ├── visualization/        # Visualization creation
│   │   └── profile_visualizer.py
│   └── utils/                # Utilities
│       ├── config.py
│       └── logger.py
├── config/
│   ├── config.yaml          # Main configuration
│   └── task_templates/      # Task template files
├── tests/                    # Unit tests
├── results/                  # Output results
├── visualizations/           # Generated visualizations
├── logs/                     # Application logs
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose config
└── README.md                # This file
```

## Understanding the Metrics

### Working Memory Index (WMI)
- **Range**: 0.0 - 1.0
- **Components**: Sequential processing, information retention, concurrent processing, chunking
- **Interpretation**: Higher scores indicate better ability to maintain and manipulate information

### Executive Function Score (EFS)
- **Range**: 0.0 - 1.0
- **Components**: Task switching, inhibition, updating, planning
- **Interpretation**: Higher scores indicate better cognitive control and flexibility

### Reasoning Styles
- **Sequential-Deductive**: Step-by-step logical reasoning
- **Pattern-Inductive**: Pattern recognition and generalization
- **Associative-Analogical**: Connection-making across domains
- **Causal-Mechanistic**: Cause-effect relationship focus

### Integration Patterns
- **Web-like-associative**: Broad connections across domains
- **Deep-hierarchical**: Structured, layered integration
- **Moderate-structured**: Balanced integration approach
- **Linear-sequential**: Step-by-step integration

## Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Solution: Adjust `rate_limit` in config.yaml
   - Use exponential backoff (already implemented)

2. **Memory Issues with Large Assessments**
   - Solution: Reduce `batch_size` in configuration
   - Run assessments sequentially instead of parallel

3. **Missing spaCy Model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Docker Build Failures**
   - Ensure Docker daemon is running
   - Check available disk space
   - Try building with `--no-cache` flag

5. **Visualization Not Loading**
   - Check if plotly is installed: `pip install plotly kaleido`
   - Ensure output directory has write permissions

### Debug Mode

Run with debug logging:
```bash
python main.py --compare --log-level DEBUG
```

Check logs:
```bash
tail -f logs/framework.log
```

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

Run specific test:
```bash
pytest tests/test_analyzer.py::test_reasoning_detection -v
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Research Citations

If you use this framework in your research, please cite:

```bibtex
@software{islam2025cognitive,
  title={LLM Cognitive Profiling Framework},
  author={Islam, Tahsina},
  year={2025},
  institution={Georgia Institute of Technology},
  url={https://github.com/yourusername/llm-cognitive-framework}
}
```

## Acknowledgments

- Georgia Tech CS6795 Cognitive Science course
- Cognitive science frameworks from Baddeley, Miyake, Kahneman, and others
- Ollama, Groq, and Google for free API access
- Meta (Llama), Mistral AI, and DeepSeek for open-source models

