Juju deployerizer
=================

This is a plugin for converting a currently running environment
into a YAML file suitable for being used with juju-deployer.

# How to use it

First install this from pip

```bash
$ sudo pip install juju-deployerizer
```

Available options

```bash
Convert your current juju environment status into a YAML suitable for being
used on juju-deployer

optional arguments:
  -h, --help            show this help message and exit
  -e environment, --environment environment
                        Juju environment to convert
  -o output, --output output
                        File to store the deployer yaml
  --include-defaults    Include configuration values even if they are the
                        default ones
  --include-placement   Include service machine/container placement
  --charm-location-format format
                        Replace charm location to format (options: local,cs)
```

Then, execute the plugin , by running

```bash
$ juju deployerizer --environment local --output local-filename.yaml
```

# Test it with juju deployer

```bash
$ juju-deployer --config local-filename.yaml
```

# Example

The following is the juju status output for a local environment

```yaml

environment: local
machines:
  "0":
    agent-state: started
    agent-version: 1.21.3.1
    dns-name: localhost
    instance-id: localhost
    series: vivid
    state-server-member-status: has-vote
  "1":
    agent-state: started
    agent-version: 1.21.3.1
    dns-name: 10.0.3.249
    instance-id: niedbalski-local-machine-1
    series: trusty
    hardware: arch=amd64
  "2":
    agent-state: started
    agent-version: 1.21.3.1
    dns-name: 10.0.3.116
    instance-id: niedbalski-local-machine-2
    series: trusty
    hardware: arch=amd64
  "3":
    agent-state: started
    agent-version: 1.21.3.1
    dns-name: 10.0.3.238
    instance-id: niedbalski-local-machine-3
    series: precise
    hardware: arch=amd64
  "4":
    agent-state: started
    agent-version: 1.21.3.1
    dns-name: 10.0.3.160
    instance-id: niedbalski-local-machine-4
    series: trusty
    hardware: arch=amd64
services:
  mysql:
    charm: local:trusty/mysql-326
    exposed: false
    relations:
      cluster:
      - mysql
      juju-info:
      - rsyslog-forwarder-ha
    units:
      mysql/0:
        agent-version: 1.21.3.1
        machine: "2"
        public-address: 10.0.3.116
  percona-cluster:
    charm: local:trusty/percona-cluster-45
    exposed: false
    relations:
      cluster:
      - percona-cluster
      juju-info:
      - rsyslog-forwarder-ha
    units:
      percona-cluster/0:
        agent-state: started
        agent-version: 1.21.3.1
        machine: "1"
        public-address: 10.0.3.249
        subordinates:
          rsyslog-forwarder-ha/0:
            upgrading-from: cs:trusty/rsyslog-forwarder-ha-4
            agent-state: started
            agent-version: 1.21.3.1
            public-address: 10.0.3.249
  rsyslog:
    charm: cs:trusty/rsyslog-7
    exposed: false
    units:
      rsyslog/0:
        agent-state: started
        agent-version: 1.21.3.1
        machine: "4"
        open-ports:
        - 514/tcp
        - 514/udp
        public-address: 10.0.3.160
  rsyslog-forwarder-ha:
    charm: cs:trusty/rsyslog-forwarder-ha-4
    exposed: false
    relations:
      juju-info:
      - mysql
      - percona-cluster
    subordinate-to:
    - mysql
    - percona-cluster
```

After running

```bash
$ juju deployerizer --environment local --output local.yaml
```

The resulting YAML looks like:

```YAML
local:
  relations:
  - - mysql
    - rsyslog-forwarder-ha
  - - percona-cluster
    - rsyslog-forwarder-ha
  services:
    mysql:
      charm: local:trusty/mysql
      num_units: 1
      options:
        wait-timeout: -1
    percona-cluster:
      charm: local:trusty/percona-cluster
      constraints: cpu-cores=9 mem=8192M
      num_units: 1
    rsyslog:
      charm: cs:trusty/rsyslog
      num_units: 1
    rsyslog-forwarder-ha:
      charm: cs:trusty/rsyslog-forwarder-ha
      num_units: 1
```

# Notes

By default juju-deployer makes a local bzr branch and uses the charms locally,
so you can notice this charms with the prefix local:series/charm.

Probably in the near future, we will add an option
for doing a local branch to a directory.
