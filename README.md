# CVE-2024-23897
Jenkins CVE-2024-23897: Arbitrary File Read Vulnerability Leading to RCE

Jenkins uses the args4j library to parse command arguments and options on the Jenkins controller when processing CLI commands. This command parser has a feature that replaces an @ character followed by a file path in an argument with the file’s contents (expandAtFiles). This feature is enabled by default and Jenkins 2.441 and earlier, LTS 2.426.2 and earlier does not disable it.

This allows attackers to read arbitrary files on the Jenkins controller file system using the default character encoding of the Jenkins controller process.

Attackers with Overall/Read permission can read entire files.

Attackers without Overall/Read permission can read the first few lines of files. The number of lines that can be read depends on available CLI commands. As of publication of this advisory, the Jenkins security team has found ways to read the first three lines of files in recent releases of Jenkins without having any plugins installed, and has not identified any plugins that would increase this line count.


more Info : 
https://www.jenkins.io/security/advisory/2024-01-24/

run : `python CVE-2024-23897.py -l host.txt -f /etc/passwd`

![image](https://github.com/h4x0r-dz/CVE-2024-23897/assets/26070859/9b547349-1783-42a9-9a02-588ab04f4d68)
