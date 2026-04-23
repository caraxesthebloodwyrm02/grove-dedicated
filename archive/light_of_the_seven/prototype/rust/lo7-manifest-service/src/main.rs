//! Lo7 document manifest (v1) — parity with Python `light_of_the_seven.lo7.build`.
use chrono::{Datelike, Duration, NaiveDate};
use clap::Parser;
use regex::Regex;
use serde_json::json;
use serde_json::Value;
use std::collections::{BTreeMap, HashSet};
use std::fs;
use std::io::{self, Write};
use std::path::Path;
use std::path::PathBuf;
use std::time::UNIX_EPOCH;
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(name = "lo7-manifest-service")]
struct Opt {
    #[arg(long, default_value = "lo7_corpus.test.yaml")]
    config: PathBuf,
    #[arg(long, default_value = "")]
    ref_date: String,
    #[arg(long, default_value = "-")]
    out: String,
}

fn main() -> Result<(), String> {
    let opt = Opt::parse();
    let text = fs::read_to_string(&opt.config).map_err(|e| e.to_string())?;
    let cfg: Value = serde_yaml::from_str(&text).map_err(|e| e.to_string())?;
    let root = PathBuf::from(
        cfg.get("root")
            .and_then(|x| x.as_str())
            .ok_or("missing root")?,
    );
    let week_starts_on = cfg
        .get("week_starts_on")
        .and_then(|x| x.as_str())
        .unwrap_or("monday");
    let empty_cell = cfg
        .get("empty_cell_level")
        .and_then(|x| x.as_i64())
        .unwrap_or(0) as i32;
    let allow: Vec<String> = cfg
        .get("allow")
        .and_then(|a| a.as_array())
        .map(|s| s.iter().filter_map(|v| v.as_str().map(String::from)).collect())
        .unwrap_or_default();
    let deny: Vec<String> = cfg
        .get("deny")
        .and_then(|a| a.as_array())
        .map(|s| s.iter().filter_map(|v| v.as_str().map(String::from)).collect())
        .unwrap_or_default();
    let refd = if opt.ref_date.is_empty() {
        None
    } else {
        Some(
            NaiveDate::parse_from_str(&opt.ref_date, "%Y-%m-%d")
                .map_err(|e| e.to_string())?,
        )
    };
    let manifest = build(
        &root,
        &allow,
        &deny,
        week_starts_on,
        empty_cell,
        refd,
    )?;
    let s = serde_json::to_string_pretty(&manifest).map_err(|e| e.to_string())?;
    if opt.out == "-" {
        io::stdout()
            .write_all(s.as_bytes())
            .map_err(|e| e.to_string())?;
    } else {
        fs::write(&opt.out, s).map_err(|e| e.to_string())?;
    }
    Ok(())
}

fn is_md(p: &Path) -> bool {
    p.extension()
        .and_then(|e| e.to_str())
        .map(|e| e == "md")
        .unwrap_or(false)
}

fn is_denied(rel: &str, deny: &[String]) -> bool {
    deny.iter().any(|p| match_one_deny(rel, p))
}

fn match_one_deny(rel: &str, pat: &str) -> bool {
    if pat.is_empty() {
        return false;
    }
    if pat == "*.md" {
        return !rel.contains('/') && rel.ends_with(".md");
    }
    if pat.ends_with("/**") {
        let pre = pat[..pat.len() - 3].trim_end_matches('/');
        if pre.is_empty() {
            return true;
        }
        return rel == pre || rel.starts_with(&(pre.to_string() + "/"));
    }
    false
}

