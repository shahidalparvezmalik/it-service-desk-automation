from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workflow import analyze_ticket


def main() -> None:
    ticket = (
        "Finance users cannot access the shared folder after a permissions change. "
        "The issue affects a business team and requires access restoration."
    )

    result = analyze_ticket(
        description=ticket,
        impact="High",
        urgency="Medium",
        action="privileged access change",
    )

    print("AI-Assisted IT Service Desk Demo")
    print("=" * 40)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
