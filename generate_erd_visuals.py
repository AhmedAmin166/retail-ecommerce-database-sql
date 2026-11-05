import os
import sys
import pymupdf

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def build_erd_svg():
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0f1d"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#070a13"/>
    </linearGradient>

    <!-- Card Background Gradient -->
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <!-- Header Table Gradients -->
    <linearGradient id="hdrBlue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>

    <linearGradient id="hdrEmerald" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>

    <linearGradient id="hdrPurple" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7c3aed"/>
      <stop offset="100%" stop-color="#6d28d9"/>
    </linearGradient>

    <linearGradient id="hdrAmber" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#d97706"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>

    <linearGradient id="hdrRose" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#e11d48"/>
      <stop offset="100%" stop-color="#be123c"/>
    </linearGradient>

    <linearGradient id="hdrIndigo" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4f46e5"/>
      <stop offset="100%" stop-color="#3730a3"/>
    </linearGradient>

    <!-- Glow Filter -->
    <filter id="cardGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="12" stdDeviation="15" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
    <filter id="lineGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#38bdf8" flood-opacity="0.5"/>
    </filter>

    <!-- Markers for Cardinality (Crow's Foot & 1) -->
    <marker id="circleEnd" markerWidth="8" markerHeight="8" refX="4" refY="4">
      <circle cx="4" cy="4" r="3" fill="#38bdf8"/>
    </marker>
    <marker id="arrowEnd" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0 1 L8 5 L0 9 z" fill="#38bdf8"/>
    </marker>
  </defs>

  <!-- Canvas Background -->
  <rect width="1920" height="1080" fill="url(#bgGrad)"/>

  <!-- Subtle Blueprint Grid Pattern -->
  <g opacity="0.04" stroke="#ffffff" stroke-width="1">
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40"/>
    </pattern>
    <rect width="1920" height="1080" fill="url(#grid)"/>
  </g>

  <!-- ========================================================================= -->
  <!-- TOP BANNER & HEADER -->
  <!-- ========================================================================= -->
  <g transform="translate(80, 45)">
    <!-- Category Badge -->
    <rect x="0" y="0" width="280" height="28" rx="14" fill="#0369a1" fill-opacity="0.3" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="14" y="19" font-size="12" font-weight="700" fill="#38bdf8" letter-spacing="1.5">RELATIONAL DATABASE PORTFOLIO</text>

    <!-- Main Title -->
    <text x="0" y="68" font-size="34" font-weight="800" fill="#f8fafc" letter-spacing="-0.5">Retail &amp; E-Commerce Database Architecture (3NF)</text>
    <text x="0" y="96" font-size="16" fill="#94a3b8">Enterprise Schema Design, Referential Integrity, Business Constraints &amp; Analytical Query Optimization</text>

    <!-- Author Badge (Right Aligned) -->
    <g transform="translate(1380, 10)">
      <rect x="0" y="0" width="380" height="75" rx="14" fill="#1e293b" fill-opacity="0.8" stroke="#334155" stroke-width="1.5"/>
      <circle cx="45" cy="38" r="22" fill="#0284c7"/>
      <text x="45" y="44" font-size="17" font-weight="800" fill="#ffffff" text-anchor="middle">AF</text>
      <text x="80" y="32" font-size="16" font-weight="700" fill="#f8fafc">Ahmed Fikry</text>
      <text x="80" y="52" font-size="13" font-weight="500" fill="#38bdf8">Data &amp; BI Analyst | SQL Architect</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- RELATIONSHIP PATHS / CONNECTIONS (Drawn Behind Cards) -->
  <!-- ========================================================================= -->
  <g stroke="#38bdf8" stroke-width="2.5" fill="none" opacity="0.85" filter="url(#lineGlow)">
    <!-- 1. CATEGORIES to PRODUCTS (1:N) -->
    <!-- Categories right center: (420, 230) -> Products left center: (520, 260) -->
    <path d="M 420 230 C 470 230, 470 260, 520 260" marker-start="url(#circleEnd)" marker-end="url(#arrowEnd)"/>

    <!-- 2. PRODUCTS to INVENTORY (1:1) -->
    <!-- Products bottom center: (700, 460) -> Inventory top center: (700, 540) -->
    <path d="M 700 460 L 700 540" stroke-dasharray="6,4" marker-start="url(#circleEnd)" marker-end="url(#arrowEnd)"/>

    <!-- 3. CUSTOMERS to ORDERS (1:N) -->
    <!-- Customers right center: (420, 640) -> Orders left center: (960, 270) -->
    <path d="M 420 640 C 690 640, 690 270, 960 270" marker-start="url(#circleEnd)" marker-end="url(#arrowEnd)"/>

    <!-- 4. PRODUCTS to ORDER_ITEMS (1:N) -->
    <!-- Products right center: (880, 310) -> Order Items left: (960, 640) -->
    <path d="M 880 310 C 920 310, 920 640, 960 640" marker-start="url(#circleEnd)" marker-end="url(#arrowEnd)"/>

    <!-- 5. ORDERS to ORDER_ITEMS (1:N) -->
    <!-- Orders bottom center: (1140, 440) -> Order Items top center: (1140, 540) -->
    <path d="M 1140 440 L 1140 540" marker-start="url(#circleEnd)" marker-end="url(#arrowEnd)"/>

    <!-- 6. ORDER_ITEMS to RETURNS (1:0..1) -->
    <!-- Order Items right center: (1320, 660) -> Returns left center: (1440, 430) -->
    <path d="M 1320 660 C 1380 660, 1380 430, 1440 430" marker-start="url(#circleEnd)" marker-end="url(#arrowEnd)"/>
  </g>

  <!-- ========================================================================= -->
  <!-- ENTITY CARDS -->
  <!-- ========================================================================= -->

  <!-- 1. CATEGORIES TABLE (Col 1 Top) -->
  <g transform="translate(80, 160)" filter="url(#cardGlow)">
    <rect width="340" height="180" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <rect width="340" height="42" rx="12" fill="url(#hdrBlue)"/>
    <rect y="30" width="340" height="12" fill="url(#hdrBlue)"/>
    <text x="16" y="27" font-size="15" font-weight="700" fill="#ffffff">CATEGORIES</text>
    <text x="324" y="26" font-size="11" font-weight="600" fill="#e0f2fe" text-anchor="end">DIMENSION</text>
    
    <!-- Rows -->
    <text x="16" y="70" font-size="13" font-weight="700" fill="#38bdf8">PK  category_id</text>
    <text x="324" y="70" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="84" x2="324" y2="84" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="108" font-size="13" font-weight="600" fill="#f8fafc">UK  category_name</text>
    <text x="324" y="108" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(50)</text>
    <line x1="16" y1="122" x2="324" y2="122" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="146" font-size="13" fill="#cbd5e1">      description</text>
    <text x="324" y="146" font-size="12" fill="#94a3b8" text-anchor="end">TEXT</text>
  </g>

  <!-- 2. CUSTOMERS TABLE (Col 1 Bottom) -->
  <g transform="translate(80, 390)" filter="url(#cardGlow)">
    <rect width="340" height="470" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <rect width="340" height="42" rx="12" fill="url(#hdrIndigo)"/>
    <rect y="30" width="340" height="12" fill="url(#hdrIndigo)"/>
    <text x="16" y="27" font-size="15" font-weight="700" fill="#ffffff">CUSTOMERS</text>
    <text x="324" y="26" font-size="11" font-weight="600" fill="#e0e7ff" text-anchor="end">MASTER ENTITY</text>

    <!-- Rows -->
    <text x="16" y="70" font-size="13" font-weight="700" fill="#38bdf8">PK  customer_id</text>
    <text x="324" y="70" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="84" x2="324" y2="84" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="112" font-size="13" font-weight="600" fill="#f8fafc">      first_name</text>
    <text x="324" y="112" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(50)</text>
    <line x1="16" y1="126" x2="324" y2="126" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="154" font-size="13" font-weight="600" fill="#f8fafc">      last_name</text>
    <text x="324" y="154" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(50)</text>
    <line x1="16" y1="168" x2="324" y2="168" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="196" font-size="13" font-weight="600" fill="#a855f7">UK  email</text>
    <text x="324" y="196" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(100)</text>
    <line x1="16" y1="210" x2="324" y2="210" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="238" font-size="13" fill="#cbd5e1">      phone</text>
    <text x="324" y="238" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(25)</text>
    <line x1="16" y1="252" x2="324" y2="252" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="280" font-size="13" fill="#cbd5e1">      city (Indexed)</text>
    <text x="324" y="280" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(50)</text>
    <line x1="16" y1="294" x2="324" y2="294" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="322" font-size="13" fill="#cbd5e1">      state</text>
    <text x="324" y="322" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(50)</text>
    <line x1="16" y1="336" x2="324" y2="336" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="364" font-size="13" fill="#cbd5e1">      country</text>
    <text x="324" y="364" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(50)</text>
    <line x1="16" y1="378" x2="324" y2="378" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="406" font-size="13" fill="#cbd5e1">      created_at</text>
    <text x="324" y="406" font-size="12" fill="#94a3b8" text-anchor="end">TIMESTAMP</text>
  </g>

  <!-- 3. PRODUCTS TABLE (Col 2 Top) -->
  <g transform="translate(520, 160)" filter="url(#cardGlow)">
    <rect width="360" height="340" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <rect width="360" height="42" rx="12" fill="url(#hdrEmerald)"/>
    <rect y="30" width="360" height="12" fill="url(#hdrEmerald)"/>
    <text x="16" y="27" font-size="15" font-weight="700" fill="#ffffff">PRODUCTS</text>
    <text x="344" y="26" font-size="11" font-weight="600" fill="#d1fae5" text-anchor="end">CORE CATALOG</text>

    <!-- Rows -->
    <text x="16" y="68" font-size="13" font-weight="700" fill="#38bdf8">PK  product_id</text>
    <text x="344" y="68" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="80" x2="344" y2="80" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="102" font-size="13" font-weight="600" fill="#34d399">FK  category_id</text>
    <text x="344" y="102" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="114" x2="344" y2="114" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="136" font-size="13" font-weight="600" fill="#f8fafc">      product_name</text>
    <text x="344" y="136" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(120)</text>
    <line x1="16" y1="148" x2="344" y2="148" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="170" font-size="13" font-weight="600" fill="#a855f7">UK  sku</text>
    <text x="344" y="170" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(30)</text>
    <line x1="16" y1="182" x2="344" y2="182" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="204" font-size="13" fill="#cbd5e1">      cost_price [CHECK &gt;= 0]</text>
    <text x="344" y="204" font-size="12" fill="#94a3b8" text-anchor="end">DECIMAL(10,2)</text>
    <line x1="16" y1="216" x2="344" y2="216" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="238" font-size="13" fill="#cbd5e1">      unit_price [&gt;= cost]</text>
    <text x="344" y="238" font-size="12" fill="#94a3b8" text-anchor="end">DECIMAL(10,2)</text>
    <line x1="16" y1="250" x2="344" y2="250" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="272" font-size="13" fill="#cbd5e1">      status [active/disc]</text>
    <text x="344" y="272" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(20)</text>
    <line x1="16" y1="284" x2="344" y2="284" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="306" font-size="13" fill="#cbd5e1">      created_at</text>
    <text x="344" y="306" font-size="12" fill="#94a3b8" text-anchor="end">TIMESTAMP</text>
  </g>

  <!-- 4. INVENTORY TABLE (Col 2 Bottom) -->
  <g transform="translate(520, 540)" filter="url(#cardGlow)">
    <rect width="360" height="260" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <rect width="360" height="42" rx="12" fill="url(#hdrAmber)"/>
    <rect y="30" width="360" height="12" fill="url(#hdrAmber)"/>
    <text x="16" y="27" font-size="15" font-weight="700" fill="#ffffff">INVENTORY</text>
    <text x="344" y="26" font-size="11" font-weight="600" fill="#fef3c7" text-anchor="end">STOCK TRACKING</text>

    <!-- Rows -->
    <text x="16" y="70" font-size="13" font-weight="700" fill="#38bdf8">PK  inventory_id</text>
    <text x="344" y="70" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="84" x2="344" y2="84" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="112" font-size="13" font-weight="600" fill="#34d399">FK  product_id (1:1)</text>
    <text x="344" y="112" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER (UK)</text>
    <line x1="16" y1="126" x2="344" y2="126" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="154" font-size="13" fill="#cbd5e1">      stock_quantity [CHECK &gt;=0]</text>
    <text x="344" y="154" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="168" x2="344" y2="168" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="196" font-size="13" fill="#cbd5e1">      reorder_level [DEFAULT 10]</text>
    <text x="344" y="196" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="210" x2="344" y2="210" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="238" font-size="13" fill="#cbd5e1">      last_restock_date</text>
    <text x="344" y="238" font-size="12" fill="#94a3b8" text-anchor="end">DATE</text>
  </g>

  <!-- 5. ORDERS TABLE (Col 3 Top) -->
  <g transform="translate(960, 160)" filter="url(#cardGlow)">
    <rect width="360" height="280" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <rect width="360" height="42" rx="12" fill="url(#hdrPurple)"/>
    <rect y="30" width="360" height="12" fill="url(#hdrPurple)"/>
    <text x="16" y="27" font-size="15" font-weight="700" fill="#ffffff">ORDERS</text>
    <text x="344" y="26" font-size="11" font-weight="600" fill="#f3e8ff" text-anchor="end">TRANSACTION HEADER</text>

    <!-- Rows -->
    <text x="16" y="68" font-size="13" font-weight="700" fill="#38bdf8">PK  order_id</text>
    <text x="344" y="68" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="80" x2="344" y2="80" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="102" font-size="13" font-weight="600" fill="#34d399">FK  customer_id</text>
    <text x="344" y="102" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="114" x2="344" y2="114" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="136" font-size="13" fill="#cbd5e1">      order_date (Indexed)</text>
    <text x="344" y="136" font-size="12" fill="#94a3b8" text-anchor="end">TIMESTAMP</text>
    <line x1="16" y1="148" x2="344" y2="148" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="170" font-size="13" fill="#cbd5e1">      order_status [Pending..]</text>
    <text x="344" y="170" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(25)</text>
    <line x1="16" y1="182" x2="344" y2="182" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="204" font-size="13" fill="#cbd5e1">      shipping_cost</text>
    <text x="344" y="204" font-size="12" fill="#94a3b8" text-anchor="end">DECIMAL(10,2)</text>
    <line x1="16" y1="216" x2="344" y2="216" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="238" font-size="13" fill="#cbd5e1">      payment_method</text>
    <text x="344" y="238" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(30)</text>
  </g>

  <!-- 6. ORDER_ITEMS TABLE (Col 3 Bottom) -->
  <g transform="translate(960, 540)" filter="url(#cardGlow)">
    <rect width="360" height="280" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <rect width="360" height="42" rx="12" fill="url(#hdrBlue)"/>
    <rect y="30" width="360" height="12" fill="url(#hdrBlue)"/>
    <text x="16" y="27" font-size="15" font-weight="700" fill="#ffffff">ORDER_ITEMS</text>
    <text x="344" y="26" font-size="11" font-weight="600" fill="#e0f2fe" text-anchor="end">FACT LINE-ITEM</text>

    <!-- Rows -->
    <text x="16" y="68" font-size="13" font-weight="700" fill="#38bdf8">PK  order_item_id</text>
    <text x="344" y="68" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="80" x2="344" y2="80" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="102" font-size="13" font-weight="600" fill="#34d399">FK  order_id [CASCADE]</text>
    <text x="344" y="102" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="114" x2="344" y2="114" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="136" font-size="13" font-weight="600" fill="#34d399">FK  product_id</text>
    <text x="344" y="136" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="148" x2="344" y2="148" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="170" font-size="13" fill="#cbd5e1">      quantity [CHECK &gt; 0]</text>
    <text x="344" y="170" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="182" x2="344" y2="182" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="204" font-size="13" fill="#cbd5e1">      unit_price [Snapshot]</text>
    <text x="344" y="204" font-size="12" fill="#94a3b8" text-anchor="end">DECIMAL(10,2)</text>
    <line x1="16" y1="216" x2="344" y2="216" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="238" font-size="13" fill="#cbd5e1">      discount_pct [0 - 100%]</text>
    <text x="344" y="238" font-size="12" fill="#94a3b8" text-anchor="end">DECIMAL(5,2)</text>
  </g>

  <!-- 7. RETURNS TABLE (Col 4 Center) -->
  <g transform="translate(1440, 290)" filter="url(#cardGlow)">
    <rect width="400" height="310" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <rect width="400" height="42" rx="12" fill="url(#hdrRose)"/>
    <rect y="30" width="400" height="12" fill="url(#hdrRose)"/>
    <text x="16" y="27" font-size="15" font-weight="700" fill="#ffffff">RETURNS</text>
    <text x="384" y="26" font-size="11" font-weight="600" fill="#ffe4e6" text-anchor="end">REVERSE LOGISTICS</text>

    <!-- Rows -->
    <text x="16" y="68" font-size="13" font-weight="700" fill="#38bdf8">PK  return_id</text>
    <text x="384" y="68" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER</text>
    <line x1="16" y1="80" x2="384" y2="80" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="102" font-size="13" font-weight="600" fill="#34d399">FK  order_item_id (1:0..1)</text>
    <text x="384" y="102" font-size="12" fill="#94a3b8" text-anchor="end">INTEGER (UK)</text>
    <line x1="16" y1="114" x2="384" y2="114" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="136" font-size="13" fill="#cbd5e1">      return_date</text>
    <text x="384" y="136" font-size="12" fill="#94a3b8" text-anchor="end">TIMESTAMP</text>
    <line x1="16" y1="148" x2="384" y2="148" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="170" font-size="13" fill="#cbd5e1">      return_reason [Defect/Size..]</text>
    <text x="384" y="170" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(100)</text>
    <line x1="16" y1="182" x2="384" y2="182" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="204" font-size="13" fill="#cbd5e1">      refund_amount [CHECK &gt;= 0]</text>
    <text x="384" y="204" font-size="12" fill="#94a3b8" text-anchor="end">DECIMAL(10,2)</text>
    <line x1="16" y1="216" x2="384" y2="216" stroke="#334155" stroke-width="0.8"/>

    <text x="16" y="238" font-size="13" fill="#cbd5e1">      return_status [Pending/Refunded]</text>
    <text x="384" y="238" font-size="12" fill="#94a3b8" text-anchor="end">VARCHAR(20)</text>
  </g>

  <!-- ========================================================================= -->
  <!-- BOTTOM ARCHITECTURE PILLARS (FOOTER) -->
  <!-- ========================================================================= -->
  <g transform="translate(80, 890)">
    <!-- Card 1 -->
    <rect x="0" y="0" width="415" height="120" rx="10" fill="#1e293b" fill-opacity="0.6" stroke="#334155" stroke-width="1.2"/>
    <text x="16" y="32" font-size="15" font-weight="700" fill="#38bdf8">1. 3NF Normalization Standard</text>
    <text x="16" y="60" font-size="12.5" fill="#cbd5e1">Zero transitive dependency. Entities separated cleanly</text>
    <text x="16" y="80" font-size="12.5" fill="#cbd5e1">to prevent modification anomalies &amp; data duplication.</text>

    <!-- Card 2 -->
    <rect x="445" y="0" width="415" height="120" rx="10" fill="#1e293b" fill-opacity="0.6" stroke="#334155" stroke-width="1.2"/>
    <text x="461" y="32" font-size="15" font-weight="700" fill="#34d399">2. Strict Business Integrity</text>
    <text x="461" y="60" font-size="12.5" fill="#cbd5e1">Declarative CHECK constraints (unit_price &gt;= cost),</text>
    <text x="461" y="80" font-size="12.5" fill="#cbd5e1">positive quantities, valid statuses &amp; non-negative stock.</text>

    <!-- Card 3 -->
    <rect x="890" y="0" width="415" height="120" rx="10" fill="#1e293b" fill-opacity="0.6" stroke="#334155" stroke-width="1.2"/>
    <text x="906" y="32" font-size="15" font-weight="700" fill="#a855f7">3. Query Optimization &amp; Indexes</text>
    <text x="906" y="60" font-size="12.5" fill="#cbd5e1">B-Tree Indexes on Foreign Keys, Dates, and Geography</text>
    <text x="906" y="80" font-size="12.5" fill="#cbd5e1">ensuring high performance for heavy aggregation queries.</text>

    <!-- Card 4 -->
    <rect x="1335" y="0" width="425" height="120" rx="10" fill="#1e293b" fill-opacity="0.6" stroke="#334155" stroke-width="1.2"/>
    <text x="1351" y="32" font-size="15" font-weight="700" fill="#f59e0b">4. Executive Business Intelligence</text>
    <text x="1351" y="60" font-size="12.5" fill="#cbd5e1">Powered by CTEs, Window Functions (DENSE_RANK, LAG)</text>
    <text x="1351" y="80" font-size="12.5" fill="#cbd5e1">calculating Net Realized Margin %, Returns &amp; RFM tiers.</text>
  </g>
</svg>
"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(base_dir, "erd_diagram.svg")
    png_path = os.path.join(base_dir, "erd_diagram.png")
    jpg_path = os.path.join(base_dir, "erd_diagram.jpg")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"✅ Generated SVG: {svg_path}")

    # Render high-resolution PNG using PyMuPDF (fitz)
    doc = pymupdf.open(svg_path)
    page = doc[0]
    
    # 2x resolution (3840 x 2160 4K Ultra-HD equivalent)
    pix = page.get_pixmap(dpi=192)
    pix.save(png_path)
    print(f"✅ Rendered High-Resolution PNG (LinkedIn Ready): {png_path} ({pix.width}x{pix.height})")

    # Render JPG version
    pix_jpg = page.get_pixmap(dpi=150)
    pix_jpg.save(jpg_path)
    print(f"✅ Rendered JPG: {jpg_path} ({pix_jpg.width}x{pix_jpg.height})")

if __name__ == "__main__":
    build_erd_svg()
