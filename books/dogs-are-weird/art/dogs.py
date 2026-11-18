#!/usr/bin/env python3
"""Procedural cartoon dog illustration engine for DOGS ARE WEIRD. WE LOVE THEM.

Every breed is described by a small spec (coat colors, markings, ears, muzzle,
head shape, fur type, eye color, expression, accessory, scene). The engine turns
specs into layered SVG portraits; render.js rasterizes them to images/*.png.
"""
import math, random

OUT = "#2B1E16"   # outline ink
SW = 7            # outline width

# ---------- palette ----------
BLACK, WHITE, CREAM, GOLD, RED, FAWN = "#2F2A2C", "#FBF8F2", "#F2E4C8", "#DDA75A", "#C8723A", "#D9B27F"
TAN, LIVER, CHOC, GREY, BLUE, SILVER = "#C98A4B", "#7B4A2E", "#5A3826", "#8D9097", "#6F7F8E", "#BCC1C7"
APRICOT, SABLE, WHEAT, RUST, BRINDLE = "#E8B27A", "#B9783F", "#E3C48E", "#B5652E", "#7E5A3C"


def hx(c):
    c = c.lstrip("#"); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    A, B = hx(a), hx(b)
    return "#%02X%02X%02X" % tuple(round(A[i] + (B[i] - A[i]) * t) for i in range(3))


def light(c, t=.25): return mix(c, "#FFFFFF", t)
def dark(c, t=.25): return mix(c, "#000000", t)


# ---------- specs ----------
# coat, c2 (secondary/white), pattern, ear, muzzle(0-3), head, fur, eye, expr, acc, scene, flags
def S(coat, c2, pat, ear, mz, head, fur, eye, expr, acc, scene, flags=""):
    return dict(coat=coat, c2=c2, pat=pat, ear=ear, mz=mz, head=head, fur=fur, eye=eye, expr=expr, acc=acc, scene=scene, flags=flags)


SPECS = {
 # Drama Queens
 "Siberian Husky": S(GREY, WHITE, "husky", "prick", 2, "normal", "fluffy", "blue", "howl", "scarf", "snow"),
 "Pug": S(FAWN, BLACK, "mask", "fold", 0, "round", "smooth", "brown", "shocked", None, "spotlight", "wrinkles"),
 "Shih Tzu": S(CREAM, GOLD, "blaze", "silky", 0, "round", "silky", "brown", "smug", "bow", "sparkle"),
 "Basset Hound": S(TAN, WHITE, "tricolor", "long", 2, "normal", "smooth", "brown", "sad", None, "library", "jowls"),
 "Cavalier King Charles Spaniel": S(RUST, WHITE, "blaze", "longsilky", 1, "round", "smooth", "brown", "cute", None, "hearts"),
 "Maltese": S(WHITE, WHITE, "solid", "silky", 1, "round", "silky", "brown", "smug", "bow", "sparkle", "tongue"),
 "Afghan Hound": S(WHEAT, BLACK, "mask", "silky", 3, "long", "silky", "brown", "dramatic", "sunglasses", "sunset"),
 "Bichon Frise": S(WHITE, WHITE, "solid", "none", 1, "round", "puff", "brown", "happy", "partyhat", "confetti"),
 "Italian Greyhound": S(BLUE, WHITE, "blaze", "rose", 3, "long", "smooth", "brown", "sad", "sweater", "cozy"),
 "Papillon": S(WHITE, LIVER, "patches", "butterfly", 2, "normal", "smooth", "brown", "happy", None, "butterflies"),
 "Bloodhound": S(TAN, BLACK, "saddlecap", "long", 3, "normal", "smooth", "brown", "sad", "detective", "fog", "wrinkles jowls"),
 "Poodle": S(BLACK, BLACK, "solid", "poodle", 3, "long", "poodle", "brown", "smug", "pearls", "fashion"),
 # Tiny Bosses
 "Chihuahua": S(FAWN, WHITE, "solid", "bigprick", 1, "apple", "smooth", "brown", "grumpy", "sunglasses", "action"),
 "French Bulldog": S(FAWN, BLACK, "mask", "bat", 0, "broad", "smooth", "brown", "grumpy", "tie", "office", "wrinkles"),
 "Yorkshire Terrier": S(BLUE, TAN, "yorkie", "prick", 2, "round", "silky", "brown", "proud", "bow", "boutique"),
 "Dachshund": S(RED, RED, "solid", "floppy", 3, "long", "smooth", "brown", "proud", "cape", "sunset"),
 "Miniature Pinscher": S(BLACK, RUST, "tanpoints", "prick", 2, "normal", "smooth", "brown", "proud", "crown", "redcarpet"),
 "Jack Russell Terrier": S(WHITE, TAN, "patches", "fold", 2, "normal", "smooth", "brown", "happy", "tennis", "park", "tongue"),
 "Boston Terrier": S(BLACK, WHITE, "blaze", "bat", 0, "apple", "smooth", "brown", "happy", "bowtie", "party"),
 "Miniature Schnauzer": S(SILVER, "#E9E9EA", "schnauzer", "fold", 2, "normal", "wire", "brown", "grumpy", "glasses", "study"),
 "West Highland White Terrier": S(WHITE, WHITE, "solid", "prick", 2, "round", "fluffy", "brown", "proud", None, "hills"),
 "Cairn Terrier": S(WHEAT, GREY, "solid", "prick", 2, "normal", "wire", "brown", "happy", None, "yellowroad"),
 "Brussels Griffon": S(RUST, BLACK, "solid", "prick", 0, "apple", "wire", "brown", "grumpy", "newspaper", "cozy"),
 "Rat Terrier": S(WHITE, BLACK, "tripatches", "prick", 2, "normal", "smooth", "brown", "alert", None, "barn"),
 "Scottish Terrier": S(BLACK, BLACK, "solid", "prick", 3, "long", "wire", "brown", "grumpy", "tartan", "castle"),
 # Fluffy Legends
 "Samoyed": S(WHITE, WHITE, "solid", "prick", 2, "normal", "fluffy", "brown", "joy", None, "snow"),
 "Pomeranian": S(APRICOT, APRICOT, "solid", "small", 1, "round", "pom", "brown", "joy", "bow", "sparkle"),
 "Chow Chow": S(RED, RED, "solid", "small", 1, "broad", "pom", "brown", "smug", "crown", "palace", "bluetongue"),
 "Keeshond": S(GREY, BLACK, "spectacles", "prick", 2, "normal", "fluffy", "brown", "joy", None, "canal"),
 "Old English Sheepdog": S(GREY, WHITE, "oes", "none", 1, "broad", "shaggy", "brown", "happy", None, "meadow"),
 "Bearded Collie": S(GREY, WHITE, "blaze", "floppy", 2, "normal", "shaggy", "brown", "joy", None, "meadow"),
 "American Eskimo Dog": S(WHITE, WHITE, "solid", "prick", 2, "normal", "fluffy", "brown", "proud", "tophat", "circus"),
 "Alaskan Malamute": S(GREY, WHITE, "husky", "prick", 2, "broad", "fluffy", "brown", "happy", None, "snow"),
 "Shetland Sheepdog": S(SABLE, WHITE, "blaze", "tipped", 3, "long", "fluffy", "brown", "cute", None, "coast"),
 "Tibetan Mastiff": S(BLACK, RUST, "tanpoints", "floppy", 2, "broad", "lion", "brown", "grumpy", None, "mountain"),
 "Rough Collie": S(SABLE, WHITE, "blaze", "tipped", 3, "long", "fluffy", "brown", "proud", None, "sunset"),
 "Coton de Tulear": S(WHITE, WHITE, "solid", "silky", 1, "round", "puff", "brown", "joy", None, "tropical"),
 # Couch Potatoes
 "Bulldog": S(WHITE, BRINDLE, "patches", "rose", 0, "broad", "smooth", "brown", "sleepy", None, "couch", "wrinkles jowls"),
 "Greyhound": S(BRINDLE, WHITE, "blaze", "rose", 3, "long", "smooth", "brown", "sleepy", "blanket", "couch"),
 "Whippet": S(FAWN, WHITE, "blaze", "rose", 3, "long", "smooth", "brown", "sleepy", "blanket", "cozy"),
 "Chinese Shar-Pei": S(FAWN, FAWN, "solid", "small", 1, "broad", "smooth", "brown", "sleepy", None, "silk", "wrinkles heavy bluetongue"),
 "Bullmastiff": S(FAWN, BLACK, "mask", "floppy", 1, "broad", "smooth", "brown", "sleepy", None, "couch", "wrinkles jowls"),
 "Clumber Spaniel": S(WHITE, APRICOT, "patches", "floppy", 2, "broad", "smooth", "brown", "sad", "teacup", "cozy", "jowls"),
 "Havanese": S(CREAM, TAN, "solid", "silky", 1, "round", "silky", "brown", "joy", "flower", "tropical"),
 "Japanese Chin": S(WHITE, BLACK, "patches", "silky", 0, "round", "silky", "brown", "smug", None, "lanterns"),
 "American Cocker Spaniel": S(GOLD, GOLD, "solid", "longsilky", 2, "round", "smooth", "brown", "cute", None, "candle"),
 "Dogue de Bordeaux": S(RUST, RUST, "solid", "floppy", 1, "massive", "smooth", "amber", "sad", None, "farm", "wrinkles jowls"),
 "Pekingese": S(GOLD, BLACK, "mask", "silky", 0, "broad", "lion", "brown", "smug", "crown", "palace"),
 "Tibetan Spaniel": S(GOLD, BLACK, "mask", "longsilky", 1, "round", "smooth", "brown", "cute", None, "mountain"),
 # Athletic
 "Golden Retriever": S(GOLD, GOLD, "solid", "floppy", 2, "normal", "feathered", "brown", "clueless", "tennis", "autumn"),
 "Labrador Retriever": S(CHOC, CHOC, "solid", "floppy", 2, "broad", "smooth", "brown", "sad", None, "kitchen", "drool"),
 "German Shepherd": S(TAN, BLACK, "saddlecap", "bigprick", 3, "normal", "smooth", "brown", "alert", "badge", "cliff"),
 "Border Collie": S(BLACK, WHITE, "blaze", "tipped", 3, "normal", "smooth", "brown", "alert", "headset", "hills"),
 "Australian Shepherd": S(BLUE, WHITE, "merle", "tipped", 2, "normal", "fluffy", "hetero", "happy", "cowboy", "ranch"),
 "Belgian Malinois": S(FAWN, BLACK, "mask", "bigprick", 3, "normal", "smooth", "brown", "alert", "tactical", "action"),
 "Vizsla": S(RUST, RUST, "solid", "floppy", 3, "long", "smooth", "amber", "joy", None, "wheat"),
 "Weimaraner": S(SILVER, SILVER, "solid", "floppy", 3, "long", "smooth", "amber", "alert", None, "fog"),
 "German Shorthaired Pointer": S(LIVER, WHITE, "ticked", "floppy", 3, "long", "smooth", "brown", "alert", None, "meadow"),
 "Dalmatian": S(WHITE, BLACK, "spots", "floppy", 3, "normal", "smooth", "brown", "proud", "firehat", "city"),
 "Boxer": S(FAWN, BLACK, "boxer", "fold", 0, "broad", "smooth", "brown", "joy", None, "confetti", "wrinkles"),
 "Doberman Pinscher": S(BLACK, RUST, "tanpoints", "bigprick", 3, "long", "smooth", "brown", "proud", "tie", "office"),
 "Australian Cattle Dog": S(BLUE, WHITE, "heeler", "prick", 2, "normal", "smooth", "brown", "alert", None, "outback"),
 "Rhodesian Ridgeback": S(WHEAT, BLACK, "mask", "floppy", 2, "normal", "smooth", "amber", "proud", None, "savanna"),
 "English Springer Spaniel": S(WHITE, LIVER, "patches", "longsilky", 3, "normal", "smooth", "brown", "joy", None, "flowers"),
 "Brittany": S(WHITE, RED, "patches", "floppy", 2, "normal", "smooth", "amber", "happy", "medal", "meadow"),
 # Gentle Giants
 "Great Dane": S(WHITE, BLACK, "harlequin", "floppy", 3, "long", "smooth", "brown", "sad", None, "cozy", "jowls"),
 "Bernese Mountain Dog": S(BLACK, WHITE, "tricolor", "floppy", 2, "broad", "fluffy", "brown", "joy", None, "alps"),
 "Newfoundland": S(BLACK, BLACK, "solid", "floppy", 1, "massive", "fluffy", "brown", "happy", "lifering", "lake", "drool"),
 "Saint Bernard": S(RUST, WHITE, "stbernard", "floppy", 1, "massive", "smooth", "brown", "happy", "barrel", "snow", "jowls drool"),
 "Mastiff": S(FAWN, BLACK, "mask", "floppy", 1, "massive", "smooth", "brown", "sleepy", None, "castle", "wrinkles jowls"),
 "Irish Wolfhound": S(GREY, GREY, "solid", "rose", 3, "long", "wire", "brown", "cute", None, "fog"),
 "Leonberger": S(GOLD, BLACK, "mask", "floppy", 2, "broad", "lion", "brown", "happy", None, "forest"),
 "Great Pyrenees": S(WHITE, WHITE, "solid", "floppy", 2, "broad", "fluffy", "brown", "smug", None, "moon"),
 "Neapolitan Mastiff": S(BLUE, BLUE, "solid", "floppy", 1, "massive", "smooth", "amber", "sad", None, "villa", "wrinkles heavy jowls drool"),
 "Scottish Deerhound": S(GREY, GREY, "solid", "rose", 3, "long", "wire", "brown", "sleepy", None, "fog"),
 "Greater Swiss Mountain Dog": S(BLACK, WHITE, "tricolor", "floppy", 2, "broad", "smooth", "brown", "happy", None, "alps"),
 "Anatolian Shepherd": S(FAWN, BLACK, "mask", "floppy", 2, "broad", "smooth", "brown", "proud", None, "savanna"),
 # Weirdest
 "Puli": S(BLACK, BLACK, "solid", "none", 1, "round", "corded", "brown", "joy", None, "studio"),
 "Komondor": S(WHITE, WHITE, "solid", "none", 1, "broad", "corded", "brown", "smug", None, "meadow"),
 "Chinese Crested": S("#D7B9A8", WHITE, "spots", "bigprick", 2, "normal", "crested", "brown", "proud", "sunglasses", "concert", "tongue"),
 "Xoloitzcuintli": S("#5D5A5E", "#5D5A5E", "solid", "bigprick", 3, "normal", "hairless", "amber", "proud", "marigold", "dayofdead"),
 "Basenji": S(RED, WHITE, "blaze", "prick", 2, "normal", "smooth", "brown", "howl", None, "savanna", "brow"),
 "Bedlington Terrier": S("#C9CBD0", "#C9CBD0", "solid", "tassel", 3, "pear", "lamb", "brown", "cute", None, "meadow"),
 "Borzoi": S(WHITE, GOLD, "patches", "rose", 3, "narrow", "silky", "brown", "dramatic", None, "palace"),
 "Bull Terrier": S(WHITE, WHITE, "solid", "prick", 3, "egg", "smooth", "brown", "smug", "partyhat", "confetti"),
 "Norwegian Lundehund": S(FAWN, WHITE, "blaze", "prick", 2, "normal", "smooth", "brown", "happy", None, "cliffsea"),
 "Catahoula Leopard Dog": S(BLUE, BLACK, "merle", "floppy", 2, "normal", "smooth", "blue", "alert", None, "bayou"),
 "Affenpinscher": S(BLACK, BLACK, "solid", "prick", 0, "apple", "wire", "brown", "grumpy", "fedora", "noir"),
 "Portuguese Water Dog": S(BLACK, WHITE, "solid", "floppy", 2, "broad", "curly", "brown", "joy", None, "sea"),
 "Dandie Dinmont Terrier": S(SILVER, WHITE, "solid", "floppy", 2, "round", "topknot", "brown", "smug", "roundglasses", "library"),
 # Own Everything
 "Pembroke Welsh Corgi": S(RED, WHITE, "blaze", "bigprick", 2, "normal", "smooth", "brown", "smug", "crown", "palace"),
 "Shiba Inu": S(RED, CREAM, "urajiro", "prick", 2, "normal", "smooth", "brown", "sideeye", None, "blossom"),
 "Beagle": S(TAN, WHITE, "tricolor", "floppy", 2, "normal", "smooth", "brown", "happy", None, "picnic"),
 "Rottweiler": S(BLACK, RUST, "tanpoints", "fold", 2, "broad", "smooth", "brown", "cute", "teddy", "porch"),
 "Akita": S(RED, WHITE, "urajiro", "prick", 2, "broad", "fluffy", "brown", "proud", None, "blossom"),
 "Cane Corso": S(BLACK, BLACK, "solid", "floppy", 1, "massive", "smooth", "amber", "proud", "chain", "villa", "jowls"),
 "American Staffordshire Terrier": S(BLUE, WHITE, "blaze", "rose", 2, "broad", "smooth", "amber", "joy", "flowers", "garden"),
 "Airedale Terrier": S(TAN, BLACK, "saddlecap", "fold", 3, "long", "wire", "brown", "proud", "crown", "castle"),
 "Saluki": S(CREAM, CREAM, "solid", "longsilky", 3, "narrow", "smooth", "brown", "dramatic", None, "desert"),
 "Lhasa Apso": S(GOLD, BLACK, "solid", "silky", 1, "round", "silky", "brown", "smug", None, "temple"),
 "Black and Tan Coonhound": S(BLACK, RUST, "tanpoints", "long", 3, "normal", "smooth", "brown", "howl", None, "moon", "jowls"),
 "Standard Schnauzer": S(SILVER, "#E9E9EA", "schnauzer", "fold", 3, "long", "wire", "brown", "grumpy", "pen", "office"),
 "Cardigan Welsh Corgi": S(BLUE, WHITE, "merle", "bigprick", 2, "normal", "smooth", "hetero", "proud", "crown", "castle"),
}