/// Mirrors Python `paths._expand_pattern` for the patterns used in production + test.
fn expand_pattern(root: &Path, pattern: &str) -> Vec<PathBuf> {
    if pattern.is_empty() {
        return vec![];
    }
    if pattern == "*.md" {
        if let Ok(rd) = root.read_dir() {
            return rd
                .filter_map(|e| e.ok())
                .map(|e| e.path())
                .filter(|p| p.is_file() && is_md(p))
                .collect();
        }
        return vec![];
    }
    if pattern.ends_with("/**") {
        let pre = pattern[..pattern.len() - 3].trim_end_matches('/');
        if pre.is_empty() {
            return WalkDir::new(root)
                .into_iter()
                .filter_map(|e| e.ok())
                .map(|e| e.path().to_path_buf())
                .filter(|p| p.is_file() && is_md(p))
                .collect();
        }
        if pre.contains('*') && pre.ends_with('*') {
            let mut out = Vec::new();
            let Ok(rd) = std::fs::read_dir(root) else {
                return vec![];
            };
            for ent in rd.filter_map(|e| e.ok()) {
                let p = ent.path();
                if !p.is_dir() {
                    continue;
                }
                let name = p.file_name().and_then(|s| s.to_str()).unwrap_or("");
                if !glob_match(name, &pre) {
                    continue;
                }
                for w in WalkDir::new(&p) {
                    if let Ok(e) = w {
                        let f = e.path();
                        if f.is_file() && is_md(f) {
                            out.push(f.to_path_buf());
                        }
                    }
                }
            }
            return out;
        }
        let d = root.join(pre);
        if d.is_dir() {
            return WalkDir::new(&d)
                .into_iter()
                .filter_map(|e| e.ok())
                .map(|e| e.path().to_path_buf())
                .filter(|p| p.is_file() && is_md(p))
                .collect();
        }
    }
    if let Some((pre, g)) = pattern.split_once("/**/") {
        let d = root.join(pre);
        if d.is_dir() && g == "*.md" {
            return WalkDir::new(&d)
                .into_iter()
                .filter_map(|e| e.ok())
                .map(|e| e.path().to_path_buf())
                .filter(|p| p.is_file() && is_md(p))
                .collect();
        }
    }
    let p = root.join(pattern);
    if p.is_file() && is_md(&p) {
        return vec![p];
    }
    vec![]
}

fn glob_match(name: &str, pat: &str) -> bool {
    if !pat.contains('*') {
        return name == pat;
    }
    let re = pat.replace('*', ".*");
    Regex::new(&format!("^{re}$"))
        .map(|r| r.is_match(name))
        .unwrap_or(false)
}

fn collect_corpus_files(root: &Path, allow: &[String], deny: &[String]) -> Vec<PathBuf> {
    let mut set: HashSet<PathBuf> = HashSet::new();
    for p in allow {
        for f in expand_pattern(root, p) {
            if f.is_file() {
                set.insert(f);
            }
        }
    }
    let mut v: Vec<PathBuf> = set.into_iter().collect();
    v.sort();
    v.into_iter()
        .filter(|p| {
            let rel = p
                .strip_prefix(root)
                .ok()
                .and_then(|r| r.to_str())
                .map(String::from)
                .unwrap_or_default();
            !is_denied(&rel, deny)
        })
        .collect()
}

struct Scanned {
    path: String,
    mtime_unix: i64,
    title: String,
    h2: Vec<String>,
    day: String,
    source_date: Option<String>,
}

fn scan_file(
    root: &Path,
    p: &Path,
    h1: &Regex,
    h2: &Regex,
    fmb: &Regex,
    dline: &Regex,
) -> Scanned {
    let rel = p
        .strip_prefix(root)
        .expect("file under root")
        .as_os_str()
        .to_str()
        .expect("utf8 rel")
        .to_string();
    let meta = fs::metadata(p).expect("read meta");
    let mtime = meta
        .modified()
        .ok()
        .and_then(|t| t.duration_since(UNIX_EPOCH).ok())
        .map(|d| d.as_secs() as i64)
        .unwrap_or(0);
    let raw = fs::read_to_string(p).unwrap_or_default();
    let title = h1
        .captures(&raw)
        .and_then(|c| c.get(1).map(|m| m.as_str().trim().to_string()))
        .filter(|s| !s.is_empty())
        .or_else(|| p.file_stem().and_then(|s| s.to_str()).map(String::from))
        .unwrap_or_else(|| "doc".into());
    let h2s: Vec<String> = h2
        .captures_iter(&raw)
        .filter_map(|c| c.get(1).map(|m| m.as_str().trim().to_string()))
        .collect();
    let (source_date, day) = if let Some(c) = fmb.captures(&raw) {
        let block = c.get(1).map(|m| m.as_str()).unwrap_or("");
        if let Some(dt) = dline.captures(block) {
            let d = dt.get(1).unwrap().as_str().to_string();
            (Some(d.clone()), d)
        } else {
            let mday = mtime_to_day(mtime);
            (None, mday)
        }
    } else {
        let mut found: Option<String> = None;
        for ln in raw.lines() {
            if let Some(dt) = dline.captures(ln) {
                found = Some(dt.get(1).unwrap().as_str().to_string());
            }
        }
        if let Some(d) = found {
            (Some(d.clone()), d)
        } else {
            (None, mtime_to_day(mtime))
        }
    };
    Scanned {
        path: rel,
        mtime_unix: mtime,
        title,
        h2: h2s,
        day,
        source_date,
    }
}

