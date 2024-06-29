#!/usr/bin/env python2

import codecs
import click
import subprocess
import json
import logging
import shutil

from bson import BSON
from bson.json_util import dumps, loads
from pathlib import Path
from rich.console import Console

CATALOG_TABLE_NAME = "_mdb_catalog"
JSON_SUFFIX = ".json"
WT_SUFFIX = ".wt"

logger = logging.getLogger(__name__)


def add_suffix(path, suffix):
    if path.suffix == suffix:
        return path
    return path.with_suffix(path.suffix + suffix)


def stream_wt_table(table_name):
    wt = shutil.which("wt")

    if wt is None:
        raise Exception(
            "Could not find 'wt' executable. "
            "Please make sure the executable is installed "
            "and PATH environment variable is correctly set."
        )

    file_name = add_suffix(Path(table_name), WT_SUFFIX)
    if not file_name.exists():
        raise FileNotFoundError(f"WiredTiger table '{file_name}' not found")

    proc = subprocess.Popen(
        [wt, "-R", "dump", "-x", table_name],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    return proc


def load_wt_table(tableName):
    proc = stream_wt_table(tableName)
    stream = proc.stdout
    arr = []

    # Skip all line until data section
    while True:
        line = stream.readline()
        if not line:
            raise Exception(f"Couldn't find data header in '{tableName}' wt table")
        line = line.strip()
        if line == b"Data":
            break

    while True:
        key_raw = stream.readline()
        if not key_raw:
            break
        key_raw = key_raw.strip()
        value_raw = stream.readline().strip()
        value_string = codecs.decode(value_raw, "hex")
        value = BSON(value_string).decode()
        arr.append(value)

    return arr


def convert_table(table_name, output_file=None):
    if output_file is None:
        output_file = add_suffix(Path(table_name), JSON_SUFFIX)

    table_decoded = load_wt_table(table_name)
    with open(output_file, "w") as f:
        f.write(dumps(table_decoded))
    logger.info(f"Converted table '{table_name}' to '{output_file}")
    return table_decoded, output_file


def load_catalog():
    catalog_path = add_suffix(Path(CATALOG_TABLE_NAME), JSON_SUFFIX)
    if catalog_path.exists():
        with catalog_path.open() as f:
            return loads(f.read())

    return convert_table(CATALOG_TABLE_NAME)[0]


def get_coll_ident(coll_name):
    for e in load_catalog():
        if e["ns"] == coll_name:
            return e["ident"]
    raise Exception(f"Collection '{coll_name}' not found in the catalog")


def load_collection(name):
    path = Path(name)

    # @name refers to an already decoded collection
    # just load it from file
    json_file = add_suffix(path, JSON_SUFFIX)
    if json_file.exists():
        logging.debug(f"Found already decoded collection '{json_file}'")
        with json_file.open() as f:
            return json.load(f), json_file

    # @name refers to an wt ident
    # convert the table and load it
    wt_file = add_suffix(path, WT_SUFFIX)
    if wt_file.exists():
        return convert_table(wt_file.stem)

    # @name refers to a collection in the catalog
    # find the ident for the collection, covert and load it
    coll_name = json_file.stem
    ident = get_coll_ident(coll_name)
    logging.debug(f"Found ident '{ident}' for collection '{coll_name}'")
    return convert_table(ident, json_file)


@click.group()
def cli():
    pass


@cli.command()
def list_collections():
    for e in load_catalog():
        ns = e["ns"]
        ident = e["ident"]
        click.echo(click.style(ns, fg="green") + " " + click.style(f"({ident})"))


@cli.command("convert")
@click.argument("coll_name")
def convert_cmd(coll_name):
    data, file = load_collection(coll_name)
    click.echo(f"Converted collection '{coll_name}' to '{file}'")


@cli.command("cat")
@click.argument("coll_name")
def cat_cmd(coll_name):
    data, file = load_collection(coll_name)

    console = Console()
    with console.pager(styles=True):
        console.print_json(dumps(data))


def main():
    logging.basicConfig(level=logging.INFO)
    cli()


if __name__ == "__main__":
    main()
