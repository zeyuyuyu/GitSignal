# GitSignal

## AI-Powered Code Change Impact Analysis

GitSignal is an intelligent system that analyzes git diffs to predict the potential impact and risks of code changes before they're merged. Using advanced ML models trained on millions of historical changes, it provides actionable insights about:

- 🔍 Estimated regression probability
- 🎯 Services and components likely to be affected
- ⚡ Performance impact predictions
- 🔒 Security vulnerability introduction risk
- 👥 Suggested reviewers based on affected code areas

### Key Features

- Real-time analysis of Pull Requests
- Integration with GitHub Actions
- Custom ML models for your codebase
- Impact visualization graphs
- Automated test selection based on changes
- Early warning system for high-risk changes

### Installation

```bash
pip install gitsignal
gitsignal init --repo-path ./
```

### Usage

```bash
# Analyze current branch changes
gitsignal analyze

# Setup GitHub Action integration
gitsignal integrate --github
```

### Configuration

Create a `gitsignal.yaml` in your repo root:

```yaml
models:
  regression: true
  performance: true
  security: true
thresholds:
  risk_score: 0.7
  performance_impact: 5
```

### Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

### License

MIT