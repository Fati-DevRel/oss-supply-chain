# Software Supply Chain Security

A comprehensive three-book series on software supply chain security, covering threats, defenses, and governance. This open-source manuscript provides security professionals, developers, and organizational leaders with practical guidance for securing modern software development practices.

## The Book Series

| Book | Title | Chapters | Focus |
|------|-------|----------|-------|
| **Book 1** | Understanding the Software Supply Chain | 1-10 | Foundations and attack patterns |
| **Book 2** | Protecting the Software Supply Chain | 11-22 | Practical defenses and implementation |
| **Book 3** | Governing the Software Supply Chain | 23-33 | Policy, compliance, and organizational strategy |

### Book 1: Understanding the Software Supply Chain

Provides the foundation for understanding supply chain security: how modern software is built, the threat landscape, historical attacks, and detailed attack patterns.

- **Part I - Foundations (Chapters 1-4)**: How software is built today, supply chain threats overview, historical attacks, and ecosystem-specific risks
- **Part II - Attack Patterns (Chapters 5-10)**: Malicious packages, dependency confusion, typosquatting, build system attacks, insider threats, and social engineering

### Book 2: Protecting the Software Supply Chain

Translates threat knowledge into practical defenses across the entire development lifecycle, from dependency selection through production deployment.

- **Part III - Risk Assessment & Testing (Chapters 11-15)**: Risk measurement, SBOMs, dependency management, security testing, and red teaming
- **Part IV - Defense & Response (Chapters 16-20)**: Securing development environments, CI/CD pipelines, distribution channels, incident response, and crisis communication
- **Part V - Operationalizing Defense (Chapters 21-22)**: Building security programs and platform engineering approaches

### Book 3: Governing the Software Supply Chain

Addresses the human, policy, and strategic dimensions of supply chain security: organizational commitment, regulatory compliance, economic incentives, and industry collaboration.

- **Part V - People & Organizations (Chapters 23-25)**: Training and security culture, open source maintainer perspectives, and vendor risk management
- **Part VI - Regulatory & Legal (Chapters 26-29)**: Regulatory landscape (EO 14028, EU CRA), compliance frameworks, legal considerations, and industry initiatives
- **Part VII - Context & Future (Chapters 30-33)**: Economics of supply chain security, geopolitical considerations, lessons from other industries, and future directions

## Repository Structure

```
contents/
├── book1/                 # Chapters 1-10
│   └── chapter-XX/        # Each chapter directory contains:
│       ├── README.md      #   Chapter overview
│       ├── ch-X.Y.md      #   Section files
│       └── img/           #   Chapter images
├── book2/                 # Chapters 11-22
├── book3/                 # Chapters 23-33
├── appendices/            # Appendices A-H
└── frontmatter/           # Author info, legal notices, templates

scripts/
├── build-all.sh           # Build all three books
├── cover-generator.py     # Generate book covers
├── custom_template.latex  # Template for building PDF
└── verify_urls.py         # URL verification utility
```

## Building PDFs

### Prerequisites

- [Pandoc](https://pandoc.org/) (document converter)
- [XeLaTeX](https://tug.org/xetex/) (PDF generation)
- [ImageMagick](https://imagemagick.org/) (image conversion)
- Python 3.x (for cover generation)

### Build Commands

Build all three books:

```bash
./scripts/build-all.sh
```

Build individual books:

```bash
./contents/book1/build-pdf.sh
./contents/book2/build-pdf.sh
./contents/book3/build-pdf.sh
```

Output PDFs are generated in the `scripts/` directory.

## Appendices

| Appendix | Title | Books |
|----------|-------|-------|
| A | Glossary | All |
| B | Resources | All |
| C | SBOM/AI-BOM Guide | Book 2 |
| D | Security Checklist | Book 2 |
| E | Sample Policies & Templates | Book 3 |
| F | Incident Timeline | Book 1 |
| G | Ecosystem Security Guides | Book 2 |
| H | Compliance Mapping Matrix | Book 3 |

## Contributing

Contributions are welcome. When contributing:

- Maintain technical accuracy on security topics
- Cite sources for factual claims and statistics
- Feel free to use AI to generate content, but read and understand it before sending a pull request.
- Use consistent terminology (refer to Appendix A: Glossary)
- Follow the existing chapter/section structure (`ch-X.Y.md` format)
- Keep real-world examples specific with verifiable details (names, dates, impacts)

See [CLAUDE.md](CLAUDE.md) for detailed content standards and writing guidelines.

## License

This work is dedicated to the public domain under [CC0 1.0 Universal](LICENSE). You can copy, modify, distribute, and use the work, even for commercial purposes, without asking permission.


