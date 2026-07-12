#!/usr/bin/env python3
"""CodingBuddy CLI — generate complete apps from a natural-language prompt."""

from __future__ import annotations

import argparse
import logging
import sys

from dotenv import load_dotenv

load_dotenv()


def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s | %(message)s",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="codingbuddy",
        description=(
            "Generate a complete small project from a natural-language prompt using Groq."
        ),
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help='What to build, e.g. "Create a simple todo list app in HTML, CSS, and JavaScript"',
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    if not args.prompt:
        print(
            'Usage: python main.py "Create a simple todo list app in HTML, CSS, and JavaScript"'
        )
        return 1

    try:
        from graph.graph import build_graph
        from graph.state import CoderState
        from graph.tools import PROJECT_ROOT, safe_project_folder
    except Exception as exc:
        logging.error("Failed to import CodingBuddy modules: %s", exc)
        return 1

    print(f"Prompt: {args.prompt}")
    print("Running planner -> architect -> coder ...")

    try:
        agent = build_graph()
        result = agent.invoke(CoderState(user_prompt=args.prompt))
    except RuntimeError as exc:
        logging.error("%s", exc)
        return 1
    except Exception as exc:
        logging.exception("Agent run failed: %s", exc)
        return 1

    if isinstance(result, dict):
        errors = result.get("errors") or []
        plan = result.get("plan")
        generated = result.get("generated_files") or []
    else:
        errors = result.errors or []
        plan = result.plan
        generated = result.generated_files or []

    if errors:
        print("\nFinished with errors:")
        for err in errors:
            print(f"  - {err}")
        if not generated:
            return 1

    project_name = plan.name if plan else "unknown"
    out_dir = safe_project_folder(project_name)

    print(f"\nProject: {project_name}")
    print(f"Output:  {out_dir}")
    print(f"Files ({len(generated)}):")
    for path in generated:
        print(f"  - {path}")

    if not generated:
        print("No files were created.")
        return 1

    print(f"\nOpen {out_dir} to use your generated project.")
    print(f"(All projects live under {PROJECT_ROOT})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
