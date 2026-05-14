#!/usr/bin/env python3
"""Skill Auto Maintain — automated lifecycle management for non-bundled Hermes skills.

Scans all skill directories under ~/.hermes/skills/, identifies non-bundled
(agent-created or user-created) skills, relocates misplaced ones to
user_skills/, registers them, detects merge candidates, optimises SKILL.md
format, and reports a comprehensive summary.

Usage:
    ~/.hermes/hermes-agent/venv/bin/python maintain.py
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────────
HERMES_HOME = os.path.expanduser("~/.hermes")
SKILLS_BASE = os.path.join(HERMES_HOME, "skills")
BUNDLED_MANIFEST = os.path.join(SKILLS_BASE, ".bundled_manifest")

USER_SKILLS_DIR = os.path.join(SKILLS_BASE, "user_skills")
USER_SKILLS_JSON = os.path.join(USER_SKILLS_DIR, "user_skills.json")

EXCLUDED_DIRS = {"user_skills"}

MERGE_THRESHOLD = 0.30


# ══════════════════════════════════════════════════════════════════════════
#  FILE I/O
# ══════════════════════════════════════════════════════════════════════════

def load_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    shutil.move(tmp, path)


def backup_file(path):
    if not os.path.exists(path):
        return
    backup_dir = os.path.join(SKILLS_BASE, ".backup")
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = os.path.basename(path)
    shutil.copy2(path, os.path.join(backup_dir, f"{ts}_{name}"))


# ══════════════════════════════════════════════════════════════════════════
#  SKILL SCANNING
# ══════════════════════════════════════════════════════════════════════════

def get_skill_name_from_frontmatter(skill_path):
    """Extract `name:` from SKILL.md frontmatter, or None."""
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return None
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read(2000)
    m = re.search(r"^name:\s*(.+)\s*$", content, re.MULTILINE)
    return m.group(1).strip().strip("\"'") if m else None


def get_skill_description(skill_path):
    """Extract `description:` from SKILL.md frontmatter."""
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return ""
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read(2000)
    m = re.search(r'description:\s*["\']?(.*?)["\']?\s*(?:\n|platforms|version|author|tags)', content)
    if m:
        desc = m.group(1).strip().rstrip("\"'")
        return desc if len(desc) < 500 else desc[:500]
    return ""


def get_skill_size(skill_path):
    path = os.path.join(skill_path, "SKILL.md")
    return os.path.getsize(path) if os.path.exists(path) else 0


def scan_skills_in_dir(directory):
    """Return dict of {skill_name: skill_path} for skills in a directory."""
    skills = {}
    if not os.path.isdir(directory):
        return skills
    for item in sorted(os.listdir(directory)):
        item_path = os.path.join(directory, item)
        if not os.path.isdir(item_path):
            continue
        if item.startswith("."):
            continue
        if os.path.exists(os.path.join(item_path, "SKILL.md")):
            skills[item] = item_path
    return skills


def load_bundled_manifest():
    """Return set of bundled skill names from .bundled_manifest."""
    if not os.path.exists(BUNDLED_MANIFEST):
        return set()
    bundled = set()
    with open(BUNDLED_MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and ":" in line:
                bundled.add(line.split(":")[0])
    return bundled


def is_bundled_skill(name, path, bundled):
    """Check if a skill is a system bundled skill.

    Two checks:
    1. Directory name matches manifest key (fast path).
    2. SKILL.md frontmatter `name:` matches manifest key (fallback).
    """
    if name in bundled:
        return True
    fm_name = get_skill_name_from_frontmatter(path)
    if fm_name and fm_name in bundled:
        return True
    return False


# ══════════════════════════════════════════════════════════════════════════
#  SKILL ANALYSIS & SIMILARITY
# ══════════════════════════════════════════════════════════════════════════

STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'doing', 'will', 'would',
    'can', 'could', 'may', 'might', 'shall', 'should', 'to', 'too', 'for',
    'of', 'in', 'on', 'at', 'by', 'with', 'from', 'as', 'and', 'or', 'but',
    'not', 'no', 'nor', 'this', 'that', 'these', 'those', 'it', 'its',
    'you', 'your', 'we', 'our', 'they', 'their', 'he', 'she', 'him', 'her',
    'all', 'any', 'each', 'every', 'some', 'most', 'many', 'much', 'few',
    'use', 'used', 'using', 'uses', 'also', 'very', 'just', 'only', 'even',
    'than', 'then', 'when', 'what', 'which', 'who', 'whom', 'where', 'how',
    'into', 'over', 'about', 'after', 'before', 'between', 'through', 'during',
    'such', 'more', 'less', 'other', 'another', 'both', 'each', 'own',
    'skill', 'setup', 'help', 'need', 'want', 'work', 'working', 'works',
    'based', 'built', 'like', 'take', 'make', 'made', 'way', 'well',
    'using', 'requires', 'including', 'supports', 'provides', 'allows',
    'enables', 'simple', 'quick', 'easy', 'basic', 'advanced',
}


def get_skill_topic_keywords(skill_path):
    """Extract keywords from SKILL.md: headings, tags, and description field."""
    keywords = set()
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return keywords
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read(3000)

    # Headings
    for match in re.finditer(r"##\s+(.*?)(?:\n|$)", content):
        keywords.add(match.group(1).strip().lower())

    # Tags
    tags_match = re.search(r"tags:\s*\[(.*?)\]", content)
    if tags_match:
        for tag in tags_match.group(1).split(","):
            tag = tag.strip().strip("\"'")
            if tag:
                keywords.add(tag.lower())

    # Description words
    desc_match = re.search(
        r'description:\s*["\']?(.*?)["\']?\s*(?:\n|platforms|version|author|tags)',
        content,
    )
    if not desc_match:
        desc_match = re.search(r'description:\s*["\']?(.*?)(?:\n[a-z])', content)
    if desc_match:
        desc = desc_match.group(1).strip().rstrip("\"'")
        words = re.findall(r'[a-zA-Z][a-zA-Z-]{2,}', desc.lower())
        for w in words:
            wc = w.strip("-")
            if wc not in STOPWORDS and len(wc) > 2:
                keywords.add(wc)

    return keywords


def get_skill_headings(skill_path):
    """Extract all ## headings for structure comparison."""
    headings = set()
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return headings
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read(3000)
    for match in re.finditer(r"##\s+(.*?)(?:\n|$)", content):
        h = match.group(1).strip().lower()
        if h:
            headings.add(h)
    return headings


