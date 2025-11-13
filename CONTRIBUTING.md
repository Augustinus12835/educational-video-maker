# Contributing to Educational Video Maker

Thank you for your interest in contributing to this project! This guide will help you get started.

## Ways to Contribute

### 🐛 Bug Reports
Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, FFmpeg version)
- Relevant error messages or logs

### 💡 Feature Requests
Have an idea? We'd love to hear it! Please:
- Check existing issues first to avoid duplicates
- Describe the use case clearly
- Explain why it would be valuable for educators
- Consider if it fits the project scope (educational video automation)

### 📝 Documentation Improvements
Documentation is crucial for educators who may not be developers:
- Fix typos or unclear explanations
- Add examples or tutorials
- Improve installation instructions
- Translate documentation (if multilingual support is added)

### 🔧 Code Contributions
Want to contribute code? Great!

#### Before You Start
1. Check existing issues or open a new one to discuss your idea
2. Fork the repository
3. Create a feature branch: `git checkout -b feature/your-feature-name`

#### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/educational-video-maker
cd educational-video-maker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test with example video
python scripts/compile_video.py example/Week-1/Video-1
```

#### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions
- Include type hints where helpful
- Keep functions focused and small (single responsibility)
- Comment complex logic

#### Testing Your Changes
Before submitting:
- [ ] Run all scripts with the example video
- [ ] Verify video output quality
- [ ] Check that documentation still matches code
- [ ] Test on a clean environment (new virtual environment)
- [ ] Ensure no personal/sensitive data in commits

#### Commit Messages
Write clear commit messages:
- Use present tense: "Add feature" not "Added feature"
- First line: Brief summary (50 chars or less)
- Blank line, then detailed explanation if needed
- Reference issues: "Fixes #123" or "Relates to #456"

Example:
```
Add support for multilingual voices

- Add voice language detection
- Update Murf API integration for international voices
- Add language parameter to TTS generation script
- Update documentation with language options

Fixes #42
```

### 🎨 Example Videos
Share your success stories!
- Create videos in other subject areas
- Share your workflow adaptations
- Contribute example templates

## Pull Request Process

1. **Update Documentation**
   - Update README.md if adding features
   - Add docstrings to new functions
   - Update relevant files in docs/

2. **Test Thoroughly**
   - Run the example video compilation
   - Test your changes in a clean environment
   - Verify no regressions in existing functionality

3. **Submit PR**
   - Provide clear description of changes
   - Link related issues
   - Explain why the change is valuable
   - Include screenshots/videos if relevant

4. **Code Review**
   - Be open to feedback
   - Respond to review comments
   - Make requested changes promptly

5. **Merge**
   - Once approved, maintainers will merge
   - Your contribution will be credited in releases

## Project Scope

This project focuses on:
- ✅ Automated educational video creation
- ✅ Integration with AI services (TTS, research, transcription)
- ✅ Command-line workflow for educators
- ✅ Cost-effective solutions
- ✅ Quality educational content

Out of scope:
- ❌ Video editing GUIs (command-line focus)
- ❌ Live streaming or real-time video
- ❌ Non-educational use cases
- ❌ Features requiring expensive/proprietary tools

## Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers and learners
- Focus on what's best for educators and students
- Accept constructive criticism gracefully
- Show empathy toward others

### Unacceptable Behavior
- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other conduct inappropriate in a professional setting

### Enforcement
Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report issues to: [your contact method]

## Questions?

- Open a GitHub issue for technical questions
- Start a discussion for general questions or ideas
- Check existing documentation first

## Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- README acknowledgments

Thank you for helping make educational video creation more accessible! 🎓
