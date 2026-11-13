# Halcyon kit v2

Feed carousels, singles, highlight covers and templates built on the Halcyon Design System v2
(https://claude.ai/artifact/DecqvQTqwhzGq8qp65G7V6). The design system is the source of truth: if this
kit and the design system disagree, fix the design system first. The old IG kit v3 (Inter, pink,
lavender, star dust) in HalcyonContentBrief is retired.

## Render

    python3 source/kit/render.py source/kit/sets/dyB.html media/ig/dyB

Each `<section class="slide">` becomes a 1080-wide JPG. `data-pg="2/6"` adds the standard footer,
`data-pg="end 6/6"` adds it without the arrow, `data-name` sets the file name. A 360 px phone contact
sheet is written to /tmp for the check. Needs Playwright plus Chrome or Chromium; Poppins installed
locally or loaded from Google Fonts.

## Sets

- `sets/dyB.html` Halcyon Dynamic in four cards (6 slides, replaces dyA).
- `sets/hl.html` highlight covers (hl_*.jpg, 1080 x 1920) and the hlSheet preview.
- `sets/md.html` market mood single. Edit only the MOOD block at the top on the day: kicker, headline,
  sub, rows (percent moves; `worst:true` on the row the story is about; `bar:false` for bps) and
  sources. Bars are drawn to scale automatically. `examples/mdCPI2.jpg` is the 10 Nov post rebuilt.

## Rules the kit bakes in

Feed grid (80 px margins, header y 136 to 420, hero y 440 to 1090, footer bottom y 1294), Poppins only,
cyan #00FBF4 as the one accent, grey plus a shape for anything down or wrong, nothing under 24 px, one
bordered panel per slide, the footer lockup on every slide, one real CTA pill on the end slide, and the
disclaimer at 26 px. Run the design system's pre-publish checklist on the rendered JPGs before a post is
marked Ready.
