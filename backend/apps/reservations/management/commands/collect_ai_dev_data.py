import csv
import re
from datetime import datetime, timedelta
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Collect AI development data into a CSV file"
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            "-o",
            default="./ai_dev_data.csv",
            help="Output CSV file path",
        )
        parser.add_argument(
            "--done-dir",
            default="../ai/features/done",
            help="Directory containing completed feature files",
        )
        parser.add_argument(
            "--specs-dir",
            default="../specs",
            help="Directory containing feature specs",
        )
        parser.add_argument(
            "--sessions-dir",
            default="../ai/sessions",
            help="Directory containing AI session logs",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"])
        done_dir = Path(options["done_dir"])
        specs_dir = Path(options["specs_dir"])
        sessions_dir = Path(options["sessions_dir"])

        if not done_dir.is_dir():
            raise CommandError(f"Done directory not found: {done_dir}")
        if not specs_dir.is_dir():
            raise CommandError(f"Specs directory not found: {specs_dir}")
        if not sessions_dir.is_dir():
            raise CommandError(f"Sessions directory not found: {sessions_dir}")

        features = self._parse_features(done_dir)
        spec_map = self._build_spec_map(specs_dir)
        session_map = self._build_session_map(sessions_dir)
        rows = []
        for feature_file, title in features:
            spec_path, spec_num = self._find_spec_and_num(spec_map, feature_file)
            specs_quality = self._assess_spec_quality(spec_path)
            sessions = self._find_sessions(session_map, spec_num, feature_file)
            model = self._extract_model(sessions)
            start_ts = self._extract_start_timestamp(sessions)
            end_ts = self._extract_end_timestamp(sessions)
            minutes = self._calculate_minutes(start_ts, end_ts)
            iterations = self._count_iterations(sessions)
            complexity = self._calculate_complexity(sessions, iterations)
            rows.append(
                [
                    title,
                    str(complexity),
                    str(minutes) if minutes is not None else "",
                    model or "",
                    start_ts.isoformat() if start_ts else "",
                    end_ts.isoformat() if end_ts else "",
                    str(specs_quality),
                    str(iterations),
                ]
            )

        self._write_csv(output_path, rows)
        self.stdout.write(
            self.style.SUCCESS(f"Generated {output_path} with {len(rows)} feature(s)")
        )

    def _parse_features(self, done_dir):
        features = []
        for f in sorted(done_dir.iterdir()):
            if f.suffix == ".md" and f.is_file():
                title = self._extract_title(f)
                if title:
                    features.append((f, title))
        return features

    def _extract_title(self, path):
        try:
            content = path.read_text(encoding="utf-8")
            for line in content.splitlines():
                if line.startswith("# "):
                    return line[2:].strip()
        except Exception:
            return None
        return None

    def _extract_slug(self, stem):
        slug = stem.lower()
        slug = re.sub(r"^\d+[_-]", "", slug)
        slug = slug.replace("_", "-")
        slug = re.sub(r"[^a-z0-9-]", "", slug)
        slug = re.sub(r"-+", "-", slug).strip("-")
        return slug

    def _build_spec_map(self, specs_dir):
        spec_map = {}
        for d in specs_dir.iterdir():
            if not d.is_dir():
                continue
            spec_file = d / "spec.md"
            if not spec_file.is_file():
                continue
            num = re.match(r"(\d+)", d.name)
            num_str = num.group(1) if num else ""
            slug = self._extract_slug(d.name)
            spec_map[d.name.lower()] = (spec_file, num_str, slug)
        return spec_map

    def _find_spec_and_num(self, spec_map, feature_path):
        raw_stem = feature_path.stem.lower()
        feature_slug = self._extract_slug(feature_path.stem)
        candidates = []
        for dir_name, (spec_file, num, slug) in spec_map.items():
            score = 0
            if slug == feature_slug:
                score = 10
            elif feature_slug in slug or slug in feature_slug:
                score = 8
            else:
                feat_tokens = set(feature_slug.split("-"))
                spec_tokens = set(slug.split("-"))
                common = feat_tokens & spec_tokens
                if len(common) >= 2:
                    score = len(common)
                elif raw_stem.replace("_", "-") in slug or slug in raw_stem.replace(
                    "_", "-"
                ):
                    score = 1
            if score:
                candidates.append((score, spec_file, num, slug))
        if candidates:
            candidates.sort(key=lambda x: (-x[0], -len(x[3])))
            return candidates[0][1], candidates[0][2]
        return None, ""

    def _assess_spec_quality(self, spec_path):
        if not spec_path or not spec_path.is_file():
            return 1
        try:
            content = spec_path.read_text(encoding="utf-8")
        except Exception:
            return 1
        score = 1
        if re.search(r"(?i)##\s*acceptance\s*(criteria|scenarios)", content):
            score = 2
        if re.search(r"(?i)##\s*constraints", content) or re.search(
            r"(?i)\*\*Constraints\*\*", content
        ):
            score = 3
        if re.search(r"(?i)##\s*(edge cases|examples)", content):
            score = 4
        if re.search(r"(?i)##\s*(assumptions|key entities|success criteria)", content):
            score = 5
        return score

    _MODEL_KEYWORDS = {
        "deepseek",
        "v4",
        "flash",
        "free",
        "big",
        "pickle",
        "opencode",
        "deepseek-v4",
        "deepseek-v4-flash",
        "deepseek-v4-flash-free",
    }

    def _session_clean_slug(self, stem):
        slug = stem.lower()
        slug = re.sub(r"\d{8,}", "", slug)
        slug = re.sub(r"\d{6}z?$", "", slug)
        tokens = slug.replace("_", "-").split("-")
        clean = [
            t for t in tokens if t and len(t) > 2 and t not in self._MODEL_KEYWORDS
        ]
        return "-".join(clean)

    def _build_session_map(self, sessions_dir):
        entries = []
        for sf in sorted(sessions_dir.iterdir()):
            if sf.suffix != ".md" or not sf.is_file():
                continue
            stem = sf.stem.lower()
            nums = re.findall(r"\d+", stem)
            slug = self._session_clean_slug(stem)
            entries.append((sf, nums, slug))
        return entries

    def _find_sessions(self, session_map, spec_num, feature_path):
        if not spec_num:
            return self._match_sessions_by_slug(session_map, feature_path)
        by_num = [sf for sf, nums, _ in session_map if spec_num in nums]
        if by_num:
            return by_num
        return self._match_sessions_by_slug(session_map, feature_path)

    def _match_sessions_by_slug(self, session_map, feature_path):
        feature_slug = self._extract_slug(feature_path.stem)
        feat_tokens = set(feature_slug.split("-")) if feature_slug else set()
        if len(feat_tokens) < 2:
            return []
        scored = []
        for sf, nums, clean_slug in session_map:
            if not clean_slug:
                continue
            sess_tokens = set(clean_slug.split("-"))
            common = feat_tokens & sess_tokens
            if len(common) >= 2:
                scored.append((len(common), sf))
        if not scored:
            return []
        scored.sort(key=lambda x: (-x[0], x[1].name))
        best = scored[0][0]
        return [sf for s, sf in scored if s == best]

    def _extract_model(self, sessions):
        for sf in sessions:
            try:
                content = sf.read_text(encoding="utf-8")
                m = re.search(r"\*\*Model\*\*:?\s*(.+)", content)
                if m:
                    return m.group(1).strip()
            except Exception:
                continue
        return None

    def _extract_date(self, sessions):
        for sf in sessions:
            try:
                content = sf.read_text(encoding="utf-8")
                m = re.search(r"\*\*Date\*\*:?\s*(\d{4}-\d{2}-\d{2})", content)
                if m:
                    return m.group(1)
            except Exception:
                continue
        return None

    def _extract_start_timestamp(self, sessions):
        if not sessions:
            return None
        return self._parse_timestamp_from_filename(sessions[0])

    def _extract_end_timestamp(self, sessions):
        if not sessions:
            return None
        return self._parse_timestamp_from_filename(sessions[-1])

    def _parse_timestamp_from_filename(self, path):
        m = re.search(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z", path.stem)
        if m:
            try:
                return datetime(
                    int(m.group(1)),
                    int(m.group(2)),
                    int(m.group(3)),
                    int(m.group(4)),
                    int(m.group(5)),
                    int(m.group(6)),
                )
            except ValueError:
                pass
        date_str = self._extract_date([path])
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                pass
        m = re.search(r"(\d{4})(\d{2})(\d{2})", path.stem)
        if m:
            try:
                return datetime(
                    int(m.group(1)),
                    int(m.group(2)),
                    int(m.group(3)),
                )
            except ValueError:
                pass
        return None

    def _calculate_minutes(self, start, end):
        if start and end:
            delta = end - start
            if isinstance(delta, timedelta):
                return int(delta.total_seconds() // 60)
        return None

    def _count_iterations(self, sessions):
        count = 0
        for sf in sessions:
            try:
                content = sf.read_text(encoding="utf-8")
                count += content.count("/speckit.specify")
                count += content.count("/speckit.implement")
            except Exception:
                continue
        return max(count, 1)

    def _calculate_complexity(self, sessions, iterations):
        num_sessions = len(sessions)
        has_bugs = False
        has_reviews = False
        for sf in sessions:
            try:
                content = sf.read_text(encoding="utf-8").lower()
                if "bug" in content or "fix" in content:
                    has_bugs = True
                if "review" in content:
                    has_reviews = True
            except Exception:
                continue
        if num_sessions <= 1 and iterations <= 2 and not has_bugs and not has_reviews:
            return 1
        if num_sessions <= 2 and iterations <= 4 and not has_bugs:
            return 2
        if num_sessions <= 4 and iterations <= 8 and not has_bugs:
            return 3
        if has_reviews and not has_bugs:
            return 5
        if has_bugs:
            return 8
        return 3

    def _write_csv(self, output_path, rows):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "feature",
                    "complexity",
                    "minutes",
                    "model",
                    "start_timestamp",
                    "end_timestamp",
                    "specs_quality",
                    "iterations",
                ]
            )
            for row in rows:
                writer.writerow(row)
