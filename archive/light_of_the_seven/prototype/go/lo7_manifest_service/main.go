// Lo7 document manifest (v1) — parity with Python / Rust for test corpus.
package main

import (
	"encoding/json"
	"flag"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

type corpusCfg struct {
	Root             string   `yaml:"root"`
	WeekStartsOn     string   `yaml:"week_starts_on"`
	EmptyCellLevel   int      `yaml:"empty_cell_level"`
	Allow            []string `yaml:"allow"`
	Deny             []string `yaml:"deny"`
}

func main() {
	cfgPath := flag.String("config", "lo7_corpus.test.yaml", "")
	refDate := flag.String("ref-date", "", "")
	out := flag.String("out", "-", "")
	flag.Parse()
	raw, err := os.ReadFile(*cfgPath)
	if err != nil {
		panic(err)
	}
	var cfg corpusCfg
	if err := yaml.Unmarshal(raw, &cfg); err != nil {
		panic(err)
	}
	root, err := filepath.Abs(cfg.Root)
	if err != nil {
		panic(err)
	}
	var ref *time.Time
	if *refDate != "" {
		t, err := time.Parse("2006-01-02", *refDate)
		if err != nil {
			panic(err)
		}
		ref = &t
	}
	m, err := build(root, &cfg, ref)
	if err != nil {
		panic(err)
	}
	b, err := json.MarshalIndent(m, "", "  ")
	if err != nil {
		panic(err)
	}
	if *out == "-" {
		_, _ = os.Stdout.Write(append(b, '\n'))
	} else {
		_ = os.WriteFile(*out, append(b, '\n'), 0o644)
	}
}

func build(root string, cfg *corpusCfg, ref *time.Time) (map[string]any, error) {
	h1 := regexp.MustCompile(`(?m)^#\s+(.+?)\s*$`)
	h2 := regexp.MustCompile(`(?m)^##\s+(.+?)\s*$`)
	fmb := regexp.MustCompile(`(?s)^---\s*\r?\n(.*?)\r?\n---\s*`)
	dline := regexp.MustCompile(`(?m)^date:\s*(\d{4}-\d{2}-\d{2})\s*$`)

	files := collectCorpus(root, cfg)
	var scans []fileScan
	for _, f := range files {
		s, err := scanFile(root, f, h1, h2, fmb, dline)
		if err != nil {
			return nil, err
		}
		scans = append(scans, s)
	}
	sort.Slice(scans, func(i, j int) bool { return scans[i].Path < scans[j].Path })
	pathD := pathDedupFlag(scans)

	bmap := map[string][]fileScan{}
	for _, s := range scans {
		id, _ := batchKey(s.Path)
		bmap[id] = append(bmap[id], s)
	}
	ids := make([]string, 0, len(bmap))
	for k := range bmap {
		ids = append(ids, k)
	}
	sort.Strings(ids)
	domainBatches := make([]any, 0, len(ids))
	for _, id := range ids {
		items := bmap[id]
		sort.Slice(items, func(i, j int) bool { return items[i].Path < items[j].Path })
		bpre := ""
		if len(items) > 0 {
			if i := strings.Index(items[0].Path, "/"); i >= 0 {
				bpre = items[0].Path[:i]
			}
		}
		filesJ := make([]any, 0, len(items))
		for _, s := range items {
			var sd any
			if s.SourceDate == nil {
				sd = nil
			} else {
				sd = *s.SourceDate
			}
			filesJ = append(filesJ, map[string]any{
				"day": s.Day, "h2": s.H2, "mtime_unix": s.MtimeUnix, "path": s.Path,
				"source_date": sd, "title": s.Title, "weight": 1.0,
			})
		}
		domainBatches = append(domainBatches, map[string]any{
			"id": id, "path_prefix": bpre, "files": filesJ,
		})
	}
	dayTo := map[string][]fileScan{}
	for _, s := range scans {
		dayTo[s.Day] = append(dayTo[s.Day], s)
	}
	dayMap := map[string]map[string]any{}
	var dkeys []string
	for d := range dayTo {
		dkeys = append(dkeys, d)
	}
	sort.Strings(dkeys)
	for _, dkey := range dkeys {
		sfs := dayTo[dkey]
		w := float64(len(sfs))
		n := int(w)
		lvl := dayWeightToLevel(n, cfg.EmptyCellLevel)
		var ps []string
		seenP := map[string]bool{}
		for _, f := range sfs {
			if !seenP[f.Path] {
				seenP[f.Path] = true
				ps = append(ps, f.Path)
			}
		}
		sort.Strings(ps)
		var titles []string
		for _, p := range ps {
			var t string
			for _, x := range sfs {
				if x.Path == p {
					t = x.Title
					break
				}
			}
			titles = append(titles, t)
		}
		dayMap[dkey] = map[string]any{
			"level": lvl, "paths": ps, "titles": titles, "weight": w,
		}
	}
	refD := time.Now()
	if ref != nil {
		refD = *ref
	} else {
		var maxD time.Time
		for _, s := range scans {
			t, e := time.Parse("2006-01-02", s.Day)
			if e == nil {
				if t.After(maxD) {
					maxD = t
				}
			}
		}
		nowD := toDateLocal(time.Now())
		if !maxD.IsZero() {
			if toDateLocal(maxD).Before(nowD) {
				refD = time.Now()
			} else {
				refD = maxD
			}
		} else {
			refD = time.Now()
		}
	}
	sunday := cfg.WeekStartsOn == "sunday"
	endW := startOfWeek(refD, sunday)
	startW := endW.AddDate(0, 0, -7*51)
	cellLevels := make([][]int, 52)
	cellDates := make([][]string, 52)
	for w := 0; w < 52; w++ {
		row := make([]int, 7)
		ddd := make([]string, 7)
		for i := range row {
			row[i] = cfg.EmptyCellLevel
		}
		for i := range ddd {
			ddd[i] = ""
		}
		cellLevels[w] = row
		cellDates[w] = ddd
	}
	for weekI := 0; weekI < 52; weekI++ {
		wk := startW.AddDate(0, 0, weekI*7)
		for col := 0; col < 7; col++ {
			d := wk.AddDate(0, 0, col)
			k := d.Format("2006-01-02")
			var lvl int
			if v, ok := dayMap[k]; ok {
				lvl = int(v["level"].(int))
			} else {
				lvl = cfg.EmptyCellLevel
			}
			ccol := colFor(d, sunday)
			if ccol < 7 {
				if lvl < 0 {
					lvl = 0
				}
				if lvl > 4 {
					lvl = 4
				}
				cellLevels[weekI][ccol] = lvl
				cellDates[weekI][ccol] = k
			}
		}
	}
	daysObj := map[string]any{}
	for k, v := range dayMap {
		daysObj[k] = v
	}
	dmin, dmax := refD.Format("2006-01-02"), refD.Format("2006-01-02")
	if len(dkeys) > 0 {
		dmin, dmax = dkeys[0], dkeys[len(dkeys)-1]
	}
	return map[string]any{
		"body": map[string]any{
			"date_max": dmax, "date_min": dmin, "file_count": len(scans), "path_dedupe_applied": pathD,
		},
		"domain_batches": domainBatches,
		"heatmap": map[string]any{
			"cell_dates": cellDates, "cell_levels": cellLevels, "columns": 7, "days": daysObj,
			"grid_start": startW.Format("2006-01-02"), "rows": 52, "week_starts_on": cfg.WeekStartsOn,
		},
		"meta": map[string]any{
			"corpus_config_note": "see lo7_corpus.yaml", "day_bucket": "local_wall_calendar",
			"empty_cell_level": cfg.EmptyCellLevel,
			"level_thresholds":  "0 files=empty_cell_level, 1=1, 2=2, 3-4=3, 5+=4 (BENCHMARK.md)",
			"mtime_only":        true,
		},
		"schema_version": "1", "type_name": "OctopusManifest",
	}, nil
}

func toDateLocal(t time.Time) time.Time {
	loc := time.Local
	return time.Date(t.In(loc).Year(), t.In(loc).Month(), t.In(loc).Day(), 0, 0, 0, 0, loc)
}

func colFor(d time.Time, sunday bool) int {
	// Go: time.Weekday Sunday=0
	if sunday {
		return int(d.Weekday())
	}
	// Monday=0: convert
	w := int(d.Weekday())
	if w == 0 {
		return 6
	}
	return w - 1
}

func startOfWeek(d time.Time, sunday bool) time.Time {
	loc := d.Location()
	day := d.In(loc)
	if sunday {
		off := int(day.Weekday())
		return time.Date(day.Year(), day.Month(), day.Day(), 0, 0, 0, 0, loc).AddDate(0, 0, -off)
	}
	off := (int(day.Weekday()) + 6) % 7
	return time.Date(day.Year(), day.Month(), day.Day(), 0, 0, 0, 0, loc).AddDate(0, 0, -off)
}

func dayWeightToLevel(n, empty int) int {
	if n <= 0 {
		if empty >= 0 && empty <= 4 {
			return empty
		}
		return 0
	}
	if n == 1 {
		return 1
	}
	if n == 2 {
		return 2
	}
	if n == 3 || n == 4 {
		return 3
	}
	return 4
}

func pathDedupFlag(s []fileScan) bool {
	var paths []string
	for _, x := range s {
		paths = append(paths, x.Path)
	}
	set := map[string]bool{}
	byn := map[string]bool{}
	for _, p := range paths {
		set[p] = true
		c := dedupeC(p)
		byn[c] = true
	}
	return len(byn) < len(set) || false
}

func dedupeC(p string) string {
	parts := strings.Split(p, "/")
	var o []string
	for _, x := range parts {
		if len(o) == 0 || o[len(o)-1] != x {
			o = append(o, x)
		}
	}
	return strings.Join(o, "/")
}

func batchKey(p string) (string, string) {
	if !strings.Contains(p, "/") {
		return "root", ""
	}
	i := strings.Index(p, "/")
	return p[:i], p[:i]
}

type fileScan struct {
	Path       string
	MtimeUnix  int64
	Title      string
	H2         []string
	Day        string
	SourceDate *string
}

func scanFile(root, rel string, h1, h2, fmb, dline *regexp.Regexp) (fileScan, error) {
	full := filepath.Join(root, rel)
	b, err := os.ReadFile(full)
	if err != nil {
		return fileScan{}, err
	}
	st, err := os.Stat(full)
	if err != nil {
		return fileScan{}, err
	}
	mtime := st.ModTime()
	mu := mtime.Unix()
	raw := string(b)
	ttl := fileStem(full)
	if m := h1.FindStringSubmatch(raw); len(m) > 1 {
		ttl = strings.TrimSpace(m[1])
	}
	if ttl == "" {
		ttl = fileStem(full)
	}
	var h2s []string
	for _, sm := range h2.FindAllStringSubmatch(raw, -1) {
		if len(sm) > 1 {
			h2s = append(h2s, strings.TrimSpace(sm[1]))
		}
	}
	day := time.Unix(mu, 0).In(time.Local).Format("2006-01-02")
	var sdt *string
	if m := fmb.FindStringSubmatch(raw); len(m) > 1 {
		if dm := dline.FindStringSubmatch(m[1]); len(dm) > 1 {
			sdt = new(string)
			*sdt = dm[1]
			day = dm[1]
		}
	} else {
		for _, ln := range strings.Split(raw, "\n") {
			if dm := dline.FindStringSubmatch(ln); len(dm) > 1 {
				sdt = new(string)
				*sdt = dm[1]
				day = dm[1]
			}
		}
	}
	return fileScan{Path: filepath.ToSlash(rel), MtimeUnix: mu, Title: ttl, H2: h2s, Day: day, SourceDate: sdt}, nil
}

func fileStem(p string) string {
	b := filepath.Base(p)
	if i := strings.LastIndex(b, "."); i >= 0 {
		return b[:i]
	}
	return b
}

func collectCorpus(root string, cfg *corpusCfg) []string {
	set := map[string]bool{}
	for _, a := range cfg.Allow {
		for _, f := range expandPattern(root, a) {
			rel, _ := filepath.Rel(root, f)
			if isDenied(filepath.ToSlash(rel), cfg.Deny) {
				continue
			}
			set[filepath.ToSlash(rel)] = true
		}
	}
	var out []string
	for r := range set {
		out = append(out, r)
	}
	sort.Strings(out)
	return out
}

func isDenied(rel string, deny []string) bool {
	for _, p := range deny {
		if matchDeny(rel, p) {
			return true
		}
	}
	return false
}

func matchDeny(rel, pat string) bool {
	if pat == "" {
		return false
	}
	if pat == "*.md" {
		return !strings.Contains(rel, "/") && strings.HasSuffix(rel, ".md")
	}
	if strings.HasSuffix(pat, "/**") {
		pre := strings.TrimSuffix(pat, "/**")
		pre = strings.TrimRight(pre, "/")
		if pre == "" {
			return true
		}
		return rel == pre || strings.HasPrefix(rel, pre+"/")
	}
	return false
}

func expandPattern(root, pattern string) []string {
	if pattern == "" {
		return nil
	}
	if pattern == "*.md" {
		m, _ := filepath.Glob(filepath.Join(root, "*.md"))
		return m
	}
	if strings.HasSuffix(pattern, "/**") {
		pre := strings.TrimSuffix(pattern, "/**")
		pre = strings.TrimRight(pre, "/")
		if pre == "" {
			var out []string
			_ = filepath.WalkDir(root, func(p string, d os.DirEntry, e error) error {
				if e != nil {
					return e
				}
				if !d.IsDir() && strings.HasSuffix(strings.ToLower(p), ".md") {
					out = append(out, p)
				}
				return nil
			})
			return out
		}
		if strings.Contains(pre, "*") {
			// e.g. knowledge_*/
			var out []string
			_ = strings.TrimRight(pre, "*")
			ents, _ := os.ReadDir(root)
			for _, e := range ents {
				if !e.IsDir() {
					continue
				}
				if ok, _ := filepath.Match(pre, e.Name()); ok {
					_ = filepath.WalkDir(filepath.Join(root, e.Name()), func(p string, d os.DirEntry, e error) error {
						if e != nil {
							return e
						}
						if !d.IsDir() && strings.HasSuffix(strings.ToLower(p), ".md") {
							out = append(out, p)
						}
						return nil
					})
				}
			}
			return out
		}
		d := filepath.Join(root, pre)
		var out []string
		_ = filepath.WalkDir(d, func(p string, d os.DirEntry, e error) error {
			if e != nil {
				return e
			}
			if !d.IsDir() && strings.HasSuffix(strings.ToLower(p), ".md") {
				out = append(out, p)
			}
			return nil
		})
		return out
	}
	if strings.Contains(pattern, "/**/") {
		parts := strings.SplitN(pattern, "/**/", 2)
		if len(parts) == 2 {
			d := filepath.Join(root, parts[0])
			g := parts[1]
			if g == "*.md" {
				var out []string
				_ = filepath.WalkDir(d, func(p string, d os.DirEntry, e error) error {
					if e != nil {
						return e
					}
					if !d.IsDir() && strings.HasSuffix(strings.ToLower(p), ".md") {
						out = append(out, p)
					}
					return nil
				})
				return out
			}
		}
	}
	p := filepath.Join(root, pattern)
	if st, e := os.Stat(p); e == nil && !st.IsDir() && strings.HasSuffix(p, ".md") {
		return []string{p}
	}
	return nil
}
