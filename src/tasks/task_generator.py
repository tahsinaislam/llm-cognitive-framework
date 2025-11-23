"""
Task Generator Module
Generates cognitive tasks across different categories
"""

import random
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import uuid

class TaskGenerator:
    """Generate cognitive assessment tasks"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize task generator with configuration"""
        self.config = config
        self.task_templates = self._load_task_templates()
        self.task_categories = [
            "working_memory",
            "executive_function", 
            "reasoning",
            "integration",
            "meta_cognitive"
        ]
    
    def _load_task_templates(self) -> Dict[str, List[Dict]]:
        """Load task templates from files"""
        templates = {}
        template_dir = Path("config/task_templates")
        
        if template_dir.exists():
            for template_file in template_dir.glob("*.json"):
                category = template_file.stem
                with open(template_file, 'r') as f:
                    templates[category] = json.load(f)
        else:
            # Use default templates if files don't exist
            templates = self._get_default_templates()
        
        return templates
    
    def generate_tasks(self, category: Optional[str] = None, count: Optional[int] = None) -> List[Dict]:
        """Generate tasks for assessment"""
        tasks = []
        
        if category:
            categories = [category] if category in self.task_categories else self.task_categories
        else:
            categories = self.task_categories
        
        tasks_per_category = count // len(categories) if count else 30
        
        for cat in categories:
            category_tasks = self._generate_category_tasks(cat, tasks_per_category)
            tasks.extend(category_tasks)
        
        # Shuffle tasks to avoid order effects
        random.shuffle(tasks)
        
        return tasks
    
    def _generate_category_tasks(self, category: str, count: int) -> List[Dict]:
        """Generate tasks for a specific category"""
        tasks = []
        
        if category == "working_memory":
            tasks.extend(self._generate_working_memory_tasks(count))
        elif category == "executive_function":
            tasks.extend(self._generate_executive_function_tasks(count))
        elif category == "reasoning":
            tasks.extend(self._generate_reasoning_tasks(count))
        elif category == "integration":
            tasks.extend(self._generate_integration_tasks(count))
        elif category == "meta_cognitive":
            tasks.extend(self._generate_meta_cognitive_tasks(count))
        
        return tasks
    
    def _generate_working_memory_tasks(self, count: int) -> List[Dict]:
        """Generate working memory assessment tasks"""
        tasks = []
        
        for i in range(count):
            task_type = random.choice([
                "serial_recall",
                "n_back",
                "mental_rotation",
                "constraint_satisfaction"
            ])
            
            if task_type == "serial_recall":
                items = random.sample(range(100, 999), random.randint(5, 9))
                prompt = f"Remember this sequence: {', '.join(map(str, items))}. Now, what was the {random.randint(1, len(items))}th number?"
            
            elif task_type == "n_back":
                sequence = [random.choice(['A', 'B', 'C', 'D']) for _ in range(10)]
                n = random.randint(2, 4)
                prompt = f"Consider this sequence: {' '.join(sequence)}. For each position, identify if the current letter matches the letter {n} positions back. List your answers."
            
            elif task_type == "mental_rotation":
                shapes = ['triangle', 'square', 'pentagon', 'hexagon']
                rotations = ['90 degrees clockwise', '180 degrees', '90 degrees counter-clockwise']
                shape = random.choice(shapes)
                rotation = random.choice(rotations)
                prompt = f"Imagine a {shape} with a dot in the upper left corner. Now rotate it {rotation}. Where is the dot now?"
            
            else:  # constraint_satisfaction
                constraints = random.randint(3, 5)
                prompt = self._generate_constraint_problem(constraints)
            
            tasks.append({
                'id': str(uuid.uuid4()),
                'type': f'working_memory_{task_type}',
                'prompt': prompt,
                'category': 'working_memory'
            })
        
        return tasks
    
    def _generate_executive_function_tasks(self, count: int) -> List[Dict]:
        """Generate executive function assessment tasks"""
        tasks = []
        
        for i in range(count):
            task_type = random.choice([
                "task_switching",
                "inhibition",
                "updating",
                "planning"
            ])
            
            if task_type == "task_switching":
                prompt = "First, list 5 animals in alphabetical order. Then, list 5 countries by population size (largest to smallest). Finally, alternate between listing a fruit and a color for 6 items total."
            
            elif task_type == "inhibition":
                prompt = "Read this paragraph and count only the words that DON'T start with a vowel: 'An elephant observed an orange umbrella under ancient oak trees. Eagles flew overhead while ants explored interesting underground tunnels.' How many words?"
            
            elif task_type == "updating":
                prompt = "Start with the number 100. Add 17, then multiply by 2, subtract 50, divide by 3, add the original number. Now update: the original number was actually 150. What's the new result?"
            
            else:  # planning
                prompt = "You need to schedule 5 meetings (A, B, C, D, E) with these constraints: A before B, C cannot be first or last, D and E cannot be adjacent, B before D. What's a valid order?"
            
            tasks.append({
                'id': str(uuid.uuid4()),
                'type': f'executive_function_{task_type}',
                'prompt': prompt,
                'category': 'executive_function'
            })
        
        return tasks
    
    def _generate_reasoning_tasks(self, count: int) -> List[Dict]:
        """Generate reasoning assessment tasks"""
        tasks = []
        
        for i in range(count):
            task_type = random.choice([
                "deductive",
                "inductive",
                "analogical",
                "causal"
            ])
            
            if task_type == "deductive":
                prompt = "All managers have access to the conference room. Some employees are managers. Sarah is an employee but not a manager. Can Sarah access the conference room? Explain your reasoning."
            
            elif task_type == "inductive":
                numbers = [2, 6, 12, 20, 30]
                prompt = f"What's the next number in this sequence and why: {', '.join(map(str, numbers))}, ?"
            
            elif task_type == "analogical":
                prompt = "Complete this analogy and explain: Tree is to forest as neuron is to ____?"
            
            else:  # causal
                prompt = "A factory's production decreased by 30% last month. Three events occurred: new equipment was installed, half the workers went on strike, and raw material prices increased. Which event most likely caused the decrease? Explain your causal reasoning."
            
            tasks.append({
                'id': str(uuid.uuid4()),
                'type': f'reasoning_{task_type}',
                'prompt': prompt,
                'category': 'reasoning'
            })
        
        return tasks
    
    def _generate_integration_tasks(self, count: int) -> List[Dict]:
        """Generate integration assessment tasks"""
        tasks = []
        
        for i in range(count):
            domains = random.sample([
                "biology", "economics", "physics", "psychology",
                "history", "mathematics", "literature", "technology"
            ], 2)
            
            prompt = f"How might concepts from {domains[0]} help us understand problems in {domains[1]}? Provide a specific example and explain the connection."
            
            tasks.append({
                'id': str(uuid.uuid4()),
                'type': 'integration_cross_domain',
                'prompt': prompt,
                'category': 'integration'
            })
        
        return tasks
    
    def _generate_meta_cognitive_tasks(self, count: int) -> List[Dict]:
        """Generate meta-cognitive assessment tasks"""
        tasks = []
        
        for i in range(count):
            task_type = random.choice([
                "confidence_calibration",
                "strategy_selection",
                "error_detection",
                "self_explanation"
            ])
            
            if task_type == "confidence_calibration":
                prompt = "Estimate the population of Nigeria to the nearest 10 million. Then rate your confidence in this estimate from 0-100%. Explain what factors influenced your confidence rating."
            
            elif task_type == "strategy_selection":
                prompt = "You need to find the sum of all integers from 1 to 100. Describe at least two different strategies you could use and explain which would be most efficient."
            
            elif task_type == "error_detection":
                prompt = "Find the error in this reasoning: 'All birds can fly. Penguins are birds. Therefore, penguins can fly.' Explain what type of logical error this represents."
            
            else:  # self_explanation
                prompt = "Solve this problem and explain your thinking step-by-step: If 3 cats catch 3 mice in 3 minutes, how many cats are needed to catch 100 mice in 100 minutes?"
            
            tasks.append({
                'id': str(uuid.uuid4()),
                'type': f'meta_cognitive_{task_type}',
                'prompt': prompt,
                'category': 'meta_cognitive'
            })
        
        return tasks
    
    def _generate_constraint_problem(self, num_constraints: int) -> str:
        """Generate a constraint satisfaction problem"""
        items = ['A', 'B', 'C', 'D', 'E'][:num_constraints]
        constraints = []
        
        for i in range(num_constraints):
            constraint_type = random.choice([
                "before",
                "after",
                "not_adjacent",
                "position"
            ])
            
            if constraint_type == "before" and i < len(items) - 1:
                constraints.append(f"{items[i]} must come before {items[i+1]}")
            elif constraint_type == "after" and i > 0:
                constraints.append(f"{items[i]} must come after {items[i-1]}")
            elif constraint_type == "not_adjacent" and i < len(items) - 1:
                constraints.append(f"{items[i]} cannot be adjacent to {items[i+1]}")
            else:
                position = random.choice(["first", "last", "middle"])
                constraints.append(f"{items[i]} must be {position}")
        
        prompt = f"Arrange the items {', '.join(items)} in a valid order given these constraints: {'; '.join(constraints)}"
        return prompt
    
    def _get_default_templates(self) -> Dict[str, List[Dict]]:
        """Get default task templates if files not found"""
        return {
            "working_memory": [],
            "executive_function": [],
            "reasoning": [],
            "integration": [],
            "meta_cognitive": []
        }