def get_skill_related(skill_path):
    """Extract related_skills from frontmatter."""
    related = set()
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return related
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read(2000)
    match = re.search(r"related_skills:\s*\[(.*?)\]", content)
    if match:
        for item in match.group(1).split(","):
            item = item.strip().strip("\"'")
            if item:
                related.add(item)
    return related


def compute_similarity(name_a, path_a, name_b, path_b):
    """Compute similarity score between two skills.

    Multi-dimensional scoring:
    - Name token overlap: +0.20
    - Content keyword overlap: +0.10/kw, max +0.30 (Jaccard-gated)
    - Heading structure overlap: +0.10 if Jaccard >= 0.25
    - Related-skills cross-reference: +0.20

    Returns (score, axes, details).
    """
    score = 0.0
    axes = set()
    details = []

    # Name overlap
    a_parts = set(name_a.lower().replace("-", " ").split())
    b_parts = set(name_b.lower().replace("-", " ").split())
    name_overlap = a_parts & b_parts
    if name_overlap:
        score += 0.20
        axes.add("name")
        details.append(f"name overlap: {name_overlap}")

    # Keyword overlap
    ka = get_skill_topic_keywords(path_a)
    kb = get_skill_topic_keywords(path_b)
    kw_overlap = ka & kb
    content_union = ka | kb
    jaccard = len(kw_overlap) / len(content_union) if content_union else 0.0

    if name_overlap and not kw_overlap:
        return 0.0, set(), ["name match but zero content overlap — skipped"]

    if ka and kb and kw_overlap:
        kw_score = min(0.30, 0.10 * len(kw_overlap))
        score += kw_score
        axes.add("content")
        details.append(f"topic: {len(kw_overlap)} shared kw (jaccard={jaccard:.2f})")

    # Heading structure overlap
    ha = get_skill_headings(path_a)
    hb = get_skill_headings(path_b)
    if ha and hb:
        h_union = ha | hb
        h_jaccard = len(ha & hb) / len(h_union) if h_union else 0.0
        if h_jaccard >= 0.25:
            score += 0.10
            axes.add("structure")
            details.append(f"heading structure (j={h_jaccard:.2f})")

    # Related-skills cross-reference
    rel_a = get_skill_related(path_a)
    rel_b = get_skill_related(path_b)
    if name_a in rel_b or name_b in rel_a:
        score += 0.20
        axes.add("xref")
        details.append("related_skills reference")

    if len(axes) < 2:
        return 0.0, axes, ["insufficient evidence axes"]

    if not name_overlap and jaccard < 0.15:
        return 0.0, axes, ["no name overlap + low content similarity"]

    return score, axes, details


