# KDP Publishing Kit: Dogs Are Weird. We Love Them.

## Print setup (Paperback)

| Setting | Value |
|---|---|
| Trim size | 8.5 x 11 in |
| Bleed | **Yes** (interior PDF is 8.625 x 11.25 in) |
| Interior | **Premium color**. The art is photorealistic, so standard color would print it dull. |
| Paper | White |
| Cover finish | **Glossy**, which makes the colors pop for a gift book |
| Page count | 150 (even, all within KDP's 24–828 range) |
| Spine width | 0.3521 in (150 × 0.002347 in, premium color) |
| Full cover size | 17.6021 x 11.25 in |
| Files | `output/interior.pdf`, `output/cover.pdf` |

If you choose **standard color** instead, rebuild the cover with `python3 build/build_cover.py standard_color` so the spine width matches.

Margins: 0.75 in gutter (KDP's minimum for 151–300 pages is 0.5 in, and 0.375 in for 24–150 pages). Outside, top and bottom: 0.5 in inside trim. All text sits at least 0.375 in from the trim edge.

## Metadata

**Title:** Dogs Are Weird. We Love Them.
**Subtitle:** 100+ Hilarious Dog Breeds, Crazy Personalities, Adorable Portraits & Facts That Will Make You Laugh
**Author:** Tayeb Msalem
**Edition number:** leave blank (KDP's field takes a number only). "Christmas Gift Edition 2027" stays on the cover and title page; don't add it to the title or subtitle, or KDP may flag the listing.
**Language:** English
**Reading age:** 12 and up
**Primary audience:** no sexually explicit content; not a low-content book
**AI-generated content:** Yes, images (Canva Dream Lab and Bing Image Creator); text as written

Title and subtitle must match the cover word for word, which they do.

### Description (paste into KDP's HTML box)

```html
<p><b>Warning: This book contains extreme levels of dog.</b></p>
<p>Why does the Husky argue about <i>everything</i>? Why does the French Bulldog act like a tiny, grumpy CEO? Why does the Golden Retriever love absolutely everyone, including the vacuum?</p>
<p><b>Dogs Are Weird. We Love Them.</b> is the laugh-out-loud gift book for everyone who has ever been stared at by a dog while eating a sandwich. Inside you'll meet <b>103 real dog breeds</b>, each with a stunning full-color portrait, real facts and a hilarious personality profile.</p>
<ul>
<li><b>103 breed profiles:</b> origin and history, size, lifespan, grooming, exercise, trainability and one surprising fact</li>
<li><b>The funny stuff:</b> "If This Dog Were a Person," "Secret Superpower" and "What This Dog Would Say If It Could Talk"</li>
<li><b>8 ridiculous categories,</b> from The Drama Queens and The Tiny Bosses to The Professional Couch Potatoes and The Dogs Who Think They Own Everything</li>
<li><b>15 comedy chapters:</b> dog dating profiles, text messages from dogs, the Great Dog Breed Awards, zombie-apocalypse survival odds and 10 signs your dog is manipulating you</li>
<li><b>Christmas bonus section:</b> festive dog portraits, "Who Would Destroy the Tree First?", a Christmas personality quiz, holiday awards and heartwarming quotes</li>
<li><b>A personal gift page</b> and a <b>keepsake page</b> for your own wonderfully weird dog</li>
</ul>
<p>It's the perfect <b>Christmas gift, stocking stuffer or birthday present</b> for dog moms, dog dads, families, teens and anyone who has ever said "Who's a good boy?" to a dog that just ate a couch cushion.</p>
<p><b>Scroll up and grab a copy. Your dog would want you to.</b></p>
```

### 7 keyword slots (each under 50 characters)

1. funny dog gifts for dog lovers
2. dog breed book with pictures for adults
3. christmas gift for dog mom
4. gift for dog dad who has everything
5. funny coffee table book about dogs
6. white elephant gift for dog owners
7. stocking stuffer for adults and teens

### Categories (KDP lets you pick 3)

1. Humor > Topic > Animals
2. Pets > Dogs > Breeds
3. Humor > Form > Pictorial

Backup if one isn't offered: Pets > Dogs > General.

### Pricing guidance

At 150 premium-color pages, KDP's printing cost is roughly $9–$10 per copy in the U.S. (check the KDP calculator, since rates change). A **$24.99 list price** fits the premium gift-book market and earns about $5 royalty at 60%. $19.99 is the floor if you want room for promotions.

## Before you press Publish: checklist

- [x] All 125 illustrations generated, checked and placed in `images/` (see `image-prompts.md`), then rebuilt
- [x] Author (Tayeb Msalem) on the cover, spine and copyright page
- [x] KDP file preflight: sizes, margins, spine, barcode area, 300 dpi images, TrueType fonts, no placeholders
- [ ] ISBN: use KDP's free ISBN (KDP prints it in the barcode; the copyright page doesn't need it)
- [ ] AI-content disclosure answered **Yes** for images (required by KDP when AI generated the art)
- [ ] Download KDP's print previewer report and fix any flags
- [ ] Order one printed proof copy and check color, gutter and spine alignment
- [ ] Fact spot-check: breed stats are typical ranges from published breed standards; review anything you plan to quote in marketing
- [ ] Publish by **late September 2027** so the book has reviews and reach before the November–December gift rush
