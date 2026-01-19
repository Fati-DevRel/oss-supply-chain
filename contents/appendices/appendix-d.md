## Appendix D: Security Checklist for Open Source Projects

This appendix provides a comprehensive security checklist for open source project maintainers. Use these checklists to assess your project's security posture, identify gaps, and prioritize improvements. Each section includes implementation guidance and links to relevant resources.

The checklist aligns with the OpenSSF Best Practices Badge[^openssf-badge] criteria and incorporates recommendations from the OpenSSF Scorecard project.

---

### Repository Security Settings

Configure your source code repository to prevent unauthorized changes and enforce security controls. These settings apply to GitHub; similar controls exist for GitLab, Bitbucket, and other platforms.

#### Branch Protection

- [ ] **Enable branch protection on default branch** — Prevent direct pushes to main branch
- [ ] **Require pull request reviews before merging** — At least one approval from a maintainer
- [ ] **Require review from code owners** — Ensure domain experts review relevant changes
- [ ] **Dismiss stale pull request approvals** — Re-review required after new commits
- [ ] **Require status checks to pass before merging** — CI must complete successfully
- [ ] **Require branches to be up to date before merging** — Prevent merge conflicts introducing issues
- [ ] **Require signed commits** — Verify commit author identity via GPG or SSH signatures
- [ ] **Require linear history** — Simplify auditing by preventing merge commits
- [ ] **Restrict who can push to matching branches** — Limit to trusted maintainers
- [ ] **Do not allow bypassing branch protection** — Apply rules to administrators too

#### Access Control

- [ ] **Enable two-factor authentication requirement** — Require 2FA for all organization members
- [ ] **Review and minimize admin access** — Limit administrative privileges to essential personnel
- [ ] **Audit collaborator permissions quarterly** — Remove inactive or unnecessary access
- [ ] **Use teams for permission management** — Avoid individual permission grants
- [ ] **Enable SSO/SAML if available** — Centralize identity management for organizations
- [ ] **Review and rotate deploy keys annually** — Remove unused keys promptly
- [ ] **Use fine-grained personal access tokens** — Avoid classic tokens with broad permissions

#### Repository Settings

- [ ] **Enable Dependabot alerts** — Receive notifications for vulnerable dependencies
- [ ] **Enable Dependabot security updates** — Automated pull requests for security fixes
- [ ] **Enable secret scanning** — Detect accidentally committed credentials
- [ ] **Enable secret scanning push protection** — Block commits containing secrets
- [ ] **Enable code scanning (CodeQL or similar)** — Automated vulnerability detection
- [ ] **Configure security advisories** — Enable private vulnerability reporting
- [ ] **Set repository visibility appropriately** — Public for open source; private for sensitive components
- [ ] **Disable unused features** — Turn off wikis, projects, discussions if not used

**Implementation Guide**: GitHub Repository Security Settings[^github-repo-security]

---

### Documentation Requirements

Security documentation communicates your project's security posture and provides guidance for users and researchers. Complete documentation builds trust and streamlines security processes.

#### Required Security Documentation

- [ ] **SECURITY.md in repository root** — Clear instructions for reporting vulnerabilities
  - [ ] Preferred contact method (email, security advisory, bug bounty platform)
  - [ ] Expected response timeline
  - [ ] Disclosure policy and timeline
  - [ ] PGP key for encrypted communications (if applicable)
  - [ ] Scope of security policy (which versions are supported)

- [ ] **Security policy published and discoverable** — Linked from README and repository settings

- [ ] **Supported versions documented** — Clear statement of which versions receive security updates

#### General Documentation

- [ ] **README.md with project overview** — Clear description of what the project does
- [ ] **Installation instructions** — Secure installation methods documented
- [ ] **LICENSE file present** — Clear licensing terms using SPDX identifier
- [ ] **CONTRIBUTING.md with guidelines** — Include security considerations for contributors
- [ ] **CODE_OF_CONDUCT.md** — Community standards and enforcement procedures
- [ ] **CHANGELOG.md or releases page** — Document changes including security fixes

#### Security-Specific Documentation