# ══════════════════════════════════════════════════════════════════════════
#  SKILL.MD OPTIMISATION & QUALITY
# ══════════════════════════════════════════════════════════════════════════

def ensure_skill_md_standard(skill_path, skill_name):
    """Fix common SKILL.md formatting issues.

    Returns (bool, message) where bool indicates if changes were made.
    """
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return False, "SKILL.md not found"

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    changes = []

    # Missing frontmatter
    if not content.startswith("---"):
        desc = skill_name.replace("-", " ").title()
        frontmatter = (
            f"---\n"
            f"name: {skill_name}\n"
            f"description: \"{desc}\"\n"
            f"version: 1.0.0\n"
            f"author: Hermes Agent\n"
            f"license: MIT\n"
            f"---\n\n"
        )
        content = frontmatter + content
        changes.append("added frontmatter")

    # Missing name in frontmatter
    if re.search(r"^name:\s*$", content, re.MULTILINE):
        content = re.sub(r"^name:\s*$", f"name: {skill_name}", content, count=1, flags=re.MULTILINE)
        changes.append("filled empty name field")

    # Missing description in frontmatter
    if re.search(r"^description:\s*$", content, re.MULTILINE):
        desc = skill_name.replace("-", " ").title()
        content = re.sub(r"^description:\s*$", f'description: "{desc}"', content, count=1, flags=re.MULTILINE)
        changes.append("filled empty description")

    # Missing H1 heading — check after frontmatter, not at file start
    body_start = 0
    if content.startswith("---"):
        end_fm = content.find("---", 3)
        if end_fm > 0:
            body_start = end_fm + 3
    body = content[body_start:].lstrip("\n")
    if not body.startswith("# "):
        title = skill_name.replace("-", " ").title()
        insert_point = content.find("---\n\n")
        if insert_point >= 0:
            insert_point = content.index("\n", insert_point + 4)
            content = content[:insert_point] + f"\n# {title}\n" + content[insert_point:]
        else:
            content = f"# {title}\n\n" + content
        changes.append("added H1 heading")

    if not changes:
        return False, "no changes needed"

    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(content)
    return True, ", ".join(changes)


