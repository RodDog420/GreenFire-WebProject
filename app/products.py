"""
products.py — File-driven product catalogue for Green Fire.

All product data lives here. Routes read from this file — no DB queries
for product display. The database handles transactions only (orders,
wishlists, reviews, users).

PRODUCT TYPES
    'heady'  — one-of-a-kind artistic pieces
    'prodo'  — production glass, regularly produced series
    'vape'   — vaporizers and accessories

SUBCATEGORIES (prodo)
    'dry-pipes' | 'bubblers' | 'beakers' | 'oil-rigs'

SUBCATEGORIES (vape)
    'vaporizers' | 'flower-accessories' | 'oil-accessories'

CREDIT LABELS
    Set credit_label per product: 'Artist', 'Studio', 'Brand',
    'Manufacturer', or None. If credit is None, nothing renders.

IMAGE SYSTEM
    Each product has an image_folder field pointing to a folder
    inside app/static/. Images inside must follow the naming
    convention:

        {FolderName}_1.jpg   ← primary image (always _1)
        {FolderName}_2.jpg   ← additional image
        {FolderName}_3.jpg   ← additional image
        etc.

    Supported extensions: .jpg .jpeg .png .webp

    The resolve_images() function scans the folder at startup,
    sorts by number, and populates primary_image and images
    automatically. No manual path management needed.

    To add a new photo: drop a correctly named file into the
    folder and restart Flask.
    To swap a photo: replace the file and restart Flask.

ADDING A PRODUCT
    1. Create a folder in static/images/<type>/<FolderName>/
    2. Add images named <FolderName>_1.jpg, _2.jpg, etc.
    3. Add an entry to the PRODUCTS list below.
    4. Set is_active: True to make it live.
    5. Set is_sold: True when the piece sells.

SLUG CONVENTION
    heady:  artist-lastname-piece-description  e.g. josh-mann-uptake-rig
    prodo:  brand-model-descriptor             e.g. us-tubes-beaker-14mm
    vape:   brand-model                        e.g. storz-bickel-mighty-plus
    unknown heady: descriptive-piece-name      e.g. worked-spoon-blue-fume

HEADY-SPECIFIC FIELDS
    series              — named series or collection (string or None)
    glass_color         — rod/tube color name (string or None)
    glass_color_company — rod manufacturer e.g. 'Northstar' (string or None)
    gemstones           — gemstone accents present (bool)
    electroform         — electroformed (bool)
    fume                — fumed (bool)
    collab              — collaborating artist name (string or None)

PRODO-SPECIFIC FIELDS
    perc                — percolator type e.g. 'showerhead' (string or None)
    fume                — fumed (bool)
    reclaimer           — includes reclaimer (bool)
    includes            — physical item(s) included with purchase e.g. 'glass bowl' (string or None)
    variants            — selectable options e.g. ['Red', 'Blue', 'Green'] (list or None)

VAPE-SPECIFIC FIELDS
    attributes          — list of descriptors e.g. ['convection', 'dual-use']
    metal_type          — e.g. 'titanium', 'stainless steel' (string or None)
    is_premium          — premium tier product (bool)
"""

import os
import re

_STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


# ==========================================================================
# IMAGE AUTO-DISCOVERY
# ==========================================================================

def resolve_images(image_folder):
    """
    Scans image_folder (relative to static/) for files named
    {anything}_{number}.{ext}, sorted by number.

    Returns (primary_path, [additional_paths]) as static-relative
    forward-slash strings for use with url_for('static', filename=...).
    Returns (None, []) if the folder is missing or has no numbered files.
    """
    if not image_folder:
        return None, []

    folder_abs = os.path.join(_STATIC_DIR, image_folder.replace('/', os.sep))
    if not os.path.isdir(folder_abs):
        return None, []

    numbered = []
    for fname in os.listdir(folder_abs):
        name, ext = os.path.splitext(fname)
        if ext.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
            continue
        match = re.search(r'_(\d+)$', name)
        if match:
            numbered.append((int(match.group(1)), fname))

    numbered.sort(key=lambda x: x[0])
    if not numbered:
        return None, []

    base = image_folder.rstrip('/')

    primary    = base + '/' + numbered[0][1]
    additional = [base + '/' + fname for _, fname in numbered[1:]]
    return primary, additional


