# Chapter 22: Platform Engineering for Supply Chain Security

This chapter explores how platform engineering transforms software supply chain security from a burden imposed on individual development teams into an embedded capability delivered through shared infrastructure. Rather than requiring every developer to become a security expert, platforms abstract security complexity behind simple interfaces, making secure practices the path of least resistance.

The chapter introduces the concept of "golden paths" or "paved roads"---platform-supported workflows where security, compliance, and operational requirements are built in by default. When developers create services using platform templates, they automatically receive dependency scanning, SBOM generation, hardened container images, and secrets management without explicit configuration.

Secure defaults and guardrails form another core theme. The most effective security controls are invisible: registries that serve only vetted dependencies, build pipelines that automatically block vulnerable releases, and admission controllers that enforce policies at deployment time. The chapter provides practical guidance on curated registries, policy-as-code implementation, and balancing flexibility with control through graduated enforcement.

Supply chain security as a platform service centralizes capabilities like dependency management, vulnerability alerting, and SBOM generation. Development teams consume these services rather than building their own, enabling consistent coverage and reducing duplicated effort across the organization.

The chapter concludes with guidance on managing AI coding assistants, which introduce novel risks including "slopsquatting"---attackers registering packages that AI models hallucinate. Organizations need clear policies, sanctioned tool lists, security-focused configurations, and developer training that addresses AI-specific concerns while preserving productivity benefits.
