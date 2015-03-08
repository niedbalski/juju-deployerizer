Juju deployerizer
=================

This is a plugin for converting a currently running environment
into a YAML file suitable for being used with juju-deployer.

# How to use it

First install this from pip

```bash
$ sudo pip install juju-deployerizer
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
        backup_dir: /var/lib/mysql/backups
        backup_retention_count: 7
        backup_schedule: ''
        bind-address: 0.0.0.0
        binlog-format: MIXED
        block-size: 5
        ceph-osd-replication-count: 3
        dataset-size: 80%
        flavor: distro
        ha-bindiface: eth0
        ha-mcastport: 5411
        max-connections: -1
        nagios_context: juju
        prefer-ipv6: false
        preferred-storage-engine: InnoDB
        query-cache-size: 0
        query-cache-type: 'OFF'
        rbd-name: mysql1
        tuning-level: safest
        vip: ''
        vip_cidr: 24
        vip_iface: eth0
        wait-timeout: -1
    percona-cluster:
      charm: local:trusty/percona-cluster
      constraints: cpu-cores=9 mem=8192M
      num_units: 1
      options:
        dataset-size: 80%
        ha-bindiface: eth0
        ha-mcastport: 5490
        innodb-file-per-table: true
        lp1366997-workaround: false
        max-connections: -1
        prefer-ipv6: false
        table-open-cache: 2048
        vip_cidr: 24
        vip_iface: eth0
        wait-timeout: -1
    rsyslog:
      charm: cs:trusty/rsyslog
      num_units: 1
      options:
        messages_rotate: 4
        nova_logs: false
        protocol: udp
        syslog_rotate: 7
    rsyslog-forwarder-ha:
      charm: cs:trusty/rsyslog-forwarder-ha
      num_units: 1
      options:
        log-locally: false
        protocol: udp
        replication-mode: fanout
```




# Notes

By default juju-deployer branches and uses the charms locally,
so you can notice this charms with the prefix local:series/charm.

Probably in the near future, we will add an option
for doing a local branch to a directory.
