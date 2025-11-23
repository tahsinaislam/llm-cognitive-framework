"""
Cognitive Analyzer Module
Analyzes LLM responses for cognitive patterns
"""

import re
from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict
import spacy
from textblob import TextBlob
import numpy as np

class CognitiveAnalyzer:
    """Analyze cognitive patterns in LLM responses"""
    
    def __init__(self):
        """Initialize the analyzer with NLP tools"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        self.reasoning_markers = {
            'deductive': ['therefore', 'thus', 'hence', 'consequently', 'it follows'],
            'inductive': ['pattern', 'trend', 'generally', 'typically', 'often'],
            'analogical': ['like', 'similar to', 'resembles', 'as', 'comparable'],
            'causal': ['because', 'causes', 'leads to', 'results in', 'due to']
        }
        
        self.meta_cognitive_markers = [
            'I think', 'I believe', 'it seems', 'perhaps', 'maybe',
            'certainly', 'definitely', 'probably', 'possibly',
            'my approach', 'my strategy', 'I would', 'let me'
        ]
    
    def analyze_responses(self, responses: List[Dict]) -> Dict[str, Any]:
        """Analyze a set of responses for cognitive patterns"""
        analysis = {
            'patterns': defaultdict(int),
            'reasoning_styles': Counter(),
            'structure_metrics': [],
            'meta_cognitive_score': 0,
            'error_patterns': Counter(),
            'integration_complexity': []
        }
        
        for response_data in responses:
            if 'error' in response_data:
                analysis['error_patterns']['api_error'] += 1
                continue
            
            response_text = response_data.get('response', '')
            task_type = response_data.get('task_type', '')
            
            # Analyze individual response
            response_analysis = self._analyze_single_response(response_text, task_type)
            
            # Aggregate results
            self._aggregate_analysis(analysis, response_analysis)
        
        # Calculate summary statistics
        analysis['summary'] = self._calculate_summary_stats(analysis)
        
        return analysis
    
    def _analyze_single_response(self, text: str, task_type: str) -> Dict[str, Any]:
        """Analyze a single response"""
        doc = self.nlp(text)
        
        analysis = {
            'structure': self._analyze_structure(doc),
            'reasoning': self._identify_reasoning_style(text),
            'meta_cognition': self._analyze_meta_cognition(text),
            'complexity': self._calculate_complexity(doc),
            'coherence': self._analyze_coherence(doc),
            'task_specific': self._task_specific_analysis(text, task_type)
        }
        
        return analysis
    
    def _analyze_structure(self, doc) -> Dict[str, Any]:
        """Analyze the structural properties of the response"""
        sentences = list(doc.sents)
        
        structure = {
            'num_sentences': len(sentences),
            'avg_sentence_length': np.mean([len(sent.text.split()) for sent in sentences]) if sentences else 0,
            'num_paragraphs': len(doc.text.split('\n\n')),
            'has_list': bool(re.search(r'^\s*[-*•]\s', doc.text, re.MULTILINE)),
            'has_numbered_list': bool(re.search(r'^\s*\d+[\.)]\s', doc.text, re.MULTILINE)),
            'uses_examples': bool(re.search(r'for example|for instance|such as|e\.g\.', doc.text, re.IGNORECASE))
        }
        
        return structure
    
    def _identify_reasoning_style(self, text: str) -> Dict[str, int]:
        """Identify reasoning patterns in the text"""
        text_lower = text.lower()
        reasoning_counts = {}
        
        for style, markers in self.reasoning_markers.items():
            count = sum(1 for marker in markers if marker in text_lower)
            reasoning_counts[style] = count
        
        # Identify dominant style
        if reasoning_counts:
            dominant = max(reasoning_counts, key=reasoning_counts.get)
            reasoning_counts['dominant'] = dominant if reasoning_counts[dominant] > 0 else 'none'
        else:
            reasoning_counts['dominant'] = 'none'
        
        return reasoning_counts
    
    def _analyze_meta_cognition(self, text: str) -> Dict[str, Any]:
        """Analyze meta-cognitive aspects of the response"""
        text_lower = text.lower()
        
        meta_cognitive = {
            'markers_found': [],
            'confidence_expressions': 0,
            'uncertainty_expressions': 0,
            'self_correction': bool(re.search(r'actually|wait|no,|correction|mistake', text_lower)),
            'explicit_strategy': bool(re.search(r'my (approach|strategy|method)|I will|let me|first.*then', text_lower))
        }
        
        for marker in self.meta_cognitive_markers:
            if marker.lower() in text_lower:
                meta_cognitive['markers_found'].append(marker)
                if marker in ['certainly', 'definitely']:
                    meta_cognitive['confidence_expressions'] += 1
                elif marker in ['perhaps', 'maybe', 'possibly']:
                    meta_cognitive['uncertainty_expressions'] += 1
        
        meta_cognitive['score'] = len(meta_cognitive['markers_found']) / len(self.meta_cognitive_markers)
        
        return meta_cognitive
    
    def _calculate_complexity(self, doc) -> Dict[str, float]:
        """Calculate complexity metrics"""
        sentences = list(doc.sents)
        words = [token for token in doc if token.is_alpha]
        
        complexity = {
            'lexical_diversity': len(set([token.lemma_ for token in words])) / len(words) if words else 0,
            'avg_word_length': np.mean([len(token.text) for token in words]) if words else 0,
            'subordinate_clauses': len([token for token in doc if token.dep_ == 'mark']),
            'noun_phrases': len(list(doc.noun_chunks)),
            'dependency_depth': self._calculate_dependency_depth(doc)
        }
        
        return complexity
    
    def _analyze_coherence(self, doc) -> Dict[str, Any]:
        """Analyze coherence and flow of the response"""
        sentences = list(doc.sents)
        
        coherence = {
            'transition_words': 0,
            'pronoun_consistency': 0,
            'topic_consistency': 0
        }
        
        transitions = ['however', 'therefore', 'moreover', 'furthermore', 'additionally',
                      'consequently', 'nevertheless', 'thus', 'hence', 'meanwhile']
        
        for sent in sentences:
            sent_text = sent.text.lower()
            for trans in transitions:
                if trans in sent_text:
                    coherence['transition_words'] += 1
        
        # Simple topic consistency check using noun overlap
        if len(sentences) > 1:
            noun_sets = []
            for sent in sentences:
                nouns = set([token.lemma_ for token in sent if token.pos_ == 'NOUN'])
                noun_sets.append(nouns)
            
            overlaps = []
            for i in range(len(noun_sets) - 1):
                if noun_sets[i] and noun_sets[i + 1]:
                    overlap = len(noun_sets[i] & noun_sets[i + 1]) / min(len(noun_sets[i]), len(noun_sets[i + 1]))
                    overlaps.append(overlap)
            
            coherence['topic_consistency'] = np.mean(overlaps) if overlaps else 0
        
        return coherence
    
    def _task_specific_analysis(self, text: str, task_type: str) -> Dict[str, Any]:
        """Perform task-specific analysis"""
        analysis = {}
        
        if 'working_memory' in task_type:
            # Check for sequential processing indicators
            analysis['sequential_markers'] = bool(re.search(r'first|second|then|next|finally', text, re.IGNORECASE))
            analysis['uses_chunking'] = bool(re.search(r'group|chunk|batch|set of', text, re.IGNORECASE))
            
        elif 'executive_function' in task_type:
            # Check for task management indicators
            analysis['explicit_switching'] = bool(re.search(r'now|switching to|moving on to|next task', text, re.IGNORECASE))
            analysis['inhibition_success'] = 'not' in text.lower() or "n't" in text.lower()
            
        elif 'reasoning' in task_type:
            # Check for logical structure
            analysis['uses_premises'] = bool(re.search(r'given that|assuming|if.*then', text, re.IGNORECASE))
            analysis['explicit_conclusion'] = bool(re.search(r'therefore|thus|in conclusion|so', text, re.IGNORECASE))
            
        elif 'integration' in task_type:
            # Check for cross-domain connections
            analysis['makes_connections'] = text.count('similar') + text.count('like') + text.count('relates to')
            analysis['synthesis_depth'] = len(re.findall(r'because|since|as a result', text, re.IGNORECASE))
            
        elif 'meta_cognitive' in task_type:
            # Check for self-awareness
            analysis['explains_thinking'] = bool(re.search(r'my (thought|reasoning|approach)', text, re.IGNORECASE))
            analysis['evaluates_answer'] = bool(re.search(r'confident|certain|sure|uncertain|unsure', text, re.IGNORECASE))
        
        return analysis
    
    def _calculate_dependency_depth(self, doc) -> float:
        """Calculate average dependency tree depth"""
        depths = []
        for sent in doc.sents:
            for token in sent:
                depth = 0
                current = token
                while current.head != current:
                    depth += 1
                    current = current.head
                depths.append(depth)
        
        return np.mean(depths) if depths else 0
    
    def _aggregate_analysis(self, aggregate: Dict, single: Dict) -> None:
        """Aggregate single response analysis into overall analysis"""
        # Update patterns
        if single['reasoning']['dominant'] != 'none':
            aggregate['reasoning_styles'][single['reasoning']['dominant']] += 1
        
        # Add structure metrics
        aggregate['structure_metrics'].append(single['structure'])
        
        # Update meta-cognitive score
        aggregate['meta_cognitive_score'] += single['meta_cognition']['score']
        
        # Add complexity metrics
        aggregate['integration_complexity'].append(single['complexity'])
        
        # Track patterns
        for key, value in single.get('task_specific', {}).items():
            if isinstance(value, bool) and value:
                aggregate['patterns'][key] += 1
            elif isinstance(value, (int, float)):
                aggregate['patterns'][key] += value
    
    def _calculate_summary_stats(self, analysis: Dict) -> Dict[str, Any]:
        """Calculate summary statistics from analysis"""
        num_responses = len(analysis['structure_metrics'])
        
        if num_responses == 0:
            return {}
        
        summary = {
            'avg_response_length': np.mean([s['num_sentences'] for s in analysis['structure_metrics']]),
            'dominant_reasoning_style': analysis['reasoning_styles'].most_common(1)[0][0] if analysis['reasoning_styles'] else 'none',
            'meta_cognitive_index': analysis['meta_cognitive_score'] / num_responses,
            'structural_consistency': np.std([s['avg_sentence_length'] for s in analysis['structure_metrics']]),
            'error_rate': sum(analysis['error_patterns'].values()) / num_responses
        }
        
        # Calculate average complexity
        if analysis['integration_complexity']:
            complexity_metrics = analysis['integration_complexity']
            summary['avg_complexity'] = {
                'lexical_diversity': np.mean([c['lexical_diversity'] for c in complexity_metrics]),
                'dependency_depth': np.mean([c['dependency_depth'] for c in complexity_metrics])
            }
        
        return summary
