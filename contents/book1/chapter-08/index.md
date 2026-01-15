# Chapter 8: Insider Threats and Social Engineering

## Summary

Chapter 8 examines how attackers exploit human trust and access rather than technical vulnerabilities to compromise the software supply chain. The chapter explores six interconnected attack vectors that target the people who maintain and secure open source projects.

The chapter begins with compromised maintainer accounts, demonstrating how credential theft through phishing, credential stuffing, or malware can provide attackers direct publishing access to packages with millions of downloads. High-profile incidents like eslint-scope, rest-client, and ua-parser-js illustrate the devastating impact when authentication is bypassed.

Malicious commits and pull requests represent a subtler approach, where attackers submit harmful code disguised as legitimate contributions. Techniques range from simple obfuscation and Unicode tricks to the sophisticated multi-year campaign behind the XZ Utils backdoor. Code review, while valuable, has inherent limitations that determined attackers can exploit.

Social engineering targeting maintainers is examined in depth, with the XZ Utils attack serving as a masterclass in long-term manipulation. Attackers build fake personas, create pressure through sock puppet accounts, and exploit maintainer burnout and isolation to gain trusted positions within projects.

The chapter also covers insider threats from within projects, including both intentional sabotage (protestware incidents like colors.js and node-ipc) and compromised insiders. Governance structures and multi-maintainer requirements serve as key mitigating controls.

Git-specific attack vectors receive detailed treatment, including malicious hooks, submodule hijacking, case sensitivity exploits, and repository manipulation. Finally, the chapter addresses fake security researchers who submit malicious "fixes" under the guise of vulnerability remediation, weaponizing the urgency of security response.

Throughout, the chapter emphasizes that technical controls alone are insufficient. Defense requires combining awareness, verification procedures, community support, and sustainable funding to reduce the human vulnerabilities that attackers increasingly target.

## Sections

- 8.1 Compromised Maintainer Accounts
- 8.2 Malicious Commits and Pull Requests
- 8.3 Social Engineering Targeting Maintainers
- 8.4 Insider Threats in Open Source Projects
- 8.5 Git-Specific Attack Vectors
- 8.6 Fake Security Researchers and Malicious "Fixes"
