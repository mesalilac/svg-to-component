import os
from models import Svg
import click
from click import style
from pathlib import Path
from transformer import parse_svg, build_tsx_component, generate_index_file


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
@click.option("--no-index-ts", "-x", is_flag=True, help="Generate index.ts file")
@click.option(
    "--header",
    "-h",
    type=str,
    help="String to prepend to generated files",
    required=False,
)
@click.option("--force", "-f", is_flag=True, help="Force overwrite existing files")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def main(
    input_dir: Path,
    output_dir: Path,
    no_index_ts,
    header: str | None,
    force: bool,
    verbose: bool,
):

    svgs: list[Svg] = []

    if not output_dir.exists():
        click.echo(
            f"Creating output directory {style(output_dir, fg='cyan', bold=True)}"
        )
        os.makedirs(output_dir)

    for file_path in input_dir.rglob("*.svg"):
        svg = parse_svg(file_path)
        svgs.append(svg)

        tsx_component = build_tsx_component(svg, header)

        component_path: Path = output_dir / f"{svg.name}.tsx"

        if component_path.exists() and not force:
            if verbose:
                click.echo(
                    f"Component {style(svg.name, fg='yellow', bold=True)} already exists. {style('Use --force to overwrite', fg='bright_black')}"
                )
            continue

        component_path.write_text(tsx_component)

        if verbose:
            click.echo(
                f"Component written to {style(component_path.name, fg='green', bold=True)}"
            )

    if not no_index_ts:
        index_ts_path = output_dir / "index.ts"
        index_ts_content = generate_index_file([svg.name for svg in svgs])
        index_ts_path.write_text(index_ts_content)
        if verbose:
            click.echo(
                f"File {style('Index.ts', fg='green', bold=True)} written to {style(index_ts_path, fg='cyan', bold=True)}"
            )


if __name__ == "__main__":
    main()