fn mtime_to_day(mtime: i64) -> String {
    chrono::DateTime::from_timestamp(mtime, 0)
        .map(|d| d.naive_local().date().format("%Y-%m-%d").to_string())
        .unwrap_or_else(|| "1970-01-01".into())
}

fn batch_key(path: &str) -> (String, String) {
    if !path.contains('/') {
        return ("root".into(), String::new());
    }
    let p = path.find('/').unwrap();
    (path[..p].to_string(), path[..p].to_string())
}

fn day_weight_to_level(n: i32, empty: i32) -> i32 {
    if n <= 0 {
        if (0..=4).contains(&empty) {
            return empty;
        }
        return 0;
    }
    if n == 1 {
        return 1;
    }
    if n == 2 {
        return 2;
    }
    if (3..=4).contains(&n) {
        return 3;
    }
    4
}

fn dedupe_collapse(s: &str) -> String {
    let parts: Vec<&str> = s.split('/').collect();
    let mut o: Vec<&str> = vec![];
    for x in &parts {
        if o.is_empty() || o.last() != Some(x) {
            o.push(x);
        }
    }
    o.join("/")
}

fn start_of_week(d: NaiveDate, sunday: bool) -> NaiveDate {
    if !sunday {
        d - Duration::days(d.weekday().num_days_from_monday() as i64)
    } else {
        d - Duration::days(d.weekday().num_days_from_sunday() as i64)
    }
}

