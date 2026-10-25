# Duplicate File Finder

A Python command-line tool that scans a folder, identifies duplicate files using SHA-256 hashes, estimates duplicate storage, writes a text report, and offers optional deletion with explicit confirmation.

## Features

- Scan any folder by entering its path.
- Detect identical file contents using SHA-256, not filenames.
- Hash large files in 1 MB chunks to reduce memory usage.
- Count duplicate copies and estimate the storage they occupy.
- Handle files that cannot be accessed.
- Save a report to `duplicate_report.txt` in the user's Downloads folder.
- Ask for the exact response `YES` before attempting deletion.

## Requirements

- Python 3.10 or newer recommended
- No third-party packages required

## Run on Windows

1. Download or clone this repository.
2. Open Command Prompt or PowerShell in the project folder.
3. Run:

   ```powershell
   python duplicate_finder.py
   ```

4. Enter the folder path when prompted, for example:

   ```text
   C:\Users\YourName\Downloads
   ```

5. Review the results. The report is saved to:

   ```text
   C:\Users\YourName\Downloads\duplicate_report.txt
   ```

## Example output

```text
Scanning: C:\Users\YourName\Downloads

Duplicate files found:

Original: file1.txt
Duplicate: file2.txt
File size: 0.01 MB

Total duplicate files found: 1
Potential duplicate storage: 0.01 MB
Files with errors: 0
```

Your results and file sizes will differ.

## Safety notes

- **Back up important files before using deletion.**
- Deletion is permanent and does **not** send files to the Windows Recycle Bin.
- Only the exact response `YES` confirms deletion. Any other response cancels it.
- Test deletion only in a disposable test folder first.
- This version scans files directly inside the selected folder. It does not recursively scan subfolders.
- The first file encountered for a hash is treated as the original; later matching files are treated as duplicates.

## How it works

1. Ask for a folder path and validate it.
2. Read each regular file in chunks and calculate its SHA-256 hash.
3. Store the first file found for each hash in a dictionary.
4. Treat later files with a matching hash as duplicate copies.
5. Calculate the size of duplicate copies and write a text report.
6. If duplicates are found, offer an optional deletion step.

## Project structure

```text
duplicate-file-finder/
├── duplicate_finder.py
├── README.md
├── .gitignore
└── LICENSE
```

## Test checklist

- [ ] Scan a folder with two different files and confirm zero duplicates.
- [ ] Scan a test folder with two identical files and confirm one duplicate is found.
- [ ] Enter an invalid folder path and confirm the program displays an error.
- [ ] Enter anything other than `YES` at the deletion prompt and confirm files remain.
- [ ] Only in a disposable test folder, type `YES` and confirm one duplicate copy is removed.

## Future improvements

- Scan subfolders recursively.
- Add a graphical interface with a Browse button.
- Add file-size filtering to reduce unnecessary hashing.
- Move duplicates to a review folder instead of permanently deleting them.

## License

Released under the MIT License. See [LICENSE](LICENSE).
