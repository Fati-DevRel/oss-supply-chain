# Chapter 1: How Software Is Built Today

Modern software development has undergone a fundamental transformation. Where developers once wrote applications largely from scratch, today they assemble software from vast ecosystems of pre-built components. The average commercial application now contains over 500 open source components, with JavaScript applications routinely exceeding 1,000 dependencies. This shift toward component-based development has enabled unprecedented innovation but created a complex web of trust relationships that most organizations barely understand.

Open source software forms the foundation of virtually all modern technology, representing an estimated $8.8 trillion in demand-side value globally. Organizations consume open source as direct dependencies, transitive dependencies, development tooling, and infrastructure software. This ubiquity means that open source security is software security.

The software supply chain encompasses all people, processes, tools, code, and infrastructure involved from initial development through production deployment. Key actors include maintainers, contributors, package registry operators, build system providers, and consumers. Trust flows through this chain implicitly: adding a dependency means trusting its maintainers, their dependencies, the build infrastructure, and distribution channels.

High-profile incidents like SolarWinds (2020), Log4Shell (2021), and the XZ Utils backdoor (2024) have made supply chain security a board-level and national security priority. Attack volumes have increased dramatically, with over 245,000 malicious packages discovered in 2023 alone. Regulatory responses including U.S. Executive Order 14028 and the EU Cyber Resilience Act now mandate supply chain security controls.

These vulnerabilities are not new. Ken Thompson's 1984 "Reflections on Trusting Trust" articulated the fundamental challenge: we cannot verify everything we trust. What has changed is the scale and velocity at which attacks can be conducted and the depth of our dependency on code we did not create.