HEADS = {  # rx, ry
    "normal": (215, 205), "round": (232, 212), "apple": (238, 220), "broad": (255, 210), "massive": (268, 222),
    "long": (182, 228), "narrow": (150, 240), "egg": (170, 250), "pear": (165, 245),
}

# ---------- scenes ----------
SCENES = {
 "snow": ("#CFE4F2", "#6E9CC2", "snow"), "spotlight": ("#F7D6E0", "#B23A5E", "spot"), "sparkle": ("#FBE3EE", "#D67FA5", "sparkle"),
 "library": ("#E9D2B0", "#7A5232", "books"), "hearts": ("#FBE0E4", "#C9566C", "hearts"), "sunset": ("#FBD8A6", "#C9603F", "sun"),
 "confetti": ("#FFF1C9", "#E0A33A", "confetti"), "cozy": ("#F2DCC0", "#9C6B45", "window"), "butterflies": ("#E2F2DD", "#6AA35F", "butterflies"),
 "fog": ("#DDE2E3", "#6F7E80", "fog"), "fashion": ("#EDEDED", "#3A3A3A", "checker"), "action": ("#F6C88B", "#B5462B", "rays"),
 "office": ("#DDE7F0", "#4F6E8F", "skyline"), "boutique": ("#F8DCE6", "#A4597A", "sparkle"), "redcarpet": ("#F7CFC9", "#9E1B1B", "spot"),
 "park": ("#D9F0C7", "#5E9E3D", "trees"), "party": ("#E6DDF7", "#6A4BB0", "confetti"), "study": ("#EAD9C1", "#6B4B30", "books"),
 "hills": ("#E1F0D6", "#5D8A4A", "hills"), "yellowroad": ("#E9F3D2", "#6F9A3C", "road"), "barn": ("#F6DDB2", "#A55A2C", "barn"),
 "castle": ("#DCE3E8", "#56697A", "castle"), "canal": ("#DDEFF6", "#3E7FA6", "tulips"), "meadow": ("#E5F3D3", "#6AA048", "hills"),
 "circus": ("#FBE3C8", "#C23B3B", "stripes"), "coast": ("#DCEEF3", "#4B8BA6", "sea"), "mountain": ("#E2E8F0", "#5F7387", "peaks"),
 "tropical": ("#E6F6DE", "#3D9C69", "palms"), "couch": ("#F1E0D0", "#8F5E44", "couch"), "silk": ("#F6DFC8", "#B04A3A", "lanterns"),
 "candle": ("#F5DEC4", "#8E3B2B", "bokeh"), "farm": ("#F2E2C4", "#9A6A3A", "barn"), "palace": ("#F6E7C1", "#A4361F", "palace"),
 "autumn": ("#FBE3BF", "#C77A2A", "leaves"), "kitchen": ("#F4E8D6", "#A3734A", "window"), "cliff": ("#D9E4EE", "#4D637A", "peaks"),
 "ranch": ("#F7DFB8", "#B0652D", "fence"), "wheat": ("#FAEBC2", "#C49A3A", "wheat"), "city": ("#E3E7EC", "#B3261E", "skyline"),
 "outback": ("#F8D8B0", "#B5532B", "sun"), "savanna": ("#F9DFAE", "#C47A2E", "acacia"), "flowers": ("#EEF6DE", "#78A84A", "flowers"),
 "alps": ("#E3EEF7", "#4E7A9E", "peaks"), "lake": ("#D6ECF6", "#2F7FAE", "sea"), "forest": ("#E2EFD8", "#4F7F3D", "trees"),
 "moon": ("#2E3A5C", "#141B33", "moon"), "villa": ("#F7DFC2", "#B66A3A", "columns"), "studio": ("#F3E6F7", "#8C5BB0", "rays"),
 "concert": ("#3B2A5C", "#160F2B", "neon"), "dayofdead": ("#FBE0C2", "#C2447A", "papel"), "cliffsea": ("#D9EBF3", "#3F6F8E", "sea"),
 "bayou": ("#E7E6C8", "#5E6B3A", "moss"), "noir": ("#5C5C66", "#22222A", "blinds"), "sea": ("#D7EEF7", "#2E86B5", "sea"),
 "blossom": ("#FCE4EC", "#C2577E", "blossom"), "picnic": ("#E6F4D6", "#5F9C3E", "picnic"), "porch": ("#F6E1C4", "#9A5F35", "window"),
 "garden": ("#EEF7DE", "#6BA04A", "flowers"), "desert": ("#FBE2B4", "#C9853A", "dunes"), "temple": ("#F6DCC4", "#A3342A", "lanterns"),
 "lanterns": ("#F8E0C8", "#B03A2E", "lanterns"),
 "xmas": ("#2D6A4C", "#0E2A1D", "xmas"),
}


def r_(seed):
    return random.Random(seed)


