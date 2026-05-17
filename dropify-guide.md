# Dropify Integration Guide — LILA Store

## What is Dropify?
Dropify is the leading Shopify dropshipping app for the Moroccan/MENA market. It connects you with local suppliers, handles product sourcing, inventory syncs, and order fulfillment.

---

## Step 1: Install Dropify
1. Go to **Shopify App Store** → Search "Dropify"
2. Install the app
3. Create account (use same email as Shopify)
4. Select plan: Free (14 days) → Basic (299 MAD/mo) or Pro (599 MAD/mo)

---

## Step 2: Find LILA Product on Dropify
Search for these suppliers/products on Dropify:

### Product Search Terms
```
- "Silk pillowcase" / "مخدة حرير"
- "Mulberry silk pillowcase"
- "Pillowcase 50x70 silk"
- "Premium silk pillowcase Morocco"
- "Taie d'oreiller en soie"
- "غطاء مخدة حرير"
```

### Supplier Criteria
| Requirement | Must Have |
|------------|-----------|
| Location | Morocco (local supplier) |
| Stock | 50+ units minimum |
| Shipping | COD compatible |
| Shipping Time | 2-5 days |
| Return Rate | < 5% |
| Quality | 4+ star rating on Dropify |

### Product Specs to Verify
- **Material**: 100% Mulberry Silk (not satin/polyester)
- **Size**: 50×70 cm (standard Moroccan pillow)
- **Colors**: Champagne gold, Dusty rose, Pearl white
- **Weight**: ~100g per pillowcase
- **Price**: 30-50 MAD ($3-5) sourcing
- **MOQ**: 1 unit (for testing, then stock 50+)

---

## Step 3: Import Product to Shopify with Dropify

### Import Workflow
```
Dropify Dashboard
  ↓
"Import Products" → Search product
  ↓
Click "Import to Store" (Sync to Shopify)
  ↓
Select product category: Home & Beauty
  ↓
Map variants: Color, Size (if any)
  ↓
Set your retail price: 199 MAD
  ↓
"Import" — product now in your Shopify admin
```

### After Import — Customize the Product
1. Go to **Shopify Admin → Products** → Find the imported product
2. Update **Title** to: "LILA Premium Silk Pillowcase — مخدة الحرير الفاخرة"
3. Update **Description** with your Darija copy (see locale file)
4. Add **SEO**: Title — "مخدة حرير فاخرة | LILA Silk Pillowcase Morocco | 199 MAD"
5. Add tags: silk, pillowcase, beauty, morocco, حرير, مخدة, جمال
6. If multiple colors: create a "Color" variant option

### Pricing Strategy
| Item | Amount |
|------|--------|
| Cost from Dropify | 45 MAD |
| Shipping (COD) | 39 MAD |
| Selling Price | 199 MAD |
| **Gross Profit** | **115 MAD per unit** |
| **Margin** | **~58%** |

---

## Step 4: Configure Dropify Settings

### General Settings
```
Auto-import orders: YES
Order status sync: YES
Tracking number sync: YES
Inventory sync: Daily
COD handling: Enable
Shipping: Enable all Moroccan cities
```

### Shipping Rules in Dropify
```
Standard: 39 MAD — 3-5 business days (all Morocco)
Free: Over 299 MAD (2+ pillows)
Express: 59 MAD — 1-2 days (Casablanca, Rabat, Marrakech)
```

### COD Settings
```
Enable COD: YES
Minimum order: 50 MAD
Maximum order: 2000 MAD
COD fee: 19 MAD (can absorb or pass to customer)
```

---

## Step 5: Order Fulfillment Workflow

### When an order comes in:
1. **Order received** in Shopify (automatically)
2. **Dropify** detects the order and shows it in dashboard
3. **Supplier** receives order notification
4. **Supplier** packages LILA pillow with your branding
5. **Supplier** hands to courier (COD)
6. **Customer** receives → pays cash → delivery confirmed
7. **Dropify** syncs tracking number back to Shopify
8. **Automated email** sent to customer with tracking

### If a COD order is rejected (customer refuses):
1. Dropify marks as "Failed Delivery"
2. Supplier returns item to stock
3. You can retarget with WhatsApp "شنو المشكل؟"

---

## Step 6: Branding with Dropify Suppliers

Ask your Dropify supplier for:
- **Custom packaging**: Gold LILA box + silk ribbon (extra 15 MAD/unit)
- **Insert card**: Small card with LILA branding + care instructions
- **Thank you note**: "شكرًا على ثقتك في LILA — نتمنى نومة هانية"
- **Deluxe option**: Pre-folded silk pillow in a gift box with ribbon

