---
name: Release Status
about: Issue template for the status document that we direct our customers to during a release cycle
title: <month> <year> Release Status per Platform, Version & Binary Type
labels: ''
assignees: ''

---

Sharing information in this issue since the TCK work is being tracked in temurin-compliance private repo not visible to the community (as per the OCTLA).  Risks and expectations for timing on the release are listed in this [issue comment](https://github.com/adoptium/adoptium/issues/3#issuecomment-866903922).  Primary platforms (x64 Linux/Windows/OSX) in **bold** are prioritized, secondary platforms not in bold follow in no particular order (as machine resources are available).

✔️ results in these Tables means the activity has successfully completed.

⏳ results means that we are actively working on closing off the runs needed for this version, platform, binaryType.

⛔ means there is no build planned for that version/platform combination.

⏸️ means activity not yet started.

### JDK8uXXX-bXX
| Platform  | jdk8 AQA  | jdk8 TCK  | jdk8 published | jdk8 installers  | jdk8 images   | Notes |
| -----     | -----     | -----     | -----          | -----            | -----         | ----- |
| **x64 Linux** | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| **x64 Windows** | ⏸️   | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| **x64 Mac** | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⛔            |       |
| aarch64 Linux | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| ppcle64 Linux | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| ppc64 AIX | ⏸️         | ⏸️         | ⏸️              | ⛔               | ⛔            |       |
| x32 Windows | ⏸️       | ⏸️         | ⏸️              | ⛔               | ⏸️             |       |
| arm32 Linux | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| x64 alpine-Linux | ⏸️  | ⏸️         | ⏸️              | ⏸️                | ⏸️             | This will be a headless build |
| sparcv9 solaris | ⏸️   | ⏸️         | ⏸️              | ⛔               | ⛔            |       |
| x86 solaris | ⏸️       | ⏸️         | ⏸️              | ⛔               | ⛔            |       |

### JDK11.0.XX+Y
| Platform | jdk11 AQA | jdk11 TCK  | jdk11 published| jdk11 installers | jdk11 images  | Notes |
| -----    | -----     | -----      | -----          | -----            | -----         | ----- |
| **x64 Linux** | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| **x64 Windows** | ⏸️   | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| **x64 Mac** | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⛔            |       |
| aarch64 Linux | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| ppcle64 Linux | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| s390x Linux   | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| ppc64 AIX | ⏸️         | ⏸️         | ⏸️              | ⛔               | ⛔            |       |
| x32 Windows | ⏸️       | ⏸️         | ⏸️              | ⏸                | ⛔            |       |
| arm32 Linux | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| x64 alpine-Linux | ⏸️  | ⏸️         | ⏸️              | ⏸️                | ⏸️             | This will be a headless build |
| aarch64 Mac | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⛔            |       |

### JDK17.0.XX+Y
| Platforms | jdk17 AQA | jdk17 TCK | jdk17 published| jdk17 installers | jdk17 images | Notes |
| -----     | -----     | -----     | -----          | -----            | -----        | ----- |
| **x64 Linux** | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️            |       |
| **x64 Windows** | ⏸️   | ⏸️         | ⏸️              | ⏸️                | ⏸️            |       |
| **x64 Mac** | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⛔           |       |
| aarch64 Linux | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️            |       |
| ppcle64 Linux | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️            |       |
| s390x Linux   | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️            |       |
| ppc64 AIX | ⏸️         | ⏸️         | ⏸️              | ⛔               | ⛔           |       |
| x32 Windows | ⏸️       | ⏸️         | ⏸️              | ⏸                | ⛔           |       |
| arm32 Linux | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⏸️            |       |
| x64 alpine-Linux | ⏸️  | ⏸️         | ⏸️              | ⏸️                | ⏸️            | This will be a headless build |
| aarch64 Mac | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⛔           |       |

### JDK20.0.XX+Y
| Platform  | jdk20 AQA | jdk20 TCK | jdk20 published| jdk20 installers | jdk20 images  | Notes |
| -----     | -----     | -----     | -----          | -----            | -----         | ----- |
| **x64 Linux** | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| **x64 Windows** | ⏸️   | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| **x64 Mac** | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⛔            |       |
| aarch64 Linux | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| ppcle64 Linux | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| s390x Linux   | ⏸️     | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| ppc64 AIX | ⏸️         | ⏸️         | ⏸️              | ⛔               | ⛔            |       |
| x32 Windows | ⏸️       | ⏸️         | ⏸️              | ⏸                | ⛔            |       |
| arm32 Linux | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⏸️             |       |
| x64 alpine-Linux | ⏸️  | ⏸️         | ⏸️              | ⏸️                | ⏸️             | This will be a headless build |
| aarch64 Mac | ⏸️       | ⏸️         | ⏸️              | ⏸️                | ⛔            |       |
