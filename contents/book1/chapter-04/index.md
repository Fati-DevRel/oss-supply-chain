# Chapter 4: Supply Chain Threat Modeling

## Summary

This chapter adapts traditional threat modeling techniques for the unique challenges of software supply chains. Unlike application security, where organizations control what they build, supply chain security requires modeling systems built, maintained, and distributed by others. This fundamental shift in control necessitates new approaches to identifying threats, assessing risk, and prioritizing defenses.

The chapter establishes threat modeling fundamentals tailored to supply chains, where external dependencies dominate attack surfaces, trust relationships are implicit and transitive, and visibility into upstream security practices is limited. It examines how established methodologies like STRIDE, PASTA, and attack trees can be adapted for dependency analysis, build pipeline security, and distribution infrastructure.

A key focus is identifying "crown jewel" dependencies that warrant elevated scrutiny. Criticality assessment considers functional importance, privilege level, execution context, data exposure, and replaceability. The chapter introduces concepts of single points of failure and common mode failures in dependency graphs, where shared libraries create correlated risks across supposedly independent systems.

Attack trees receive detailed treatment as particularly effective tools for supply chain scenarios. Worked examples demonstrate modeling adversary paths to production compromise, secret exfiltration, and maintainer account takeover, with annotations for cost, likelihood, and detection probability that guide defensive prioritization.

The chapter concludes by positioning threat modeling as a continuous practice rather than a one-time exercise. Lightweight approaches enable routine integration into development workflows, while comprehensive analysis addresses high-risk decisions. Training developers in supply chain threat thinking distributes security capability across teams.

## Sections

- 4.1 Supply Chain Threat Modeling Fundamentals
- 4.2 Threat Modeling Methodologies Applied
- 4.3 Identifying Crown Jewels in Your Dependency Graph
- 4.4 Building Attack Trees for Supply Chain Scenarios
- 4.5 Threat Modeling as a Continuous Practice