- [ ] **Threat model documented** — Key assets, threats, and mitigations described
- [ ] **Security architecture overview** — How security controls are implemented
- [ ] **Authentication/authorization model** — If applicable, document access control design
- [ ] **Cryptography usage documented** — Algorithms, key management, and rationale
- [ ] **Known limitations documented** — Security boundaries and out-of-scope threats
- [ ] **Hardening guide** — Secure configuration recommendations for users
- [ ] **Dependency policy** — How dependencies are selected and evaluated

**Template**: GitHub SECURITY.md Template[^github-security-template]

**Tool**: OpenSSF Disclosure Check[^openssf-disclosure-check] — Verify vulnerability disclosure mechanisms

---

### Build and Release Security

Secure build processes prevent tampering and ensure users receive authentic artifacts. These controls form the foundation of supply chain integrity.

#### Build Environment Security

- [ ] **Use CI/CD for all builds** — No builds from local developer machines for releases
- [ ] **Pin CI/CD action versions by hash** — Prevent malicious action updates

  ```yaml
  # Good: Pinned by SHA
  uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608
  # Risky: Floating tag
  uses: actions/checkout@v4
  ```

- [ ] **Minimize build dependencies** — Only include necessary tools and packages
- [ ] **Use ephemeral build environments** — Fresh environment for each build
- [ ] **Isolate build environments** — Prevent network access during build where possible
- [ ] **Pin all dependency versions** — Use lockfiles for reproducible builds
- [ ] **Verify dependency integrity** — Check hashes during dependency resolution
- [ ] **Scan dependencies before build** — Fail builds with known vulnerable dependencies

#### Build Process

- [ ] **Document build process completely** — Anyone should be able to reproduce the build
- [ ] **Enable compiler security flags** — Stack canaries, ASLR, PIE, FORTIFY_SOURCE
- [ ] **Run SAST during build** — Static analysis integrated into CI pipeline
- [ ] **Run tests including security tests** — Unit tests, integration tests, security-specific tests
- [ ] **Generate SBOM during build** — Automated bill of materials creation
- [ ] **Build from verified source only** — Clone from official repository, verify tags

#### Release Signing

- [ ] **Sign all release artifacts** — Use GPG, Sigstore, or platform-native signing
- [ ] **Publish signing keys/certificates** — Make verification possible for users
- [ ] **Sign git tags for releases** — `git tag -s` for signed tags
- [ ] **Document verification process** — Instructions for users to verify signatures
- [ ] **Use Sigstore for keyless signing** — Reduce key management burden
- [ ] **Generate provenance attestations** — SLSA provenance for build transparency
- [ ] **Publish attestations with releases** — Make provenance verifiable

#### Release Process

- [ ] **Use protected release branches/tags** — Prevent unauthorized release modifications
- [ ] **Require multiple approvals for releases** — No single person can release alone
- [ ] **Automate release process** — Reduce human error and intervention points
- [ ] **Publish to official registries only** — npm, PyPI, Maven Central, etc.
- [ ] **Use trusted publishing where available** — OIDC-based publishing without long-lived secrets
- [ ] **Include SBOM with release** — Ship bill of materials with artifacts
- [ ] **Announce releases through official channels** — Prevent impersonation

**Implementation Guide**: SLSA Requirements[^slsa-requirements]

**Tool**: Sigstore[^sigstore] — Free signing infrastructure for open source

---

### Vulnerability Management

Effective vulnerability management protects your users and maintains trust in your project. Establish clear processes before vulnerabilities are discovered.

#### Vulnerability Reporting

- [ ] **Private reporting channel established** — Security advisories, email, or bug bounty platform
- [ ] **Designated security contact(s)** — Named individuals responsible for security issues
- [ ] **Acknowledgment timeline defined** — Respond within 48-72 hours
- [ ] **Assessment timeline defined** — Initial severity assessment within 1 week
- [ ] **Fix timeline expectations set** — Critical: days, High: weeks, Medium: months
- [ ] **Disclosure timeline defined** — Typically 90 days, coordinated with reporter
- [ ] **Safe harbor statement** — Protect good-faith security researchers

#### Vulnerability Response Process

- [ ] **Triage process documented** — How reports are evaluated and prioritized
- [ ] **Severity rating methodology** — CVSS or equivalent for consistent assessment
- [ ] **Fix development process** — Private branch/fork for developing fixes
- [ ] **Testing requirements for fixes** — Verify fix addresses vulnerability without regression
- [ ] **Backporting policy defined** — Which older versions receive security fixes
- [ ] **Communication plan** — How users are notified of vulnerabilities and fixes

