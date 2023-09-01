---
name: Release Checklist
about: Issue template for release champion and team to track release progress
title: Checklist for Temurin Release <x>
labels: ''
assignees: ''

---

**NOTE: Items marked `jdkxx` and `TEMPLATE_UPDATEME` should be replaced while deploying this issue template. It is recommended to delete this line once you've done so :-)**

This Temurin release checklist based on the [release doc](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md) captures what activities must happen during a release.

The target release date is: _________

The release champion for this release is: _________

Planned absences during the release cycle:

The role of the release champion is to ensure that all release activities listed in this checklist get completed (by delegation to the broader team or by the release champion themselves).  The final task of the release champion during a release is to confirm that all items in the checklist were completed satisfactorily and the release can be declared complete.

Everyone participating in a release, including the release champion are requested to provide feedback into the release retrospective so that the release process can be continuously improved (through simplification and/or automation).

-------

### Two Weeks Prior To Release

- [ ] **Release Champion named** whose responsibility is to ensure every item in this checklist gets completed
- [ ] **Release Checklist Created**  Create this issue to track the release and the preparation tasks.
- [ ] **Identify Expected Release Versions** - Find out the version numbers from [here](https://www.java.com/releases/)

- [ ] **Notify release branching of build repositories** : [Slack message, branching build repositories](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md#branching-message-for-build-related-repositories)
- [ ] **Create build repositories release Branches** : [Create build repository release branches](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md#create-release-branch-on-below-repositories)

- [ ] **Identify the aqa branch name for the upcoming release**

Ensure ALL nodes online prior to running these following TC steps:
 - [ ] TC: Run the DeleteJCKMultiNode process cleaning job on all ci.role.test nodes, to remove any now redundent jck-versions, to ensure healthy state, verify all nodes successful: https://ci.eclipse.org/temurin-compliance/job/DeleteJCKMultiNode
 - [ ] TC: Run the ProcessCheckMultiNode process cleaning job on all ci.role.test nodes, to ensure healthy state, verify all nodes successful: https://ci.eclipse.org/temurin-compliance/job/ProcessCheckMultiNode/build?delay=0sec
 - [ ] TC: Run the Setup_JCK_Run_Multinode job with CLEAN_DIR=true (to purge any old release contents/results) on all ci.role.test nodes, this will extract the jck_run folder with all the temurin.jtx exclude files, verify all nodes successful : https://ci.eclipse.org/temurin-compliance/job/Setup_JCK_Run_Multinode/build?delay=0sec

 - [ ] **Check the nagios server to ensure there are no critical infrastructure issues**
	 Log in to the public [nagios](https://nagios.adoptopenjdk.net/nagios/) server, and check the Problems / Services page. If you do not have access, please request it via an issue in the infrastructure repository. If there are any issues, then please log an issue in the infrastructure repository.
 - [ ] **Regenerate The Release Build Pipeline Jobs In Jenkins**
 - [ ] **Prepare & Perform Dry Run Of Build & Tests** : [Dry-run](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md#auto-way---before-release-week-dry-run-release-test) 
 - [ ] **Triage dry-run TCK job results**
 - [ ] **Perform TCK Auto-manuals on x64Linux for each dry-run version**

### One Week Prior To Release
- [ ] **Final Code Freeze Warning** post a message to the build & release slack channels : [Slack message](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md#code-freeze-message)

After 1 day, then :-

- [ ] **Declare code freeze** to ensure stability of build systems and infrastructure during release process : #build and #release slack message: "Code Freeze is now being enabled"

- [ ] **Enable code freeze bot** : [Enabling code freeze](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md#enable-code-freeze-on--main-branches-of-below-repositories)

- [ ] **Disable standard builds temporarily; both nightlies and weeklies**
  - This frees up resources and ensures no competing jobs during release week. 
  - This should be done by running [build-pipeline-generator](https://ci.adoptium.net/job/build-scripts/job/utils/job/build-pipeline-generator/) with the default for ENABLE_PIPELINE_SCHEDULE set to false.
- [ ] **Disable evaluation builds temporarily; both nightlies and weeklies** 
  - This frees up resources and ensures no competing jobs during release week. 
  - This should be done by running [evaluation-pipeline-generator](https://ci.adoptium.net/job/build-scripts/job/utils/job/evaluation-pipeline-generator/) with the default for ENABLE_PIPELINE_SCHEDULE set to false.

- [ ] **Prepare For Release**
  - [ ] Ensure that there is an [aqa-tests branch](https://github.com/adoptium/aqa-tests/branches) that matches the name of the [latest aqa-tests release version](https://github.com/adoptium/aqa-tests/releases/latest).
  - [ ] Update [releaseVersions](https://github.com/adoptium/ci-jenkins-pipelines/blob/187d92c3030354557b2fc105cbff3e5ec631674c/pipelines/build/regeneration/release_pipeline_generator.groovy#L10C35-L10C35) with release versions.
  - [ ] Update [releasePlan.cfg](https://github.com/adoptium/mirror-scripts/blob/master/releasePlan.cfg) with expected tags, for more detail see [here](https://github.com/zdtsw/mirror-scripts/tree/issue/3167#skara-repos-and-processes).
  - [ ] Generate release pipeline jobs with [release-pipeline-generator](https://ci.adoptopenjdk.net/job/build-scripts/job/utils/job/release-pipeline-generator).
    - DO NOT use default job parameter values. aqaReference should be the [latest aqa-tests release version](https://github.com/adoptium/aqa-tests/releases/latest).

**Wait For All Of The Above To Complete Successfully Before Proceeding!**

- [ ] Log a helpdesk ticket with EF , to get all test materials updated
- [ ] TC: Run the ProcessCheckMultiNode process cleaning job on all ci.role.test nodes, to ensure healthy state, verify all nodes successful: https://ci.eclipse.org/temurin-compliance/job/ProcessCheckMultiNode/build?delay=0sec
- [ ] TC: Run the Setup_JCK_Run_Multinode job with CLEAN_DIR=true (to purge any old release contents/results) on all ci.role.test nodes, this will extract the jck_run folder with all the temurin.jtx exclude files, verify all nodes successful : https://ci.eclipse.org/temurin-compliance/job/Setup_JCK_Run_Multinode/build?delay=0sec
- [ ] Check the nagios server to ensure there are no critical infrastructure issues
- [ ] **Trigger a trial release pipeline dry-run** to ensure less surprises on release day (typically against a milestone build), see here for [details](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md#auto-way---before-release-week-auto-test)

- [ ] Confirm successful trial release pipelines and successful jck completion
- [ ] Calculate the "expected" openjdk build tags for the releases being published, and update all the JDKnn_BRANCH values in the testenv.properties file for the aqa-tests release branch, eg: https://github.com/adoptium/aqa-tests/blob/v0.9.6-release/testenv/testenv.properties

-------

Release Week Checklist:

- [ ] **Add website banner** (this is done by making a PR then it gets automate published to website) - Announce that we target releases to be available within 48-72 hours of the GA tags being available
- [ ]   -- Check All Nodes Online https://ci.eclipse.org/temurin-compliance/label/ci.role.test/
- [ ]  Run https://ci.eclipse.org/temurin-compliance/job/ProcessCheckMultiNode/ -- with defaults
- [ ] Run Setup_JCK_Multinode with CLEAN_DIR=true for ( ci.role.test )
- [ ] Disable Setup_JCK_Multinode To Ensure Test Evidence Is Not Lost
- [ ] As detailed earlier, again check the nagios server to ensure there are no critical infrastructure issues
- [ ] Create the Github Issues for tracking progress against each Java version
- [ ] Create the Github issues for the Adoptium public retro & TC retro
- [ ] Update the links on the slack channel for the release status and retrospective issues.

#### Release Day Onwards

- [ ] **Check Tags have been released upstream** - Look for mailing list announcements and `-ga` tags in version control.
- [ ] Check the published GA tags are the "expected" tags entered in the aqa-tests release branch testenv.properties. If they are not then update.
- [ ] **Check Tags have been Mirrored** [Mirrors](https://ci.adoptopenjdk.net/view/git-mirrors/job/git-mirrors/job/adoptium/).
- [ ] **Check "auto-trigger" pipelines or Launch build pipelines** for each version being released. Verify if the release pipline "auto-triggered", if not (maybe expected tag was wrong), then manually launch [(as per release doc](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md#steps-for-every-version)) once release tags are available via [launch page](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/build) in Jenkins.  Provide links in this issue to each version's pipeline build(s). There may be multiple pipelines per version if primary and secondary platforms are separated to expedite the release.  In some cases,  where there are unforeseen configuration or infrastructure issues, reruns may be needed.
  - jdk8 pipeline(s):
    - **primary jdk8 pipeline:**
      - rerun(s):
    - **secondary jdk8 pipeline:**
      - reruns(s):
  - jdk11 pipeline(s):
    - **primary jdk11 pipeline:**
      - rerun(s):
    - **secondary jdk11 pipeline:**
      - rerun(s):
  - jdkxx pipeline(s):
    - **primary jdkxx pipeline:**
      - rerun(s):
    - **secondary jdkxx pipeline:**
      - rerun(s):
- [ ] **Check Upstream Tags, Mirror Tags & Trigger Builds For JDK8 AARCH32** This specific version is built from a separate mirror repository and has a separate build process, this is CURRENTLY not part of the automation which is handled for the other platforms and version. Also note that there is a seperate properties file (testenv_arm32.properties) which needs to be updated.
- [ ] **Add links to the [status doc](https://github.com/adoptium/adoptium/issues/TEMPLATE_UPDATEME)** to indicate per-platform builds ready
- [ ] **Summarize test results**.  Find each launched build pipeline in [TRSS](https://trss.adoptium.net/) to view a summary of test results.  Can use the Release Summary Report feature in TRSS to generate a summary of failures, history and possible issues in markup format to be added to this issue as a comment.
- [ ] **Triage** each build and test failure in the release summary report (following the [Triage guidelines](https://github.com/adoptium/aqa-tests/blob/master/doc/Triage.md)) and determine blocking or non-blocking.  Supply links to triage issues or docs for each version here.
  - jdk8 triage summary:
  - jdk11 triage summary:
  - jdk17 triage summary:
  - jdkXX triage summary:
- [ ] **Fix** blocking failures if they exist and confirm others are non-blocking.
- [ ] **Confirm Temurin-compliance items completed**, per platform/version/binaryType
- [ ] **Get PMC 'ready to publish' approval**, once no blocking failures exist.
- [ ] **Generate The Release Notes Per JDK Version **, ( Use https://ci.adoptium.net/job/build-scripts/job/release/job/create_release_notes/ )
- [ ] **Publish the release** (run the restricted access [release tool job](https://ci.adoptopenjdk.net/job/build-scripts/job/release/job/refactor_openjdk_release_tool/) on Jenkins) ( also publish release notes )
- [ ] **Verify binaries published successfully** to github releases repo and website (_automate_*, this could also be an automated test)

- [ ] **Publish updates to the containers to dockerhub**
- [ ] **Edit the [Homebrew Temurin Cask](https://github.com/Homebrew/homebrew-cask/blob/master/Casks/temurin.rb)** and replace the version and sha256 as appropriate.  This means for Homebrew users that they install the latest by default and can use the `@` notation to install older versions if they wish.
- [ ] **Update support page** (_automate_* github workflow to create a PR to update [support webpage](https://github.com/adoptium/adoptium.net/blob/main/content/asciidoc-pages/supported-platforms/index.adoc))
- [ ] **Update release notes** (_automate_* - github workflow to create update for release notes pages - [example](https://adoptium.net/temurin/release-notes/?version=jdk8u382-b05))
- [ ] **Trigger linux installers pipeline** currently it is part of the build pipelines (will eventually be updated to run independently)
- [ ] **Publicize the release** via Slack #release channel and Twitter (can be partially automated)
- [ ] **Declare code freeze end** opening up the code for further development
- [ ] **Disable code freeze bot** In order to enable the code freeze GitHub you need to change the line `if: github.repository_owner == 'adoptium' && true` to be `if: github.repository_owner == 'adoptium' && false` in the [code-freeze.yml](https://github.com/adoptium/.github/blob/main/.github/workflows/code-freeze.yml#L21) GitHub workflow. Please contact the PMC if you need help merging this change.
- [ ] **Remove website banner** (_automate_* via github workflow in website repository)
- [ ] **Check for presence of jdk8u aarch32 GA tag and mirror it** [Mercurial repo](https://hg.openjdk.java.net/aarch32-port/jdk8u) - [Mirror job](https://ci.adoptopenjdk.net/view/git-mirrors/job/git-mirrors/job/adoptium/job/git-hg-aarch32-jdk8u/)
- [ ] **Do all of the above for the jdk8u/aarch32 build: Ensure to specify overridePublishName param**
- [ ] **Archive/upload all TCK results**
- [ ] **Declare the release complete** and close this issue
- [ ] **Re-enable testing: Once the release is deployed, don't forget to re-enable any testing that was disabled during the release process to ensure that the system is working as expected. This includes unit tests, integration tests, end-to-end tests, and any other testing that was temporarily paused. Be sure to validate that all tests are running successfully before considering the release complete.**