fn build(
    root: &Path,
    allow: &[String],
    deny: &[String],
    week_starts_on: &str,
    empty_cell: i32,
    reference_date: Option<NaiveDate>,
) -> Result<Value, String> {
    let h1 = Regex::new(r"(?m)^#\s+(.+?)\s*$").map_err(|e| e.to_string())?;
    let h2 = Regex::new(r"(?m)^##\s+(.+?)\s*$").map_err(|e| e.to_string())?;
    let fmb = Regex::new(r"^---\s*\r?\n(.*?)\r?\n---\s*").map_err(|e| e.to_string())?;
    let dline = Regex::new(r"(?m)^date:\s*(\d{4}-\d{2}-\d{2})\s*$")
        .map_err(|e| e.to_string())?;
    let files = collect_corpus_files(root, allow, deny);
    let mut scanned: Vec<Scanned> = files
        .iter()
        .map(|f| scan_file(root, f, &h1, &h2, &fmb, &dline))
        .collect();
    scanned.sort_by(|a, b| a.path.cmp(&b.path));
    let paths: Vec<String> = scanned.iter().map(|s| s.path.clone()).collect();
    let mut setp: HashSet<String> = HashSet::new();
    for p in &paths {
        setp.insert(dedupe_collapse(p));
    }
    let path_dedupe = setp.len() < paths.len();
    let mut bmap: BTreeMap<String, Vec<&Scanned>> = BTreeMap::new();
    for s in &scanned {
        let (id, _pr) = batch_key(&s.path);
        bmap.entry(id).or_default().push(s);
    }
    let mut domain_batches: Vec<Value> = vec![];
    for (id, items) in bmap {
        let bpre = items
            .first()
            .and_then(|f| f.path.find('/').map(|i| f.path[..i].to_string()))
            .unwrap_or_default();
        let files_j: Vec<Value> = items
            .iter()
            .map(|s| {
                json!({
                    "day": s.day,
                    "h2": s.h2,
                    "mtime_unix": s.mtime_unix,
                    "path": s.path,
                    "source_date": s.source_date,
                    "title": s.title,
                    "weight": 1.0
                })
            })
            .collect();
        domain_batches.push(json!({
            "id": id,
            "path_prefix": bpre,
            "files": files_j
        }));
    }
    let mut day_to: BTreeMap<String, Vec<&Scanned>> = BTreeMap::new();
    for s in &scanned {
        day_to.entry(s.day.clone()).or_default().push(s);
    }
    let mut day_map: BTreeMap<String, Value> = BTreeMap::new();
    for (dkey, sfs) in &day_to {
        let w = sfs.len() as f64;
        let n = sfs.len() as i32;
        let level = day_weight_to_level(n, empty_cell);
        let mut ps: Vec<String> = sfs.iter().map(|x| x.path.as_str().to_string()).collect();
        ps.sort();
        let mut titles: Vec<String> = vec![];
        for p in &ps {
            let t = sfs
                .iter()
                .find(|x| &x.path == p)
                .map(|x| x.title.clone())
                .unwrap_or_default();
            titles.push(t);
        }
        day_map.insert(
            dkey.clone(),
            json!({
                "level": level,
                "paths": ps,
                "titles": titles,
                "weight": w
            }),
        );
    }
    let refd: NaiveDate = if let Some(r) = reference_date {
        r
    } else {
        let max_f: Option<NaiveDate> = day_to
            .keys()
            .filter_map(|d| NaiveDate::parse_from_str(d, "%Y-%m-%d").ok())
            .max();
        let now = chrono::Local::now().date_naive();
        match max_f {
            None => now,
            Some(f) if f < now => now,
            Some(f) => f,
        }
    };
    let sunday = week_starts_on == "sunday";
    let end_week = start_of_week(refd, sunday);
    let start_week = end_week - Duration::weeks(51);
    let mut cell_levels: Vec<Vec<i32>> = (0..52).map(|_| vec![empty_cell; 7]).collect();
    let mut cell_dates: Vec<Vec<String>> = (0..52).map(|_| vec![String::new(); 7]).collect();
    for week_i in 0..52 {
        let wk = start_week + Duration::weeks(week_i as i64);
        for col in 0..7 {
            let d = wk + Duration::days(col as i64);
            let k = d.format("%Y-%m-%d").to_string();
            let level = day_map
                .get(&k)
                .and_then(|v| v.get("level").and_then(|l| l.as_i64().map(|x| x as i32)))
                .unwrap_or(empty_cell);
            let ccol = if sunday {
                d.weekday().num_days_from_sunday() as usize
            } else {
                d.weekday().num_days_from_monday() as usize
            };
            if ccol < 7 {
                cell_levels[week_i][ccol] = level.clamp(0, 4);
                cell_dates[week_i][ccol] = k;
            }
        }
    }
    let mut days_obj: serde_json::Map<String, Value> = serde_json::Map::new();
    for (k, v) in &day_map {
        days_obj.insert(k.clone(), v.clone());
    }
    let mut dates: Vec<String> = day_to.keys().cloned().collect();
    dates.sort();
    let dmin = dates
        .first()
        .cloned()
        .unwrap_or_else(|| refd.format("%Y-%m-%d").to_string());
    let dmax = dates
        .last()
        .cloned()
        .unwrap_or_else(|| refd.format("%Y-%m-%d").to_string());
    let manifest = json!({
        "body": {
            "date_max": dmax,
            "date_min": dmin,
            "file_count": scanned.len(),
            "path_dedupe_applied": path_dedupe
        },
        "domain_batches": domain_batches,
        "heatmap": {
            "cell_dates": cell_dates,
            "cell_levels": cell_levels,
            "columns": 7,
            "days": Value::Object(days_obj),
            "grid_start": start_week.format("%Y-%m-%d").to_string(),
            "rows": 52,
            "week_starts_on": week_starts_on
        },
        "meta": {
            "corpus_config_note": "see lo7_corpus.yaml",
            "day_bucket": "local_wall_calendar",
            "empty_cell_level": empty_cell,
            "level_thresholds": "0 files=empty_cell_level, 1=1, 2=2, 3-4=3, 5+=4 (BENCHMARK.md)",
            "mtime_only": true
        },
        "schema_version": "1",
        "type_name": "OctopusManifest"
    });
    Ok(manifest)
}