#### Vulnerability Disclosure

- [ ] **Request CVE for confirmed vulnerabilities** — Use CNA or MITRE process
- [ ] **Publish security advisory** — GitHub Security Advisories or equivalent
- [ ] **Credit reporters appropriately** — Acknowledge researchers per their preference
- [ ] **Provide clear upgrade guidance** — Tell users exactly what to do
- [ ] **Document workarounds if available** — Temporary mitigations before patching
- [ ] **Coordinate with downstream projects** — Notify known significant consumers

#### Ongoing Vulnerability Management

- [ ] **Monitor for dependency vulnerabilities** — Dependabot, Snyk, or similar
- [ ] **Regular dependency updates** — Keep dependencies current, not just security fixes
- [ ] **Periodic security assessments** — Self-assessment or external audit annually
- [ ] **Track security debt** — Known issues and their remediation timeline
- [ ] **Review past vulnerabilities** — Learn from patterns to prevent recurrence

**Implementation Guide**: CERT Guide to Coordinated Vulnerability Disclosure[^cert-cvd-guide]

**Template**: GitHub Security Advisory Process[^github-security-advisory]

---

### Community and Governance

Clear governance and community practices ensure security decisions are made transparently and that the project can sustain security efforts long-term.

#### Project Governance

- [ ] **Governance model documented** — Decision-making process is clear
- [ ] **Maintainer roles defined** — Who can merge, release, handle security
- [ ] **Succession plan exists** — Project continuity if maintainers leave
- [ ] **Multiple active maintainers** — No single point of failure (bus factor > 1)
- [ ] **Foundation or organizational backing** — For critical projects, formal support structure
- [ ] **Funding model transparent** — How the project sustains development

#### Contributor Security

- [ ] **Contributor verification process** — Validate significant new contributors
- [ ] **CLA or DCO requirement** — Legal clarity for contributions
- [ ] **New contributor review requirements** — Enhanced scrutiny for first-time contributors
- [ ] **Commit access progression** — Clear path from contributor to committer
- [ ] **Periodic access review** — Remove inactive maintainer access

#### Security Culture

- [ ] **Security discussed in project communications** — Regular presence in meetings/updates
- [ ] **Security champion identified** — Point person for security matters
- [ ] **Security training for maintainers** — At least basic secure development training
- [ ] **Incident response plan** — Steps to take if project is compromised
- [ ] **Post-incident review process** — Learn from security incidents

#### Transparency

- [ ] **Public issue tracker** — Visible development activity (excluding security issues)
- [ ] **Public roadmap** — Development direction is visible
- [ ] **Meeting notes published** — For projects with governance meetings
- [ ] **Security improvements communicated** — Share security enhancements publicly
- [ ] **Annual security report** — Summary of security activities and status

**Implementation Guide**: OpenSSF Best Practices Badge[^openssf-badge-criteria]

---

### Self-Assessment Template

Use this scoring template to assess your project's security maturity. Score each category and identify priority improvements.

#### Scoring Guide

| Score | Meaning |
|-------|---------|
| 0 | Not implemented |
| 1 | Partially implemented or planned |
| 2 | Fully implemented |
| N/A | Not applicable to this project |

#### Assessment Worksheet

**Repository Security** (Max: 20 points)

| Control | Score (0-2) | Notes |
|---------|-------------|-------|
| Branch protection enabled | | |
| Required reviews configured | | |
| 2FA required for org members | | |
| Signed commits required/encouraged | | |
| Dependabot/security scanning enabled | | |
| Secret scanning enabled | | |
| Code scanning enabled | | |
| Access permissions reviewed | | |
| Security advisories enabled | | |
| Deploy keys/tokens minimized | | |

**Documentation** (Max: 14 points)

| Control | Score (0-2) | Notes |
|---------|-------------|-------|
| SECURITY.md present and complete | | |
| Supported versions documented | | |
| README with security considerations | | |
| CONTRIBUTING.md with security guidance | | |
| Threat model documented | | |
| Hardening guide available | | |
| Dependency policy documented | | |

