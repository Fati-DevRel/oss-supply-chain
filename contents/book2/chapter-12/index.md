# Chapter 12: Software Composition Analysis and Inventory

This chapter establishes the foundational practices of software inventory and transparency that underpin all supply chain security efforts. It begins with the critical principle that you cannot secure what you cannot see, examining discovery methods for building comprehensive software inventory across source code, build systems, and runtime environments.

The chapter provides extensive guidance on Software Bills of Materials (SBOMs), covering the two dominant formats (SPDX and CycloneDX), generation approaches, content requirements, and regulatory drivers like Executive Order 14028 and the EU Cyber Resilience Act. It then extends these concepts to AI systems through AI Bills of Materials (AI-BOMs), addressing the unique inventory challenges posed by machine learning models, training datasets, and model provenance.

A critical examination of vulnerability databases reveals significant gaps in the ecosystem. The CVE/NVD system faces assignment delays and enrichment backlogs, while different databases provide inconsistent severity scores and coverage. The chapter recommends multi-source strategies that aggregate public and commercial vulnerability data.

License compliance emerges as a parallel concern that shares infrastructure with security scanning. The same SBOMs and SCA tools that enable vulnerability management also reveal license obligations, making unified governance approaches more effective than separate processes.

The chapter concludes with practical guidance on selecting software composition analysis tools, comparing open source options (Trivy, Grype, Syft, OWASP Dependency-Check), commercial platforms (Snyk, Sonatype, Black Duck), and platform-integrated solutions (GitHub Advanced Security, GitLab Security). Key evaluation criteria include detection accuracy, ecosystem coverage, vulnerability data sources, and integration capabilities.
