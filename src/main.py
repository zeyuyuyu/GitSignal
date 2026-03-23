import os
import git
import torch
from typing import Dict, List
from .models import ImpactAnalyzer
from .diff_parser import DiffParser
from .visualizer import ImpactVisualizer

class GitSignal:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
        self.analyzer = ImpactAnalyzer()
        self.parser = DiffParser()
        self.visualizer = ImpactVisualizer()
    
    def analyze_changes(self) -> Dict:
        """Analyze current branch changes and predict impact."""
        diff = self.repo.head.commit.diff()
        parsed_diff = self.parser.parse(diff)
        
        impact_analysis = self.analyzer.predict(
            parsed_diff,
            model_types=['regression', 'performance', 'security']
        )
        
        return {
            'risk_score': impact_analysis.risk_score,
            'affected_services': impact_analysis.affected_services,
            'performance_impact': impact_analysis.performance_metrics,
            'security_risks': impact_analysis.security_findings,
            'suggested_reviewers': self._get_suggested_reviewers(parsed_diff)
        }
    
    def _get_suggested_reviewers(self, diff_data: Dict) -> List[str]:
        """Suggest reviewers based on affected code areas."""
        return self.analyzer.get_relevant_reviewers(diff_data)

def main():
    signal = GitSignal(os.getcwd())
    analysis = signal.analyze_changes()
    print(analysis)

if __name__ == '__main__':
    main()