If supplier can't do custom packaging:
- Order packaging separately from a local printer
- Use 3rd party fulfillment service that does kitting

---

## Best Shopify Apps Compatible with Dropify

### Essential (Must-Have)
| App | Purpose | Price | Link |
|-----|---------|-------|------|
| **Dropify** | Product sourcing & fulfillment | 299 MAD/mo | Shopify App Store |
| **WhatsApp Chat +** | WhatsApp integration | Free | Shopify App Store |
| **TinyIMG** | Image compression + SEO | Free/$ | Shopify App Store |
| **PageFly** | Landing page builder (if not using Dawn) | Free/24$ | Shopify App Store |

### Conversion Optimization
| App | Purpose | Price |
|-----|---------|-------|
| **Loox** | Photo reviews UGC | Free/10$ |
| **Sales Pop** | Recent purchase notifications | Free/5$ |
| **Countdown Cart** | Abandoned cart recovery | Free/7$ |
| **Frequently Bought Together** | Bundle upsells | Free/10$ |
| **Selly** | COD order management | 149 MAD/mo |
| **Bundler** | Discounted bundles for upsells | Free/6$ |

### Marketing
| App | Purpose | Price |
|-----|---------|-------|
| **TikTok** | TikTok Pixel + ads | Free |
| **Facebook & Instagram** | Meta Pixel + shop | Free |
| **Mailchimp** | Email marketing | Free/13$ |
| **Omnisend** | SMS + email automation | Free/16$ |
| **Back in Stock** | Restock alerts | Free/10$ |

### Trust & Conversion
| App | Purpose | Price |
|-----|---------|-------|
| **Trust Badges** | Trust seals | Free |
| **Judge.me** | Review widget (alternative to Loox) | Free/15$ |
| **Stamped.io** | Reviews + Q&A + loyalty | Free/23$ |
| **Nudgify** | Social proof notifications | Free/19$ |

---

## Shopify Theme: Dawn — Customization for LILA

### Why Dawn?
- **Free** (no extra cost)
- **Fast**: Google PageSpeed 90+ on mobile
- **Flexible**: Sections everywhere — JSON templates
- **Dropify compatible**: Works out of the box
- **Mobile-first**: Built for mobile shopping
- **All features**: Sticky header, mega menu, product media

### Customization Steps
1. **Add LILA logo** (see brand-guide.md)
2. **Set fonts**: Playfair Display + Montserrat + Tajawal
3. **Set colors**: See brand palette in brand-guide.md
4. **Add custom CSS** from `assets/theme.css`
5. **Add custom JS** from `assets/theme.js`
6. **Create sections** from the files in the `sections/` directory
7. **Upload** product images (high quality, white background + lifestyle)
8. **Set up homepage** using `templates/index.json` structure
9. **Add WhatsApp** button + sticky ATC
10. **Test** on mobile, tablet, desktop

### Theme Settings Summary
```json
{
  "typography_preset": "custom",
  "heading_font": "Playfair Display",
  "body_font": "Montserrat",
  "color_scheme": "custom",
  "primary_color": "#C4956A",
  "secondary_color": "#2D2D2D",
  "background_color": "#FFFCF9",
  "button_style": "solid",
  "button_shape": "rounded",
  "product_card_style": "standard",
  "enable_sticky_header": true,
  "enable_quick_add": true,
  "enable_product_image_zoom": true
}
```

---

## Dropify Order Management Tips for Morocco

1. **COD Rejections**: Morocco has ~15-25% COD rejection. Budget for this. Have a WhatsApp retargeting flow for rejected orders.
2. **Friday deliveries**: Courier COD collections are harder on Friday/Jumu'ah. Prefer Saturday-Wednesday delivery windows.
3. **Ramadan effect**: Bedtime changes during Ramadan. Marketing shifts to "suhoor to fajr sleep" angle. Orders spike after Iftar.
4. **Aid Al-Adha / Eid**: 3-5 day shipping delays. Plan inventory accordingly.
5. **Remote areas**: Some villages can't do COD. Check Dropify's coverage map.

### Best Cities for COD in Morocco
| Tier | Cities | COD Success Rate |
|------|--------|------------------|
| ✅ Excellent | Casablanca, Rabat, Marrakech | 90%+ |
| ✅ Good | Tangier, Fes, Agadir, Safi | 85%+ |
| ⚠️ Medium | Oujda, Meknes, Kenitra, Tetouan | 75%+ |
| ⚠️ Check | Errachidia, Laayoune, Dakhla | 60-70% |
