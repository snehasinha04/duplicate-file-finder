import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024  # Read 1 MB at a time


def calculate_hash(file_path: Path) -> str:
    """Return a SHA-256 hash without loading the entire file into memory."""
    sha256 = hashlib.sha256()
    with file_path.open("rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


def main() -> None:
    folder_path = input("Enter the folder path to scan: ").strip().strip('"')
    folder = Path(folder_path).expanduser()

    if not folder.exists() or not folder.is_dir():
        print("Error: The folder does not exist. Please enter a valid folder path.")
        return

    report_file = Path.home() / "Downloads" / "duplicate_report.txt"
    seen = {}
    duplicates = []
    errors = 0

    print(f"\nScanning: {folder}\n")

    try:
        files = list(folder.iterdir())
    except OSError as error:
        print(f"Error: Could not access the folder: {error}")
        return

    for file_path in files:
        try:
            if not file_path.is_file():
                continue

            fingerprint = calculate_hash(file_path)
            if fingerprint in seen:
                duplicates.append((file_path, seen[fingerprint]))
            else:
                seen[fingerprint] = file_path
        except OSError as error:
            errors += 1
            print(f"Could not scan {file_path.name}: {error}")

    total_duplicate_bytes = 0
    report_lines = [
        "DUPLICATE FILE FINDER REPORT",
        "=" * 35,
        "",
        f"Scanned folder: {folder}",
        "",
    ]

    if duplicates:
        print("Duplicate files found:\n")
        for duplicate, original in duplicates:
            try:
                file_size = duplicate.stat().st_size
                total_duplicate_bytes += file_size
                size_mb = round(file_size / (1024 * 1024), 2)
                details = (
                    f"Original: {original.name}\n"
                    f"Duplicate: {duplicate.name}\n"
                    f"File size: {size_mb} MB\n"
                )
                print(details)
                report_lines.extend([details, ""])
            except OSError as error:
                errors += 1
                message = f"Could not read file size for {duplicate.name}: {error}"
                print(message)
                report_lines.extend([message, ""])
    else:
        print("No duplicate files found.")
        report_lines.extend(["No duplicate files found.", ""])

    total_mb = round(total_duplicate_bytes / (1024 * 1024), 2)
    summary = (
        f"Total duplicate files found: {len(duplicates)}\n"
        f"Potential duplicate storage: {total_mb} MB\n"
        f"Files with errors: {errors}"
    )
    print(summary)
    report_lines.extend([summary, ""])

    if duplicates:
        print(
            "\nWARNING: Deletion permanently removes files and does not use "
            "the Recycle Bin."
        )
        choice = input(
            "Delete the listed duplicate files? Type YES to confirm: "
        ).strip()

        if choice == "YES":
            deleted = 0
            for duplicate, _original in duplicates:
                try:
                    duplicate.unlink()
                    deleted += 1
                    print(f"Deleted: {duplicate.name}")
                except OSError as error:
                    errors += 1
                    print(f"Could not delete {duplicate.name}: {error}")
            deletion_summary = f"Files deleted: {deleted}"
            print(f"\n{deletion_summary}")
            report_lines.extend(["", deletion_summary])
        else:
            print("Deletion cancelled. No files were deleted.")
            report_lines.extend(["", "Deletion cancelled. No files were deleted."])

    try:
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        print(f"\nReport saved to: {report_file}")
    except OSError as error:
        print(f"Could not save the report: {error}")


if __name__ == "__main__":
    main()
