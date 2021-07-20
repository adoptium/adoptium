---
name: Release Checklist
about: Issue template for release champion and team to track release progress
title: Checklist for Temurin Release <x>
labels: ''
assignees: ''

---

This Temurin release checklist based on the [release doc](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md) captures what activities must happen during a release.  

The target release date is: _________

The release champion for this release is: _________

The role of the release champion is to ensure that all release activities listed in this checklist get completed (by delegation to the broader team or by the release champion themselves).  The final task of the release champion during a release is to confirm that all items in the checklist were completed satisfactorily and the release can be declared complete. 

Everyone participating in a release, including the release champion are requested to provide feedback into the release retrospective so that the release process can be continuously improved (through simplification and/or automation).

-------

One Week Prior to Release:
- [ ] **Release Champion named** whose responsibility is to ensure every item in this checklist gets completed
- [ ] **Declare code freeze** to ensure stability of build systems and infrastructure during release process
- [ ] **Disable nightly testing** to free up resources and ensure no competing jobs during release week
- [ ] **Update list of CA certificates** if required, following this [security/README](https://github.com/adoptium/temurin-build/blob/master/security/README.md)
- [ ] **Run a trial release pipeline** to ensure less surprises on release day (typically against a milestone build)

-------

Release Week Checklist:
- [ ] **Add website banner** (_automate_* via github workflow in website repository) - Announce that we target releases to be available within 48-72 hours of the GA tags being available
- [ ] **Launch build pipelines** for each version being released [(as per release doc](https://github.com/adoptium/temurin-build/blob/master/RELEASING.md#steps-for-every-version)) once release tags are available via [launch page](https://ci.adoptopenjdk.net/job/build-scripts/job/openjdk8-pipeline/build) in Jenkins.  Provide links in this issue to each version's pipeline build(s). There may be multiple pipelines per version if primary and secondary platforms are separated to expedite the release.  In some cases,  where there are unforeseen configuration or infrastructure issues, reruns may be needed.
  - jdk8 pipeline(s):
    - primary jdk8 pipeline:
      - rerun(s):
    - secondary jdk8 pipeline: 
      - reruns(s):
  - jdk11 pipeline(s): 
    - primary jdk11 pipeline:
      - rerun(s):
    - secondary jdk11 pipeline:
      - rerun(s):
  - jdkxx pipeline(s): 
    - primary jdkxx pipeline:
      - rerun(s):
    - secondary jdkxx pipeline:
      - rerun(s):
- [ ] **Summarize test results**.  Find each launched build pipeline in [TRSS](https://trss.adoptium.net/) to view a summary of test results.  Can use the Release Summary Report feature in TRSS to generate a summary of failures, history and possible issues in markup format to be added to this issue as a comment. 
- [ ] **Triage** each build and test failure in the release summary report (following the [Triage guidelines](https://github.com/adoptium/aqa-tests/blob/master/doc/Triage.md)) and determine blocking or non-blocking.  Supply links to triage issues or docs for each version here.
  - jdk8 triage summary:
  - jdk11 triage summary:
  - jdkxx triage summary:
- [ ] **Fix** blocking failures if they exist and confirm others are non-blocking.
- [ ] **Get PMC 'ready to publish' approval**, once no blocking failures exist.
- [ ] **Publish the release** (run the restricted access [release tool job](https://ci.adoptopenjdk.net/job/build-scripts/job/release/job/refactor_openjdk_release_tool/) on Jenkins)
- [ ] **Verify binaries published successfully** to github releases repo and website (_automate_*, this could also be an automated test)
- [ ] **Update support page** (_automate_* github workflow to create a PR to update [support.handlebars](https://github.com/adoptium/adoptium.net/blob/master/src/handlebars/support.handlebars))
- [ ] **Update release notes** (_automate_* - github workflow to create update for [release notes page](https://adoptium.net/release_notes.html))
- [ ] **Trigger linux installers pipeline** currently it is part of the build pipelines (will eventually be updated to run independently)
- [ ] **Publicize the release** via Slack #release channel and Twitter (can be partially automated)
- [ ] **Trigger docker images pipeline** via the [GitHub Actions job](https://github.com/AdoptOpenJDK/openjdk-docker/actions/workflows/updater.yml). Click Run Workflow, keep the branch as Master and click `Run Workflow`. This updater job checks the API and updates the relevant dockerfiles. A Pull Request is then created by the adoptopenjdk-bot account which will need merging once all the CI tests pass.  *TBD - how this step evolves for Temurin releases.
- [ ] **Declare code freeze end** opening up the code for further development
- [ ] **Remove website banner** (_automate_* via github workflow in website repository)
- [ ] **Declare the release complete** and close this issue

To reinstate Later

- [ ] **Update Official Docker Images** Once the dockerfiles have been updated in the previous step you can run the `dockerhub_doc_config_update.sh` script. This will create a file called adoptopenjdk which will need to be copy and pasted into the [official adoptopenjdk config](https://github.com/docker-library/official-images/blob/master/library/adoptopenjdk) (example PR https://github.com/docker-library/official-images/pull/10083) *TBD - how this step evolves for Temurin releases.
