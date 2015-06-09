#!/usr/bin/env python

from __future__ import print_function

import yaml
import shlex
import subprocess
import argparse
import re
import sys
import os

__author__ = "Jorge Niedbalski <jorge.niedbalski@canonical.com>"


def run(cmd):
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.PIPE)


def load_yaml(cmd):
    return yaml.load(run(cmd))


def get_environment():
    environment = os.environ.get("JUJU_ENV", None)
    if not environment:
        try:
            environment = run("juju env").strip()
        except:
            environment = None
    return environment


class Service:

    def __init__(self, name, environment,
                 skip_relations=["cluster", ]):
        self.name = name
        self.skip_relations = skip_relations
        self.status = environment.environment.get("services")[self.name]
        self.environment = environment

    def to_dict(self):
        r = {
            'num_units': self.units,
            'charm': self.charm,
        }

        if self.constraints:
            r.update({
                'constraints': self.constraints,
            })

        if len(self.options):
            r.update({
                'options': self.options,
            })

        if self.environment.options.include_placement and self.placement:
            r.update({
                'to': self.placement,
            })

        return r

    @property
    def constraints(self):
        try:
            return run("juju get-constraints %s" % self.name).strip("\n")
        except:
            return None

    @property
    def options(self):
        config = load_yaml("juju get %s" % self.name)
        options = {}
        inc_defaults = self.environment.options.include_defaults
        for k, v in config.get('settings').items():
            if 'value' in v and (not v.get('default', False) or inc_defaults):
                options[k] = v['value']
        return options

    @property
    def relations(self):
        if 'relations' in self.status:
            for name, items in self.status.get('relations').items():
                if name not in self.skip_relations:
                    for item in items:
                        if self.name != item:
                            yield sorted([self.name, item])

    @property
    def units(self):
        if 'units' in self.status:
            return len(self.status.get("units"))
        return 1

    @property
    def charm(self):
        def r(m):
            return m.groups()[0]

        format = self.environment.options.location_format

        if self.environment.options.include_charm_versions:
            charm = self.status.get('charm')
        else:
            charm = re.sub("(.*)(\-[0-9]+)", r,
                           self.status.get('charm'))

        if format == "cs" and charm.startswith("local"):
            return charm.replace("local", "cs")
        elif format == "local" and charm.startswith("cs"):
            return charm.replace("cs", "local")
        else:
            return charm

    @property
    def placement(self):
        units = self.status.get('units', None)
        if units:
            if len(units) > 1:
                return map(lambda x: x.get('machine'), units.values())
            else:
                return units[units.keys()[0]].get('machine')
        return None


class Environment:

    def __init__(self, options):
        self.options = options
        self.environment = load_yaml("juju status -e %s --format=yaml" %
                                     self.options.environment)

    @property
    def services(self):
        services = []
        for service in self.environment.get('services').keys():
            services.append(Service(service, self))
        return services

    def deployerize(self):
        output = {
            self.options.environment: {
                'services': {},
                'relations': [],
            }
        }
        relations = []

        for service in self.services:

            for relation in service.relations:
                if relation not in relations:
                    relations.append(relation)

            output[self.options.environment]['services'][
                service.name] = service.to_dict()

        output[self.options.environment]['relations'] = relations

        dump = yaml.dump(output, default_flow_style=False)
        if self.options.output:
            with open(self.options.output, 'w+') as f:
                f.write(dump)
        else:
            sys.stdout.write(dump)


def parse_options():
    parser = argparse.ArgumentParser(
        description='Convert your current juju environment status\
            into a YAML suitable for being used on juju-deployer')

    parser.add_argument("-e", "--environment",
                        help='Juju environment to convert',
                        type=str,
                        default="",
                        metavar='environment')

    parser.add_argument("-o", "--output",
                        help='File to save the yaml bundle (default: stdout)',
                        type=str,
                        default="",
                        metavar='output')

    parser.add_argument('--include-defaults',
                        action='store_true',
                        dest='include_defaults',
                        help=('Include configuration values even if they are'
                              ' the default ones'))

    parser.add_argument('--include-charm-versions',
                        action='store_true',
                        default=False,
                        dest='include_charm_versions',
                        help=('Include the exact deployed charm version'))

    parser.add_argument('--include-placement',
                        action='store_true',
                        dest='include_placement',
                        help=('Include service machine/container placement'))

    parser.add_argument('--charm-location-format',
                        metavar='format',
                        default="",
                        type=str,
                        dest='location_format',
                        help=('Replace charm location to format \
                        (options: local,cs)'))

    args = parser.parse_args()

    if args.environment == "":
        environment = get_environment()
        if not environment:
            parser.error("Not found juju env, please lease use --environment")
        else:
            args.environment = environment

    return args


def main():
    options = parse_options()
    d = Environment(options)
    d.deployerize()

if __name__ == "__main__":
    main()
