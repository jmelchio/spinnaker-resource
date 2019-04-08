# spinnaker-resource
A resource that allows a Spinnaker stage to be a Concourse task input and trigger.

## Summary
The `spinnaker-resource` is a resource that allows a Spinnaker `Concourse` stage to trigger jobs in a Concourse pipeline.
It does this by querying a given Spinnaker instance for the presence of Concourse stages that satisfy given query 
parameters set in the configuration of the resource in the `check` script providing a new version for the resource.

This in turn will trigger the `in` script which will trigger the connected `job` and notify Spinnaker that execution has
started.

After this the Spinnaker stage will monitor Concourse for the completion of the job. *The `spinnaker-resource` must be
configured as a trigger on the job it serves as input to in order to work properly.* The `out` script is a no-op and 
should not be configured at this time.

## Parameters
* base_url - URI that points to your *GATE* endpoint on your Spinnaker installation. **Must** include the final `/` so
that is looks like `http://spin.gate:8084/`.
* user_name - User name for basic auth connection to Spinnaker.
* password - Password for basic auth connection to Spinnaker.
* app_name - Name of the Spinnaker application this applies to. This is used for querying Spinnaker for pipeline 
executions.
* master (*optional*) - Name of the Concourse connection defined in Spinnaker. If only one connection is defined in the
Spinnaker setup this can be omitted. Otherwise it will be used to query Spinnaker for pipeline executions.
* team_name - Team name of the Concourse team for the pipeline that Spinnaker connects to. This should match the name of 
the `team` in Concourse that owns the Concourse pipeline that is targeted from Spinnaker. Used to query Spinnaker for 
pipeline executions.
* pipeline_name - Name of the Concourse pipeline that Spinnaker connects to. This should match the name of the pipeline
in Concourse as used in the `fly` command when launching the pipeline. Used to query Spinnaker for pipeline executions.
* resource_name - Name of the resource set up to connect Concourse and Spinnaker. This should match the name of the 
`spinnaker-resource` in the Concourse `pipeline.yml` file. Used to query Spinnaker for pipeline executions.
* path - name of the file that is written for any input parameters the Spinnaker configuration may provide to the 
Concourse job in its context. This will end up in the mounted `input` volume on the task container.

## Sample configurations
Your `pipeline.yml` should look something like this:

```yaml
resource_types:
- name: spinnaker-resource
  type: docker-image
  source:
    repository: cfspinnaker/spinnaker-resource
    tag: latest

resources:
  - name: spin-resource-name
    type: spinnaker-resource
    source:
      base_url: http://spinnaker.gate:8084/
      user_name: some-name
      password: password
      app_name: demo456
      master: concourse-account-name
      team_name: concourse-team-name
      pipeline_name: name-of-concourse-pipeline
      resource_name: spin-resource-name
      path: configuration.properties

jobs:
  - name: some-build
    public: true
    plan:
      - get: spin-resource-name
        trigger: true
      - task: build
        file: source/concourse/build.yml
```

The `source/concourse/buld.yml` (for the task) should look like this:

```yaml
platform: linux

image_resource:
  type: docker-image
  source: {repository: java, tag: openjdk-8}

inputs:
  - name: spin-resource-name

run:
  path: source/concourse/build.sh
```
