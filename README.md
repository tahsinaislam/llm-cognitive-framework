# LLM Cognitive Profiling Framework

A computational framework for characterizing and comparing the cognitive-like information processing patterns of Large Language Models (GPT-4, Claude, Gemini, DeepSeek).

## Overview

This framework applies cognitive science principles to systematically evaluate and profile how different LLM architectures process information. It assesses models across multiple cognitive dimensions including:

- **Working Memory** - Information retention and manipulation
- **Executive Function** - Task switching, inhibition, and updating
- **Reasoning Strategies** - Deductive, inductive, analogical, and causal reasoning
- **Integration Patterns** - Cross-domain synthesis and connections
- **Meta-Cognitive Awareness** - Self-monitoring and strategy selection

## Features

- 🧠 **Cognitive Assessment Battery**: 150+ carefully designed tasks across 5 cognitive categories
- 📊 **Automated Analysis**: Pattern recognition and metric calculation
- 📈 **Visualization Dashboard**: Interactive charts and comparative profiles
- 🔄 **Multi-Model Support**: Unified interface for GPT-4, Claude, Gemini, and DeepSeek
- 📝 **Comprehensive Reports**: Detailed cognitive profiles and statistical comparisons

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
cp .env.example .env
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
cp .env.example .env
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

### Basic Usage

**Run comparative assessment for all models:**
```bash
python main.py --compare
```

**Assess a specific model:**
```bash
python main.py --model GPT-4
```

**Run specific task category:**
```bash
python main.py --category working_memory
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
    model = ModelInterface("GPT-4", config)
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

The framework requires API keys for each LLM provider:

1. **OpenAI (GPT-4)**
   - Get key from: https://platform.openai.com/api-keys
   - Set: `OPENAI_API_KEY=sk-...`

2. **Anthropic (Claude)**
   - Get key from: https://console.anthropic.com/
   - Set: `ANTHROPIC_API_KEY=sk-ant-...`

3. **Google (Gemini)**
   - Get key from: https://makersuite.google.com/app/apikey
   - Set: `GOOGLE_API_KEY=...`

4. **DeepSeek**
   - Get key from: https://platform.deepseek.com/
   - Set: `DEEPSEEK_API_KEY=...`

## Output Structure

```
results/
├── results_20240315_143022.json      # Raw response data
├── metrics_20240315_143022.json      # Calculated metrics
└── report_20240315_143022.md         # Markdown report

visualizations/
├── cognitive_radar.html              # Interactive radar chart
├── metrics_comparison.html           # Bar chart comparison
├── metrics_heatmap.html             # Heatmap visualization
└── cognitive_dashboard.html          # Comprehensive dashboard
```

## Deployment

### Cloud Deployment (AWS EC2)

1. **Launch EC2 instance** (t2.medium or larger recommended)

2. **Install Docker and Docker Compose:**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER
```

3. **Clone and configure:**
```bash
git clone https://github.com/yourusername/llm-cognitive-framework.git
cd llm-cognitive-framework
nano .env  # Add your API keys
```

4. **Run with Docker Compose:**
```bash
docker-compose up -d
```

5. **Access dashboard:**
   - Configure security group to allow port 8080
   - Access at: http://your-ec2-ip:8080

### Kubernetes Deployment

1. **Create ConfigMap for configuration:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cognitive-framework-config
data:
  config.yaml: |
    # Your configuration here
```

2. **Create Secret for API keys:**
```bash
kubectl create secret generic api-keys \
  --from-literal=OPENAI_API_KEY=your_key \
  --from-literal=ANTHROPIC_API_KEY=your_key \
  --from-literal=GOOGLE_API_KEY=your_key \
  --from-literal=DEEPSEEK_API_KEY=your_key
```

3. **Deploy application:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cognitive-framework
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cognitive-framework
  template:
    metadata:
      labels:
        app: cognitive-framework
    spec:
      containers:
      - name: framework
        image: llm-cognitive-framework:latest
        envFrom:
        - secretRef:
            name: api-keys
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: results
          mountPath: /app/results
      volumes:
      - name: config
        configMap:
          name: cognitive-framework-config
      - name: results
        persistentVolumeClaim:
          claimName: results-pvc
```

### GitHub Actions CI/CD

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy Framework

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        python -m spacy download en_core_web_sm
    - name: Run tests
      run: pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build and push Docker image
      env:
        DOCKER_REGISTRY: ${{ secrets.DOCKER_REGISTRY }}
      run: |
        docker build -t $DOCKER_REGISTRY/cognitive-framework:latest .
        docker push $DOCKER_REGISTRY/cognitive-framework:latest
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /opt/cognitive-framework
          docker-compose pull
          docker-compose up -d
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Georgia Tech CS6795 Cognitive Science course
- Cognitive science frameworks from Baddeley, Miyake, Kahneman, and others
- OpenAI, Anthropic, Google, and DeepSeek for API access

## Contact

Tahsina Islam - tislam38@gatech.edu

Project Link: https://github.com/yourusername/llm-cognitive-framework

## Future Work

- [ ] Add support for more LLM providers (Llama, Mistral, etc.)
- [ ] Implement real-time cognitive load monitoring
- [ ] Add cross-cultural task adaptations
- [ ] Develop fine-tuning recommendations based on profiles
- [ ] Create interactive web interface for custom assessments
- [ ] Add longitudinal tracking of model updates
- [ ] Implement multi-modal cognitive assessments
