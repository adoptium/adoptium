---
name: Release Status
about: Issue template for the status document that we direct our customers to during a release cycle
title: <month> <year> Release Status per Platform, Version & Binary Type
labels: ''
assignees: ''

---

Sharing information in this issue since the TCK work is being tracked in temurin-compliance private repo not visible to the community (as per the OCTLA).  Risks and expectations for timing on the release are listed in this [issue comment](https://github.com/adoptium/adoptium/issues/3#issuecomment-866903922).  Primary platforms (x64 Linux/Windows/OSX) in **bold** are prioritized, secondary platforms not in bold follow in no particular order (as machine resources are available).

👍 results in these Tables means the activity has successfully completed.
⏳ results means that we are actively working on closing off the runs needed for this version, platform, binaryType.
⛔ means there is no build planned for that version/platform combination.
📂 means activity not yet started.

### JDK8u322
| Platform | jdk8 AQA  | jdk8 TCK | jdk8 installers | jdk8 containers | Notes |
| -----  | ----- | ----- | ----- | ----- | ----- |
| [**x64 Linux**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/linux/x64/hotspot) | 📂 | 📂 | 📂 | 📂 |   |
| [**x64 Windows**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/windows/x64/hotspot) | 📂 | 📂 | 📂 | 📂 |   |
| [**x64 Mac**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/mac/x64/hotspot) | 📂 | 📂 | 📂 | ⛔ |   |
| [aarch64 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/linux/aarch64/hotspot) | 📂  | 📂 | 📂 | 📂 |   |
| [ppcle64 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/linux/ppc64le/hotspot) | 📂 | 📂 | 📂 | 📂 |   |
| [ppc64 AIX](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/aix/ppc64/hotspot) | 📂 | 📂 | ⛔ | ⛔ |   |
| [x32 Windows](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/windows/x86-32/hotspot) | 📂 | 📂 | 📂 | ⛔ |   |
| [arm32 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/yyyy/artifact/target/linux/arm/hotspot) | 📂 | 📂 | 📂 | 📂 |   |
| [sparcv9 solaris](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/solaris/sparcv9/hotspot) | 📂 | 📂 | ⛔  | ⛔ |   |
| [x86 solaris](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/xxxx/artifact/target/solaris/x64/hotspot) |  📂   | 📂   | ⛔  | ⛔ |  |

### JDK11.0.14
| Platform  | jdk11 AQA  | jdk11 TCK | jdk11 installers | jdk11 containers | Notes |
| ----- | ----- | ----- | ----- | ----- | ----- |
| [**x64 Linux**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/linux/x64/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [**x64 Windows**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/windows/x64/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [**x64 Mac**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/mac/x64/hotspot/) | 📂 | 📂 | 📂 | ⛔ |   |
| [aarch64 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/linux/aarch64/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [ppcle64 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/linux/ppc64le/hotspot/) |  📂 | 📂 | 📂 | 📂 |   |
| [s390x Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/linux/s390x/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [ppc64 AIX](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/aix/ppc64/hotspot/) | 📂 | 📂 | ⛔ |⛔ |   |
| [x32 Windows](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/windows/x86-32/hotspot/) | 📂 | 📂 | 📂 | ⛔ |   |
| [arm32 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/linux/arm/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [x64 alpine-Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk11-pipeline/xxxx/artifact/target/alpine-linux/x64/hotspot/) | 📂 | 📂 | 📂 | 📂 |  This will be a headless build |
| [aarch64 Mac](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxxx/artifact/target/mac/aarch64/hotspot/) | 📂 | 📂 | 📂 | ⛔ |   |

### JDK17.0.2
| Platforms  | jdk17 AQA  | jdk17 TCK | jdk17 installers | jdk17 containers | Notes |
| ----- | ----- | ----- | ----- | ----- | ----- |
| [**x64 Linux**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/linux/x64/hotspot/)| 📂 | 📂 | 📂 | 📂 |   |
| [**x64 Windows**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/windows/x64/hotspot/) | 📂 | 📂 | 📂  | 📂  |   |
| [**x64 Mac**](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/mac/x64/hotspot/) | 📂 | 📂 | 📂  | ⛔ |   |
| [aarch64 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/linux/aarch64/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [ppcle64 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/linux/ppc64le/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [s390x Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/linux/s390x/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [ppc64 AIX](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/aix/ppc64/hotspot/)| 📂 | 📂 | ⛔ |⛔  |   |
| [x32 Windows](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/windows/x86-32/hotspot/) | 📂 | 📂 | 📂 | ⛔ |   |
| [arm32 Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/linux/arm/hotspot/) | 📂 | 📂 | 📂 | 📂 |   |
| [x64 alpine-Linux](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/alpine-linux/x64/hotspot/) | 📂 | 📂 | 📂 | 📂 | This will be a headless build |
| [aarch64 Mac](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk17-pipeline/xxx/artifact/target/mac/aarch64/hotspot/) | 📂 | 📂 | 📂 | ⛔ |   |
