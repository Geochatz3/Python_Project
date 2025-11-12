"""Compatibility shim that forwards to the packaged CLI implementation."""

from cursor_python import (  # noqa: F401
    Circle,
    CircleSummary,
    Settings,
    configure_logging,
    format_circle_stats,
    generate_random_circles,
    main,
    parse_args,
    run_demo,
    summarize_circles,
)

if __name__ == "__main__":
    raise SystemExit(main())