def scene_svg(scene, W, H, seed):
    lo, hi, kind = SCENES.get(scene, SCENES["studio"])
    R = r_(seed)
    s = [f'<defs><radialGradient id="bg{seed}" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="{light(lo, .35)}"/>'
         f'<stop offset=".55" stop-color="{lo}"/><stop offset="1" stop-color="{mix(lo, hi, .55)}"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#bg{seed})"/>']
    a = lambda o: f'fill-opacity="{o}"'
    if kind in ("snow", "xmas"):
        for _ in range(int(W * H / 9000)):
            x, y, rr = R.uniform(0, W), R.uniform(0, H), R.uniform(3, 10)
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="#fff" {a(R.uniform(.35, .9))}/>')
        if kind == "xmas":
            for i in range(9):
                x = W * (i + .5) / 9 + R.uniform(-20, 20); y = R.uniform(40, 140)
                col = R.choice(["#E8C766", "#D93A2E", "#F2F2F2", "#5FB37A"])
                s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="{col}" fill-opacity=".85"/><circle cx="{x-5:.0f}" cy="{y-5:.0f}" r="5" fill="#fff" fill-opacity=".6"/>')
            s.append(f'<path d="M0 {H*0.1} Q {W/4} {H*0.16} {W/2} {H*0.1} T {W} {H*0.1}" stroke="#2C4A30" stroke-width="5" fill="none"/>')
    elif kind == "spot":
        s.append(f'<ellipse cx="{W/2}" cy="{H*0.45}" rx="{W*0.42}" ry="{H*0.5}" fill="#fff" {a(.35)}/>')
    elif kind == "sparkle":
        for _ in range(26):
            x, y, k = R.uniform(0, W), R.uniform(0, H * .7), R.uniform(10, 26)
            s.append(f'<path d="M{x} {y-k} Q{x} {y} {x+k} {y} Q{x} {y} {x} {y+k} Q{x} {y} {x-k} {y} Q{x} {y} {x} {y-k}Z" fill="#fff" {a(.85)}/>')
    elif kind == "hearts":
        for _ in range(16):
            x, y, k = R.uniform(0, W), R.uniform(0, H * .75), R.uniform(16, 36)
            s.append(f'<path transform="translate({x:.0f},{y:.0f}) scale({k/30:.2f})" d="M0 10 C -25 -12 -12 -32 0 -16 C 12 -32 25 -12 0 10Z" fill="#E66B83" {a(.55)}/>')
    elif kind in ("sun", "rays"):
        cx, cy = W / 2, H * .42
        for i in range(18):
            t1, t2 = i * math.pi / 9, i * math.pi / 9 + .09
            s.append(f'<path d="M{cx} {cy} L{cx+2000*math.cos(t1):.0f} {cy+2000*math.sin(t1):.0f} L{cx+2000*math.cos(t2+.08):.0f} {cy+2000*math.sin(t2+.08):.0f}Z" fill="#fff" {a(.13)}/>')
        if kind == "sun":
            s.append(f'<circle cx="{W*0.78}" cy="{H*0.22}" r="{W*0.09}" fill="#FFE7A3" {a(.9)}/>')
    elif kind == "confetti":
        for _ in range(70):
            x, y = R.uniform(0, W), R.uniform(0, H * .8)
            col = R.choice(["#E84A5F", "#2A9D8F", "#F4A261", "#6A4BB0", "#3A86FF", "#FFBE0B"])
            s.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{R.uniform(10,20):.0f}" height="{R.uniform(6,10):.0f}" rx="3" transform="rotate({R.uniform(0,180):.0f} {x:.0f} {y:.0f})" fill="{col}" {a(.85)}/>')
    elif kind in ("books", "window", "couch", "blinds"):
        if kind == "books":
            for row in range(3):
                y = 60 + row * 190; x = 10
                while x < W:
                    w = R.uniform(28, 50); h = R.uniform(120, 165)
                    col = R.choice(["#8E3B2B", "#2F5E4E", "#C08A2D", "#3E4F7A", "#6B4B30", "#A5603D"])
                    s.append(f'<rect x="{x:.0f}" y="{y+165-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{col}" fill-opacity=".45"/>')
                    x += w + 4
                s.append(f'<rect x="0" y="{y+165}" width="{W}" height="16" fill="{hi}" fill-opacity=".35"/>')
        elif kind == "window":
            s.append(f'<rect x="{W*0.62}" y="{H*0.06}" width="{W*0.3}" height="{H*0.38}" rx="12" fill="#FFF6E0" {a(.75)} stroke="{hi}" stroke-opacity=".4" stroke-width="10"/>'
                     f'<path d="M{W*0.77} {H*0.06} V{H*0.44} M{W*0.62} {H*0.25} H{W*0.92}" stroke="{hi}" stroke-opacity=".4" stroke-width="8"/>')
        elif kind == "couch":
            s.append(f'<rect x="-40" y="{H*0.55}" width="{W+80}" height="{H*0.5}" rx="70" fill="{hi}" {a(.55)}/>'
                     f'<rect x="-40" y="{H*0.42}" width="{W+80}" height="{H*0.2}" rx="60" fill="{hi}" {a(.4)}/>')
        else:
            for i in range(10):
                s.append(f'<rect x="0" y="{i*H/10:.0f}" width="{W}" height="{H/22:.0f}" fill="#fff" {a(.08)} transform="skewY(-8)"/>')
    elif kind in ("hills", "meadow", "road", "wheat", "flowers", "picnic"):
        s.append(f'<path d="M0 {H*0.62} Q {W*0.3} {H*0.5} {W*0.6} {H*0.6} T {W} {H*0.58} V{H} H0Z" fill="{hi}" {a(.35)}/>'
                 f'<path d="M0 {H*0.72} Q {W*0.4} {H*0.62} {W} {H*0.72} V{H} H0Z" fill="{hi}" {a(.45)}/>')
        if kind == "road":
            s.append(f'<path d="M{W*0.45} {H} L{W*0.52} {H*0.62} L{W*0.56} {H*0.62} L{W*0.7} {H}Z" fill="#F2D54A" {a(.9)}/>')
        if kind in ("flowers", "picnic", "meadow"):
            for _ in range(24):
                x, y = R.uniform(0, W), R.uniform(H * .66, H)
                col = R.choice(["#F28CA5", "#FFD166", "#FFFFFF", "#C77DFF"])
                s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{col}"/><circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="#E09F3E"/>')
        if kind == "wheat":
            for _ in range(40):
                x = R.uniform(0, W); y = R.uniform(H * .6, H)
                s.append(f'<path d="M{x:.0f} {y:.0f} q 4 -40 0 -70" stroke="#C49A3A" stroke-width="5" fill="none" stroke-opacity=".7"/>')
    elif kind in ("peaks", "castle", "acacia", "dunes", "columns", "palace", "skyline", "trees", "barn", "fence", "palms", "sea", "tulips", "moss"):
        if kind == "peaks":
            s.append(f'<path d="M0 {H*0.6} L{W*0.22} {H*0.25} L{W*0.4} {H*0.5} L{W*0.62} {H*0.18} L{W*0.85} {H*0.48} L{W} {H*0.35} V{H} H0Z" fill="{hi}" {a(.35)}/>'
                     f'<path d="M{W*0.62} {H*0.18} L{W*0.56} {H*0.27} L{W*0.6} {H*0.25} L{W*0.64} {H*0.29} L{W*0.68} {H*0.26}Z" fill="#fff" {a(.9)}/>')
        elif kind == "castle":
            x0 = W * .58
            s.append(f'<path d="M{x0} {H*0.6} V{H*0.2} h40 v-30 h30 v30 h30 v-30 h30 v30 h40 V{H*0.6}Z" fill="{hi}" {a(.3)}/>')
        elif kind == "acacia":
            s.append(f'<circle cx="{W*0.8}" cy="{H*0.22}" r="{W*0.08}" fill="#FFE7A3" {a(.9)}/>'
                     f'<path d="M{W*0.18} {H*0.62} V{H*0.4}" stroke="{hi}" stroke-opacity=".5" stroke-width="16"/><ellipse cx="{W*0.18}" cy="{H*0.37}" rx="{W*0.16}" ry="{H*0.05}" fill="{hi}" {a(.45)}/>'
                     f'<rect x="0" y="{H*0.62}" width="{W}" height="{H}" fill="{hi}" {a(.25)}/>')
        elif kind == "dunes":
            s.append(f'<path d="M0 {H*0.65} Q {W*0.3} {H*0.45} {W*0.6} {H*0.62} T {W} {H*0.55} V{H} H0Z" fill="{hi}" {a(.35)}/>'
                     f'<path d="M{W*0.68} {H*0.56} L{W*0.8} {H*0.34} L{W*0.92} {H*0.56}Z" fill="{hi}" {a(.4)}/>')
        elif kind in ("columns", "palace"):
            for i in range(5):
                x = W * (.06 + i * .22)
                s.append(f'<rect x="{x:.0f}" y="{H*0.1}" width="{W*0.06:.0f}" height="{H*0.6}" fill="#fff" {a(.35)}/>')
            if kind == "palace":
                s.append(f'<rect x="0" y="{H*0.7}" width="{W}" height="{H*0.3}" fill="#8E1B1B" {a(.25)}/>')
        elif kind == "skyline":
            x = 0
            while x < W:
                w = R.uniform(60, 120); h = R.uniform(H * .2, H * .45)
                s.append(f'<rect x="{x:.0f}" y="{H*0.65-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{hi}" {a(.28)}/>'); x += w + 8
        elif kind in ("trees", "palms"):
            for i in range(6):
                x = R.uniform(0, W); y = H * R.uniform(.35, .55); k = R.uniform(60, 110)
                s.append(f'<path d="M{x:.0f} {y-k:.0f} L{x+k*0.6:.0f} {y+k*0.6:.0f} L{x-k*0.6:.0f} {y+k*0.6:.0f}Z" fill="{hi}" {a(.3)}/>' if kind == "trees" else
                         f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{k:.0f}" ry="{k*0.35:.0f}" fill="{hi}" {a(.3)}/>')
        elif kind == "barn":
            s.append(f'<path d="M{W*0.6} {H*0.6} V{H*0.3} L{W*0.75} {H*0.15} L{W*0.9} {H*0.3} V{H*0.6}Z" fill="#B5462B" {a(.35)}/>'
                     f'<rect x="0" y="{H*0.6}" width="{W}" height="{H}" fill="#E5B85C" {a(.35)}/>')
        elif kind == "fence":
            for i in range(14):
                s.append(f'<rect x="{i*W/13:.0f}" y="{H*0.48}" width="18" height="{H*0.2}" fill="{hi}" {a(.35)}/>')
            s.append(f'<rect x="0" y="{H*0.52}" width="{W}" height="14" fill="{hi}" {a(.35)}/><rect x="0" y="{H*0.6}" width="{W}" height="14" fill="{hi}" {a(.35)}/>')
        elif kind in ("sea", "moss"):
            for i in range(5):
                y = H * (.55 + i * .08)
                s.append(f'<path d="M0 {y:.0f} Q {W*0.25} {y-25:.0f} {W*0.5} {y:.0f} T {W} {y:.0f} V{H} H0Z" fill="{hi}" {a(.12)}/>')
        elif kind == "tulips":
            for _ in range(20):
                x, y = R.uniform(0, W), R.uniform(H * .7, H)
                col = R.choice(["#E84A5F", "#FFBE0B", "#F28CA5"])
                s.append(f'<path d="M{x:.0f} {y:.0f} q -14 -20 0 -36 q 14 16 0 36Z" fill="{col}"/>')
    elif kind in ("stripes",):
        for i in range(12):
            s.append(f'<path d="M{W/2} {-H*0.2} L{i*W/11-60:.0f} {H} L{i*W/11:.0f} {H}Z" fill="#fff" {a(.18 if i % 2 else 0)}/>')
    elif kind in ("lanterns", "bokeh", "neon", "papel", "blossom", "leaves", "butterflies", "moon", "fog", "checker"):
        if kind == "lanterns":
            for i in range(5):
                x = W * (i + .5) / 5; y = R.uniform(70, 160)
                s.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="40" ry="52" fill="#E63A2E" {a(.55)}/><rect x="{x-14:.0f}" y="{y-60:.0f}" width="28" height="10" fill="#C9A227" {a(.6)}/>')
        elif kind in ("bokeh", "neon"):
            for _ in range(22):
                col = R.choice(["#FFD38A", "#FFFFFF", "#F7A072"] if kind == "bokeh" else ["#FF4FD8", "#3AF2FF", "#B14CFF"])
                s.append(f'<circle cx="{R.uniform(0,W):.0f}" cy="{R.uniform(0,H*0.7):.0f}" r="{R.uniform(18,50):.0f}" fill="{col}" {a(R.uniform(.15,.4))}/>')
        elif kind == "papel":
            for i in range(8):
                col = ["#E84A5F", "#FFBE0B", "#2A9D8F", "#C77DFF"][i % 4]
                x = i * W / 8
                s.append(f'<path d="M{x:.0f} 40 H{x+W/8:.0f} V150 L{x+W/16:.0f} 185 L{x:.0f} 150Z" fill="{col}" {a(.75)}/>')
        elif kind in ("blossom", "leaves", "butterflies"):
            for _ in range(30):
                x, y = R.uniform(0, W), R.uniform(0, H)
                if kind == "blossom":
                    s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R.uniform(6,12):.0f}" fill="#F8BBD0" {a(.85)}/>')
                elif kind == "leaves":
                    col = R.choice(["#E07A2E", "#D4A12A", "#B5462B"])
                    s.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="16" ry="8" transform="rotate({R.uniform(0,180):.0f} {x:.0f} {y:.0f})" fill="{col}" {a(.8)}/>')
                else:
                    col = R.choice(["#FFB703", "#8ECAE6", "#F28CA5"])
                    s.append(f'<g transform="translate({x:.0f},{y:.0f})" fill="{col}" fill-opacity=".8"><ellipse cx="-9" cy="0" rx="10" ry="14"/><ellipse cx="9" cy="0" rx="10" ry="14"/></g>')
        elif kind == "moon":
            s.append(f'<circle cx="{W*0.78}" cy="{H*0.2}" r="{W*0.1}" fill="#FFF3C4"/>')
            for _ in range(40):
                s.append(f'<circle cx="{R.uniform(0,W):.0f}" cy="{R.uniform(0,H*0.6):.0f}" r="{R.uniform(1.5,4):.1f}" fill="#fff" {a(.8)}/>')
        elif kind == "fog":
            for _ in range(8):
                s.append(f'<ellipse cx="{R.uniform(0,W):.0f}" cy="{R.uniform(H*0.3,H):.0f}" rx="{R.uniform(180,360):.0f}" ry="60" fill="#fff" {a(.35)}/>')
        elif kind == "checker":
            sq = 90
            for i in range(0, W // sq + 1):
                for j in range(int(H * .62) // sq, H // sq + 1):
                    if (i + j) % 2:
                        s.append(f'<rect x="{i*sq}" y="{j*sq}" width="{sq}" height="{sq}" fill="#000" {a(.18)}/>')
    s.append(f'<ellipse cx="{W/2}" cy="{H-10}" rx="{W*0.45}" ry="{H*0.06}" fill="#000" {a(.12)}/>')
    return "".join(s)


# ---------- dog drawing (head-and-shoulders, centered at 500,430 in a 1000x1000 frame) ----------
def ell(cx, cy, rx, ry, fill, stroke=True, extra=""):
    st = f' stroke="{OUT}" stroke-width="{SW}"' if stroke else ""
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}"{st} {extra}/>'


def path(d, fill, stroke=True, extra=""):
    st = f' stroke="{OUT}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{st} {extra}/>'


def scallop(cx, cy, rx, ry, n, bump, fill, stroke=True, start=0, end=2 * math.pi, close=True):
    pts = []
    for i in range(n + 1):
        t = start + (end - start) * i / n
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        nx, ny = mx - cx, my - cy
        L = math.hypot(nx, ny) or 1
        d += f" Q{mx + nx / L * bump:.1f} {my + ny / L * bump:.1f} {x1:.1f} {y1:.1f}"
    if close:
        d += "Z"
    return path(d, fill, stroke)


def mirror(svg):
    return f'<g transform="translate(1000,0) scale(-1,1)">{svg}</g>'


def dog_svg(spec, seed=0, acc_override=None, expr_override=None):
    R = r_(seed)
    coat, c2, pat = spec["coat"], spec["c2"], spec["pat"]
    expr = expr_override or spec["expr"]
    acc = acc_override if acc_override is not None else spec["acc"]
    accs = acc if isinstance(acc, (list, tuple)) else [acc]
    flags = spec["flags"].split()
    rx, ry = HEADS[spec["head"]]
    HX, HY = 500, 440
    fur = spec["fur"]
    tilt = {"howl": -12, "dramatic": 8, "clueless": -8, "cute": -6, "sideeye": 0, "smug": 4}.get(expr, 0)
    out = []

    white_muzzle = pat in ("blaze", "tricolor", "husky", "patches", "urajiro", "stbernard", "oes", "heeler", "tripatches", "boxer")
    muz_col = {"mask": dark(coat, .55) if coat != BLACK else BLACK, "saddlecap": BLACK, "schnauzer": c2, "spectacles": light(coat, .35),
               "yorkie": TAN, "tanpoints": c2, "urajiro": c2, "boxer": BLACK}.get(pat, c2 if white_muzzle else light(coat, .18))
    if pat == "boxer":
        muz_col = dark(coat, .6)
    ear_col = {"tricolor": BLACK if coat == BLACK else (dark(coat, .2) if coat != TAN else TAN), "patches": c2, "tripatches": BLACK,
               "mask": dark(coat, .5), "saddlecap": BLACK if spec["ear"] in ("bigprick", "prick") else dark(coat, .35),
               "harlequin": BLACK, "spots": BLACK, "spectacles": dark(coat, .3), "stbernard": RUST, "merle": dark(coat, .2)}.get(pat, coat)
    if pat == "patches" and c2 == WHITE:
        ear_col = coat
    if pat == "oes":
        ear_col = coat
    if spec["ear"] in ("silky", "longsilky", "poodle") and pat in ("blaze", "solid", "patches"):
        ear_col = coat if pat != "patches" else c2

    # body / chest
    body_col = coat if pat not in ("patches", "spots", "harlequin", "ticked", "tripatches") else WHITE
    if pat == "ticked":
        body_col = mix(WHITE, LIVER, .25)
    if pat in ("tanpoints", "saddlecap", "tricolor") and coat == BLACK or pat == "yorkie":
        body_col = coat
    out.append(ell(HX, 975, 320 if spec["head"] not in ("massive", "broad") else 360, 340, body_col))
    out.append(path(f"M{HX-150} 560 L{HX+150} 560 L{HX+190} 720 L{HX-190} 720Z", body_col, False))
    if pat == "saddlecap":
        out.append(path(f"M{HX-300} 900 Q {HX} 700 {HX+300} 900 L{HX+330} 1000 L{HX-330} 1000Z", BLACK, False))
        out.append(ell(HX, 1010, 210, 290, coat, False))
    if pat in ("blaze", "tricolor", "husky", "stbernard", "boxer", "urajiro", "oes", "heeler", "tripatches") or (pat == "patches" and c2 != WHITE and coat == WHITE):
        out.append(ell(HX, 1010, 150, 290, WHITE if pat != "urajiro" else c2, False))
    if pat in ("tanpoints", "yorkie"):
        out.append(ell(HX - 70, 760, 34, 26, c2, False)); out.append(ell(HX + 70, 760, 34, 26, c2, False))
    if pat == "spots" or pat == "harlequin":
        for _ in range(9 if pat == "spots" else 4):
            out.append(ell(R.uniform(220, 780), R.uniform(760, 980), R.uniform(14, 26) if pat == "spots" else R.uniform(40, 70), R.uniform(12, 22) if pat == "spots" else R.uniform(30, 50), c2, False))
    if pat == "merle" or pat == "ticked" or pat == "heeler":
        for _ in range(14 if pat != "merle" else 6):
            out.append(ell(R.uniform(200, 800), R.uniform(760, 990), R.uniform(8, 16) if pat != "merle" else R.uniform(30, 55), R.uniform(8, 14) if pat != "merle" else R.uniform(22, 40), dark(coat, .45) if pat == "merle" else (LIVER if pat == "ticked" else dark(coat, .3)), False))
    # chest ruff for fluffy
    if fur in ("fluffy", "pom", "lion", "shaggy", "feathered"):
        out.append(scallop(HX, 760, 250 if fur != "pom" else 300, 150, 12, 22, white_muzzle and WHITE or (light(coat, .12) if fur != "lion" else coat)))
    out.append(ell(HX, 690, 190, 60, "#000", False, 'fill-opacity=".12"'))

    g = []  # head group (rotated by tilt)

    # fur halo behind head
    if fur in ("fluffy", "pom", "lion", "shaggy", "puff", "curly", "poodle", "lamb"):
        k = {"fluffy": 1.18, "pom": 1.38, "lion": 1.42, "shaggy": 1.2, "puff": 1.3, "curly": 1.18, "poodle": 1.05, "lamb": 1.08}[fur]
        bump = {"pom": 30, "lion": 34, "puff": 26, "curly": 16, "poodle": 14, "lamb": 12}.get(fur, 24)
        n = {"pom": 18, "lion": 16, "puff": 22, "curly": 26, "poodle": 26, "lamb": 24}.get(fur, 16)
        halo = coat if fur != "lion" else dark(coat, .12)
        if pat == "husky" or pat == "urajiro":
            halo = coat
        g.append(scallop(HX, HY + 10, rx * k, ry * k * (0.95 if fur != "lion" else 1.0), n, bump, halo))
        if fur == "lion" and spec["pat"] == "tanpoints":
            pass

    # back ears (prick/bat/tipped/rose/butterfly)
    ear = spec["ear"]
    inner = "#F0A7A5"

    def prick(scale=1.0, wide=1.0, rounded=False, tipped=False, butterfly=False):
        ex1, ey1 = HX - rx * 0.88 * wide, HY - ry * 0.28
        ex2, ey2 = HX - rx * 0.22, HY - ry * 0.88
        tx, ty = HX - rx * 0.78 * wide, HY - ry * (0.88 + 0.62 * scale)
        if rounded:
            d = f"M{ex1:.1f} {ey1:.1f} Q{tx-60:.1f} {ty:.1f} {tx:.1f} {ty:.1f} Q{tx+50:.1f} {ty-10:.1f} {ex2:.1f} {ey2:.1f}Z"
        else:
            d = f"M{ex1:.1f} {ey1:.1f} Q{tx-18:.1f} {(ty+ey1)/2:.1f} {tx:.1f} {ty:.1f} Q{(tx+ex2)/2+18:.1f} {(ty+ey2)/2:.1f} {ex2:.1f} {ey2:.1f}Z"
        s = path(d, ear_col)
        if not butterfly:
            ix1, iy1 = ex1 + (tx - ex1) * .2 + 22, ey1 + (ty - ey1) * .2
            ix2, iy2 = ex2 + (tx - ex2) * .2 - 4, ey2 + (ty - ey2) * .2 + 8
            itx, ity = tx + (HX - tx) * .08, ty + 34
            s += path(f"M{ix1:.1f} {iy1:.1f} Q{itx-8:.1f} {(ity+iy1)/2:.1f} {itx:.1f} {ity:.1f} Q{(itx+ix2)/2+6:.1f} {(ity+iy2)/2:.1f} {ix2:.1f} {iy2:.1f}Z", inner if pat not in ("husky",) else light(inner, .3), False)
        if tipped:
            s += path(f"M{tx-8:.1f} {ty+70:.1f} Q{tx-70:.1f} {ty+80:.1f} {tx-55:.1f} {ty+125:.1f} Q{tx-20:.1f} {ty+100:.1f} {tx+30:.1f} {ty+80:.1f}Z", ear_col)
        if butterfly:
            for i in range(7):
                a1 = i / 6
                x = ex1 + (tx - ex1) * a1 - 30
                s += f'<path d="M{x:.0f} {ey1 + (ty - ey1) * a1:.0f} q -40 10 -55 -10" stroke="{OUT}" stroke-width="5" fill="none"/>'
        return s

    if ear in ("prick", "bigprick", "bat", "tipped", "butterfly", "small"):
        args = {"prick": (1.0, 1.0, False, False, False), "bigprick": (1.35, 1.05, False, False, False), "bat": (1.15, 1.12, True, False, False),
                "tipped": (0.9, 1.0, False, True, False), "butterfly": (1.4, 1.35, True, False, True), "small": (0.45, 0.95, True, False, False)}[ear]
        e = prick(*args)
        g.append(e); g.append(mirror(e))
    if ear == "rose":
        e = path(f"M{HX-rx*0.7:.1f} {HY-ry*0.75:.1f} Q{HX-rx*1.25:.1f} {HY-ry*1.05:.1f} {HX-rx*1.2:.1f} {HY-ry*0.4:.1f} Q{HX-rx*1.05:.1f} {HY-ry*0.62:.1f} {HX-rx*0.85:.1f} {HY-ry*0.45:.1f}Z", ear_col)
        g.append(e); g.append(mirror(e))

    # head
    head_col = coat
    if pat in ("patches", "spots", "harlequin", "ticked", "tripatches") and coat == WHITE:
        head_col = WHITE
    if pat == "ticked":
        head_col = LIVER
    if spec["head"] == "egg":
        g.append(path(f"M{HX} {HY-ry} C{HX+rx*1.3} {HY-ry} {HX+rx*1.15} {HY+ry*1.05} {HX} {HY+ry} C{HX-rx*1.15} {HY+ry*1.05} {HX-rx*1.3} {HY-ry} {HX} {HY-ry}Z", head_col))
    else:
        g.append(ell(HX, HY, rx, ry, head_col))
    # head markings (clipped inside head)
    clip = f'<clipPath id="hc{seed}"><ellipse cx="{HX}" cy="{HY}" rx="{rx-3}" ry="{ry-3}"/></clipPath>'
    m = []
    if pat == "husky":
        m.append(path(f"M{HX-rx} {HY+10} Q{HX-rx*0.7} {HY-ry*0.35} {HX-rx*0.3} {HY-ry*0.12} Q{HX-rx*0.12} {HY-ry*0.6} {HX} {HY-ry*0.75} Q{HX+rx*0.12} {HY-ry*0.6} {HX+rx*0.3} {HY-ry*0.12} Q{HX+rx*0.7} {HY-ry*0.35} {HX+rx} {HY+10} V{HY+ry} H{HX-rx}Z", c2, False))
        m.append(ell(HX - rx * 0.42, HY - ry * 0.05, rx * 0.2, ry * 0.12, coat, False)); m.append(ell(HX + rx * 0.42, HY - ry * 0.05, rx * 0.2, ry * 0.12, coat, False))
    if pat == "urajiro":
        m.append(ell(HX - rx * 0.45, HY + ry * 0.45, rx * 0.42, ry * 0.42, c2, False)); m.append(ell(HX + rx * 0.45, HY + ry * 0.45, rx * 0.42, ry * 0.42, c2, False))
        m.append(ell(HX - rx * 0.42, HY - ry * 0.32, rx * 0.12, ry * 0.07, c2, False)); m.append(ell(HX + rx * 0.42, HY - ry * 0.32, rx * 0.12, ry * 0.07, c2, False))
    if pat in ("blaze", "tricolor", "stbernard", "boxer", "heeler", "tripatches") or (pat == "merle" and c2 == WHITE):
        w = rx * (0.12 if pat != "stbernard" else 0.2)
        m.append(path(f"M{HX-w} {HY-ry} L{HX+w} {HY-ry} L{HX+w*1.6} {HY+ry*0.1} L{HX-w*1.6} {HY+ry*0.1}Z", WHITE, False))
    if pat in ("tanpoints", "tricolor", "yorkie", "saddlecap") and pat != "saddlecap":
        tc = c2 if pat != "tricolor" else (RUST if coat == BLACK else TAN)
        m.append(ell(HX - rx * 0.42, HY - ry * 0.33, rx * 0.12, ry * 0.07, tc, False)); m.append(ell(HX + rx * 0.42, HY - ry * 0.33, rx * 0.12, ry * 0.07, tc, False))
        m.append(ell(HX - rx * 0.5, HY + ry * 0.42, rx * 0.3, ry * 0.3, tc, False)); m.append(ell(HX + rx * 0.5, HY + ry * 0.42, rx * 0.3, ry * 0.3, tc, False))
    if pat == "tricolor" and coat == TAN:  # beagle/basset: tan head, white blaze, black saddle not visible
        pass
    if pat == "saddlecap":
        m.append(path(f"M{HX-rx*0.5} {HY-ry} Q{HX} {HY-ry*0.3} {HX+rx*0.5} {HY-ry}Z", BLACK, False))
    if pat == "yorkie":
        m.append(path(f"M{HX-rx} {HY+ry*0.05} Q{HX} {HY-ry*0.4} {HX+rx} {HY+ry*0.05} V{HY+ry} H{HX-rx}Z", TAN, False))
        m.append(path(f"M{HX-rx} {HY-ry*0.2} Q{HX} {HY-ry*1.3} {HX+rx} {HY-ry*0.2} V{HY-ry} H{HX-rx}Z", GOLD, False))
    if pat == "patches" or pat == "tripatches":
        pc = c2 if coat == WHITE else coat
        if pat == "tripatches":
            pc = BLACK
        m.append(ell(HX - rx * 0.55, HY - ry * 0.25, rx * 0.42, ry * 0.45, pc, False))
        if R.random() < 0.7:
            m.append(ell(HX + rx * 0.6, HY - ry * 0.3, rx * 0.36, ry * 0.4, pc, False))
    if pat == "spectacles":
        for sgn in (-1, 1):
            m.append(f'<path d="M{HX+sgn*rx*0.25:.0f} {HY-ry*0.12:.0f} Q{HX+sgn*rx*0.42:.0f} {HY-ry*0.32:.0f} {HX+sgn*rx*0.68:.0f} {HY-ry*0.3:.0f}" stroke="{BLACK}" stroke-width="16" fill="none" stroke-linecap="round"/>')
        m.append(ell(HX, HY + ry * 0.45, rx * 0.5, ry * 0.4, dark(coat, .45), False))
    if pat == "oes":
        m.append(path(f"M{HX-rx} {HY-ry*0.1} Q{HX} {HY-ry*0.5} {HX+rx} {HY-ry*0.1} V{HY+ry} H{HX-rx}Z", WHITE, False))
    if pat == "stbernard":
        m.append(ell(HX - rx * 0.42, HY - ry * 0.05, rx * 0.26, ry * 0.22, dark(RUST, .45), False)); m.append(ell(HX + rx * 0.42, HY - ry * 0.05, rx * 0.26, ry * 0.22, dark(RUST, .45), False))
    if pat in ("spots", "harlequin"):
        for _ in range(7 if pat == "spots" else 3):
            ang = R.uniform(0, 2 * math.pi); dd = R.uniform(.35, .85)
            x, y = HX + math.cos(ang) * rx * dd, HY - abs(math.sin(ang)) * ry * dd * .9
            m.append(ell(x, y, R.uniform(12, 20) if pat == "spots" else R.uniform(40, 60), R.uniform(10, 16) if pat == "spots" else R.uniform(30, 45), c2, False))
    if pat == "merle":
        for _ in range(5):
            m.append(ell(HX + R.uniform(-rx * .8, rx * .8), HY + R.uniform(-ry * .8, ry * .1), R.uniform(25, 45), R.uniform(20, 35), dark(coat, .45), False))
        m.append(ell(HX - rx * 0.5, HY - ry * 0.3, rx * 0.35, ry * 0.4, BLACK, False))
    if pat == "ticked":
        m.append(path(f"M{HX-rx*0.1} {HY-ry} L{HX+rx*0.1} {HY-ry} L{HX+rx*0.12} {HY-ry*0.4} L{HX-rx*0.12} {HY-ry*0.4}Z", WHITE, False))
    if pat == "schnauzer":
        m.append(ell(HX, HY + ry * 0.55, rx * 0.65, ry * 0.5, c2, False))
    if pat == "heeler":
        for _ in range(30):
            m.append(ell(HX + R.uniform(-rx, rx), HY + R.uniform(-ry, ry), 5, 5, WHITE, False, 'fill-opacity=".5"'))
        m.append(ell(HX - rx * 0.5, HY - ry * 0.15, rx * 0.3, ry * 0.3, BLACK, False))
    g.append(clip + f'<g clip-path="url(#hc{seed})">{"".join(m)}</g>' if spec["head"] != "egg" else "".join(m[:0]))
    # soft highlight
    g.append(ell(HX - rx * 0.25, HY - ry * 0.55, rx * 0.45, ry * 0.22, "#fff", False, 'fill-opacity=".14"'))

    # wrinkles
    if "wrinkles" in flags:
        n = 3 if "heavy" not in flags else 5
        for i in range(n):
            y = HY - ry * 0.55 + i * 22
            g.append(f'<path d="M{HX-rx*0.35:.0f} {y:.0f} Q{HX:.0f} {y-18:.0f} {HX+rx*0.35:.0f} {y:.0f}" stroke="{dark(coat, .4)}" stroke-width="6" fill="none" stroke-linecap="round"/>')
        if "heavy" in flags:
            for sgn in (-1, 1):
                for i in range(3):
                    g.append(f'<path d="M{HX+sgn*rx*(0.7+i*0.08):.0f} {HY-ry*0.1+i*40:.0f} q {sgn*-20} 30 0 60" stroke="{dark(coat, .35)}" stroke-width="6" fill="none" stroke-linecap="round"/>')

    # eyes
    ex_off = rx * (0.42 if spec["head"] not in ("long", "narrow", "egg", "pear") else 0.4)
    ey = HY - ry * 0.05
    er = rx * 0.13 * (1.25 if spec["head"] in ("apple", "round") else 1.0)
    if spec["head"] in ("egg", "pear"):
        er *= 0.7
    if expr == "shocked":
        er *= 1.3
    ecol = {"brown": "#3B2314", "blue": "#57A6DB", "amber": "#B9792B"}
    iris = [ecol.get(spec["eye"], "#3B2314")] * 2
    if spec["eye"] == "hetero":
        iris = ["#57A6DB", "#3B2314"]
    look = {"dramatic": (0.35, -0.35), "sideeye": (0.45, 0), "smug": (0.3, 0), "sad": (0, -0.3), "cute": (0, -0.2), "clueless": (0, -0.4)}.get(expr, (0, 0))
    lid_col = head_col if pat not in ("husky", "urajiro") else c2
    for idx, sgn in enumerate((-1, 1)):
        x = HX + sgn * ex_off
        if expr in ("sleepy", "howl", "joy"):
            if expr == "joy":
                g.append(f'<path d="M{x-er:.0f} {ey+4:.0f} Q{x:.0f} {ey-er*1.2:.0f} {x+er:.0f} {ey+4:.0f}" stroke="{OUT}" stroke-width="9" fill="none" stroke-linecap="round"/>')
            else:
                g.append(f'<path d="M{x-er:.0f} {ey-2:.0f} Q{x:.0f} {ey+er*0.9:.0f} {x+er:.0f} {ey-2:.0f}" stroke="{OUT}" stroke-width="9" fill="none" stroke-linecap="round"/>')
            continue
        g.append(ell(x, ey, er, er * 1.05, "#FFFFFF"))
        lx, ly = look
        if expr == "clueless":
            lx = 0.25 * sgn * -1
        g.append(ell(x + lx * er * 0.45, ey + ly * er * 0.45, er * 0.78, er * 0.8, iris[idx], False))
        g.append(ell(x + lx * er * 0.5, ey + ly * er * 0.5, er * (0.4 if expr != "shocked" else 0.25), er * (0.42 if expr != "shocked" else 0.27), "#111", False))
        g.append(ell(x + lx * er * 0.45 - er * 0.3, ey + ly * er * 0.45 - er * 0.32, er * 0.24, er * 0.24, "#fff", False))
        g.append(ell(x + lx * er * 0.45 + er * 0.25, ey + ly * er * 0.45 + er * 0.25, er * 0.1, er * 0.1, "#fff", False))
        if expr in ("grumpy", "smug", "sideeye"):
            # heavy lids
            lid = (f"M{x-er-6:.0f} {ey-er-6:.0f} H{x+er+6:.0f} V{ey-er*(0.05 if expr=='grumpy' else 0.15)+(sgn*-1)*(er*0.35 if expr=='grumpy' else 0):.0f} "
                   f"L{x-er-6:.0f} {ey-er*(0.05 if expr=='grumpy' else 0.15)+(sgn)*(er*0.35 if expr=='grumpy' else 0):.0f}Z")
            g.append(path(lid, lid_col, False))
            g.append(f'<path d="M{x-er:.0f} {ey-er*(0.05 if expr=="grumpy" else 0.15)+(sgn)*(er*0.32 if expr=="grumpy" else 0):.0f} L{x+er:.0f} {ey-er*(0.05 if expr=="grumpy" else 0.15)-(sgn)*(er*0.32 if expr=="grumpy" else 0):.0f}" stroke="{OUT}" stroke-width="7" stroke-linecap="round"/>')
        if expr == "sad" or "brow" in flags:
            g.append(f'<path d="M{x-er*0.9:.0f} {ey-er*1.45+(sgn*-1)*0:.0f} L{x+er*0.9:.0f} {ey-er*1.45-(sgn)*er*0.45*(-1):.0f}" stroke="{dark(head_col, .45)}" stroke-width="9" stroke-linecap="round"/>' if expr == "sad" else
                     f'<path d="M{x-er:.0f} {ey-er*1.5:.0f} Q{x:.0f} {ey-er*1.9:.0f} {x+er:.0f} {ey-er*1.5:.0f}" stroke="{dark(head_col, .45)}" stroke-width="7" fill="none" stroke-linecap="round"/>')
        if expr == "shocked" or (expr == "dramatic" and sgn == 1):
            g.append(f'<path d="M{x-er:.0f} {ey-er*1.55:.0f} Q{x:.0f} {ey-er*2.1:.0f} {x+er:.0f} {ey-er*1.55:.0f}" stroke="{dark(head_col, .5)}" stroke-width="8" fill="none" stroke-linecap="round"/>')
        if expr == "grumpy":
            g.append(f'<path d="M{x-sgn*er*1.1:.0f} {ey-er*1.55:.0f} L{x+sgn*er*0.9:.0f} {ey-er*1.05:.0f}" stroke="{dark(head_col, .55) if head_col != BLACK else "#555"}" stroke-width="11" stroke-linecap="round"/>')

    # wire beard & brows
    if fur == "wire" or pat == "schnauzer":
        bc = c2 if pat == "schnauzer" else light(coat, .1)
        for sgn in (-1, 1):
            g.append(scallop(HX + sgn * ex_off, ey - er * 1.55, er * 1.3, er * 0.45, 7, 8, bc, True, math.pi, 2 * math.pi))
    # muzzle
    mz = spec["mz"]
    mrx, mry = [(0.42, 0.24), (0.44, 0.29), (0.42, 0.34), (0.36, 0.38)][mz]
    mrx *= rx; mry *= ry
    mcy = HY + ry * (0.42 + 0.06 * mz)
    if spec["head"] in ("egg", "pear", "narrow"):
        mcy = HY + ry * 0.55
    g.append(ell(HX, mcy, mrx, mry, muz_col))
    if fur in ("wire",) or pat == "schnauzer":
        bc = c2 if pat == "schnauzer" else light(coat, .1)
        g.append(scallop(HX, mcy + mry * 0.55, mrx * 1.05, mry * 0.9, 12, 14, bc, True, 0, math.pi))
    # jowls
    if "jowls" in flags:
        for sgn in (-1, 1):
            g.append(path(f"M{HX+sgn*mrx*0.2:.0f} {mcy+mry*0.2:.0f} Q{HX+sgn*mrx*1.2:.0f} {mcy+mry*0.1:.0f} {HX+sgn*mrx*1.05:.0f} {mcy+mry*1.25:.0f} Q{HX+sgn*mrx*0.5:.0f} {mcy+mry*1.45:.0f} {HX+sgn*mrx*0.1:.0f} {mcy+mry*0.9:.0f}Z", muz_col))
    # nose
    ny = mcy - mry * 0.42
    nw = mrx * 0.42
    g.append(path(f"M{HX-nw:.0f} {ny-nw*0.35:.0f} Q{HX:.0f} {ny-nw*0.75:.0f} {HX+nw:.0f} {ny-nw*0.35:.0f} Q{HX+nw*0.8:.0f} {ny+nw*0.45:.0f} {HX:.0f} {ny+nw*0.55:.0f} Q{HX-nw*0.8:.0f} {ny+nw*0.45:.0f} {HX-nw:.0f} {ny-nw*0.35:.0f}Z",
                  "#2A1A14" if coat not in (LIVER, CHOC, RED) or pat in ("mask", "boxer") else "#5A3020", False))
    g.append(ell(HX - nw * 0.35, ny - nw * 0.3, nw * 0.25, nw * 0.13, "#fff", False, 'fill-opacity=".5"'))
    # mouth
    my = ny + nw * 0.55
    mw = mrx * 0.55
    ink = f'stroke="{OUT}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    tongue = "#5B7FC4" if "bluetongue" in flags else "#F07A8A"
    if expr in ("happy", "clueless", "joy", "proud") and expr != "proud" or expr == "alert" and False:
        h = mry * 0.75
        g.append(path(f"M{HX-mw:.0f} {my+8:.0f} Q{HX:.0f} {my+h*1.6:.0f} {HX+mw:.0f} {my+8:.0f} Q{HX:.0f} {my+h*0.25:.0f} {HX-mw:.0f} {my+8:.0f}Z", "#5A1F24"))
        tx = HX + (mw * 0.35 if expr == "clueless" else 0)
        g.append(path(f"M{tx-mw*0.45:.0f} {my+h*0.65:.0f} Q{tx-mw*0.5:.0f} {my+h*1.9:.0f} {tx:.0f} {my+h*1.9:.0f} Q{tx+mw*0.5:.0f} {my+h*1.9:.0f} {tx+mw*0.45:.0f} {my+h*0.65:.0f}Z", tongue))
        g.append(f'<path d="M{tx:.0f} {my+h*0.9:.0f} V{my+h*1.5:.0f}" stroke="{dark(tongue, .25)}" stroke-width="4"/>')
    elif expr in ("shocked", "howl"):
        g.append(f'<path d="M{HX} {ny+nw*0.5:.0f} V{my+4:.0f}" {ink}/>')
        g.append(ell(HX, my + mry * 0.5, mw * 0.42, mry * 0.48, "#5A1F24"))
        g.append(ell(HX, my + mry * 0.75, mw * 0.25, mry * 0.18, tongue, False))
    elif expr in ("grumpy", "sad"):
        g.append(f'<path d="M{HX} {ny+nw*0.5:.0f} V{my+10:.0f} M{HX-mw:.0f} {my+mry*0.45:.0f} Q{HX:.0f} {my-6:.0f} {HX+mw:.0f} {my+mry*0.45:.0f}" {ink}/>')
    elif expr in ("smug", "sideeye"):
        g.append(f'<path d="M{HX} {ny+nw*0.5:.0f} V{my+6:.0f} M{HX-mw*0.6:.0f} {my+14:.0f} Q{HX:.0f} {my+22:.0f} {HX+mw:.0f} {my-4:.0f}" {ink}/>')
    else:  # cute, proud, alert, sleepy, dramatic
        g.append(f'<path d="M{HX} {ny+nw*0.5:.0f} V{my+4:.0f} M{HX-mw*0.8:.0f} {my-2:.0f} Q{HX-mw*0.4:.0f} {my+mry*0.4:.0f} {HX:.0f} {my+4:.0f} Q{HX+mw*0.4:.0f} {my+mry*0.4:.0f} {HX+mw*0.8:.0f} {my-2:.0f}" {ink}/>')
        if expr in ("proud", "cute") and ("tongue" in flags or expr == "proud"):
            g.append(path(f"M{HX-mw*0.22:.0f} {my+2:.0f} Q{HX:.0f} {my+mry*0.75:.0f} {HX+mw*0.22:.0f} {my+2:.0f}Z", tongue))
    if "tongue" in flags and expr in ("smug",):
        g.append(path(f"M{HX-mw*0.18:.0f} {my+10:.0f} Q{HX:.0f} {my+mry*0.7:.0f} {HX+mw*0.18:.0f} {my+10:.0f}Z", tongue))
    if "drool" in flags:
        g.append(path(f"M{HX+mw*0.7:.0f} {my+mry*0.4:.0f} q 8 50 0 80 q -12 -10 -6 -40Z", "#DDF3FF", True, 'stroke-width="4"'))
    # cheek blush
    g.append(ell(HX - rx * 0.62, HY + ry * 0.28, rx * 0.13, ry * 0.06, "#FF7F8A", False, 'fill-opacity=".28"'))
    g.append(ell(HX + rx * 0.62, HY + ry * 0.28, rx * 0.13, ry * 0.06, "#FF7F8A", False, 'fill-opacity=".28"'))

    # front ears
    def flop(length=1.0, wide=1.0, col=None, silky=False):
        col = col or ear_col
        x0, y0 = HX - rx * 0.6, HY - ry * 0.85
        x1, y1 = HX - rx * (1.12 * wide), HY - ry * 0.35
        x2, y2 = HX - rx * (1.02 * wide), HY + ry * (0.15 + 0.9 * (length - 1) + 0.35 * length)
        x3, y3 = HX - rx * 0.62, HY - ry * 0.05 + (length - 1) * ry * 0.4
        d = f"M{x0:.0f} {y0:.0f} Q{x1-20:.0f} {y0-10:.0f} {x1:.0f} {y1:.0f} Q{x1-25:.0f} {(y1+y2)/2:.0f} {x2:.0f} {y2:.0f} Q{(x2+x3)/2+20:.0f} {y2+30:.0f} {x3:.0f} {y3:.0f} Q{x3+30:.0f} {(y0+y3)/2:.0f} {x0:.0f} {y0:.0f}Z"
        if silky:
            d = (f"M{x0:.0f} {y0:.0f} Q{x1-30:.0f} {y0-10:.0f} {x1-6:.0f} {y1:.0f} " +
                 " ".join(f"Q{x1-30 + i*4:.0f} {y1 + (y2-y1)*(i+0.5)/3:.0f} {x1-14 + i*6:.0f} {y1 + (y2-y1)*(i+1)/3:.0f}" for i in range(3)) +
                 " " + " ".join(f"Q{x2 + (x3-x2)*(i+0.5)/3:.0f} {y2+30:.0f} {x2 + (x3-x2)*(i+1)/3:.0f} {y2-6+((i+1)%2)*12:.0f}" for i in range(3)) +
                 f" Q{x3+20:.0f} {(y0+y3)/2:.0f} {x0:.0f} {y0:.0f}Z")
        s = path(d, col)
        if silky:
            for i in range(3):
                xx = x1 + 30 + i * 22
                s += f'<path d="M{xx:.0f} {y1+20:.0f} Q{xx-10:.0f} {(y1+y2)/2:.0f} {xx-4:.0f} {y2-20:.0f}" stroke="{dark(col, .25)}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        return s

    def fold():
        x0, y0 = HX - rx * 0.78, HY - ry * 0.62
        x1, y1 = HX - rx * 0.28, HY - ry * 0.9
        tx, ty = HX - rx * 0.62, HY - ry * 0.18
        return path(f"M{x0:.0f} {y0:.0f} Q{(x0+x1)/2:.0f} {y1-50:.0f} {x1:.0f} {y1:.0f} Q{(x1+tx)/2+10:.0f} {(y1+ty)/2:.0f} {tx:.0f} {ty:.0f} Q{(x0+tx)/2-20:.0f} {(y0+ty)/2:.0f} {x0:.0f} {y0:.0f}Z", ear_col)

    fe = None
    if ear == "floppy":
        fe = flop(1.0)
    elif ear == "long":
        fe = flop(1.75, 1.05)
    elif ear == "longsilky":
        fe = flop(1.55, 1.12, silky=True)
    elif ear == "silky":
        fe = flop(1.9, 1.2, coat if pat != "patches" else c2, silky=True)
    elif ear == "poodle":
        fe = scallop(HX - rx * 0.98, HY + ry * 0.2, rx * 0.3, ry * 0.6, 12, 14, coat)
    elif ear == "fold":
        fe = fold()
    elif ear == "tassel":
        fe = flop(1.3, 0.98) + ell(HX - rx * 1.0, HY + ry * 0.75, 26, 34, light(coat, .2))
    if fe:
        g.append(fe); g.append(mirror(fe))

    # special fur overlays
    if fur == "corded":
        cords = []
        for row in range(3):
            n = 9 + row
            for i in range(n):
                x = HX - rx * 1.1 + (2.2 * rx) * (i + .5) / n + R.uniform(-8, 8)
                y0 = HY - ry * (1.05 - row * 0.35)
                L = R.uniform(90, 150) + row * 30
                if row == 2 and abs(x - HX) < rx * 0.55:
                    continue  # keep face visible
                cords.append(path(f"M{x-15:.0f} {y0:.0f} Q{x-22:.0f} {y0+L*0.6:.0f} {x-6:.0f} {y0+L:.0f} Q{x+4:.0f} {y0+L+12:.0f} {x+12:.0f} {y0+L-4:.0f} Q{x+20:.0f} {y0+L*0.5:.0f} {x+15:.0f} {y0:.0f}Z",
                                  coat if R.random() < .6 else (light(coat, .12) if coat != BLACK else "#3A3437")))
        g.append("".join(cords))
    if fur in ("shaggy",):
        g.append(scallop(HX, HY - ry * 0.35, rx * 1.02, ry * 0.42, 14, 20, coat if pat != "oes" else WHITE, True, math.pi * 1.0, math.pi * 2))
        g.append(scallop(HX, HY - ry * 0.12, rx * 0.8, ry * 0.18, 10, 16, coat if pat != "oes" else WHITE, True, 0, math.pi))
    if fur in ("puff", "topknot", "poodle", "lamb", "curly"):
        tk = {"puff": (0.8, 0.42), "topknot": (0.65, 0.4), "poodle": (0.75, 0.48), "lamb": (0.5, 0.3), "curly": (0.65, 0.32)}[fur]
        g.append(scallop(HX, HY - ry * 0.82, rx * tk[0], ry * tk[1], 14, 16, light(coat, .12) if fur != "poodle" else coat))
    if fur == "silky":
        g.append(path(f"M{HX-rx*0.55:.0f} {HY-ry*0.7:.0f} Q{HX:.0f} {HY-ry*1.25:.0f} {HX+rx*0.55:.0f} {HY-ry*0.7:.0f} Q{HX:.0f} {HY-ry*0.95:.0f} {HX-rx*0.55:.0f} {HY-ry*0.7:.0f}Z", light(coat, .1), True))
    if fur == "crested":
        for i in range(9):
            x = HX - 90 + i * 22
            g.append(path(f"M{x:.0f} {HY-ry*0.75:.0f} Q{x-30:.0f} {HY-ry*1.4:.0f} {x+R.uniform(-60,60):.0f} {HY-ry*1.6:.0f} Q{x+10:.0f} {HY-ry*1.2:.0f} {x+14:.0f} {HY-ry*0.75:.0f}Z", WHITE))
    if fur == "hairless":
        g.append(f'<path d="M{HX-50} {HY-ry*0.62:.0f} q50 -16 100 0 M{HX-40} {HY-ry*0.52:.0f} q40 -12 80 0" stroke="{dark(coat, .35)}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    if fur == "feathered":
        pass

    A = []
    N = []
    for acc in accs:
        # accessories (head-relative)
        top = HY - ry
        if fur in ("pom", "lion", "puff", "corded", "poodle"):
            top -= ry * 0.3
        if acc == "crown":
            A.append(path(f"M{HX-95} {top+10} L{HX-110} {top-90} L{HX-50} {top-40} L{HX} {top-115} L{HX+50} {top-40} L{HX+110} {top-90} L{HX+95} {top+10}Z", "#F2C230"))
            for x in (-110, 0, 110):
                A.append(ell(HX + x, top - (90 if x else 115), 14, 14, "#E0473B"))
        elif acc == "santa":
            A.append(path(f"M{HX-rx*0.8} {top+40} Q{HX-rx*0.3} {top-170} {HX+rx*0.75} {top-140} Q{HX+rx*0.6} {top-60} {HX+rx*0.8} {top+40}Z", "#D62E2E"))
            A.append(ell(HX + rx * 0.82, top - 140, 34, 34, WHITE))
            A.append(path(f"M{HX-rx*0.95} {top+60} Q{HX} {top-20} {HX+rx*0.95} {top+60} Q{HX+rx*0.95} {top+110} {HX+rx*0.85} {top+100} Q{HX} {top+30} {HX-rx*0.85} {top+100} Q{HX-rx*0.95} {top+110} {HX-rx*0.95} {top+60}Z", WHITE))
        elif acc == "antlers":
            for sgn in (-1, 1):
                A.append(f'<path d="M{HX+sgn*rx*0.45:.0f} {top+30:.0f} q {sgn*20} -80 {sgn*60} -140 M{HX+sgn*rx*0.55:.0f} {top-40:.0f} q {sgn*40} -10 {sgn*70} -40 M{HX+sgn*rx*0.62:.0f} {top-80:.0f} q {sgn*-30} -30 {sgn*-20} -70" stroke="#8B5A2B" stroke-width="22" fill="none" stroke-linecap="round"/>')
            A.append(ell(HX, ny, nw * 1.1, nw * 0.8, "#E23B3B"))
        elif acc == "partyhat":
            A.append(path(f"M{HX-70} {top+30} L{HX+10} {top-170} L{HX+80} {top+30}Z", "#6A4BB0"))
            A.append(f'<path d="M{HX-45} {top-30} L{HX+60} {top-10} M{HX-20} {top-95} L{HX+40} {top-80}" stroke="#FFD166" stroke-width="14"/>')
            A.append(ell(HX + 10, top - 175, 22, 22, "#FFD166"))
        elif acc == "tophat":
            A.append(path(f"M{HX-80} {top+20} V{top-130} H{HX+80} V{top+20}Z", "#2B2B33"))
            A.append(ell(HX, top + 20, 140, 26, "#2B2B33")); A.append(f'<rect x="{HX-80}" y="{top-20}" width="160" height="26" fill="#C23B3B"/>')
        elif acc == "fedora":
            A.append(path(f"M{HX-110} {top+30} Q{HX} {top-10} {HX+110} {top+30} Q{HX+60} {top-40} {HX+70} {top-90} Q{HX} {top-130} {HX-70} {top-90} Q{HX-60} {top-40} {HX-110} {top+30}Z", "#4A4038"))
            A.append(f'<path d="M{HX-75} {top-20} Q{HX} {top-35} {HX+75} {top-20}" stroke="#1C1A18" stroke-width="18" fill="none"/>')
        elif acc == "cowboy":
            A.append(path(f"M{HX-210} {top+40} Q{HX} {top+100} {HX+210} {top+40} Q{HX+120} {top+20} {HX+90} {top-80} Q{HX} {top-60} {HX-90} {top-80} Q{HX-120} {top+20} {HX-210} {top+40}Z", "#9A6638"))
        elif acc == "firehat":
            A.append(path(f"M{HX-170} {top+50} Q{HX} {top-170} {HX+170} {top+50} Q{HX} {top+10} {HX-170} {top+50}Z", "#C8231B"))
            A.append(path(f"M{HX-30} {top-10} H{HX+30} V{top-80} H{HX-30}Z", "#F2C230"))
        elif acc == "detective":
            A.append(path(f"M{HX-150} {top+40} Q{HX} {top-150} {HX+150} {top+40} Q{HX} {top+10} {HX-150} {top+40}Z", "#8C7A5B"))
            A.append(f'<path d="M{HX-130} {top+10} Q{HX} {top-60} {HX+130} {top+10}" stroke="#5D4E37" stroke-width="10" fill="none"/>')
        elif acc == "bow":
            bx, by = HX + rx * 0.35, top + 30
            A.append(path(f"M{bx} {by} L{bx-70} {by-45} L{bx-70} {by+45}Z", "#F06292")); A.append(path(f"M{bx} {by} L{bx+70} {by-45} L{bx+70} {by+45}Z", "#F06292"))
            A.append(ell(bx, by, 18, 18, "#E04F82"))
        elif acc == "flower" or acc == "flowers" or acc == "marigold":
            cols = ["#FF8FAB", "#FFD166", "#C77DFF", "#7BDFF2"] if acc != "marigold" else ["#F7931E", "#FFB627", "#E8590C"]
            for i in range(7 if acc != "flower" else 1):
                ang = math.pi * (1.1 + i * 0.13) if acc != "flower" else math.pi * 1.7
                fx, fy = HX + rx * 0.95 * math.cos(ang), HY + ry * 0.95 * math.sin(ang)
                col = cols[i % len(cols)]
                for k in range(6):
                    A.append(ell(fx + 20 * math.cos(k), fy + 20 * math.sin(k), 16, 16, col, False))
                A.append(ell(fx, fy, 12, 12, "#E09F3E", False))
        elif acc == "headset":
            A.append(f'<path d="M{HX-rx*0.95:.0f} {HY:.0f} Q{HX:.0f} {top-80:.0f} {HX+rx*0.95:.0f} {HY:.0f}" stroke="#333" stroke-width="16" fill="none"/>')
            A.append(ell(HX - rx * 0.95, HY, 30, 42, "#333")); A.append(f'<path d="M{HX-rx*0.95:.0f} {HY+30:.0f} Q{HX-rx*0.6:.0f} {mcy+40:.0f} {HX-mrx*0.6:.0f} {mcy+10:.0f}" stroke="#333" stroke-width="8" fill="none"/>')

        # eyewear
        if acc in ("sunglasses",):
            for sgn in (-1, 1):
                A.append(path(f"M{HX+sgn*ex_off-er*1.5:.0f} {ey-er*0.9:.0f} H{HX+sgn*ex_off+er*1.5:.0f} Q{HX+sgn*ex_off+er*1.4:.0f} {ey+er*1.3:.0f} {HX+sgn*ex_off:.0f} {ey+er*1.2:.0f} Q{HX+sgn*ex_off-er*1.4:.0f} {ey+er*1.3:.0f} {HX+sgn*ex_off-er*1.5:.0f} {ey-er*0.9:.0f}Z", "#1C1C22"))
                A.append(f'<path d="M{HX+sgn*ex_off-er*0.8:.0f} {ey-er*0.4:.0f} l {er*0.5:.0f} {er*0.5:.0f}" stroke="#fff" stroke-opacity=".6" stroke-width="7" stroke-linecap="round"/>')
            A.append(f'<path d="M{HX-ex_off+er*1.5:.0f} {ey-er*0.6:.0f} H{HX+ex_off-er*1.5:.0f}" stroke="#1C1C22" stroke-width="10"/>')
        if acc in ("glasses", "roundglasses"):
            for sgn in (-1, 1):
                A.append(f'<circle cx="{HX+sgn*ex_off:.0f}" cy="{ey:.0f}" r="{er*1.45:.0f}" fill="#fff" fill-opacity=".15" stroke="#3A2A1C" stroke-width="9"/>')
            A.append(f'<path d="M{HX-ex_off+er*1.45:.0f} {ey:.0f} Q{HX} {ey-20:.0f} {HX+ex_off-er*1.45:.0f} {ey:.0f}" stroke="#3A2A1C" stroke-width="8" fill="none"/>')

        # neck items (not rotated)
        if acc in ("tie", "bowtie", "scarf", "tartan", "sweater", "barrel", "medal", "badge", "pearls", "chain", "tactical", "lifering", "cape"):
            if acc == "tie":
                N.append(path(f"M{HX-90} 700 L{HX+90} 700 L{HX+40} 750 H{HX-40}Z", WHITE))
                N.append(path(f"M{HX-32} 712 H{HX+32} L{HX+22} 760 L{HX+55} 940 L{HX} 1000 L{HX-55} 940 L{HX-22} 760Z", "#B3261E"))
            elif acc == "bowtie":
                N.append(path(f"M{HX} 730 L{HX-80} 690 L{HX-80} 770Z", "#B3261E")); N.append(path(f"M{HX} 730 L{HX+80} 690 L{HX+80} 770Z", "#B3261E"))
                N.append(ell(HX, 730, 20, 20, "#8E1B1B"))
            elif acc in ("scarf", "tartan"):
                col = "#2E5E8C" if acc == "scarf" else "#B3261E"
                N.append(path(f"M{HX-230} 690 Q{HX} 790 {HX+230} 690 L{HX+240} 760 Q{HX} 860 {HX-240} 760Z", col))
                N.append(path(f"M{HX+120} 760 L{HX+190} 960 L{HX+110} 970 L{HX+70} 790Z", col))
                if acc == "tartan":
                    for i in range(-3, 4):
                        N.append(f'<path d="M{HX+i*60} 720 V860" stroke="#1E5B3A" stroke-width="12" stroke-opacity=".7"/>')
            elif acc == "sweater":
                N.append(path(f"M{HX-340} 1000 Q{HX-330} 760 {HX-170} 700 Q{HX} 760 {HX+170} 700 Q{HX+330} 760 {HX+340} 1000Z", "#C0392B"))
                N.append(scallop(HX, 715, 185, 40, 16, 10, "#F5F5F5", True, 0, math.pi))
                for i in range(-3, 4):
                    N.append(f'<path d="M{HX+i*80-15} 880 l15 -25 l15 25 l-15 25Z" fill="#fff"/>')
            elif acc == "barrel":
                N.append(f'<path d="M{HX-200} 720 Q{HX} 800 {HX+200} 720" stroke="#8B1E1E" stroke-width="22" fill="none"/>')
                N.append(path(f"M{HX-70} 790 H{HX+70} Q{HX+90} 860 {HX+70} 930 H{HX-70} Q{HX-90} 860 {HX-70} 790Z", "#A86B32"))
                N.append(f'<path d="M{HX-75} 815 H{HX+75} M{HX-75} 905 H{HX+75}" stroke="#5B3A1A" stroke-width="10"/>')
            elif acc in ("medal", "badge"):
                N.append(f'<path d="M{HX-80} 700 L{HX} 820 L{HX+80} 700" stroke="#2E5E8C" stroke-width="22" fill="none"/>')
                N.append(ell(HX, 850, 42, 42, "#F2C230")); N.append(f'<text x="{HX}" y="866" font-size="44" text-anchor="middle" fill="#9C7A12" font-family="sans-serif">★</text>')
            elif acc == "pearls":
                for i in range(15):
                    t = math.pi * (0.1 + 0.8 * i / 14)
                    N.append(ell(HX - 220 * math.cos(t), 700 + 90 * math.sin(t), 16, 16, "#FFFDF5"))
            elif acc == "chain":
                for i in range(13):
                    t = math.pi * (0.1 + 0.8 * i / 12)
                    N.append(f'<ellipse cx="{HX-230*math.cos(t):.0f}" cy="{705+95*math.sin(t):.0f}" rx="18" ry="11" fill="none" stroke="#E5B83A" stroke-width="8"/>')
            elif acc == "tactical":
                N.append(path(f"M{HX-280} 1000 Q{HX-270} 780 {HX-150} 730 L{HX+150} 730 Q{HX+270} 780 {HX+280} 1000Z", "#3B4A35"))
                N.append(f'<rect x="{HX-70}" y="820" width="140" height="60" rx="8" fill="#2A3526"/><text x="{HX}" y="864" font-size="34" font-family="sans-serif" font-weight="800" text-anchor="middle" fill="#E8E4D0">K-9</text>')
            elif acc == "lifering":
                N.append(f'<circle cx="{HX}" cy="880" r="150" fill="none" stroke="#F25C3B" stroke-width="56"/>')
                for t in range(4):
                    a_ = t * math.pi / 2 + .6
                    N.append(f'<path d="M{HX+122*math.cos(a_):.0f} {880+122*math.sin(a_):.0f} L{HX+178*math.cos(a_):.0f} {880+178*math.sin(a_):.0f}" stroke="#fff" stroke-width="40"/>')
            elif acc == "cape":
                N.append(path(f"M{HX-180} 700 Q{HX-420} 900 {HX-380} 1000 H{HX+380} Q{HX+420} 900 {HX+180} 700 Q{HX} 760 {HX-180} 700Z", "#B3261E"))
                N.append(ell(HX, 720, 30, 30, "#F2C230"))
        if acc == "teddy":
            N.append(f'<g transform="translate({HX+230},800)">' + ell(-55, -70, 30, 30, "#B07A4A") + ell(55, -70, 30, 30, "#B07A4A") + ell(0, 30, 100, 110, "#B07A4A") + ell(0, -40, 80, 70, "#B07A4A") + ell(-25, -45, 8, 8, "#222", False) + ell(25, -45, 8, 8, "#222", False) + ell(0, -20, 26, 18, "#E2C29B") + "</g>")
        if acc == "tennis":
            N.append(f'<g transform="translate({HX+250},860)">' + ell(0, 0, 70, 70, "#D7F04A") + '<path d="M-60 -30 Q0 0 -60 40 M60 -40 Q0 0 60 30" stroke="#fff" stroke-width="8" fill="none"/></g>')
        if acc in ("newspaper", "pen", "teacup", "blanket", "candycane", "lights"):
            if acc == "newspaper":
                N.append(f'<g transform="translate({HX},880) rotate(-6)"><rect x="-230" y="-60" width="460" height="200" fill="#F4F1EA" stroke="{OUT}" stroke-width="7"/>'
                         f'<text x="0" y="-12" text-anchor="middle" font-family="serif" font-size="40" font-weight="800" fill="#222">DAILY BARK</text>'
                         + "".join(f'<rect x="-200" y="{10+i*24}" width="{180 if i%2 else 400}" height="10" fill="#9A958A"/>' for i in range(4)) + "</g>")
            elif acc == "pen":
                N.append(f'<rect x="{HX-300}" y="880" width="600" height="160" fill="#5B3A22" stroke="{OUT}" stroke-width="7"/><path d="M{HX+120} 870 l80 -70" stroke="#222" stroke-width="16" stroke-linecap="round"/>')
            elif acc == "teacup":
                N.append(f'<g transform="translate({HX+250},880)">' + path("M-70 -40 H70 Q65 60 0 70 Q-65 60 -70 -40Z", "#F7F3EA") + '<path d="M70 -10 q40 0 30 40 q-10 25 -35 20" stroke="#2B1E16" stroke-width="7" fill="none"/>' + ell(0, 80, 110, 18, "#F7F3EA") + "</g>")
            elif acc == "blanket":
                N.append(path(f"M{HX-360} 1000 Q{HX-330} 720 {HX-120} 700 Q{HX} 760 {HX+120} 700 Q{HX+330} 720 {HX+360} 1000Z", "#7FA7C9"))
                for i in range(-4, 5):
                    N.append(f'<path d="M{HX+i*70} 760 V1000" stroke="#fff" stroke-width="10" stroke-opacity=".4"/>')
            elif acc == "candycane":
                N.append(f'<g transform="translate({HX+180},780) rotate(15)"><path d="M0 220 V0 Q0 -60 50 -60 Q100 -60 100 0" stroke="#fff" stroke-width="34" fill="none" stroke-linecap="round"/>'
                         f'<path d="M0 220 V0 Q0 -60 50 -60 Q100 -60 100 0" stroke="#D62E2E" stroke-width="34" stroke-dasharray="22 22" fill="none"/></g>')
            elif acc == "lights":
                pts = [(HX - 300 + i * 50, 760 + 40 * math.sin(i)) for i in range(13)]
                N.append(f'<path d="M' + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + '" stroke="#2C4A30" stroke-width="6" fill="none"/>')
                for i, (x, y) in enumerate(pts):
                    col = ["#FF4D4D", "#FFD23F", "#3BCEAC", "#4D96FF"][i % 4]
                    N.append(ell(x, y + 18, 12, 18, col))

    paw_col = WHITE if pat in ("blaze", "tricolor", "husky", "stbernard", "boxer", "patches", "tripatches", "oes", "spots", "harlequin") else (c2 if pat in ("tanpoints", "yorkie", "urajiro") else light(coat, .08))
    if not any(a_ in ("sweater", "blanket", "tactical", "lifering", "cape") for a_ in accs):
        for sgn in (-1, 1):
            N.append(ell(HX + sgn * 125, 935, 78, 50, paw_col))
            for k in (-1, 0, 1):
                N.append(f'<path d="M{HX + sgn*125 + k*24:.0f} 910 v22" stroke="{OUT}" stroke-width="5" stroke-linecap="round"/>')
    rot = f'rotate({tilt} {HX} {HY + ry * 0.6})'
    return "".join(out) + "".join(N) + f'<g transform="{rot}">' + "".join(g) + "".join(A) + "</g>"


def portrait_svg(name, seed=0, size=1000, scene=None, acc=None, expr=None, extra=""):
    spec = SPECS[name]
    W = H = 1000
    bg = scene_svg(scene or spec["scene"], W, H, seed)
    dog = dog_svg(spec, seed, acc, expr)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{size}" height="{size}">'
            f'{bg}<g transform="translate(0,40)">{dog}</g>{extra}</svg>')


def group_svg(names, W, H, scene, seed, accs=None, exprs=None, rows=1, extra="", spread=700):
    """Several dogs side by side (rows=2 puts a smaller back row)."""
    bg = scene_svg(scene, W, H, seed)
    parts = []
    n = len(names)
    if rows == 1:
        sc = min(W / (n * 820), H / 1050)
        for i, nm in enumerate(names):
            x = W * (i + .5) / n - 500 * sc
            y = H - 1000 * sc + 10
            parts.append((f'<g transform="translate({x:.1f},{y:.1f}) scale({sc:.3f})">', nm, i))
    else:
        k = (n - 1) // 2
        back, front = names[:k], names[k:]
        m = len(front)
        sf = min(W / (m * spread), H / 880)
        sb = sf * 0.84
        yf = H - 1000 * sf + 90 * sf
        yb = yf - 300 * sb
        gaps = [round((j + .5) * (m - 1) / k - .5) for j in range(k)]
        for j, nm in enumerate(back):
            cx = W * (gaps[j] + 1) / m
            parts.append((f'<g transform="translate({cx - 500*sb:.1f},{yb:.1f}) scale({sb:.3f})">', nm, j))
        for i, nm in enumerate(front):
            cx = W * (i + .5) / m
            parts.append((f'<g transform="translate({cx - 500*sf:.1f},{yf:.1f}) scale({sf:.3f})">', nm, i + 10))
    body = []
    for tr, nm, i in parts:
        a = (accs or {}).get(nm)
        e = (exprs or {}).get(nm)
        body.append(tr + dog_svg(SPECS[nm], seed * 31 + i, a, e) + "</g>")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{bg}{"".join(body)}{extra}</svg>'
