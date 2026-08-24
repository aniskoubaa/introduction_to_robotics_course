# 02 — Course Syllabus

**Status:** ✅ Drafted, following the **SE 446 Spring 2026** syllabus, which is the most recent
use of the AU student-centred template (approved Jan 2026). Section order, headings and policy
wording match it, so the two read as one department's documents.

> ⚠️ **Still provisional.** The specification (section 01) is pending Department Council
> approval, and the syllabus must not contradict approved CLOs, weights or topic order. If the
> Council changes anything, change it here too — the consistency list at the bottom says where.

| File | Description |
|---|---|
| `ee414-syllabus-fall2026.md` | The source. Edit **this**, then rebuild. |
| `ee414-syllabus-fall2026.docx` / `.pdf` | Generated. Do not hand-edit — the next rebuild overwrites them. |
| `_patch_docx.py` | Post-processing the build cannot do without. See below. |
| `template-au-syllabus-approved-jan2026.docx` / `.pdf` | Blank institutional form (approved Jan 2026). |

## Rebuilding

```bash
pandoc -f gfm -t docx --reference-doc="template-au-syllabus-approved-jan2026.docx" \
       -o ee414-syllabus-fall2026.docx ee414-syllabus-fall2026.md
python3 _patch_docx.py
soffice --headless --convert-to pdf --outdir . ee414-syllabus-fall2026.docx
```

**`_patch_docx.py` is not optional.** Pandoc's output does not render correctly inside the AU
template without it, and the failure is silent — you get a document that looks finished and is
not. It fixes three things:

| Problem | Effect if unpatched |
|---|---|
| Pandoc writes `<w:tblStyle w:val="Table"/>`, which the template does not define | Dangling style reference |
| Pandoc styles cell paragraphs `Compact`, and `--reference-doc` replaces `styles.xml` wholesale so that style disappears | **Every table renders empty**, with the cell text spilled into the body as loose paragraphs. Word tolerates it; LibreOffice does not |
| The template header carries `Course Code, Title` / `Department Name` / `College Name` / `Term and Year` | Placeholders printed on every page. `Course Code, Title` is split across two runs, so a plain search-and-replace misses it |

## Before issuing to students

The syllabus ends with a **"Notes for the instructors"** section listing what is unresolved.
**Delete that section before publishing**, once each line is settled:

- Class days, time, room · office locations, phones, office hours
- **Dr. Asem Ibrahim Alalwan's email**
- **The spelling of Dr. Alalwan's surname.** The superseded V2024 specification writes
  *Alalawan*; this syllabus and every slide deck write *Alalwan*. One of them is wrong.
- Week dates — derived from a Week 1 start of Sunday 23 August 2026, **not** checked against
  the academic calendar. Check whether Saudi National Day (23 September) displaces a Week 5
  session.
- Final exam date, once the Registrar sets it.

## Consistency with the specification

If any of these change in section 01, change them here:

- The four CLOs, verbatim, with their Bloom verbs.
- Assessment weights: participation 5, assignments 15, quizzes 5, MT1 15, MT2 15, project 20,
  final 25.
- The exam calendar: Midterm I Week 6, Midterm II Week 12, project demonstration Week 14, final
  in the examination week.
- Teams form Week 4; project proposal due Week 5.
- The pinned stack — named here and in `../setup/README.md`, and nowhere else.