**Build and Release** (Max: 16 points)

| Control | Score (0-2) | Notes |
|---------|-------------|-------|
| CI/CD used for releases | | |
| Dependencies pinned with lockfiles | | |
| Build process documented | | |
| Release artifacts signed | | |
| SBOM generated | | |
| Provenance attestations created | | |
| Trusted publishing enabled | | |
| Multiple approvals for release | | |

**Vulnerability Management** (Max: 14 points)

| Control | Score (0-2) | Notes |
|---------|-------------|-------|
| Private reporting channel exists | | |
| Response timeline defined | | |
| Severity rating process defined | | |
| CVE process established | | |
| Security advisory process defined | | |
| Dependency monitoring active | | |
| Backporting policy defined | | |

**Governance** (Max: 12 points)

| Control | Score (0-2) | Notes |
|---------|-------------|-------|
| Governance model documented | | |
| Multiple active maintainers | | |
| Contributor verification process | | |
| Security champion identified | | |
| Incident response plan exists | | |
| Access review performed periodically | | |

#### Maturity Levels

| Total Score | Maturity Level | Description |
|-------------|----------------|-------------|
| 0-19 | **Initial** | Basic security awareness; significant gaps |
| 20-39 | **Developing** | Some controls in place; key areas need attention |
| 40-59 | **Defined** | Most controls implemented; refinement needed |
| 60-69 | **Managed** | Strong security posture; continuous improvement |
| 70-76 | **Optimizing** | Excellent security practices; industry leader |

#### Priority Matrix

After scoring, prioritize improvements using this matrix:

| Impact | Low Effort | High Effort |
|--------|-----------|-------------|
| **High** | Do immediately | Plan for next quarter |
| **Low** | Quick wins when time permits | Evaluate necessity |

**High-impact, low-effort items typically include:**

- Enabling Dependabot and secret scanning
- Creating SECURITY.md
- Enabling branch protection
- Setting up 2FA requirements

---

### Additional Resources

- **OpenSSF Best Practices Badge**: https://www.bestpractices.dev/[^openssf-badge-resource]
- **OpenSSF Scorecard**: https://securityscorecards.dev/[^openssf-scorecard]
- **CISA Secure Software Development Attestation**: https://www.cisa.gov/secure-software-attestation-form[^cisa-attestation]
- **GitHub Security Hardening Guide**: https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions[^github-hardening]
- **AllStar (Automated Security Policy Enforcement)**: https://github.com/ossf/allstar[^allstar]
- **Scorecard Action**: https://github.com/ossf/scorecard-action[^scorecard-action]

[^openssf-badge]: Open Source Security Foundation, "Best Practices Badge," https://www.bestpractices.dev/

[^github-repo-security]: GitHub, "Managing security and analysis settings for your repository," https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository

[^github-security-template]: GitHub, "Adding a security policy to your repository," https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository

[^openssf-disclosure-check]: Open Source Security Foundation, "Disclosure Check," https://github.com/ossf/disclosure-check

[^slsa-requirements]: SLSA, "Requirements," https://slsa.dev/spec/v1.0/requirements

[^sigstore]: Sigstore, "Sigstore," https://www.sigstore.dev/

[^cert-cvd-guide]: CERT, "Guide to Coordinated Vulnerability Disclosure," https://vuls.cert.org/confluence/display/CVD

[^github-security-advisory]: GitHub, "About repository security advisories," https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories

[^openssf-badge-criteria]: Open Source Security Foundation, "Best Practices Badge Criteria," https://www.bestpractices.dev/en/criteria

[^openssf-badge-resource]: Open Source Security Foundation, "Best Practices Badge," https://www.bestpractices.dev/

[^openssf-scorecard]: Open Source Security Foundation, "Scorecard," https://securityscorecards.dev/

[^cisa-attestation]: CISA, "Secure Software Development Attestation Form," https://www.cisa.gov/secure-software-attestation-form

[^github-hardening]: GitHub, "Security hardening for GitHub Actions," https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions

[^allstar]: Open Source Security Foundation, "AllStar," https://github.com/ossf/allstar

[^scorecard-action]: Open Source Security Foundation, "Scorecard Action," https://github.com/ossf/scorecard-action
