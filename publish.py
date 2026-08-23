import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.resolve()
INBOX_DIR = ROOT_DIR / "inbox"
DPPS_DIR = ROOT_DIR / "dpps"
MANIFEST_FILE = ROOT_DIR / "daily-dpps.json"


def find_inbox_files():
    """Finds the first pair of .json and .pdf in the inbox directory."""
    if not INBOX_DIR.exists():
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created inbox folder at: {INBOX_DIR}")
        return None, None

    json_files = list(INBOX_DIR.glob("*.json"))
    pdf_files = list(INBOX_DIR.glob("*.pdf"))

    if not json_files:
        print("❌ Error: No .json file found in the 'inbox/' folder.")
        return None, None

    json_file = json_files[0]
    pdf_file = pdf_files[0] if pdf_files else None

    return json_file, pdf_file


def run_git_command(args):
    """Executes a git command and returns the output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=ROOT_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git error on 'git {' '.join(args)}': {e.stderr.strip()}")
        return None


def publish():
    print("\n" + "=" * 55)
    print(" 🚀 SMA PHYSICS — 1-CLICK PUBLISHER ENGINE")
    print("=" * 55 + "\n")

    # 1. Detect Files
    json_source, pdf_source = find_inbox_files()
    if not json_source:
        print("ℹ️ Drop your daily .json (and optional .pdf) into 'inbox/' and run again.\n")
        return

    # 2. Parse & Validate JSON
    try:
        with open(json_source, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to parse JSON file {json_source.name}: {e}")
        return

    meta = data.get("meta", {})
    dpp_id = meta.get("dppId", "").lower().replace("_", "-").replace("sma-", "")
    
    # Fallback to file name if dppId is missing in JSON
    if not dpp_id:
        dpp_id = json_source.stem.lower()

    title = meta.get("title", f"Daily Practice Problem {dpp_id.upper()}")
    chapter = meta.get("chapter", "Physics Mechanics")
    question_count = len(data.get("questions", []))
    
    # Automatically get target date from JSON or use today
    publish_date = meta.get("publishDate", datetime.now().strftime("%Y-%m-%d"))

    # Determine default exam badge
    sample_exam = "JEE Main & NEET"
    if question_count > 0:
        sample_exam = data["questions"][0].get("exam", sample_exam)

    print(f"📦 Target DPP ID     : {dpp_id.upper()}")
    print(f"📖 Title             : {title}")
    print(f"📚 Chapter           : {chapter}")
    print(f"🔢 Question Count    : {question_count}")
    print(f"📅 Publish Date      : {publish_date}")

    # 3. Create Package Directory
    dest_dir = DPPS_DIR / dpp_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_json = dest_dir / f"{dpp_id}.json"
    dest_pdf = dest_dir / f"SMA_{dpp_id.upper().replace('-', '_')}.pdf"

    # Move and standardize filenames
    shutil.move(str(json_source), str(dest_json))
    print(f"✅ Moved JSON to     : dpps/{dpp_id}/{dest_json.name}")

    rel_pdf_path = ""
    if pdf_source and pdf_source.exists():
        shutil.move(str(pdf_source), str(dest_pdf))
        rel_pdf_path = f"/dpps/{dpp_id}/{dest_pdf.name}"
        print(f"✅ Moved PDF to      : dpps/{dpp_id}/{dest_pdf.name}")
    else:
        print("⚠️ No PDF file supplied in inbox (CBT online only mode).")

    # 4. Update daily-dpps.json
    manifest = []
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = []

    # Filter out existing duplicate entry if re-publishing the same ID
    manifest = [item for item in manifest if item.get("id") != dpp_id]

    # Prepend the new DPP entry
    new_entry = {
        "id": dpp_id,
        "date": publish_date,
        "jsonFile": f"/dpps/{dpp_id}/{dest_json.name}",
        "pdfFile": rel_pdf_path,
        "title": title,
        "chapter": chapter,
        "exam": sample_exam,
        "questionCount": question_count
    }
    manifest.insert(0, new_entry)

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("✅ Updated Master Manifest : daily-dpps.json")

    # 5. Git Automation (Stage, Commit & Push)
    print("\n📡 Syncing with GitHub & Deploying to Vercel...")
    run_git_command(["add", "."])
    
    commit_msg = f"Publish {dpp_id.upper()}: {title}"
    run_git_command(["commit", "-m", commit_msg])
    
    push_out = run_git_command(["push"])
    if push_out is not None:
        print("🚀 Successfully pushed to Git! Live deployment triggered.")
        print(f"🌐 Practice URL: https://smaphysics.com/practice/{dpp_id}\n")
    else:
        print("⚠️ Could not push to Git automatically. You can manually run 'git push'.\n")


if __name__ == "__main__":
    publish()