def check_skill_quality(skill_path, skill_name):
    """Check SKILL.md for content quality issues.

    Returns list of warning strings.
    """
    warnings = []
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return [f"SKILL.md not found"]

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # Description too short or generic
    desc = get_skill_description(skill_path)
    if len(desc) < 20:
        warnings.append("description too short (< 20 chars)")
    generic_desc_patterns = ["description of what this skill does",
                             "example skill", "your skill", "a skill for"]
    for pat in generic_desc_patterns:
        if pat in desc.lower():
            warnings.append(f"description appears generic ('{pat}')")

    # No tags
    if "tags:" not in content[:2000]:
        warnings.append("no tags defined in frontmatter")

    # Empty or missing triggers
    has_triggers = bool(re.search(r"triggers:\s*\[.*?\]", content[:2000]))
    if not has_triggers:
        warnings.append("no triggers defined")

    # Very short SKILL.md (likely placeholder)
    if len(content) < 200:
        warnings.append(f"SKILL.md very short ({len(content)} chars) — possible placeholder")

    # No ## sections
    sections = re.findall(r"^##\s+", content, re.MULTILINE)
    if not sections:
        warnings.append("no structural sections (## headings)")

    return warnings


# ══════════════════════════════════════════════════════════════════════════
#  REGISTRY (user_skills.json)
# ══════════════════════════════════════════════════════════════════════════

def load_registry():
    """Load user_skills.json, create default if missing."""
    registry = load_json(USER_SKILLS_JSON)
    if registry is None:
        registry = {
            "version": "1.0",
            "description": "User-managed non-bundled skills registry",
            "skills": [],
        }
        save_json(USER_SKILLS_JSON, registry)
        print("  [Registry] Created user_skills.json (empty)")
    return registry


def save_registry(registry):
    backup_file(USER_SKILLS_JSON)
    save_json(USER_SKILLS_JSON, registry)


def find_registry_entry(registry, name):
    """Find entry by name, return index or -1."""
    for i, entry in enumerate(registry["skills"]):
        if entry.get("name") == name:
            return i
    return -1


def register_skill(registry, name, description, origin, merged_from=None):
    """Register or update a skill in user_skills.json.

    Args:
        registry: The registry dict.
        name: Skill directory name.
        description: Description from SKILL.md.
        origin: Source path ("auto-generated/<name>", "creative/<name>", etc.)
        merged_from: If merged, list of source skill names.

    Returns:
        True if new entry, False if updated existing.
    """
    idx = find_registry_entry(registry, name)
    now = datetime.now().isoformat()

    if idx >= 0:
        entry = registry["skills"][idx]
        entry["modification_count"] = entry.get("modification_count", 0) + 1
        entry["last_updated"] = now
        if description:
            entry["description"] = description
        entry["status"] = "merged" if merged_from else "active"
        if merged_from:
            entry["origin"] = f"merged: {', '.join(merged_from)}"
        return False

    entry = {
        "name": name,
        "description": description or "",
        "status": "merged" if merged_from else "active",
        "origin": f"merged: {', '.join(merged_from)}" if merged_from else origin,
        "optimized": False,
        "modification_count": 0,
        "created": now,
        "last_updated": now,
    }
    registry["skills"].append(entry)
    return True


def mark_optimized(registry, name):
    idx = find_registry_entry(registry, name)
    if idx >= 0:
        registry["skills"][idx]["optimized"] = True
        registry["skills"][idx]["modification_count"] = \
            registry["skills"][idx].get("modification_count", 0) + 1
        registry["skills"][idx]["last_updated"] = datetime.now().isoformat()


# ══════════════════════════════════════════════════════════════════════════
#  PHASE 1: SCAN & MIGRATE
# ══════════════════════════════════════════════════════════════════════════

def scan_all_directories():
    """Scan all skill directories under SKILLS_BASE, excluding hidden and user_skills.

    Returns dict of {category_path: {skill_name: skill_path}}.
    """
    categories = {}
    if not os.path.exists(SKILLS_BASE):
        return categories

    for item in sorted(os.listdir(SKILLS_BASE)):
        if item.startswith("."):
            continue
        if item in EXCLUDED_DIRS:
            continue
        item_path = os.path.join(SKILLS_BASE, item)
        if not os.path.isdir(item_path):
            continue
        skills = scan_skills_in_dir(item_path)
        if skills:
            categories[item_path] = skills
    return categories