PRODUCTS = [

    # ------------------------------------------------------------------
    # HEADY
    # ------------------------------------------------------------------
    {
        'slug':                'amy-likes-fire-purple-pony',
        'name':                'Purple Pony',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              "Amy's Ponies",
        'credit_label':        'Artist',
        'credit':              'Amy Likes Fire',
        'instagram':           'amylikesfire',
        'collab':              None,
        'price_cents':         650000,
        'height':              '7 inches',
        'technique':           None,
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           True,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Amy_Likes_Fire',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'creep-ganesh',
        'name':                'Ganesh',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Creep',
        'instagram':           'creepglass',
        'collab':              None,
        'price_cents':         1350000,
        'height':              '12 inches',
        'technique':           None,
        'joint_size':          '18mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Creep_Ganesh',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'creep-totem',
        'name':                'Totem',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Creep',
        'instagram':           'creepglass',
        'collab':              None,
        'price_cents':         600000,
        'height':              '12 inches',
        'technique':           'Reticello',
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Creep_Totem',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'emperial-runtz-bottle',
        'name':                'Runtz Swiss Baby Bottle',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Emperial Glass',
        'instagram':           'emperial1',
        'collab':              'High-Tech',
        'price_cents':         750000,
        'height':              '12 inches',
        'technique':           'Swiss-perc',
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Emperial_Runtz',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'emperial-sour-patch-kidz-bottle',
        'name':                'Sour Patch Kidz Swiss Baby Bottle',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Emperial Glass',
        'instagram':           'emperial1',
        'collab':              'High-Tech',
        'price_cents':         750000,
        'height':              '12 inches',
        'technique':           'Swiss-perc',
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Emperial_SourPatchKids',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'glassfish-ewok',
        'name':                'Ewok',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'TheGlassFish13',
        'instagram':           'theglassfish13',
        'collab':              None,
        'price_cents':         1000000,
        'height':              '8 inches',
        'technique':           None,
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Ewok',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'jedi-jack-skillington',
        'name':                'Jack Skillington Rig',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Jedi Glass',
        'instagram':           'jediglassworks',
        'collab':              None,
        'price_cents':         120000,
        'height':              '14 inches',
        'technique':           None,
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Jedi_Jack',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'jenkins-bonzai-tree',
        'name':                'Bonzai Tree',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Ryan Jenkins',
        'instagram':           'thinkins_glass',
        'collab':              None,
        'price_cents':         1000000,
        'height':              '16 inches',
        'technique':           None,
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         True,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Jenkins_Bonzai',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'jenkins-reef-rig',
        'name':                'Reef Rig',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Ryan Jenkins',
        'instagram':           'thinkins_glass',
        'collab':              None,
        'price_cents':         1500000,
        'height':              '12 inches',
        'technique':           None,
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         True,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Jenkins_Coral',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'josh-mann-uptake-rig',
        'name':                'Uptake Rig',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Josh Mann',
        'instagram':           'joshmann_glass',
        'collab':              None,
        'price_cents':         45000,
        'height':              '8 inches',
        'technique':           'worked, fumed',
        'joint_size':          '14mm',
        'glass_color':         'cobalt',
        'glass_color_company': 'Northstar',
        'gemstones':           False,
        'electroform':         False,
        'fume':                True,
        'description':         '',
        'image_folder':        'images/heady/Josh_Mann_Uptake_Rig',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'merc-blue-minion',
        'name':                'Blue Minion',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Merc',
        'instagram':           'minion_cca',
        'collab':              None,
        'price_cents':         1500000,
        'height':              '10 inches',
        'technique':           None,
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           True,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Merc_Minion_Blue',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'merc-alien-tech-minion',
        'name':                'Alien-Tech Minion',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Merc',
        'instagram':           'minion_cca',
        'collab':              None,
        'price_cents':         1500000,
        'height':              '10 inches',
        'technique':           None,
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           True,
        'electroform':         False,
        'fume':                False,
        'description':         '',
        'image_folder':        'images/heady/Merc_Minion_Green-Gold',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    {
        'slug':                'opinicus-o-ring-rig',
        'name':                'O-ring Rig',
        'product_type':        'heady',
        'subcategory':         None,
        'series':              None,
        'credit_label':        'Artist',
        'credit':              'Opinicus',
        'instagram':           'opinicus9',
        'collab':              None,
        'price_cents':         800000,
        'height':              '8 inches',
        'technique':           'Sandblasting and frosting',
        'joint_size':          '14mm',
        'glass_color':         None,
        'glass_color_company': None,
        'gemstones':           False,
        'electroform':         False,
        'fume':                True,
        'description':         '',
        'image_folder':        'images/heady/Opinicus',
        'is_sold':             False,
        'is_active':           True,
        'meta_description':    None,
    },

    # ------------------------------------------------------------------
    # PRODO
    # ------------------------------------------------------------------

    # OIL RIGS

    {
        'slug':             'borofarm-bell-rig',
        'name':             'BoroFarm Bell Rig',
        'product_type':     'prodo',
        'subcategory':      'oil-rigs',
        'series':           None,
        'credit_label':     'Brand',
        'credit':           'BoroFarm',
        'instagram':        'borofarm',
        'collab':           None,
        'price_cents':      25000,
        'height':           '8 inches',
        'technique':        None,
        'joint_size':       '14mm',
        'perc':             'Showerhead',
        'fume':             False,
        'reclaimer':        False,
        'includes':         'Quartz nail',
        'variants':         None,
        'description':      '',
        'image_folder':     'images/prodo/BoroFarm_bell-rig',
        'is_sold':          False,
        'is_active':        True,
        'meta_description': None,
    },

    {
        'slug':             'joshmann-banger-ground-joint',
        'name':             'J-Mann Banger w/ Ground Joint',
        'product_type':     'prodo',
        'subcategory':      'oil-rigs',
        'series':           None,
        'credit_label':     'Artist',
        'credit':           'Josh Mann',
        'instagram':        'joshmann_glass',
        'collab':           None,
        'price_cents':      15000,
        'height':           '8 inches',
        'technique':        None,
        'joint_size':       '14mm Ground Joint',
        'perc':             'Three hole diffusion',
        'fume':             False,
        'reclaimer':        False,
        'includes':         '14mm Quartz Nail',
        'variants':         None,
        'description':      '',
        'image_folder':     'images/prodo/joshmann_14mm_ground-joint',
        'is_sold':          False,
        'is_active':        True,
        'meta_description': None,
    },

    {
        'slug':             'joshmann-clear-banger',
        'name':             'J-Mann Clear Banger',
        'product_type':     'prodo',
        'subcategory':      'oil-rigs',
        'series':           None,
        'credit_label':     'Artist',
        'credit':           'Josh Mann',
        'instagram':        'joshmann_glass',
        'collab':           None,
        'price_cents':      15000,
        'height':           '8 inches',
        'technique':        None,
        'joint_size':       '14mm',
        'perc':             'Three hole diffusion',
        'fume':             False,
        'reclaimer':        False,
        'includes':         '14mm Quartz Nail',
        'variants':         None,
        'description':      '',
        'image_folder':     'images/prodo/joshmann_clear_rig',
        'is_sold':          False,
        'is_active':        True,
        'meta_description': None,
    },

    {
        'slug':             'joshmann-gold-fume-banger',
        'name':             'J-Mann Gold Fume Banger',
        'product_type':     'prodo',
        'subcategory':      'oil-rigs',
        'series':           None,
        'credit_label':     'Artist',
        'credit':           'Josh Mann',
        'instagram':        'joshmann_glass',
        'collab':           None,
        'price_cents':      15000,
        'height':           '8 inches',
        'technique':        None,
        'joint_size':       '14mm',
        'perc':             'Three hole diffusion',
        'fume':             True,
        'reclaimer':        False,
        'includes':         '14mm Quartz Nail',
        'variants':         None,
        'description':      '',
        'image_folder':     'images/prodo/joshmann_gold_fume',
        'is_sold':          False,
        'is_active':        True,
        'meta_description': None,
    },

    {
        'slug':             'joshmann-straight-rig',
        'name':             'J-Mann Straight Rig',
        'product_type':     'prodo',
        'subcategory':      'oil-rigs',
        'series':           None,
        'credit_label':     'Artist',
        'credit':           'Josh Mann',
        'instagram':        'joshmann_glass',
        'collab':           None,
        'price_cents':      15000,
        'height':           '8 inches',
        'technique':        None,
        'joint_size':       '14mm',
        'perc':             'Three hole diffusion',
        'fume':             True,
        'reclaimer':        False,
        'includes':         '14mm Quartz Nail',
        'variants':         None,
        'description':      '',
        'image_folder':     'images/prodo/joshmann_upright',
        'is_sold':          False,
        'is_active':        True,
        'meta_description': None,
    },

    # DRY PIPES

    {
        'slug':             'joshmann-spoons',
        'name':             'J-Mann Spoons',
        'product_type':     'prodo',
        'subcategory':      'dry-pipes',
        'series':           None,
        'credit_label':     'Artist',
        'credit':           'Josh Mann',
        'instagram':        'joshmann_glass',
        'collab':           None,
        'price_cents':      2800,
        'height':           '4.5 inches',
        'technique':        None,
        'joint_size':       None,
        'perc':             'Carb hole',
        'fume':             False,
        'reclaimer':        False,
        'includes':         None,
        'variants':         [
            'Orange', 'Red', 'Green', 'Blue',
            'Purple', 'Yellow', 'Black',
            'Gold Fume', 'Silver Fume',
        ],
        'description':      '',
        'image_folder':     'images/prodo/joshmann_spoons',
        'is_sold':          False,
        'is_active':        True,
        'meta_description': None,
    },

    # ------------------------------------------------------------------
    # VAPE / ACCESSORY
    # ------------------------------------------------------------------

    {
        'slug':             'gf-510-thread-battery',
        'name':             'Screw-on 510 Thread Vape Battery',
        'product_type':     'vape',
        'subcategory':      'oil-accessories',
        'series':           None,
        'credit_label':     'Brand',
        'credit':           'Green Fire',
        'instagram':        None,
        'collab':           None,
        'price_cents':      2000,
        'height':           None,
        'technique':        None,
        'joint_size':       None,
        'attributes':       ['900 mAh'],
        'metal_type':       None,
        'is_premium':       False,
        'includes':         'Micro-USB Cable',
        'description':      '',
        'image_folder':     'images/accessories/Vapes/GF_510-thread',
        'is_sold':          False,
        'is_active':        True,
        'meta_description': None,
    },

    {
        'slug':             'pbi-vape-battery',
        'name':             'PBI Vape Battery',
        'product_type':     'vape',
        'subcategory':      'oil-accessories',
        'series':           None,
        'credit_label':     'Brand',
        'credit':           'Hamilton Devices',
        'instagram':        None,
        'collab':           None,
        'price_cents':      7500,
        'height':           None,
        'technique':        None,
        'joint_size':       None,
        'attributes':       ['510 thread', '900 mAh'],
        'metal_type':       None,
        'is_premium':       False,
        'includes':         None,
        'description':      '',
        'image_folder':     'images/accessories/Vapes/PBI_vape',
        'is_sold':          False,
        'is_active':        True,
        'meta_description': None,
    },

]


# ==========================================================================
# STARTUP — resolve images for all products once at import time
# ==========================================================================

for _p in PRODUCTS:
    _primary, _additional = resolve_images(_p.get('image_folder'))
    _p['primary_image'] = _primary
    _p['images']        = _additional


# ==========================================================================
# META DESCRIPTION GENERATION
# ==========================================================================

_SUBCATEGORY_LABELS = {
    'dry-pipes':          'dry pipe',
    'bubblers':           'bubbler',
    'beakers':            'beaker',
    'oil-rigs':           'oil rig',
    'vaporizers':         'vaporizer',
    'flower-accessories': 'flower accessory',
    'oil-accessories':    'oil accessory',
}

_META_SUFFIX_HEADY = ' — heady glass at Green Fire, Lincoln NE.'
_META_SUFFIX_PRODO = ' — American production glass at Green Fire, Lincoln NE.'
_META_SUFFIX_VAPE  = ' at Green Fire, Lincoln NE.'

_META_LIMIT = 155


def _build_meta(base, specs, suffix):
    """
    Greedily append spec strings to base while staying within _META_LIMIT.
    Each spec is tried in order — appended only if the full result
    (accumulated + ', ' + spec + suffix) still fits within the limit.
    Returns accumulated specs joined to base, followed by suffix.
    """
    result = base
    for spec in specs:
        candidate = result + ', ' + spec + suffix
        if len(candidate) <= _META_LIMIT:
            result += ', ' + spec
    return result + suffix


def _meta_heady(p):
    if p.get('credit'):
        base = p['credit'] + ' ' + p['name']
    else:
        base = p['name']

    specs = []
    if p.get('technique'):
        specs.append(p['technique'])
    if p.get('glass_color'):
        color = p['glass_color']
        if p.get('glass_color_company'):
            color += ' (' + p['glass_color_company'] + ')'
        specs.append(color)
    if p.get('gemstones'):
        specs.append('gemstone accents')
    if p.get('electroform'):
        specs.append('electroformed')
    if p.get('fume'):
        specs.append('fumed')
    if p.get('height'):
        specs.append(p['height'])
    if p.get('joint_size'):
        specs.append(p['joint_size'])

    return _build_meta(base, specs, _META_SUFFIX_HEADY)


def _meta_prodo(p):
    if p.get('credit'):
        base = p['credit'] + ' ' + p['name']
    else:
        base = p['name']

    cat = _SUBCATEGORY_LABELS.get(p.get('subcategory') or '', '')
    if cat:
        base += ' ' + cat

    specs = []
    if p.get('perc'):
        specs.append(p['perc'])
    if p.get('height'):
        specs.append(p['height'])
    if p.get('joint_size'):
        specs.append(p['joint_size'])
    if p.get('fume'):
        specs.append('fumed')
    if p.get('reclaimer'):
        specs.append('with reclaimer')

    return _build_meta(base, specs, _META_SUFFIX_PRODO)


def _meta_vape(p):
    if p.get('credit'):
        base = p['credit'] + ' ' + p['name']
    else:
        base = p['name']

    cat = _SUBCATEGORY_LABELS.get(p.get('subcategory') or '', '')
    if cat:
        base += ' ' + cat

    specs = []
    if p.get('attributes'):
        specs.extend(p['attributes'])
    if p.get('metal_type'):
        specs.append(p['metal_type'])
    if p.get('is_premium'):
        specs.append('premium')

    return _build_meta(base, specs, _META_SUFFIX_VAPE)


def auto_meta_description(p):
    """
    Auto-generate a meta description for a product dict.
    Respects the explicit meta_description field — only call this
    when that field is absent or None.
    Selects the correct sub-formula by product_type.
    Output stays within _META_LIMIT (155) characters.
    """
    ptype = p.get('product_type', '')
    if ptype == 'heady':
        return _meta_heady(p)
    elif ptype == 'prodo':
        return _meta_prodo(p)
    else:
        return _meta_vape(p)


# ==========================================================================
# HELPER FUNCTIONS
# ==========================================================================

def get_headies():
    """
    Active, unsold heady pieces sorted alphabetically by credit name.
    Pieces with no credit sort to the end.
    Sold pieces are excluded — they appear only in the archive.
    """
    pieces = [p for p in PRODUCTS
              if p['product_type'] == 'heady'
              and p['is_active']
              and not p['is_sold']]
    return sorted(pieces, key=lambda p: (p['credit'] is None, p['credit'] or ''))


def get_sold_headies():
    """
    All sold heady pieces for the archive page, sorted alphabetically
    by credit name. Pieces with no credit sort to the end.
    """
    pieces = [p for p in PRODUCTS
              if p['product_type'] == 'heady' and p['is_sold']]
    return sorted(pieces, key=lambda p: (p['credit'] is None, p['credit'] or ''))


def get_prodos():
    """
    All active prodo pieces. Returned unsorted — the /prodos template
    groups them by subcategory using Jinja2 logic.
    """
    return [p for p in PRODUCTS
            if p['product_type'] == 'prodo' and p['is_active']]


def get_vapes_accessories():
    """
    All active vape and accessory products. Returned unsorted — the
    /vapes-accessories template groups them by subcategory.
    """
    return [p for p in PRODUCTS
            if p['product_type'] == 'vape' and p['is_active']]


def get_product(slug):
    """
    Return a single product dict by slug, or None if not found.
    Includes sold and inactive products — the template handles display.
    """
    for product in PRODUCTS:
        if product['slug'] == slug:
            return product
    return None


def get_product_neighbours(slug):
    """
    Returns (prev_product, next_product) for prev/next navigation on
    the product detail page. Navigation stays within the same list
    the product appears in:
      - Unsold heady  → get_headies() order
      - Sold heady    → get_sold_headies() order
      - Prodo         → get_prodos() order
      - Vape          → get_vapes_accessories() order
    Returns None at list boundaries.
    """
    product = get_product(slug)
    if not product:
        return None, None

    ptype = product['product_type']
    if ptype == 'heady':
        catalogue = get_sold_headies() if product['is_sold'] else get_headies()
    elif ptype == 'prodo':
        catalogue = get_prodos()
    else:
        catalogue = get_vapes_accessories()

    slugs = [p['slug'] for p in catalogue]
    if slug not in slugs:
        return None, None

    idx    = slugs.index(slug)
    prev_p = catalogue[idx - 1] if idx > 0 else None
    next_p = catalogue[idx + 1] if idx < len(catalogue) - 1 else None
    return prev_p, next_p
