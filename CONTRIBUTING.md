# Contributing to the Software Supply Chain Security Book Series

Thank you for your interest in improving these books. Community contributions help ensure the content stays accurate, comprehensive, and useful.

## Repository Structure

The repository contains three books:

| Directory | Book | Chapters |
|-----------|------|----------|
| `contents/book1/` | Understanding the Software Supply Chain | 1-10 |
| `contents/book2/` | Protecting the Software Supply Chain | 11-22 |
| `contents/book3/` | Governing the Software Supply Chain | 23-33 |

Each chapter has its own directory (e.g., `chapter-05/`) containing section files named `ch-X.Y.md`.

## Types of Contributions

### Quick Fixes (No Issue Required)
- Typos and grammar corrections
- Broken link fixes
- Minor clarifications

### Larger Changes (Open an Issue First)
- Factual corrections
- New content or sections
- Structural reorganizations
- Adding citations to unsourced claims

## Content Standards

### Voice and Tone
- Use **"we"** for recommendations: "We recommend using lock files..."
- Use **"you"** for direct guidance: "You should verify signatures..."
- Professional but accessible: authoritative without being academic

### Formatting
- `### Heading` for main sections, `#### Subheading` for subsections
- **Bold** for key terms when first introduced
- `backticks` for package names, commands, and code
- `> blockquote` for practitioner quotes or notable findings

### Linting and Validation

The repository uses automated linting to ensure markdown quality and Material for MkDocs compatibility:

- **markdownlint-cli2**: Standard Markdown linting rules
- **mkdocs-material-linter**: Validates Material for MkDocs specific syntax (admonitions, content tabs, etc.)
- **cspell**: Spell checking
- **URL validation**: Checks for broken links

These checks run automatically on pull requests. To run them locally:

```bash
# Install linting tools
npm install -g markdownlint-cli2 mkdocs-material-linter

# Lint markdown files
markdownlint-cli2 --config .github/workflows/.markdownlint-cli2.jsonc "contents/**/*.md"

# Auto-fix some issues
markdownlint-cli2 --fix --config .github/workflows/.markdownlint-cli2.jsonc "contents/**/*.md"
```

Common Material for MkDocs features that are validated:
- Admonitions: `!!! note`, `!!! warning`, `!!! tip`, etc.
- Content tabs: `=== "Tab Name"`
- Collapsible blocks: `??? "Collapsible Title"`
- Code block annotations
- Proper indentation within special blocks

### Citations
All factual claims must be cited, with a URL wherever possible. Use Markdown reference links:

```markdown
According to recent research, 90% of applications contain open source components[^1].

[^1]: Synopsys, "Open Source Security and Risk Analysis Report," 2024. https://link-to-report.example.com
```

### Real-World Examples
When describing security incidents:
- **What** happened (the attack or vulnerability)
- **When** it occurred (specific date or timeframe)
- **Who** was affected (scope of impact)
- **Lessons learned** (what we can take away)

Never invent or hallucinate incidents. If you're unsure whether something happened, verify it first.

### Structure
- One main idea per paragraph
- Open sections with context establishing relevance
- Include concrete, actionable recommendations
- Cross-reference related sections where appropriate

## AI-Generated Content

AI tools (ChatGPT, Claude, Copilot, etc.) may be used to assist with contributions, but with important caveats:

### Disclosure Required
If AI tools contributed substantially to your submission, note this in your pull request description. Minor use (grammar checking, rephrasing a sentence) doesn't require disclosure.

### Human Verification Required
All AI-generated content **must be verified by the contributor** before submission:

- **Facts and statistics**: AI models can hallucinate. Verify every number, percentage, and claim against authoritative sources.
- **Citations and URLs**: AI frequently invents plausible-sounding but nonexistent references. Every citation must be manually verified to exist and say what you claim it says.
- **Security incidents**: AI models commonly fabricate security events that never happened. Cross-reference all incidents against news sources, CVE databases, or official advisories.
- **Dates and timelines**: Verify all dates. AI often gets timing wrong, especially for recent events.
- **Tool and project names**: Confirm that tools, libraries, and projects actually exist and work as described.

### What AI Can Help With
- Drafting initial prose that you then fact-check and revise
- Improving clarity and readability of your own writing
- Generating outlines or structures to organize your thoughts
- Suggesting related topics to cover

### What AI Cannot Replace
- Verifying that security incidents actually occurred
- Confirming citations point to real, accessible sources
- Ensuring technical accuracy of security recommendations
- Judgment about what content is appropriate and relevant

**Bottom line**: You are responsible for everything in your contribution. "The AI wrote it" is not an acceptable explanation for factual errors, hallucinated citations, or invented incidents.

## Submitting Changes

1. **Fork** the repository
2. **Create a branch** for your changes
3. **Make your edits** following the standards above
4. **Submit a pull request** using the PR template
5. **Respond to feedback** from reviewers

## Finding Things to Work On

- Check [open issues](https://github.com/scovetta/oss-supply-chain/issues) for tasks labeled `good first issue` or `help wanted`
- Search the content for `TODO` or `[citation needed]` markers
- Run link checking to find broken URLs
- Review recent security incidents that could be added to Appendix F

## Questions?

Open a [discussion](https://github.com/scovetta/oss-supply-chain/discussions) for questions about content, structure, or the contribution process.
