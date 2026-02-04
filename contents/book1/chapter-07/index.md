# Chapter 7: Build System and Distribution Attacks

## Summary

This chapter examines how attackers compromise the infrastructure that transforms source code into distributed software. Build systems occupy a uniquely privileged position in the software supply chain, with access to source code, signing keys, credentials, and distribution channels. A single compromised build system can affect millions of downstream users.

The chapter analyzes landmark incidents that reshaped industry understanding of supply chain risk. The SolarWinds SUNBURST attack (2020) demonstrated nation-state capability to infiltrate build processes, reaching approximately 18,000 organizations through legitimately signed updates. The 3CX compromise (2023) revealed cascading supply chain attacks, where compromise of one vendor (Trading Technologies) enabled attackers to reach another (3CX) through an employee's personal device. The Codecov incident (2021) showed how a single modified script executed in thousands of CI/CD pipelines could harvest credentials at scale. The XZ Utils backdoor (2024) exposed how patient adversaries can spend years building trust with overwhelmed maintainers to insert sophisticated backdoors into critical infrastructure.

Beyond case studies, the chapter provides a systematic taxonomy of CI/CD vulnerabilities including secrets exposure, insufficient access controls, pull request exploitation, cache poisoning, and runner security weaknesses. It examines code signing's role and limitations, emphasizing that signatures prove integrity and attribution but not safety. Modern alternatives like Sigstore, SLSA provenance attestations, and the in-toto framework address these gaps by providing verifiable claims about how software was built.

The chapter concludes with distribution channel attacks, including the Polyfill.io incident (2024) that weaponized a trusted CDN to inject malicious code into over 100,000 websites. Defense requires treating the entire path from developer to consumer as potential attack surface.

## Sections

- 7.1 Compromising Build Infrastructure
- 7.2 Case Study: SolarWinds and the SUNBURST Attack
- 7.3 Case Study: 3CX Desktop App Compromise (2023)
- 7.4 Case Study: Codecov Bash Uploader (2021)
- 7.5 Case Study: XZ Utils Backdoor (2024)
- 7.6 CI/CD Pipeline Vulnerabilities
- 7.7 Code Signing and Its Limitations
- 7.8 Attacks on Distribution Channels
- 7.9 Case Study: Notepad++ Update Hijacking (2025)
