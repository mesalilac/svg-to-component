import os
from models import Svg
import click
from click import style
from pathlib import Path
from transformer import parse_svg, build_tsx_component, generate_index_file
import shutil


@click.command()
@click.option(
    "--input-dir",
    "-i",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to directory containing SVG files",
    required=True,
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to directory to output component files",
    required=True,
)
@click.option(
    "--no-index-ts", "-x", is_flag=True, help="Don't generate a index.ts file"
)
@click.option(
    "--header",
    "-h",
    type=str,
    help="String to prepend to generated files",
    required=False,
)
@click.option("--force", "-f", is_flag=True, help="Force overwrite existing files")
@click.option("--flat", "-F", is_flag=True, help="Flatten icons in output directory")
@click.option(
    "--clean", "-c", is_flag=True, help="Remove and recreate output directory"
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def main(
    input_dir: Path,
    output_dir: Path,
    no_index_ts,
    header: str | None,
    force: bool,
    flat: bool,
    clean: bool,
    verbose: bool,
):

    svgs: list[Svg] = []

    if clean and output_dir.exists():
        if verbose:
            click.echo(
                f"Deleting output directory {style(output_dir, fg='red', bold=True)}"
            )
        shutil.rmtree(output_dir)

    if not output_dir.exists():
        if verbose:
            click.echo(
                f"Creating output directory {style(output_dir, fg='green', bold=True)}"
            )
            click.echo()
        os.makedirs(output_dir)

    for source_svg_path in input_dir.rglob("*.svg"):
        svg = parse_svg(source_svg_path)

        if flat:
            relative_dir = "."
        else:
            relative_dir = source_svg_path.parent.relative_to(input_dir).as_posix()

        dest_tsx_path: Path = output_dir / relative_dir / f"{svg.name}.tsx"

        os.makedirs(dest_tsx_path.parent, exist_ok=True)

        svg.relative_path = relative_dir

        svgs.append(svg)

        tsx_code = build_tsx_component(svg, header)

        if dest_tsx_path.exists() and not force:
            if verbose:
                click.echo(
                    f"Component {style(svg.name, fg='yellow', bold=True)} already exists. {style('Use --force to overwrite', fg='bright_black')}"
                )
            continue

        dest_tsx_path.write_text(tsx_code)

        if verbose:
            click.echo(
                f"Component written to {style(dest_tsx_path.name, fg='green', bold=True)}"
            )

    if not no_index_ts:
        index_ts_path = output_dir / "index.ts"
        index_ts_content = generate_index_file(svgs)
        index_ts_path.write_text(index_ts_content)
        if verbose:
            click.echo()
            click.echo(
                f"File {style('Index.ts', fg='green', bold=True)} written to {style(index_ts_path, fg='green', bold=True)}"
            )


if __name__ == "__main__":
    main()
