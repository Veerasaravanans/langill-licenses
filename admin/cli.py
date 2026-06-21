#!/usr/bin/env python3
"""langill-admin — Admin CLI for managing Langill license keys.

ADMIN ONLY: This file lives in your personal repo and the license repo.
It is NEVER distributed to users or included in compiled binaries.

Usage:
  export LANGILL_ADMIN_TOKEN="ghp_your_github_pat"
  python admin/cli.py generate-key --label "john-doe"
  python admin/cli.py list-keys
  python admin/cli.py revoke-key LGL-A7X9-K2M4-P8Q1
  python admin/cli.py unbind-key LGL-A7X9-K2M4-P8Q1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from langill.license.admin import create_key, list_keys, revoke_key, unbind_key


def cmd_generate_key(args: argparse.Namespace) -> None:
    key = create_key(label=args.label)
    print(f"Generated key: {key}")
    if args.label:
        print(f"  Label: {args.label}")
    print("  Status: active")
    print("  Device: unbound (will bind on first install)")


def cmd_list_keys(args: argparse.Namespace) -> None:
    keys = list_keys()
    if not keys:
        print("No keys found.")
        return

    print(f"{'Key':<22} {'Label':<15} {'Status':<10} {'Device':<20} {'Version':<10}")
    print("-" * 77)
    for entry in keys:
        device = entry.get("device", {})
        device_str = device.get("hostname", "unbound") if device else "unbound"
        print(
            f"{entry['key']:<22} "
            f"{entry['label']:<15} "
            f"{entry['status']:<10} "
            f"{device_str:<20} "
            f"{entry['version']:<10}"
        )


def cmd_revoke_key(args: argparse.Namespace) -> None:
    if revoke_key(args.key):
        print(f"Revoked: {args.key}")
    else:
        print(f"Key not found: {args.key}")
        sys.exit(1)


def cmd_unbind_key(args: argparse.Namespace) -> None:
    if unbind_key(args.key):
        print(f"Unbound: {args.key} (can be installed on a new device)")
    else:
        print(f"Key not found: {args.key}")
        sys.exit(1)


def cmd_device_info(args: argparse.Namespace) -> None:
    keys = list_keys()
    for entry in keys:
        if entry["key"] == args.key:
            device = entry.get("device", {})
            if not device:
                print(f"Key {args.key}: no device bound")
                return
            print(f"Key:       {args.key}")
            print(f"Label:     {entry['label']}")
            print(f"Status:    {entry['status']}")
            print(f"Machine:   {device.get('machine_id', 'N/A')}")
            print(f"Hostname:  {device.get('hostname', 'N/A')}")
            print(f"IP:        {device.get('ip', 'N/A')}")
            print(f"OS:        {device.get('os', 'N/A')}")
            print(f"First:     {device.get('first_seen', 'N/A')}")
            print(f"Last:      {device.get('last_seen', 'N/A')}")
            return
    print(f"Key not found: {args.key}")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="langill-admin",
        description="Manage Langill license keys",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate-key", help="Generate a new license key")
    gen.add_argument("--label", default="", help="User label for the key")
    gen.set_defaults(func=cmd_generate_key)

    ls = sub.add_parser("list-keys", help="List all license keys")
    ls.set_defaults(func=cmd_list_keys)

    rev = sub.add_parser("revoke-key", help="Revoke a license key")
    rev.add_argument("key", help="License key to revoke")
    rev.set_defaults(func=cmd_revoke_key)

    unb = sub.add_parser("unbind-key", help="Unbind a key from its device")
    unb.add_argument("key", help="License key to unbind")
    unb.set_defaults(func=cmd_unbind_key)

    dev = sub.add_parser("device-info", help="Show device details for a key")
    dev.add_argument("key", help="License key")
    dev.set_defaults(func=cmd_device_info)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
