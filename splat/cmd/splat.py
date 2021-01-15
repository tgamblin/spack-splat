# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

from spack.spec import Spec
import spack.repo

description = "print values of various parts of packages"
section = 'developer'
level = 'long'

actions = {}


def action(func):
    actions[func.__name__] = func


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='splat_command')
    for action, func in actions.items():
        sp.add_parser(action, help=func.__doc__)


@action
def dependency_conditions(args):
    for pkg in spack.repo.path.all_package_classes():
        for name, conditions in pkg.dependencies.items():
            for cond, dep in conditions.items():
                print(cond)


@action
def dependency_conditions_no_version_no_variant(args):
    for pkg in spack.repo.path.all_package_classes():
        for name, conditions in pkg.dependencies.items():
            for cond, dep in conditions.items():
                spec = cond.copy()
                spec.versions = Spec().versions
                spec.variants = Spec().variants
                print(spec)


@action
def dependency_constraints(args):
    for pkg in spack.repo.path.all_package_classes():
        for name, conditions in pkg.dependencies.items():
            for cond, dep in conditions.items():
                constraint = dep.spec.copy()
                constraint.name = None
                print(constraint)


@action
def deptypes(args):
    for pkg in spack.repo.path.all_package_classes():
        for name, conditions in pkg.dependencies.items():
            for cond, dep in conditions.items():
                print(','.join(sorted(dep.type)))


@action
def variant_names(args):
    for pkg in spack.repo.path.all_package_classes():
        for name in pkg.variants:
            print(name)


@action
def variant_defaults(args):
    for pkg in spack.repo.path.all_package_classes():
        for name, variant in pkg.variants.items():
            print(variant.default)


@action
def variant_values(args):
    for pkg in spack.repo.path.all_package_classes():
        for name, variant in pkg.variants.items():
            print(variant.values)


@action
def variant_names_values(args):
    for pkg in spack.repo.path.all_package_classes():
        for name, variant in pkg.variants.items():
            print("%30s:" % (pkg.name + '.' + name), variant.values)


def splat(parser, args):
    actions[args.splat_command](args)