def phase_scan_and_migrate(registry):
    """[Scan] Phase: scan all directories, find orphans, migrate to user_skills/.

    Returns dict of report data.
    """
    print("  [Scan] Scanning all skill directories...")
    bundled = load_bundled_manifest()
    all_found = {}
    orphan_count = 0
    migrated = []
    already_registered = []
    bundled_found = 0

    categories = scan_all_directories()

    for cat_path, skills in categories.items():
        cat_name = os.path.basename(cat_path)
        for skill_name, skill_path in skills.items():
            all_found[skill_name] = skill_path

            # Skip bundled skills
            if is_bundled_skill(skill_name, skill_path, bundled):
                bundled_found += 1
                continue

            # Determine if this skill is in user_skills/ already
            if cat_name == "user_skills":
                # Already in user_skills — just ensure it's registered
                if find_registry_entry(registry, skill_name) < 0:
                    desc = get_skill_description(skill_path)
                    register_skill(registry, skill_name, desc, f"user_skills/{skill_name}")
                    already_registered.append(skill_name)
                continue

            # This is an orphan — migrate to user_skills/
            target_path = os.path.join(USER_SKILLS_DIR, skill_name)
            file_exists = os.path.exists(target_path)

            if file_exists:
                print(f"  ! {skill_name}: target user_skills/{skill_name} already exists (skipped)")
                continue

            shutil.move(skill_path, target_path)
            desc = get_skill_description(target_path)
            is_new = register_skill(registry, skill_name, desc, f"{cat_name}/{skill_name}")
            orphan_count += 1
            migrated.append(f"✓ {skill_name}: {cat_name}/ → user_skills/")

    return {
        "categories_scanned": len(categories),
        "total_found": len(all_found),
        "bundled_skipped": bundled_found,
        "orphans_migrated": orphan_count,
        "already_registered": already_registered,
        "migrated": migrated,
    }


# ══════════════════════════════════════════════════════════════════════════
#  PHASE 2: COMPARE & MERGE CANDIDATE DETECTION
# ══════════════════════════════════════════════════════════════════════════

def phase_compare(registry):
    """[Compare] Phase: pairwise comparison of user_skills/ skill skills.

    Reports merge candidates above threshold.
    """
    print("  [Compare] Analysing skill similarity...")
    candidates = []

    # Get all active skills in user_skills/
    skills_in_dir = scan_skills_in_dir(USER_SKILLS_DIR)
    active_names = [s["name"] for s in registry["skills"] if s.get("status") in ("active", None)]
    active_in_dir = {n: p for n, p in skills_in_dir.items() if n in active_names}
    names = sorted(active_in_dir.keys())

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            score, axes, details = compute_similarity(a, active_in_dir[a], b, active_in_dir[b])
            if score >= MERGE_THRESHOLD:
                candidates.append({
                    "a": a,
                    "b": b,
                    "score": round(score, 2),
                    "axes": sorted(axes),
                    "details": details,
                })

    return {
        "total_active": len(active_in_dir),
        "merge_candidates": candidates,
    }


# ══════════════════════════════════════════════════════════════════════════
#  PHASE 3: OPTIMISE SKILL.MD
# ══════════════════════════════════════════════════════════════════════════

def phase_optimize(registry):
    """[Optimise] Phase: fix SKILL.md format and check quality for unoptimised skills.

    Returns dict of report data.
    """
    print("  [Optimise] Checking SKILL.md format and quality...")
    formatted = []
    quality_warnings = []

    for entry in registry["skills"]:
        name = entry["name"]
        if entry.get("optimized"):
            continue

        skill_path = os.path.join(USER_SKILLS_DIR, name)
        if not os.path.isdir(skill_path):
            continue

        # Format fix
        fixed, msg = ensure_skill_md_standard(skill_path, name)
        if fixed:
            formatted.append(f"✓ {name}: {msg}")

        # Quality check
        warnings = check_skill_quality(skill_path, name)
        if warnings:
            quality_warnings.append({"name": name, "warnings": warnings})

        mark_optimized(registry, name)

    return {
        "formatted": formatted,
        "quality_warnings": quality_warnings,
    }


