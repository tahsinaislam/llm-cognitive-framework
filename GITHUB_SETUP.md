# GitHub Setup Instructions for LLM Cognitive Profiling Framework

## Step-by-Step Guide to Publishing Your Project on GitHub

### 1. Create a GitHub Account (if you don't have one)
- Go to [github.com](https://github.com)
- Click "Sign up"
- Use your Georgia Tech email (tislam38@gatech.edu) for academic verification

### 2. Create a New Repository

1. Log into GitHub
2. Click the "+" icon in the top right
3. Select "New repository"
4. Configure your repository:
   - **Repository name:** `llm-cognitive-framework`
   - **Description:** "A computational framework for characterizing cognitive profiles of Large Language Models"
   - **Visibility:** Public (recommended for academic work)
   - **Initialize:** Don't add README, .gitignore, or license (we already have them)
5. Click "Create repository"

### 3. Prepare Your Local Repository

Open terminal/command prompt and navigate to your project:

```bash
# Extract the archive if you haven't already
tar -xzf cognitive_framework.tar.gz
cd cognitive_framework

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: LLM Cognitive Profiling Framework"
```

### 4. Connect to GitHub Repository

Replace `yourusername` with your actual GitHub username:

```bash
# Add GitHub repository as remote origin
git remote add origin https://github.com/yourusername/llm-cognitive-framework.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 5. Set Up GitHub Secrets (for CI/CD)

1. Go to your repository on GitHub
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Add the following secrets (optional, for automated testing):
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `GOOGLE_API_KEY`
   - `DEEPSEEK_API_KEY`

### 6. Configure GitHub Pages (for Documentation)

1. Go to "Settings" → "Pages"
2. Source: "Deploy from a branch"
3. Branch: `main` → `/docs` folder
4. Click "Save"

### 7. Add Repository Topics

1. Go to your repository main page
2. Click the gear icon next to "About"
3. Add topics:
   - `cognitive-science`
   - `llm`
   - `artificial-intelligence`
   - `gpt-4`
   - `claude`
   - `gemini`
   - `python`
   - `research`
   - `georgia-tech`

### 8. Create a Release

1. Click "Releases" on the right sidebar
2. Click "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: "Initial Release - v1.0.0"
5. Describe the release:
   ```markdown
   ## LLM Cognitive Profiling Framework v1.0.0
   
   Initial release of the framework for characterizing cognitive profiles of Large Language Models.
   
   ### Features
   - Support for GPT-4, Claude, Gemini, and DeepSeek
   - 150+ cognitive assessment tasks
   - Automated analysis and visualization
   - Docker deployment support
   
   ### Requirements
   - Python 3.8+
   - API keys for supported LLMs
   
   See README for installation and usage instructions.
   ```
6. Attach the `cognitive_framework.tar.gz` file
7. Click "Publish release"

### 9. Update README Links

After creating the repository, update these placeholders in your README.md:

```bash
# Replace 'yourusername' with your actual GitHub username
sed -i 's/yourusername/YOUR_GITHUB_USERNAME/g' README.md
git add README.md
git commit -m "docs: update repository URLs"
git push
```

### 10. Add Badges to README

Add these badges to the top of your README.md (after the title):

```markdown
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub Stars](https://img.shields.io/github/stars/yourusername/llm-cognitive-framework?style=social)
![GitHub Issues](https://img.shields.io/github/issues/yourusername/llm-cognitive-framework)
![GitHub Actions](https://github.com/yourusername/llm-cognitive-framework/workflows/CI%2FCD%20Pipeline/badge.svg)
```

### 11. Academic Citation

Add this to your GitHub repository for academic citations:

1. Create file `CITATION.cff`:
```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
- family-names: "Islam"
  given-names: "Tahsina"
  orcid: "https://orcid.org/0000-0000-0000-0000"
  affiliation: "Georgia Institute of Technology"
  email: "tislam38@gatech.edu"
title: "LLM Cognitive Profiling Framework"
version: 1.0.0
date-released: 2025-01-01
url: "https://github.com/yourusername/llm-cognitive-framework"
```

### 12. Project Settings

1. Go to "Settings" → "General"
2. Features:
   - ✅ Issues
   - ✅ Projects
   - ✅ Preserve this repository
   - ✅ Discussions (for Q&A)
3. Pull Requests:
   - ✅ Allow merge commits
   - ✅ Allow squash merging
   - ✅ Automatically delete head branches

### 13. Add a Project Board

1. Click "Projects" tab
2. Click "New project"
3. Select "Board" template
4. Name: "Development Roadmap"
5. Add columns:
   - To Do
   - In Progress
   - Testing
   - Done
6. Add initial issues/tasks

### 14. Branch Protection (Optional)

1. Go to "Settings" → "Branches"
2. Add rule for `main` branch:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Include administrators

### 15. Share Your Repository

Once published, share your repository:

1. **Academic Profile:** Add to your academic portfolio/CV
2. **LinkedIn:** Share as a project accomplishment
3. **Course Submission:** Include the GitHub link in your project submission
4. **Research Community:** Share in relevant academic forums

## Common Git Commands for Maintenance

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "type: description"

# Push changes
git push

# Pull latest changes
git pull

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge branch
git merge feature/new-feature

# View history
git log --oneline
```

## Troubleshooting

### Authentication Issues
If you get authentication errors:
1. Generate a Personal Access Token:
   - Go to Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Select scopes: repo, workflow
2. Use token as password when pushing

### Large File Issues
If files are too large:
```bash
# Use Git LFS for large files
git lfs track "*.pkl"
git lfs track "*.h5"
git add .gitattributes
```

### Permission Denied
```bash
# Check remote URL
git remote -v

# Update remote URL if needed
git remote set-url origin https://github.com/yourusername/llm-cognitive-framework.git
```

## Benefits of Publishing on GitHub

1. **Version Control:** Track all changes to your code
2. **Collaboration:** Easy for others to contribute
3. **Portfolio:** Showcase your work to employers/academics
4. **CI/CD:** Automated testing and deployment
5. **Community:** Get feedback and contributions
6. **Backup:** Cloud backup of your project
7. **DOI:** Can get DOI through Zenodo for citations

## Next Steps After Publishing

1. **Documentation:** Consider adding API documentation
2. **Tests:** Add comprehensive test coverage
3. **Examples:** Add jupyter notebooks with examples
4. **Docker Hub:** Publish Docker image
5. **PyPI:** Publish as Python package
6. **Paper:** Link to your research paper when published
7. **Blog Post:** Write about your findings

Good luck with your project! 🚀
