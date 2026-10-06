from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI(title="RAF Market & Admin API")

def init_db():
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER,
            image_url TEXT,
            description TEXT,
            model TEXT,
            art TEXT,
            color TEXT,
            power TEXT,
            energy TEXT,
            sales_count INTEGER DEFAULT 0,
            fav_count INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buyer_name TEXT,
            phone TEXT,
            address TEXT,
            comment TEXT,
            items TEXT,
            total REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('store_address', 'г. Душанбе, ул. Рудаки 120')")
    
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("Электрочайник RAF R.788", "Чайники", 220, 15, "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500", "Современный электрический чайник RAF для быстрого кипячения воды.", "R.788", "R788", "Черный", "1500 Вт", "1.5 кВт/ч", 5, 12),
            ("Блендер RAF R.281", "Блендеры", 350, 20, "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=500", "Мощный кухонный блендер RAF для приготовления коктейлей и соусов.", "R.281", "R281", "Черный", "800 Вт", "0.8 кВт/ч", 10, 8),
            ("Миксер RAF", "Миксеры", 390, 8, "https://images.unsplash.com/photo-1585412727339-54e4bae3bbf9?w=500", "Компактный миксер RAF с несколькими режимами скорости.", "R.500", "R500", "Белый", "500 Вт", "0.5 кВт/ч", 3, 15)
        ]
        cursor.executemany("INSERT INTO products (name, category, price, stock, image_url, description, model, art, color, power, energy, sales_count, fav_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_products)
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title id="pageTitle">RAF market — Бытовая техника в Таджикистане</title>
    <meta name="description" content="Официальный сайт RAF в Таджикистане. Бытовая техника, товары и услуги." />
    <meta name="keywords" content="Raf Таджикистан, раф, raf company, бытовая техника таджикистан" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
</head>
  <style>
    :root {
      --bg-main: #070707;
      --bg-secondary: #0d0d0f;
      --bg-card: rgba(18, 18, 20, 0.75);
      --bg-card-solid: #111113;
      --text-main: #f5f5f5;
      --text-secondary: #c8c8c8;
      --text-muted: #888;
      --accent: #ff6a00;
      --accent-light: #ff8a33;
      --accent-dark: #d94f00;
      --border-color: rgba(255, 255, 255, 0.12);
      --border-accent: rgba(255, 106, 0, 0.35);
      --success: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
      --shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
      --nav-height: 78px;
    }
    [data-theme="light"] {
      --bg-main: #f5f5f7;
      --bg-secondary: #ffffff;
      --bg-card: rgba(255, 255, 255, 0.82);
      --bg-card-solid: #ffffff;
      --text-main: #151515;
      --text-secondary: #444;
      --text-muted: #777;
      --border-color: rgba(0, 0, 0, 0.1);
      --shadow: 0 20px 50px rgba(0, 0, 0, 0.12);
    }
    [data-theme="cyberpunk"] {
      --bg-main: #0b0f19;
      --bg-secondary: #131c31;
      --bg-card: rgba(19, 28, 49, 0.75);
      --bg-card-solid: #131c31;
      --text-main: #00ffcc;
      --text-secondary: #8a99ad;
      --text-muted: #53647c;
      --accent: #00ffcc;
      --accent-light: #66ffde;
      --border-color: rgba(0, 255, 204, 0.2);
    }
    [data-theme="sunset"] {
      --bg-main: #2b1028;
      --bg-secondary: #3e1b3a;
      --bg-card: rgba(62, 27, 58, 0.75);
      --bg-card-solid: #3e1b3a;
      --text-main: #ffffff;
      --text-muted: #d1b2cd;
      --accent: #ff5e62;
      --accent-light: #ff8b8f;
      --border-color: rgba(255, 94, 98, 0.2);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; transition: background 0.3s, color 0.3s; }
    body { min-height: 100vh; background: var(--bg-main); color: var(--text-main); overflow-x: hidden; padding-bottom: calc(var(--nav-height) + 25px); position: relative; }

    /* Живой анимированный фон (светлячки) */
    .animated-bg { position: fixed; inset: 0; z-index: -10; overflow: hidden; pointer-events: none; }
    .glow-orb { position: absolute; width: 550px; height: 550px; border-radius: 50%; filter: blur(110px); opacity: 0.35; animation: orbFloat 10s ease-in-out infinite alternate; }
    .orb-1 { top: -10%; left: -10%; background: var(--accent); animation-duration: 12s; }
    .orb-2 { right: -10%; top: 40%; background: #ff007f; animation-duration: 15s; }
    .orb-3 { bottom: -10%; left: 30%; background: #00ffcc; animation-duration: 10s; }
    @keyframes orbFloat { 
      0% { transform: translate3d(0, 0, 0) scale(1); } 
      50% { transform: translate3d(80px, -60px, 0) scale(1.15); }
      100% { transform: translate3d(-50px, 70px, 0) scale(0.95); } 
    }

    #toast {
      position: fixed; bottom: 95px; left: 50%; transform: translateX(-50%) translateY(30px);
      background: rgba(30, 30, 35, 0.9); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-accent); color: var(--text-main); padding: 12px 24px; border-radius: 20px;
      font-size: 13px; font-weight: 800; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
      transition: opacity 0.3s ease, transform 0.3s ease; z-index: 99999; pointer-events: none; opacity: 0;
    }
    #toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }

    .header { position: relative; width: 100%; height: 86px; display: flex; align-items: center; justify-content: space-between; padding: 0 25px; border-bottom: 1px solid var(--border-color); background: var(--bg-card); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); z-index: 50; }
    .logo-text-orange { color: var(--accent); font-size: 32px; font-weight: 1000; letter-spacing: -2px; line-height: 1; text-shadow: 0 0 18px rgba(255, 106, 0, 0.35); }
    .header-address { font-size: 12px; color: var(--text-secondary); text-align: right; max-width: 300px; font-weight: 600; }

    main { position: relative; width: 100%; }
    .hero { position: relative; width: min(1180px, calc(100% - 32px)); min-height: 440px; margin: 32px auto 0; display: flex; align-items: center; padding: 65px; overflow: hidden; border: 1px solid var(--border-color); border-radius: 30px; background: var(--bg-card); box-shadow: var(--shadow); backdrop-filter: blur(18px); }
    .hero-text { position: relative; z-index: 2; max-width: 690px; }
    .small-title { margin-bottom: 14px; color: var(--accent); font-size: 12px; font-weight: 800; letter-spacing: 3px; }
    .hero h1 { font-size: clamp(38px, 6vw, 72px); line-height: 0.98; letter-spacing: -3px; font-weight: 950; margin-bottom: 22px; }
    .hero p:not(.small-title) { color: var(--text-secondary); font-size: 16px; line-height: 1.75; margin-bottom: 30px; }
    .hero button { padding: 14px 23px; border-radius: 13px; color: #fff; background: var(--accent); font-weight: 800; cursor: pointer; box-shadow: 0 10px 30px rgba(255, 106, 0, 0.22); border: none; }

    .filters-panel { width: min(1180px, calc(100% - 32px)); margin: 25px auto 35px; padding: 18px; border: 1px solid var(--border-color); border-radius: 20px; background: var(--bg-card); backdrop-filter: blur(18px); box-shadow: 0 15px 45px rgba(0, 0, 0, 0.18); position: relative; z-index: 10; }
    .filters-row { display: grid; grid-template-columns: 1fr; gap: 10px; }
    .search-box { display: flex; align-items: center; overflow: hidden; border: 1px solid var(--border-color); border-radius: 13px; background: rgba(255, 255, 255, 0.035); }
    .search-box input { flex: 1; height: 46px; border: none; background: transparent; color: var(--text-main); padding: 0 13px; outline: none; }
    .search-box button { width: 44px; height: 44px; background: transparent; color: var(--text-secondary); font-size: 17px; cursor: pointer; border: none; }
    .filters-row > input { width: 100%; height: 46px; padding: 0 13px; border: 1px solid var(--border-color); border-radius: 13px; background: rgba(255, 255, 255, 0.035); color: var(--text-main); outline: none; }

    .category-wrapper { display: flex; align-items: center; gap: 8px; margin-top: 14px; position: relative; }
    .category-list { display: flex; align-items: center; gap: 8px; overflow-x: auto; scrollbar-width: none; }
    .category-list::-webkit-scrollbar { display: none; }
    .cat-btn { min-height: 39px; padding: 8px 13px; border: 1px solid var(--border-color); border-radius: 10px; background: rgba(255, 255, 255, 0.035); color: var(--text-secondary); font-size: 12px; font-weight: 700; cursor: pointer; white-space: nowrap; }
    .cat-btn.active { color: #fff; background: var(--accent); border-color: var(--accent); }
    
    .category-dropdown { 
      position: absolute; right: 0; top: calc(100% + 10px); z-index: 999999 !important; 
      width: 280px; max-height: 340px; overflow-y: auto; padding: 10px; 
      border: 2px solid var(--accent); border-radius: 16px; 
      background: #121216 !important; box-shadow: 0 25px 60px rgba(0,0,0,0.95); 
    }
    .category-dropdown.hidden { display: none !important; }
    .dropdown-item { width: 100%; padding: 10px 14px; border-radius: 8px; background: transparent; color: var(--text-main); text-align: left; font-size: 13px; font-weight: 700; cursor: pointer; border: none; margin-bottom: 2px; }
    .dropdown-item:hover { background: var(--accent); color: #fff; }

    #productsSection { width: min(1180px, calc(100% - 32px)); margin: 0 auto; position: relative; z-index: 1; }
    .section-title { display: flex; align-items: flex-end; justify-content: space-between; gap: 15px; margin-bottom: 18px; }
    .section-title h2 { font-size: 25px; font-weight: 900; }

    .products { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 15px; }
    .product-card { position: relative; overflow: hidden; border: 1px solid var(--border-color); border-radius: 18px; background: var(--bg-card); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2); transition: transform 0.25s ease, border-color 0.25s ease; cursor: pointer; }
    .product-card:hover { transform: translateY(-5px); border-color: var(--border-accent); }
    .product-image { position: relative; width: 100%; aspect-ratio: 1 / 1; background: rgba(255, 255, 255, 0.02); }
    .product-image img { width: 100%; height: 100%; object-fit: contain; padding: 12px; }
    .product-info { padding: 15px; }
    .product-info h3 { font-size: 15px; margin-bottom: 7px; font-weight: 800; color: var(--text-main); }
    .product-price { color: var(--accent); font-size: 19px; font-weight: 900; margin-bottom: 10px; }
    .product-category { color: var(--text-muted); font-size: 11px; margin-bottom: 4px; }

    .order-button { width: 100%; min-height: 43px; padding: 10px 15px; border-radius: 11px; background: var(--accent); color: #fff; font-weight: 800; cursor: pointer; border: none; box-shadow: 0 8px 22px rgba(255, 106, 0, 0.16); }
    .secondary-button { width: 100%; min-height: 43px; margin-top: 8px; padding: 10px 15px; border: 1px solid var(--border-color); border-radius: 11px; background: rgba(255, 255, 255, 0.035); color: var(--text-secondary); font-weight: 750; cursor: pointer; }

    .favorite-btn { position: absolute; top: 10px; right: 10px; z-index: 5; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 50%; background: rgba(0, 0, 0, 0.45); color: #fff; cursor: pointer; }
    .favorite-btn.active { color: #ff4b4b; }

    .bottom-nav { position: fixed; left: 50%; bottom: 13px; transform: translateX(-50%); z-index: 1000; width: min(600px, calc(100% - 24px)); height: var(--nav-height); display: grid; grid-template-columns: repeat(4, 1fr); align-items: center; padding: 8px; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 23px; background: rgba(15, 15, 17, 0.82); box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px); }
    .bottom-nav-btn { min-width: 0; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; border-radius: 17px; background: transparent; color: var(--text-muted); font-size: 10px; font-weight: 700; cursor: pointer; border: none; }
    .bottom-nav-btn.cart-highlight { color: var(--accent); background: rgba(255, 106, 0, 0.08); }
    .badge { position: absolute; top: 8px; right: 12px; min-width: 19px; height: 19px; padding: 0 5px; display: flex; align-items: center; justify-content: center; border-radius: 50px; background: var(--accent); color: #fff; font-size: 10px; font-weight: 900; }

    .modal { position: fixed; inset: 0; z-index: 200000; display: flex; align-items: center; justify-content: center; padding: 20px; background: rgba(0, 0, 0, 0.72); backdrop-filter: blur(10px); }
    .modal[hidden] { display: none; }
    .modal-content { position: relative; width: min(540px, 100%); max-height: min(850px, calc(100vh - 40px)); overflow-y: auto; padding: 25px; border: 1px solid var(--border-color); border-radius: 22px; background: var(--bg-card-solid); color: var(--text-main); box-shadow: var(--shadow); }
    .close { position: absolute; top: 12px; right: 13px; width: 37px; height: 37px; display: flex; align-items: center; justify-content: center; border: 1px solid var(--border-color); border-radius: 50%; background: rgba(255, 255, 255, 0.04); color: var(--text-secondary); font-size: 25px; cursor: pointer; }
    .modal input, .modal select, .modal textarea { width: 100%; margin-bottom: 10px; padding: 12px 13px; border: 1px solid var(--border-color); border-radius: 11px; background: rgba(255, 255, 255, 0.035); color: var(--text-main); outline: none; }

    @media (max-width: 1000px) { .products { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
    @media (max-width: 700px) { .products { grid-template-columns: repeat(2, minmax(0, 1fr)); } .hero { padding: 30px; } }
  </style>
</head>
<body>

  <div class="animated-bg" aria-hidden="true">
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>
    <div class="glow-orb orb-3"></div>
  </div>

  <div id="toast">Уведомление</div>

  <header class="header">
    <a href="/" class="logo" aria-label="RAF market" style="text-decoration:none;">
      <span class="logo-text-orange">RAF market</span>
    </a>
    <div class="header-address" id="headerAddressDisplay">📍 г. Душанбе, ул. Рудаки 120</div>
  </header>

  <nav class="bottom-nav">
    <button type="button" class="bottom-nav-btn" onclick="openFavoritesModal()">
      <span class="nav-icon">❤</span>
      <span id="navFavText">Избранное</span>
    </button>
    <button type="button" class="bottom-nav-btn" onclick="openSettingsModal()">
      <span class="nav-icon">⚙</span>
      <span id="navHomeText">Общие</span>
    </button>
    <button type="button" class="bottom-nav-btn" onclick="openProfileModal()">
      <span class="nav-icon">👤</span>
      <span id="navProfileText">Профиль</span>
    </button>
    <button type="button" class="bottom-nav-btn cart-highlight" onclick="openCart()">
      <span class="nav-icon">🛒</span>
      <span id="cartCount" class="badge">0</span>
      <span id="navCartText">Корзина</span>
    </button>
  </nav>

  <main>
    <section class="hero">
      <div class="hero-text">
        <p class="small-title" id="heroSmall">ОФИЦИАЛЬНЫЙ КАТАЛОГ</p>
        <h1 id="heroTitle">Премиальная техника RAF</h1>
        <p id="heroDesc">Современная высокотехнологичная техника для вашего дома и кухни с официальной гарантией в Таджикистане.</p>
        <button type="button" onclick="scrollToProducts()" id="heroBtn">Смотреть каталог</button>
      </div>
    </section>

    <div class="filters-panel">
      <div class="filters-row">
        <div class="search-box" role="search">
          <input type="search" id="searchInput" placeholder="Поиск товара..." autocomplete="off" oninput="renderProducts()">
          <input type="file" id="photoSearchInput" accept="image/*" style="display:none;" onchange="handlePhotoSearch(this)">
          <button type="button" onclick="document.getElementById('photoSearchInput').click()" title="Поиск по фото">📸</button>
          <button type="button" onclick="renderProducts()">🔍</button>
        </div>
        <input type="text" id="filterModelInput" placeholder="Фильтр по модели (например: R.788)..." oninput="renderProducts()" autocomplete="off">
      </div>

      <div class="category-wrapper">
        <div class="category-list" id="categoryList">
          <button type="button" class="cat-btn active" onclick="filterCategory('all', this)" id="btnAllCat">Все товары</button>
          <button type="button" class="cat-btn" onclick="filterCategory('Миксеры', this)">Миксеры</button>
          <button type="button" class="cat-btn" onclick="filterCategory('Блендеры', this)">Блендеры</button>
          <button type="button" class="cat-btn" onclick="filterCategory('Чайники', this)">Чайники</button>
        </div>

        <div class="category-more-container" style="position:relative;">
          <button type="button" class="cat-btn category-more-btn" onclick="toggleCategoryDropdown(event)" id="btnMoreCat">Все категории ▾</button>
          <div class="category-dropdown hidden" id="categoryDropdown">
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Миксеры', this)">Миксеры</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Блендеры', this)">Блендеры</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Мясорубки', this)">Мясорубки</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Соковыжималки', this)">Соковыжималки</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Чайники', this)">Чайники</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Мультиварке', this)">Мультиварке</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Электрические термосы', this)">Электрические термосы</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Духовки', this)">Духовки</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Микроволновки', this)">Микроволновки</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Аэрогрили', this)">Аэрогрили</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Кофемашины', this)">Кофемашины</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Кофемашины полуавтомат', this)">Кофемашины полуавтомат</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Кофемолки-измильчитили', this)">Кофемолки-измильчитили</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Кондиционеры', this)">Кондиционеры</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Лёд машины', this)">Лёд машины</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Стиральной машины', this)">Стиральной машины</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Телевизоры', this)">Телевизоры</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Пылесосы', this)">Пылесосы</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Пылесосы ручные', this)">Пылесосы ручные</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Кувшин фильтр для воды', this)">Кувшин фильтр для воды</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Паровые очистители', this)">Паровые очистители</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Пылесос портативный моющие', this)">Пылесос портативный моющие</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Моющие пылесосы', this)">Моющие пылесосы</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Холодильники', this)">Холодильники</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Холодильники для кофемашины', this)">Холодильники для кофемашины</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Фритюрницы', this)">Фритюрницы</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Аппараты для выпечки', this)">Аппараты для выпечки</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Тостеры', this)">Тостеры</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Кулеры', this)">Кулеры</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Комбайны', this)">Комбайны</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Чопперы', this)">Чопперы</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Утюги паровые ручные', this)">Утюги паровые ручные</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Утюги', this)">Утюги</button>
            <button type="button" class="dropdown-item" onclick="filterCategoryDropdown('Электронные плиты', this)">Электронные плиты</button>
          </div>
        </div>
      </div>
    </div>

    <section id="productsSection">
      <div class="section-title">
        <h2 id="prodTitle">Витрина товаров</h2>
        <span id="productCount" aria-live="polite"></span>
      </div>
      <div id="products" class="products"></div>
    </section>
  </main>

  <!-- Модалки -->
  <div id="favoritesModal" class="modal" hidden>
    <div class="modal-content">
      <button type="button" class="close" onclick="closeFavoritesModal()">×</button>
      <h2 id="favModalTitle">❤ Избранные товары</h2>
      <div id="favItems"></div>
    </div>
  </div>

  <div id="profileModal" class="modal" hidden>
    <div class="modal-content">
      <button type="button" class="close" onclick="closeProfileModal()">×</button>
      <h2 id="profileModalTitle">👤 Профиль покупателя RAF</h2>
      <div id="profileGuestView">
        <input type="text" id="regName" placeholder="Ваше имя">
        <input type="tel" id="regPhone" placeholder="Номер телефона">
        <input type="password" id="regPassword" placeholder="Пароль">
        <button type="button" class="order-button" id="regBtn" onclick="registerUser()">Зарегистрироваться</button>
        <button type="button" class="secondary-button" id="toLoginBtn" onclick="showLoginForm()">Войти</button>
      </div>
      <div id="profileLoginView" hidden>
        <input type="tel" id="loginPhone" placeholder="Номер телефона">
        <input type="password" id="loginPassword" placeholder="Пароль">
        <button type="button" class="order-button" id="loginBtn" onclick="loginUser()">Войти</button>
      </div>
      <div id="profileUserView" hidden>
        <h3 id="profileUserName">Пользователь</h3>
        <p id="profileUserPhone"></p>
        <button type="button" class="order-button" id="orderHistoryBtn" onclick="openOrderHistory()" style="margin: 12px 0 8px;">📦 История заказов и статусы</button>
        <button type="button" class="secondary-button" id="logoutBtn" onclick="logoutUser()" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.3);">🚪 Выйти из аккаунта</button>
      </div>
    </div>
  </div>

  <div id="settingsModal" class="modal" hidden>
    <div class="modal-content">
      <button type="button" class="close" onclick="closeSettingsModal()">×</button>
      <h2 id="settingsTitle">⚙️ Настройки</h2>
      
      <div class="settings-section" style="margin-bottom: 15px;">
        <label id="currLabel" style="display:block; margin-bottom: 6px; font-size: 13px; font-weight:700;">Валюта</label>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">
          <button type="button" class="cat-btn currency-btn active" onclick="setCurrency('som', this)">Сомони</button>
          <button type="button" class="cat-btn currency-btn" onclick="setCurrency('usd', this)">USD ($)</button>
          <button type="button" class="cat-btn currency-btn" onclick="setCurrency('rub', this)">Рубль (₽)</button>
        </div>
      </div>

      <div class="settings-section" style="margin-bottom: 15px;">
        <label id="themeLabel" style="display:block; margin-bottom: 6px; font-size: 13px; font-weight:700;">Тема оформления</label>
        <div class="theme-buttons" style="display:grid; grid-template-columns: 1fr 1fr; gap: 8px;">
          <button type="button" class="secondary-button" style="margin:0;" onclick="setTheme('dark')">🌙 Тёмная</button>
          <button type="button" class="secondary-button" style="margin:0;" onclick="setTheme('light')">☀️ Светлая</button>
          <button type="button" class="secondary-button" style="margin:0;" onclick="setTheme('cyberpunk')">⚡ Киберпанк</button>
          <button type="button" class="secondary-button" style="margin:0;" onclick="setTheme('sunset')">🌅 Закат</button>
        </div>
      </div>

      <div class="settings-section" style="margin-bottom: 15px;">
        <label id="langLabel" style="display:block; margin-bottom: 6px; font-size: 13px; font-weight:700;">Язык</label>
        <select id="languageSelect" onchange="changeLanguage(this.value)">
          <option value="ru">Русский</option>
          <option value="tj">Тоҷикӣ</option>
          <option value="en">English</option>
        </select>
      </div>

      <div class="settings-section" style="margin-bottom: 12px;">
        <button type="button" class="secondary-button" style="margin:0; background:rgba(16, 185, 129, 0.15); color:#10b981; border-color:rgba(16, 185, 129, 0.4); font-weight:800;" onclick="window.open('https://wa.me/992970664488', '_blank')">💬 Поддержка (WhatsApp)</button>
      </div>

      <div class="settings-section">
        <button type="button" class="order-button" id="adminPanelBtn" onclick="closeSettingsModal(); openAdminModal();">🔐 Панель администратора</button>
      </div>
    </div>
  </div>

  <div id="cartModal" class="modal" hidden>
    <div class="modal-content">
      <button type="button" class="close" onclick="closeCart()">×</button>
      <h2 id="cartModalTitle">🛒 Корзина</h2>
      <div id="cartItems"></div>
      <div id="cartTotal" class="cart-total" style="margin:15px 0; font-weight:900;">Итого: 0 сом</div>
      <button type="button" class="order-button" id="checkoutBtn" onclick="checkoutCart()">Оформить заказ</button>
    </div>
  </div>

  <!-- Полная модалка характеристик товара для покупателя -->
  <div id="productModal" class="modal" hidden>
    <div class="modal-content">
      <button type="button" class="close" onclick="closeProductModal()">×</button>
      <div id="productModalContent"></div>
    </div>
  </div>

  <div id="checkoutModal" class="modal" hidden>
    <div class="modal-content">
      <button type="button" class="close" onclick="closeCheckoutModal()">×</button>
      <h2 id="checkoutModalTitle">📦 Оформление заказа</h2>
      <input type="text" id="checkoutName" placeholder="Ваше имя">
      <input type="tel" id="checkoutPhone" placeholder="Номер телефона">
      <input type="text" id="checkoutAddress" placeholder="Адрес доставки">
      
      <label id="paymentLabel" style="display:block; margin: 8px 0 4px; font-size:12px; font-weight:700;">Способ оплаты:</label>
      <select id="checkoutPaymentMethod" onchange="handlePaymentMethodChange()" style="width:100%; margin-bottom:10px; padding:10px; border-radius:11px; background:rgba(255,255,255,0.035); color:var(--text-main); border:1px solid var(--border-color);">
        <option value="dc">Dushanbe City (DC NEXT)</option>
        <option value="whatsapp">WhatsApp (+992 970 66 44 88)</option>
      </select>

      <div id="checkoutQrContainer" style="display: flex; flex-direction: column; align-items: center; margin: 10px 0; padding: 12px; background: #fff; border-radius: 12px;">
        <div id="dcQrCode"></div>
        <p style="color: #000; font-size: 11px; margin-top: 6px; font-weight:700;">Сканируйте для открытия DC NEXT</p>
      </div>

      <textarea id="checkoutComment" placeholder="Комментарий к заказу" style="width:100%; min-height:60px; padding:10px; border-radius:11px; background:rgba(255,255,255,0.035); color:var(--text-main); border:1px solid var(--border-color);"></textarea>
      <button type="button" class="order-button" id="confirmOrderBtn" onclick="submitOrder()">Подтвердить заказ</button>
    </div>
  </div>

  <div id="ordersModal" class="modal" hidden>
    <div class="modal-content">
      <button type="button" class="close" onclick="closeOrderHistory()">×</button>
      <h2 id="ordersModalTitle">📦 Статусы и история заказов</h2>
      <div id="orderHistoryList"></div>
    </div>
  </div>

  <!-- Админ панель с полным управлением (Добавление, Редактирование, Удаление) -->
  <div id="adminModal" class="modal" hidden>
    <div class="modal-content">
      <button type="button" class="close" onclick="closeAdminModal()">×</button>
      <h2>🔐 Панель администратора RAF</h2>
      <div id="adminLoginSection">
        <input type="text" id="adminLogin" placeholder="Логин">
        <input type="password" id="adminPassword" placeholder="Пароль">
        <button type="button" class="order-button" onclick="adminLoginSubmit()">Войти</button>
      </div>
      <div id="adminPanel" hidden>
        <div style="display:flex; gap:5px; margin-bottom:15px; overflow-x:auto;">
          <button type="button" id="tabAddProd" class="cat-btn active" onclick="switchAdminTab('add')">➕ Товары</button>
          <button type="button" id="tabOrders" class="cat-btn" onclick="switchAdminTab('orders')">🔔 Заявки (<span id="pendingOrdersCount">0</span>)</button>
          <button type="button" id="tabAddress" class="cat-btn" onclick="switchAdminTab('address')">🏪 Адрес</button>
          <button type="button" id="tabReports" class="cat-btn" onclick="switchAdminTab('reports')">📊 Статистика</button>
        </div>
        
        <div id="addProductForm">
          <input type="hidden" id="editProductId" value="">
          <h3 id="formTitleMode" style="margin-bottom:10px; color:var(--accent); font-size:15px;">➕ Добавить новый товар</h3>
          
          <label>Название товара *:</label>
          <input type="text" id="newProdName" placeholder="Например: RAF Чайник">
          
          <label>Цена (сомони) *:</label>
          <input type="number" id="newProdPrice" placeholder="250">
          
          <label>Категория *:</label>
          <select id="newProdCategory">
            <option value="Миксеры">Миксеры</option>
            <option value="Блендеры">Блендеры</option>
            <option value="Мясорубки">Мясорубки</option>
            <option value="Соковыжималки">Соковыжималки</option>
            <option value="Чайники">Чайники</option>
            <option value="Мультиварке">Мультиварке</option>
            <option value="Электрические термосы">Электрические термосы</option>
            <option value="Духовки">Духовки</option>
            <option value="Микроволновки">Микроволновки</option>
            <option value="Аэрогрили">Аэрогрили</option>
            <option value="Кофемашины">Кофемашины</option>
            <option value="Кофемашины полуавтомат">Кофемашины полуавтомат</option>
            <option value="Кофемолки-измильчитили">Кофемолки-измильчитили</option>
            <option value="Кондиционеры">Кондиционеры</option>
            <option value="Лёд машины">Лёд машины</option>
            <option value="Стиральной машины">Стиральной машины</option>
            <option value="Телевизоры">Телевизоры</option>
            <option value="Пылесосы">Пылесосы</option>
            <option value="Пылесосы ручные">Пылесосы ручные</option>
            <option value="Кувшин фильтр для воды">Кувшин фильтр для воды</option>
            <option value="Паровые очистители">Паровые очистители</option>
            <option value="Пылесос портативный моющие">Пылесос портативный моющие</option>
            <option value="Моющие пылесосы">Моющие пылесосы</option>
            <option value="Холодильники">Холодильники</option>
            <option value="Холодильники для кофемашины">Холодильники для кофемашины</option>
            <option value="Фритюрницы">Фритюрницы</option>
            <option value="Аппараты для выпечки">Аппараты для выпечки</option>
            <option value="Тостеры">Тостеры</option>
            <option value="Кулеры">Кулеры</option>
            <option value="Комбайны">Комбайны</option>
            <option value="Чопперы">Чопперы</option>
            <option value="Утюги паровые ручные">Утюги паровые ручные</option>
            <option value="Утюги">Утюги</option>
            <option value="Электронные плиты">Электронные плиты</option>
          </select>

          <label>Модель:</label>
          <input type="text" id="newProdModel" placeholder="R.788">
          
          <label>Артикул *:</label>
          <input type="text" id="newProdArt" placeholder="R788">
          
          <label>Цвет *:</label>
          <input type="text" id="newProdColor" placeholder="Черный">

          <label>Мощность:</label>
          <input type="text" id="newProdPower" placeholder="1500 Вт">

          <label>Энергопотребление:</label>
          <input type="text" id="newProdEnergy" placeholder="1.5 кВт/ч">
          
          <label>Фото товара из галереи *:</label>
          <input type="file" id="newProdImageFile" accept="image/*" style="padding: 8px;" onchange="previewNewProductImage(this)">
          <div id="imagePreviewContainer" style="margin-bottom: 10px; display: none;">
            <img id="previewImgTag" src="" alt="Превью" style="width: 80px; height: 80px; object-fit: contain; border-radius: 8px; border: 1px solid var(--border-color);">
          </div>
          <input type="hidden" id="newProdImageBase64" value="">

          <label>Описание *:</label>
          <textarea id="newProdDesc" placeholder="Описание товара..." style="width:100%; min-height:80px; padding:10px; border-radius:11px; background:rgba(255,255,255,0.035); color:var(--text-main); border:1px solid var(--border-color);"></textarea>
          
          <div style="display:flex; gap:8px;">
            <button type="button" class="order-button" id="addBtnText" onclick="handleSaveProduct()">Сохранить товар</button>
            <button type="button" class="secondary-button" id="cancelEditBtn" onclick="resetProductForm()" style="display:none; margin:0;">Отмена</button>
          </div>

          <h3 style="margin: 20px 0 10px; font-size:15px;">Список существующих товаров (Управление):</h3>
          <div id="adminProductList" style="max-height: 280px; overflow-y: auto;"></div>
        </div>

        <div id="ordersSection" hidden>
          <h3>🔔 Активные заявки покупателей:</h3>
          <div id="adminPendingOrdersList"></div>
          
          <h3 style="margin-top:20px;">📜 История заявок (одобренные / отклонённые):</h3>
          <div id="adminHistoryOrdersList" style="margin-top:8px;"></div>
        </div>

        <div id="addressSection" hidden>
          <h3>🏪 Изменить адрес магазина:</h3>
          <p style="font-size:12px; color:var(--text-muted); margin-bottom:10px;">Этот адрес увидят покупатели в шапке сайта и при оформлении заказа.</p>
          <input type="text" id="storeAddressInput" placeholder="Введите новый адрес...">
          <button type="button" class="order-button" onclick="saveStoreAddress()">Сохранить адрес</button>
        </div>

        <div id="reportsSection" hidden>
          <h3 style="margin-bottom:12px; color:var(--accent);">📊 Статистика популярных товаров:</h3>
          <div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:12px; border:1px solid var(--border-color); margin-bottom:12px;">
            <p style="font-weight:800; margin-bottom:6px;">1) Большинство проданных товаров:</p>
            <div id="topSoldList" style="font-size:13px; color:var(--text-secondary);">Нет данных</div>
          </div>
          <div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:12px; border:1px solid var(--border-color); margin-bottom:12px;">
            <p style="font-weight:800; margin-bottom:6px;">2) Большинство добавленных в избранные:</p>
            <div id="topFavList" style="font-size:13px; color:var(--text-secondary);">Нет данных</div>
          </div>
          <p style="margin-top:15px; font-size:14px;">ОБЩАЯ ВЫРУЧКА: <strong id="revTotal" style="color:var(--accent);">0 сом</strong></p>
        </div>
        
        <button type="button" onclick="adminLogout()" class="secondary-button" style="margin-top:15px; background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.3);">🚪 Выйти из админки</button>
      </div>
    </div>
  </div>

  <script>
    let products = [];
    let cart = [];
    let favorites = JSON.parse(localStorage.getItem('raf_fav_v14') || '[]');
    let currentCategory = 'all';
    let currentCurrency = 'som';
    let currencyRates = { som: 1, usd: 0.092, rub: 8.5 };
    let currencySymbol = { som: 'сом', usd: '$', rub: '₽' };
    let currentUser = JSON.parse(localStorage.getItem('raf_current_user_v14') || 'null');
    let users = JSON.parse(localStorage.getItem('raf_users_v14') || '[]');
    let orders = JSON.parse(localStorage.getItem('raf_orders_v14') || '[]');
    let currentLang = localStorage.getItem('raf_lang_v14') || 'ru';
    let storeAddress = 'г. Душанбе, ул. Рудаки 120';

    const translations = {
      ru: {
        smallTitle: "ОФИЦИАЛЬНЫЙ КАТАЛОГ",
        heroTitle: "Премиальная техника RAF",
        heroDesc: "Современная высокотехнологичная техника для вашего дома и кухни с официальной гарантией в Таджикистане.",
        heroBtn: "Смотреть каталог",
        searchPlaceholder: "Поиск товара...",
        modelPlaceholder: "Фильтр по модели (например: R.788)...",
        allGoods: "Все товары",
        more: "Все категории ▾",
        vitrine: "Витрина товаров",
        toCart: "🛒 В корзину",
        fav: "Избранное",
        general: "Общие",
        profile: "Профиль",
        cart: "Корзина",
        settingsTitle: "⚙️ Настройки",
        currency: "Валюта",
        theme: "Тема оформления",
        language: "Язык",
        adminBtn: "🔐 Панель администратора",
        checkout: "Оформить заказ",
        total: "Итого",
        emptyCart: "Корзина пуста.",
        emptyFav: "Избранных товаров нет."
      },
      tj: {
        smallTitle: "КАТАЛОГИ РАСМӢ",
        heroTitle: "Техникаи премиалии RAF",
        heroDesc: "Техникаи муосир ва баландтехнологии рӯзгор бо кафолати расмӣ дар Тоҷикистон.",
        heroBtn: "Дидани каталог",
        searchPlaceholder: "Ҷустуҷӯи мол...",
        modelPlaceholder: "Филтр аз рӯи модел (масалан: R.788)...",
        allGoods: "Ҳамаи молҳо",
        more: "Ҳамаи категорияҳо ▾",
        vitrine: "Витринаи молҳо",
        toCart: "🛒 Ба сабад",
        fav: "Панҷгона",
        general: "Умумӣ",
        profile: "Профил",
        cart: "Сабад",
        settingsTitle: "⚙ Танзимот",
        currency: "Асъор",
        theme: "Мавзӯи намуди зоҳирӣ",
        language: "Забон",
        adminBtn: "🔐 Панели муҳофиз (Админ)",
        checkout: "Фармоиш додан",
        total: "Ҳамагӣ",
        emptyCart: "Сабад холӣ аст.",
        emptyFav: "Молҳои дӯстдошта нестанд."
      },
      en: {
        smallTitle: "OFFICIAL CATALOG",
        heroTitle: "RAF Premium Appliances",
        heroDesc: "Modern high-tech appliances for your home and kitchen with official warranty in Tajikistan.",
        heroBtn: "View Catalog",
        searchPlaceholder: "Search product...",
        modelPlaceholder: "Filter by model (e.g., R.788)...",
        allGoods: "All Products",
        more: "All Categories ▾",
        vitrine: "Product Showcase",
        toCart: "🛒 Add to cart",
        fav: "Favorites",
        general: "General",
        profile: "Profile",
        cart: "Cart",
        settingsTitle: "⚙️ Settings",
        currency: "Currency",
        theme: "Theme",
        language: "Language",
        adminBtn: "🔐 Administrator Panel",
        checkout: "Checkout",
        total: "Total",
        emptyCart: "Cart is empty.",
        emptyFav: "No favorite items."
      }
    };

    function applyLanguage(lang) {
      currentLang = lang;
      localStorage.setItem('raf_lang_v14', lang);
      const t = translations[lang] || translations.ru;

      document.getElementById('heroSmall').textContent = t.smallTitle;
      document.getElementById('heroTitle').textContent = t.heroTitle;
      document.getElementById('heroDesc').textContent = t.heroDesc;
      document.getElementById('heroBtn').textContent = t.heroBtn;
      document.getElementById('searchInput').placeholder = t.searchPlaceholder;
      document.getElementById('filterModelInput').placeholder = t.modelPlaceholder;
      document.getElementById('btnAllCat').textContent = t.allGoods;
      document.getElementById('btnMoreCat').textContent = t.more;
      document.getElementById('prodTitle').textContent = t.vitrine;
      document.getElementById('navFavText').textContent = t.fav;
      document.getElementById('navHomeText').textContent = t.general;
      document.getElementById('navProfileText').textContent = t.profile;
      document.getElementById('navCartText').textContent = t.cart;
      document.getElementById('settingsTitle').textContent = t.settingsTitle;
      document.getElementById('currLabel').textContent = t.currency;
      document.getElementById('themeLabel').textContent = t.theme;
      document.getElementById('langLabel').textContent = t.language;
      document.getElementById('adminPanelBtn').textContent = t.adminBtn;
      document.getElementById('checkoutBtn').textContent = t.checkout;
      
      const langSel = document.getElementById('languageSelect');
      if(langSel) langSel.value = lang;
    }

    function showToast(text) {
      const t = document.getElementById('toast');
      t.innerText = text;
      t.classList.add('show');
      setTimeout(() => { t.classList.remove('show'); }, 2500);
    }

    async function loadProducts() {
      const res = await fetch('/products');
      products = await res.json();
      renderProducts();
      renderFavorites();
      updateCartCount();
      loadStoreAddress();
      loadOrdersFromServer();
      renderAdminProductList();
    }

    async function loadOrdersFromServer() {
      try {
        const res = await fetch('/orders');
        orders = await res.json();
      } catch(e) {}
    }

    async function loadStoreAddress() {
      try {
        const res = await fetch('/settings/store_address');
        const data = await res.json();
        if(data.address) {
          storeAddress = data.address;
          const displayEl = document.getElementById('headerAddressDisplay');
          if(displayEl) displayEl.textContent = '📍 ' + storeAddress;
          const addrInput = document.getElementById('storeAddressInput');
          if(addrInput) addrInput.value = storeAddress;
        }
      } catch(e) {}
    }

    function formatPrice(somValue) {
      let val = somValue * currencyRates[currentCurrency];
      return `${val.toFixed(currentCurrency === 'usd' ? 2 : 0)} ${currencySymbol[currentCurrency]}`;
    }

    function setCurrency(curr, el) {
      currentCurrency = curr;
      document.querySelectorAll('.currency-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
      renderProducts();
      renderFavorites();
      renderCart();
    }

    function renderProducts(list = null) {
      const grid = document.getElementById('products');
      const search = (document.getElementById('searchInput')?.value || '').toLowerCase();
      const modelFilter = (document.getElementById('filterModelInput')?.value || '').toLowerCase();
      grid.innerHTML = '';
      
      let source = list || products;
      let filtered = source.filter(p => {
        const matchCat = currentCategory === 'all' || p.category === currentCategory;
        const matchSearch = p.name.toLowerCase().includes(search) || (p.description && p.description.toLowerCase().includes(search));
        const matchModel = !modelFilter || (p.model && p.model.toLowerCase().includes(modelFilter)) || (p.art && p.art.toLowerCase().includes(modelFilter));
        return matchCat && matchSearch && matchModel;
      });

      const t = translations[currentLang] || translations.ru;

      filtered.forEach(p => {
        const isFav = favorites.includes(p.id);
        grid.innerHTML += `
          <article class="product-card" onclick="openProductModal(${p.id})">
            <div class="product-image">
              <button type="button" class="favorite-btn ${isFav ? 'active' : ''}" onclick="event.stopPropagation(); toggleFavorite(${p.id})">${isFav ? '♥' : '♡'}</button>
              <img src="${p.image_url || 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500'}" alt="${p.name}">
            </div>
            <div class="product-info">
              <div class="product-category">${p.category || 'RAF'}</div>
              <h3>${p.name}</h3>
              <div class="product-price">${formatPrice(p.price)}</div>
              <button type="button" class="order-button" onclick="event.stopPropagation(); addToCart(${p.id})">${t.toCart}</button>
            </div>
          </article>
        `;
      });
      document.getElementById('productCount').textContent = `${filtered.length} товаров`;
    }

    function toggleFavorite(id) {
      if (favorites.includes(id)) {
        favorites = favorites.filter(i => i !== id);
        showToast('Удалено из избранного');
      } else {
        favorites.push(id);
        showToast('Добавлено в избранное ❤️');
      }
      localStorage.setItem('raf_fav_v14', JSON.stringify(favorites));
      renderProducts();
      renderFavorites();
    }

    function renderFavorites() {
      const container = document.getElementById('favItems');
      if (!container) return;
      container.innerHTML = '';
      const favProducts = products.filter(p => favorites.includes(p.id));
      const t = translations[currentLang] || translations.ru;
      if (favProducts.length === 0) {
        container.innerHTML = `<p style="color:var(--text-muted); text-align:center; padding:20px;">${t.emptyFav}</p>`;
        return;
      }
      favProducts.forEach(p => {
        container.innerHTML += `
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px; padding:10px; border:1px solid var(--border-color); border-radius:12px;">
            <img src="${p.image_url}" style="width:50px; height:50px; object-fit:contain; border-radius:8px;">
            <div style="flex:1;">
              <h4 style="font-size:13px;">${p.name}</h4>
              <strong style="color:var(--accent);">${formatPrice(p.price)}</strong>
            </div>
            <button type="button" class="secondary-button" style="width:auto; padding:6px 12px; margin:0;" onclick="toggleFavorite(${p.id})">Удалить</button>
          </div>
        `;
      });
    }

    function addToCart(id) {
      const item = products.find(p => p.id === id);
      const found = cart.find(i => i.id === id);
      if (found) { found.quantity++; } else { cart.push({productId: id, quantity: 1}); }
      updateCartCount();
      renderCart();
      showToast('Товар добавлен в корзину! 🛒');
    }

    function updateCartCount() {
      const count = cart.reduce((sum, i) => sum + i.quantity, 0);
      const badge = document.getElementById('cartCount');
      if (badge) badge.textContent = count;
    }

    function renderCart() {
      const container = document.getElementById('cartItems');
      if (!container) return;
      container.innerHTML = '';
      let total = 0;
      const t = translations[currentLang] || translations.ru;
      if (cart.length === 0) {
        container.innerHTML = `<p style="color:var(--text-muted); text-align:center; padding:20px;">${t.emptyCart}</p>`;
        document.getElementById('cartTotal').textContent = `${t.total}: ` + formatPrice(0);
        return;
      }
      cart.forEach((item, idx) => {
        const p = products.find(prod => prod.id === item.productId);
        if (!p) return;
        total += p.price * item.quantity;
        container.innerHTML += `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; padding:10px; border:1px solid var(--border-color); border-radius:12px;">
            <div>
              <h4 style="font-size:13px;">${p.name}</h4>
              <span style="font-size:12px; color:var(--text-muted);">${formatPrice(p.price)} x ${item.quantity}</span>
            </div>
            <button type="button" class="secondary-button" style="width:auto; padding:4px 10px; margin:0; background:rgba(239,68,68,0.1); color:#ef4444;" onclick="cart.splice(${idx},1); updateCartCount(); renderCart();">✕</button>
          </div>
        `;
      });
      document.getElementById('cartTotal').textContent = `${t.total}: ` + formatPrice(total);
    }

    function openCart() { renderCart(); document.getElementById('cartModal').hidden = false; }
    function closeCart() { document.getElementById('cartModal').hidden = true; }
    function openFavoritesModal() { renderFavorites(); document.getElementById('favoritesModal').hidden = false; }
    function closeFavoritesModal() { document.getElementById('favoritesModal').hidden = true; }
    function openSettingsModal() { document.getElementById('settingsModal').hidden = false; }
    function closeSettingsModal() { document.getElementById('settingsModal').hidden = true; }
    function openProfileModal() { updateProfileUI(); document.getElementById('profileModal').hidden = false; }
    function closeProfileModal() { document.getElementById('profileModal').hidden = true; }

    function updateProfileUI() {
      document.getElementById('profileGuestView').hidden = currentUser !== null;
      document.getElementById('profileLoginView').hidden = true;
      document.getElementById('profileUserView').hidden = currentUser === null;
      if (currentUser) {
        document.getElementById('profileUserName').textContent = currentUser.name;
        document.getElementById('profileUserPhone').textContent = currentUser.phone;
      }
    }

    function registerUser() {
      const name = document.getElementById('regName').value.trim();
      const phone = document.getElementById('regPhone').value.trim();
      const password = document.getElementById('regPassword').value;
      if (!name || !phone || !password) { alert('Заполните все поля!'); return; }
      currentUser = { id: Date.now(), name, phone, password };
      
      let existingIndex = users.findIndex(u => u.phone === phone);
      if (existingIndex >= 0) {
        users[existingIndex] = currentUser;
      } else {
        users.push(currentUser);
      }
      
      localStorage.setItem('raf_users_v14', JSON.stringify(users));
      localStorage.setItem('raf_current_user_v14', JSON.stringify(currentUser));
      updateProfileUI();
      showToast('Регистрация успешна!');
    }

    function showLoginForm() {
      document.getElementById('profileGuestView').hidden = true;
      document.getElementById('profileLoginView').hidden = false;
    }

    function loginUser() {
      const phone = document.getElementById('loginPhone').value.trim();
      const password = document.getElementById('loginPassword').value;
      const found = users.find(u => u.phone === phone && u.password === password);
      if (found) {
        currentUser = found;
        localStorage.setItem('raf_current_user_v14', JSON.stringify(currentUser));
        updateProfileUI();
        showToast('Вход выполнен!');
      } else {
        alert('Неверный телефон или пароль.');
      }
    }

    function logoutUser() {
      currentUser = null;
      localStorage.removeItem('raf_current_user_v14');
      updateProfileUI();
      showToast('Вы вышли из аккаунта');
    }

    function checkoutCart() {
      if (cart.length === 0) { alert('Корзина пуста!'); return; }
      if (currentUser) {
        document.getElementById('checkoutName').value = currentUser.name || '';
        document.getElementById('checkoutPhone').value = currentUser.phone || '';
      }
      document.getElementById('checkoutAddress').value = storeAddress;
      document.getElementById('checkoutModal').hidden = false;
      generateDcQr();
    }

    function closeCheckoutModal() { document.getElementById('checkoutModal').hidden = true; }

    function generateDcQr() {
      const container = document.getElementById('dcQrCode');
      container.innerHTML = '';
      const dcUrl = "dcnext://transfer?phone=992970664488";
      new QRCode(container, {
        text: dcUrl,
        width: 140,
        height: 140,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
      });
    }

    function handlePaymentMethodChange() {
      const method = document.getElementById('checkoutPaymentMethod').value;
      const qrBox = document.getElementById('checkoutQrContainer');
      qrBox.style.display = method === 'dc' ? 'flex' : 'none';
    }

    async function submitOrder() {
      const name = document.getElementById('checkoutName').value.trim();
      const phone = document.getElementById('checkoutPhone').value.trim();
      const address = document.getElementById('checkoutAddress').value.trim();
      const comment = document.getElementById('checkoutComment').value.trim();
      const paymentMethod = document.getElementById('checkoutPaymentMethod').value;

      if (!name || !phone || !address) { alert('Заполните обязательные поля!'); return; }

      let total = 0;
      let itemsSummary = cart.map(item => {
        const p = products.find(prod => prod.id === item.productId);
        if (p) {
          total += p.price * item.quantity;
          return `${p.name} (x${item.quantity})`;
        }
        return '';
      }).join(', ');

      const res = await fetch('/orders', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, phone, address, comment, items: itemsSummary, total})
      });

      if (res.ok) {
        showToast('Заказ оформлен! Статус: Ожидает одобрения продавцом ⏳');
        cart = [];
        updateCartCount();
        closeCheckoutModal();
        closeCart();
        loadOrdersFromServer();

        if (paymentMethod === 'whatsapp') {
          const waText = encodeURIComponent(`Здравствуйте! Новый заказ от ${name} (${phone}). Адрес: ${address}. Товары: ${itemsSummary}. Итого: ${total} сом. Комментарий: ${comment}`);
          window.location.href = `https://wa.me/992970664488?text=${waText}`;
        } else {
          window.location.href = "dcnext://transfer?phone=992970664488";
        }
      }
    }

    function previewNewProductImage(input) {
      if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
          document.getElementById('previewImgTag').src = e.target.result;
          document.getElementById('newProdImageBase64').value = e.target.result;
          document.getElementById('imagePreviewContainer').style.display = 'block';
        }
        reader.readAsDataURL(input.files[0]);
      }
    }

    // Детальный просмотр со всеми характеристиками для покупателя
    function openProductModal(id) {
      const p = products.find(item => item.id === id);
      if (!p) return;
      const modal = document.getElementById('productModal');
      const content = document.getElementById('productModalContent');
      content.innerHTML = `
        <img src="${p.image_url}" style="width:100%; height:220px; object-fit:contain; border-radius:12px; margin-bottom:12px;">
        <h2>${p.name}</h2>
        <p style="color:var(--accent); font-size:22px; font-weight:900; margin-bottom:12px;">${formatPrice(p.price)}</p>
        
        <div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:12px; border:1px solid var(--border-color); margin-bottom:15px; font-size:13px; line-height:1.6;">
          <p><strong>Категория:</strong> ${p.category || '—'}</p>
          <p><strong>Модель:</strong> ${p.model || '—'}</p>
          <p><strong>Артикул:</strong> ${p.art || '—'}</p>
          <p><strong>Цвет:</strong> ${p.color || '—'}</p>
          <p><strong>Мощность:</strong> ${p.power || '—'}</p>
          <p><strong>Энергопотребление:</strong> ${p.energy || '—'}</p>
        </div>

        <p style="font-size:13px; color:var(--text-secondary); margin-bottom:18px;"><strong>Описание:</strong><br>${p.description || 'Описание отсутствует.'}</p>
        <button type="button" class="order-button" onclick="addToCart(${p.id}); closeProductModal();">В корзину</button>
      `;
      modal.hidden = false;
    }
    function closeProductModal() { document.getElementById('productModal').hidden = true; }

    async function openOrderHistory() {
      if (!currentUser) { alert('Войдите в профиль.'); return; }
      await loadOrdersFromServer();
      const container = document.getElementById('orderHistoryList');
      container.innerHTML = '';
      const userOrders = orders.filter(o => o.phone === currentUser.phone);
      if (userOrders.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted);">У вас пока нет заказов.</p>';
      } else {
        userOrders.forEach(o => {
          let statusText = 'Ожидает подтверждения продавцом ⏳';
          let statusColor = '#f59e0b';
          if (o.status === 'approved') {
            statusText = 'Заказ принят и отправляется ✅';
            statusColor = '#10b981';
          } else if (o.status === 'rejected') {
            statusText = 'Заказ отклонён ❌';
            statusColor = '#ef4444';
          }
          container.innerHTML += `
            <div style="padding:12px; border:1px solid var(--border-color); border-radius:12px; margin-bottom:10px; background:rgba(255,255,255,0.02);">
              <strong>Заказ #${o.id}</strong><br>
              Товары: ${o.items}<br>
              Сумма: <b>${o.total} сом</b><br>
              Статус: <span style="color:${statusColor}; font-weight:800;">${statusText}</span>
            </div>
          `;
        });
      }
      document.getElementById('ordersModal').hidden = false;
    }
    function closeOrderHistory() { document.getElementById('ordersModal').hidden = true; }

    function setTheme(theme) {
      document.documentElement.dataset.theme = theme;
      localStorage.setItem('raf_theme_v14', theme);
    }
    const savedTheme = localStorage.getItem('raf_theme_v14');
    if (savedTheme) setTheme(savedTheme);

    function changeLanguage(lang) {
      applyLanguage(lang);
      renderProducts();
    }

    // Админка
    function openAdminModal() { document.getElementById('adminModal').hidden = false; }
    function closeAdminModal() { document.getElementById('adminModal').hidden = true; }

    function adminLoginSubmit() {
      const u = document.getElementById('adminLogin').value;
      const p = document.getElementById('adminPassword').value;
      if (u === 'admin' && p === 'RAF2026') {
        document.getElementById('adminLoginSection').hidden = true;
        document.getElementById('adminPanel').hidden = false;
        loadAdminOrders();
        loadStoreAddress();
        updateReports();
        renderAdminProductList();
      } else {
        alert('Неверный логин или пароль!');
      }
    }

    function adminLogout() {
      document.getElementById('adminLoginSection').hidden = false;
      document.getElementById('adminPanel').hidden = true;
    }

    function switchAdminTab(tab) {
      document.getElementById('addProductForm').hidden = tab !== 'add';
      document.getElementById('ordersSection').hidden = tab !== 'orders';
      document.getElementById('addressSection').hidden = tab !== 'address';
      document.getElementById('reportsSection').hidden = tab !== 'reports';
      
      document.querySelectorAll('#adminPanel .cat-btn').forEach(b => b.classList.remove('active'));
      if (tab === 'add') document.getElementById('tabAddProd').classList.add('active');
      if (tab === 'orders') { document.getElementById('tabOrders').classList.add('active'); loadAdminOrders(); }
      if (tab === 'address') { document.getElementById('tabAddress').classList.add('active'); loadStoreAddress(); }
      if (tab === 'reports') { document.getElementById('tabReports').classList.add('active'); updateReports(); }
    }

    async function saveStoreAddress() {
      const newAddr = document.getElementById('storeAddressInput').value.trim();
      if(!newAddr) { alert('Введите адрес!'); return; }
      const res = await fetch('/settings/store_address', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({address: newAddr})
      });
      if(res.ok) {
        storeAddress = newAddr;
        const displayEl = document.getElementById('headerAddressDisplay');
        if(displayEl) displayEl.textContent = '📍 ' + storeAddress;
        showToast('Адрес магазина обновлен! 🏪');
      }
    }

    // Сохранение или обновление товара
    async function handleSaveProduct() {
      const editId = document.getElementById('editProductId').value;
      const name = document.getElementById('newProdName').value.trim();
      const price = parseFloat(document.getElementById('newProdPrice').value);
      const category = document.getElementById('newProdCategory').value;
      const art = document.getElementById('newProdArt').value.trim();
      const color = document.getElementById('newProdColor').value.trim();
      const description = document.getElementById('newProdDesc').value.trim();
      const base64Img = document.getElementById('newProdImageBase64').value;
      const model = document.getElementById('newProdModel').value.trim();
      const power = document.getElementById('newProdPower').value.trim();
      const energy = document.getElementById('newProdEnergy').value.trim();

      if (!name || isNaN(price) || !art || !color) { 
        alert('Заполните обязательные поля (название, цена, артикул, цвет)!'); 
        return; 
      }

      const imageUrl = base64Img || 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500';

      let url = '/products';
      let method = 'POST';
      let bodyData = {name, price, category, art, color, description, model, power, energy, image_url: imageUrl};

      if (editId) {
        url = `/products/${editId}`;
        method = 'PUT';
      }

      const res = await fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(bodyData)
      });
      
      if (res.ok) {
        showToast(editId ? 'Товар успешно обновлен! ✏️' : 'Товар успешно добавлен! 🎉');
        resetProductForm();
        loadProducts();
      } else {
        alert('Ошибка при сохранении товара.');
      }
    }

    function resetProductForm() {
      document.getElementById('editProductId').value = '';
      document.getElementById('newProdName').value = '';
      document.getElementById('newProdPrice').value = '';
      document.getElementById('newProdArt').value = '';
      document.getElementById('newProdColor').value = '';
      document.getElementById('newProdDesc').value = '';
      document.getElementById('newProdModel').value = '';
      document.getElementById('newProdPower').value = '';
      document.getElementById('newProdEnergy').value = '';
      document.getElementById('newProdImageBase64').value = '';
      document.getElementById('imagePreviewContainer').style.display = 'none';
      document.getElementById('formTitleMode').textContent = '➕ Добавить новый товар';
      document.getElementById('addBtnText').textContent = 'Сохранить товар';
      document.getElementById('cancelEditBtn').style.display = 'none';
    }

    function editProduct(id) {
      const p = products.find(item => item.id === id);
      if (!p) return;
      document.getElementById('editProductId').value = p.id;
      document.getElementById('newProdName').value = p.name || '';
      document.getElementById('newProdPrice').value = p.price || '';
      document.getElementById('newProdCategory').value = p.category || 'Миксеры';
      document.getElementById('newProdModel').value = p.model || '';
      document.getElementById('newProdArt').value = p.art || '';
      document.getElementById('newProdColor').value = p.color || '';
      document.getElementById('newProdPower').value = p.power || '';
      document.getElementById('newProdEnergy').value = p.energy || '';
      document.getElementById('newProdDesc').value = p.description || '';
      
      if (p.image_url) {
        document.getElementById('previewImgTag').src = p.image_url;
        document.getElementById('newProdImageBase64').value = p.image_url;
        document.getElementById('imagePreviewContainer').style.display = 'block';
      }

      document.getElementById('formTitleMode').textContent = `✏️ Редактирование товара #${p.id}`;
      document.getElementById('addBtnText').textContent = 'Обновить товар';
      document.getElementById('cancelEditBtn').style.display = 'block';
      document.getElementById('addProductForm').scrollIntoView({behavior: 'smooth'});
    }

    async function deleteProduct(id) {
      if (!confirm('Вы действительно хотите удалить этот товар?')) return;
      const res = await fetch(`/products/${id}`, { method: 'DELETE' });
      if (res.ok) {
        showToast('Товар удален 🗑');
        loadProducts();
      }
    }

    function renderAdminProductList() {
      const container = document.getElementById('adminProductList');
      if (!container) return;
      container.innerHTML = '';
      if (products.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted); font-size:12px;">Товаров нет</p>';
        return;
      }
      products.forEach(p => {
        container.innerHTML += `
          <div style="display:flex; align-items:center; gap:8px; padding:8px; border:1px solid var(--border-color); border-radius:10px; margin-bottom:6px; background:rgba(255,255,255,0.02);">
            <img src="${p.image_url}" style="width:36px; height:36px; object-fit:contain; border-radius:6px;">
            <div style="flex:1; font-size:12px;">
              <strong>${p.name}</strong><br>
              <span style="color:var(--accent);">${p.price} сом</span> | ${p.category}
            </div>
            <button type="button" class="secondary-button" style="width:auto; padding:4px 8px; margin:0; font-size:11px;" onclick="editProduct(${p.id})">✏️</button>
            <button type="button" class="secondary-button" style="width:auto; padding:4px 8px; margin:0; font-size:11px; background:rgba(239,68,68,0.1); color:#ef4444;" onclick="deleteProduct(${p.id})">🗑</button>
          </div>
        `;
      });
    }

    async function loadAdminOrders() {
      await loadOrdersFromServer();
      const pendingContainer = document.getElementById('adminPendingOrdersList');
      const historyContainer = document.getElementById('adminHistoryOrdersList');
      pendingContainer.innerHTML = '';
      historyContainer.innerHTML = '';
      
      const pending = orders.filter(o => o.status === 'pending');
      const history = orders.filter(o => o.status === 'approved' || o.status === 'rejected');
      
      document.getElementById('pendingOrdersCount').textContent = pending.length;
      
      if (pending.length === 0) {
        pendingContainer.innerHTML = '<p style="color:var(--text-muted); font-size:12px;">Нет новых заявок</p>';
      } else {
        pending.forEach(o => {
          pendingContainer.innerHTML += `
            <div style="border:1px solid var(--border-color); padding:10px; border-radius:10px; margin-bottom:8px; font-size:13px;">
              <strong>Заказ #${o.id}</strong> — ${o.buyer_name} (${o.phone})<br>
              Адрес: ${o.address}<br>
              Товары: ${o.items}<br>Сумма: <b>${o.total} сом</b>
              <div style="display:flex; gap:6px; margin-top:8px;">
                <button type="button" class="order-button" style="padding:6px;" onclick="updateOrderStatus(${o.id}, 'approved')">Одобрить</button>
                <button type="button" class="secondary-button" style="padding:6px; margin:0; background:#ef4444; color:#fff;" onclick="updateOrderStatus(${o.id}, 'rejected')">Отклонить</button>
              </div>
            </div>
          `;
        });
      }

      if (history.length === 0) {
        historyContainer.innerHTML = '<p style="color:var(--text-muted); font-size:12px;">История пуста</p>';
      } else {
        history.forEach(o => {
          let badgeColor = o.status === 'approved' ? '#10b981' : '#ef4444';
          let statusLabel = o.status === 'approved' ? 'Одобрен' : 'Отклонён';
          historyContainer.innerHTML += `
            <div style="border:1px solid var(--border-color); padding:10px; border-radius:10px; margin-bottom:8px; font-size:12px; background:rgba(255,255,255,0.01);">
              <strong>Заказ #${o.id}</strong> | Покупатель: <b>${o.buyer_name}</b> (${o.phone})<br>
              Товары: ${o.items} | Сумма: ${o.total} сом<br>
              Статус: <span style="color:${badgeColor}; font-weight:800;">${statusLabel}</span>
            </div>
          `;
        });
      }
    }

    async function updateOrderStatus(id, status) {
      await fetch(`/orders/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status})
      });
      loadAdminOrders();
      updateReports();
    }

    async function updateReports() {
      await loadOrdersFromServer();
      const approved = orders.filter(o => o.status === 'approved');
      const totalRev = approved.reduce((sum, o) => sum + o.total, 0);
      document.getElementById('revTotal').textContent = totalRev + ' сом';

      let sortedBySales = [...products].sort((a, b) => (b.sales_count || 0) - (a.sales_count || 0));
      let topSoldHtml = sortedBySales.slice(0, 3).map(p => `• ${p.name} (продано: ${p.sales_count || 0})`).join('<br>') || 'Нет данных';
      document.getElementById('topSoldList').innerHTML = topSoldHtml;

      let sortedByFav = [...products].sort((a, b) => {
        let countA = favorites.includes(a.id) ? 1 : 0;
        let countB = favorites.includes(b.id) ? 1 : 0;
        return countB - countA;
      });
      let topFavHtml = sortedByFav.slice(0, 3).map(p => `• ${p.name} ${favorites.includes(p.id) ? '(В избранном)' : ''}`).join('<br>') || 'Нет данных';
      document.getElementById('topFavList').innerHTML = topFavHtml;
    }

    function filterCategory(cat, btn) {
      currentCategory = cat;
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      if(btn) btn.classList.add('active');
      renderProducts();
    }
    
    function toggleCategoryDropdown(e) { 
      e.stopPropagation(); 
      document.getElementById('categoryDropdown').classList.toggle('hidden'); 
    }
    
    document.addEventListener('click', () => {
      const dropdown = document.getElementById('categoryDropdown');
      if (dropdown && !dropdown.classList.contains('hidden')) {
        dropdown.classList.add('hidden');
      }
    });

    function filterCategoryDropdown(cat, btn) {
      currentCategory = cat;
      document.getElementById('categoryDropdown').classList.add('hidden');
      renderProducts();
    }

    function scrollToProducts() { document.getElementById('productsSection').scrollIntoView({behavior: 'smooth'}); }

    applyLanguage(currentLang);
    loadProducts();
  </script>
</body>
</html>
    """

@app.get("/products")
def get_products():
    conn = sqlite3.connect("raf_store.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/products")
def create_product(data: dict):
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, price, stock, image_url, description, model, art, color, power, energy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (data.get("name"), data.get("category"), data.get("price"), data.get("stock", 10), data.get("image_url"), data.get("description", ""), data.get("model", ""), data.get("art", ""), data.get("color", ""), data.get("power", ""), data.get("energy", ""))
    )
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.put("/products/{id}")
def update_product(id: int, data: dict):
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET name=?, category=?, price=?, image_url=?, description=?, model=?, art=?, color=?, power=?, energy=? WHERE id=?",
        (data.get("name"), data.get("category"), data.get("price"), data.get("image_url"), data.get("description", ""), data.get("model", ""), data.get("art", ""), data.get("color", ""), data.get("power", ""), data.get("energy", ""), id)
    )
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.delete("/products/{id}")
def delete_product(id: int):
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/settings/store_address")
def get_store_address():
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key='store_address'")
    row = cursor.fetchone()
    conn.close()
    return {"address": row[0] if row else ""}

@app.post("/settings/store_address")
def update_store_address(data: dict):
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('store_address', ?)", (data.get("address"),))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/orders")
def get_orders():
    conn = sqlite3.connect("raf_store.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/orders")
def create_order(data: dict):
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (buyer_name, phone, address, comment, items, total, status) VALUES (?, ?, ?, ?, ?, ?, 'pending')",
        (data.get("name"), data.get("phone"), data.get("address"), data.get("comment"), str(data.get("items")), data.get("total"))
    )
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.put("/orders/{id}")
def update_order_status(id: int, data: dict):
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status=? WHERE id=?", (data.get("status"), id))
    conn.commit()
    conn.close()
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