# ══════════════════════════════════════════════════════════════════════════
#  REPORT
# ══════════════════════════════════════════════════════════════════════════

def generate_report(scan_result, compare_result, optimise_result):
    """Generate a professional summary report."""
    lines = []
    lines.append("")
    lines.append("=" * 66)
    lines.append("  Skill Auto Maintain — Scan Complete")
    lines.append(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 66)
    lines.append("")

    # Scan summary
    lines.append("  ── Scan Results ──")
    lines.append(f"    Categories scanned:     {scan_result['categories_scanned']}")
    lines.append(f"    Total skills found:     {scan_result['total_found']}")
    lines.append(f"    Bundled skills skipped: {scan_result['bundled_skipped']}")
    lines.append(f"    Orphans migrated:       {scan_result['orphans_migrated']}")
    if scan_result["migrated"]:
        for m in scan_result["migrated"]:
            lines.append(f"    {m}")
    lines.append("")

    # Registration
    if scan_result["already_registered"]:
        lines.append("  ── Registration ──")
        for r in scan_result["already_registered"]:
            lines.append(f"    Registered: {r}")
        lines.append("")

    # Merge candidates
    lines.append("  ── Merge Analysis ──")
    if compare_result["merge_candidates"]:
        lines.append(f"    Merge candidates detected ({len(compare_result['merge_candidates'])} pair(s)):")
        for c in compare_result["merge_candidates"]:
            axes_str = "+".join(c["axes"])
            det = "; ".join(c["details"][:3])
            lines.append(f"    ! {c['a']} <-> {c['b']} (score={c['score']:.2f}, axes=[{axes_str}], {det})")
        lines.append("    → Review candidates above and decide whether to merge.")
    else:
        lines.append("    No merge candidates detected (all skills are sufficiently distinct).")
    lines.append("")

    # Optimisation
    lines.append("  ── SKILL.md Optimisation ──")
    if optimise_result["formatted"]:
        for f in optimise_result["formatted"]:
            lines.append(f"    {f}")
    else:
        lines.append("    All SKILL.md files are already properly formatted.")
    lines.append("")

    # Quality warnings
    if optimise_result["quality_warnings"]:
        lines.append("  ── Quality Warnings ──")
        for qw in optimise_result["quality_warnings"]:
            for w in qw["warnings"]:
                lines.append(f"    ! {qw['name']}: {w}")
        lines.append("    → Review the flagged skills and consider updating their content.")
        lines.append("")
    else:
        lines.append("    No quality issues detected.")
        lines.append("")

    # Final summary
    lines.append("  ── Summary ──")
    lines.append(f"    Total active in user_skills/: {compare_result['total_active']}")
    lines.append(f"    Skills formatted:           {len(optimise_result['formatted'])}")
    lines.append(f"    Skills with quality issues: {len(optimise_result['quality_warnings'])}")
    lines.append("")
    lines.append("=" * 66)
    lines.append("")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print()
    print("=" * 66)
    print("  Skill Auto Maintain v1.0")
    print("  Automated lifecycle management for non-bundled Hermes skills")
    print("=" * 66)

    # Ensure user_skills/ directory exists before any operation
    os.makedirs(USER_SKILLS_DIR, exist_ok=True)

    # Load registry
    registry = load_registry()

    # Phase 1: Scan & Migrate
    scan_result = phase_scan_and_migrate(registry)

    # Phase 2: Compare
    compare_result = phase_compare(registry)

    # Phase 3: Optimise
    optimise_result = phase_optimize(registry)

    # Save registry
    save_registry(registry)
    print(f"  [Registry] Saved: {USER_SKILLS_JSON}")

    # Report
    report = generate_report(scan_result, compare_result, optimise_result)
    print(report)


if __name__ == "__main__":
    main()
