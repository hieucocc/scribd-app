// State
let allAddons = [];
let filteredAddons = [];
let currentSim = 'msfs-2024';
let currentCatFilter = 'all';
let filterOnlyDirect = false;
let currentPage = 1;
const ITEMS_PER_PAGE = 6;

// i18n State & Dictionary
let currentLang = localStorage.getItem('skybound_lang') || 'vi';

const TRANSLATIONS = {
  vi: {
    page_title: "Skybound Archive - Kho Addon MSFS 2024, 2020 & X-Plane 12",
    app_title: "Skybound Archive",
    app_subtitle: "Kho lưu trữ & trích xuất link download Addon Flight Simulator",
    status_online: "Sẵn sàng trực tuyến",
    logout: "Đăng xuất",
    logout_title: "Đăng xuất khỏi hệ thống",
    sim_msfs2024_desc: "Airbus, Boeing PMDG, Black Square, Fenix & Tiện ích",
    sim_msfs2020_desc: "PMDG 777, TFDi MD-11, Soundpacks & FSLabs",
    sim_xplane12_desc: "ToLiss A319, A320, A321, A346 & Global Scenery",
    search_placeholder: "Tìm kiếm máy bay, addon hoặc nhà phát triển (vd: PMDG, 737, Fenix, Learjet, TBM, ToLiss...)",
    clear_search: "Xoá tìm kiếm",
    cat_all: "ALL ADDONS",
    cat_aircraft: "AIRCRAFT",
    cat_misc: "MISC",
    cat_scenery: "SCENERY",
    cat_utilities: "UTILITIES",
    report_prefix: "Báo cáo trích xuất:",
    report_ratio: "{withLinks} / {total} addon lấy được link",
    report_subtext: "{withLinks} addon có link tải trực tiếp • {locked} addon yêu cầu đăng nhập trên Skybound ({sim})",
    report_view_detail: "Xem chi tiết",
    report_collapse: "Thu gọn",
    report_col_success: "Lấy được link tải",
    report_col_locked: "Khóa đăng nhập Clerk",
    report_badge_locked: "🔒 Cần đăng nhập",
    report_badge_success: "{n} link ({host})",
    report_btn: "Báo cáo",
    toggle_report_title: "Hiện/ẩn khung báo cáo trích xuất",
    results_title: "Danh sách bài viết",
    copy_all: "Sao chép tất cả link",
    copy_all_title: "Sao chép toàn bộ link đang hiển thị",
    empty_title: "Không tìm thấy addon phù hợp",
    empty_desc: "Hãy thử tìm từ khoá khác hoặc chọn lại danh mục \"Tất cả\".",
    page_prev: "Trang trước",
    page_next: "Trang sau",
    page_info: "Trang {current} / {total}",
    card_pass_label: "Pass:",
    card_pass_copy: "Sao chép mật khẩu",
    card_versions_title: "Danh sách Link Download",
    card_open_link: "Mở link",
    card_download_fallback: "Tải về",
    card_locked_msg: "🔒 Link bài viết này được bảo vệ sau lớp đăng nhập Clerk trên trang gốc Skybound tại thời điểm lưu trữ.",
    card_resources_title: "Tài nguyên & Link liên quan",
    card_status_has_links: "✅ {n} link download",
    card_status_locked: "🔒 Yêu cầu đăng nhập",
    custom_extract_title: "Trích xuất link từ snapshot tuỳ ý",
    custom_extract_desc: "Dán bất kỳ liên kết snapshot nào của Skybound từ Wayback Machine để công cụ tự động bóc tách link download và mật khẩu.",
    custom_extract_placeholder: "Dán link archive.org (vd: https://web.archive.org/web/.../https://skybound.cx/...)",
    custom_extract_btn: "Trích xuất ngay",
    custom_samples: "Mẫu thử nhanh:",
    loading_data: "Đang tải dữ liệu...",
    loading_extracting: "Đang trích xuất snapshot...",
    loading_archive: "Đang tải dữ liệu kho lưu trữ Skybound...",
    footer_text: "Skybound Archive Extractor • Hoạt động hoàn toàn tự động",
    toast_copied: "Đã sao chép vào bộ nhớ tạm!",
    toast_no_links: "Không có link nào để sao chép trong danh sách hiện tại!",
    toast_copied_all: "Đã sao chép {links} link download của {addons} addon vào bộ nhớ tạm!",
    toast_enter_url: "Vui lòng nhập link Skybound!",
    toast_extract_success: "Đã trích xuất thành công: {title}",
    toast_extract_not_found: "Không tìm thấy link trong bài này!",
    toast_extract_error: "Lỗi: {error}",
    toast_logged_out: "Đã đăng xuất khỏi hệ thống.",
    toast_login_success: "Đăng nhập thành công! Chào mừng admin.",
    auth_title: "Xác thực quyền truy cập",
    auth_subtitle: "Vui lòng đăng nhập để mở kho lưu trữ và trích xuất link addon.",
    auth_user_label: "Tài khoản",
    auth_user_placeholder: "Tên đăng nhập (admin)",
    auth_pass_label: "Mật khẩu",
    auth_pass_placeholder: "Mật khẩu truy cập",
    auth_pwd_toggle: "Hiện/ẩn mật khẩu",
    auth_error: "Tài khoản hoặc mật khẩu không chính xác!",
    auth_submit: "Đăng nhập hệ thống",
    addons_count_suffix: "Addons"
  },
  en: {
    page_title: "Skybound Archive - MSFS 2024, 2020 & X-Plane 12 Addon Repository",
    app_title: "Skybound Archive",
    app_subtitle: "Flight Simulator Addon Archive & Direct Download Link Extractor",
    status_online: "Online & Ready",
    logout: "Log out",
    logout_title: "Log out of system",
    sim_msfs2024_desc: "Airbus, Boeing PMDG, Black Square, Fenix & Utilities",
    sim_msfs2020_desc: "PMDG 777, TFDi MD-11, Soundpacks & FSLabs",
    sim_xplane12_desc: "ToLiss A319, A320, A321, A346 & Global Scenery",
    search_placeholder: "Search aircraft, addons or developers (e.g. PMDG, 737, Fenix, Learjet, TBM, ToLiss...)",
    clear_search: "Clear search",
    cat_all: "ALL ADDONS",
    cat_aircraft: "AIRCRAFT",
    cat_misc: "MISC",
    cat_scenery: "SCENERY",
    cat_utilities: "UTILITIES",
    report_prefix: "Extraction Report:",
    report_ratio: "{withLinks} / {total} addons with links found",
    report_subtext: "{withLinks} direct download addons • {locked} addons require Skybound login ({sim})",
    report_view_detail: "View details",
    report_collapse: "Collapse",
    report_col_success: "Download links extracted",
    report_col_locked: "Clerk Login Protected",
    report_badge_locked: "🔒 Login required",
    report_badge_success: "{n} links ({host})",
    report_btn: "Report",
    toggle_report_title: "Show/hide extraction report banner",
    results_title: "Articles list",
    copy_all: "Copy all links",
    copy_all_title: "Copy all currently displayed links",
    empty_title: "No matching addons found",
    empty_desc: "Try searching with different keywords or select the \"ALL ADDONS\" category.",
    page_prev: "Previous",
    page_next: "Next",
    page_info: "Page {current} / {total}",
    card_pass_label: "Pass:",
    card_pass_copy: "Copy password",
    card_versions_title: "Download Links",
    card_open_link: "Open link",
    card_download_fallback: "Download",
    card_locked_msg: "🔒 Links for this article were protected behind Clerk authentication on the original Skybound snapshot at time of archiving.",
    card_resources_title: "Resources & Related Links",
    card_status_has_links: "✅ {n} download links",
    card_status_locked: "🔒 Login required",
    custom_extract_title: "Extract link from custom snapshot",
    custom_extract_desc: "Paste any Skybound snapshot link from Wayback Machine to automatically extract download links and passwords.",
    custom_extract_placeholder: "Paste archive.org link (e.g. https://web.archive.org/web/.../https://skybound.cx/...)",
    custom_extract_btn: "Extract now",
    custom_samples: "Quick presets:",
    loading_data: "Loading data...",
    loading_extracting: "Extracting snapshot...",
    loading_archive: "Loading Skybound archive data...",
    footer_text: "Skybound Archive Extractor • Fully automated",
    toast_copied: "Copied to clipboard!",
    toast_no_links: "No links available to copy in current view!",
    toast_copied_all: "Copied {links} download links from {addons} addons to clipboard!",
    toast_enter_url: "Please enter a Skybound link!",
    toast_extract_success: "Successfully extracted: {title}",
    toast_extract_not_found: "No links found in this article!",
    toast_extract_error: "Error: {error}",
    toast_logged_out: "Logged out of system.",
    toast_login_success: "Login successful! Welcome admin.",
    auth_title: "Access Authentication",
    auth_subtitle: "Please log in to access the archive and extract addon links.",
    auth_user_label: "Username",
    auth_user_placeholder: "Username (admin)",
    auth_pass_label: "Password",
    auth_pass_placeholder: "Access password",
    auth_pwd_toggle: "Show/hide password",
    auth_error: "Incorrect username or password!",
    auth_submit: "Sign in to system",
    addons_count_suffix: "Addons"
  }
};

function t(key, params = {}) {
  const dict = TRANSLATIONS[currentLang] || TRANSLATIONS.vi;
  let text = dict[key] || TRANSLATIONS.vi[key] || key;
  for (const [k, v] of Object.entries(params)) {
    text = text.replace(new RegExp(`\\{${k}\\}`, 'g'), v);
  }
  return text;
}

function setLanguage(lang) {
  if (lang !== 'vi' && lang !== 'en') lang = 'vi';
  currentLang = lang;
  localStorage.setItem('skybound_lang', lang);
  document.documentElement.lang = lang;

  // Update page title
  document.title = t('page_title');

  // Update active state on all lang-switch buttons across header & modal
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
  });

  // Update text for all elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (key && TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) {
      el.textContent = t(key);
    }
  });

  // Update placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (key) el.setAttribute('placeholder', t(key));
  });

  // Update titles
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    if (key) el.setAttribute('title', t(key));
  });

  // Update report details toggle text if present
  if (reportToggleText && reportDetails) {
    const isHidden = reportDetails.classList.contains('hidden');
    reportToggleText.textContent = isHidden ? t('report_view_detail') : t('report_collapse');
  }

  // Update dynamic content
  updateSimCounts();
  if (allAddons.length > 0) {
    updateReportBanner();
    renderPage();
  }
}

// Delegated listener for language switcher buttons
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.lang-btn');
  if (btn) {
    const lang = btn.getAttribute('data-lang');
    if (lang) {
      setLanguage(lang);
    }
  }
});

// Elements
const tabSkybound = document.getElementById('tabSkybound');
const tabCustomExtract = document.getElementById('tabCustomExtract');
const skyboundView = document.getElementById('skyboundView');
const customExtractView = document.getElementById('customExtractView');

const simCards = document.querySelectorAll('.sim-card');
const countMsfs2024 = document.getElementById('countMsfs2024');
const countMsfs2020 = document.getElementById('countMsfs2020');
const countXplane12 = document.getElementById('countXplane12');

const catalogSearchInput = document.getElementById('catalogSearchInput');
const btnClearSearch = document.getElementById('btnClearSearch');
const categoryFilterChips = document.getElementById('categoryFilterChips');


const activeSimLabel = document.getElementById('activeSimLabel');
const resultsCount = document.getElementById('resultsCount');
const cardsGrid = document.getElementById('cardsGrid');
const btnCopyAllRaw = document.getElementById('btnCopyAllRaw');

const paginationControls = document.getElementById('paginationControls');
const btnPrevPage = document.getElementById('btnPrevPage');
const btnNextPage = document.getElementById('btnNextPage');
const pageInfo = document.getElementById('pageInfo');

if (btnPrevPage) {
  btnPrevPage.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      renderPage();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
}

if (btnNextPage) {
  btnNextPage.addEventListener('click', () => {
    const totalPages = Math.ceil(filteredAddons.length / ITEMS_PER_PAGE);
    if (currentPage < totalPages) {
      currentPage++;
      renderPage();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
}

// Report elements
const reportBanner = document.getElementById('reportBanner');
const reportToggle = document.getElementById('reportToggle');
const btnToggleReport = document.getElementById('btnToggleReport');
const reportToggleText = document.getElementById('reportToggleText');
const reportArrow = document.getElementById('reportArrow');
const reportDetails = document.getElementById('reportDetails');
const reportRatio = document.getElementById('reportRatio');
const reportSubtext = document.getElementById('reportSubtext');
const countSuccess = document.getElementById('countSuccess');
const countLocked = document.getElementById('countLocked');
const listSuccess = document.getElementById('listSuccess');
const listLocked = document.getElementById('listLocked');

// Toggle report details
function toggleReportDetails() {
  const isHidden = reportDetails.classList.toggle('hidden');
  reportArrow.classList.toggle('rotated', !isHidden);
  reportToggleText.textContent = isHidden ? 'Xem chi tiết' : 'Thu gọn';
}

reportToggle.addEventListener('click', (e) => {
  // Prevent double toggle if button itself clicked
  if (e.target.closest('#btnToggleReport')) return;
  toggleReportDetails();
});
btnToggleReport.addEventListener('click', toggleReportDetails);

const btnToggleReportBanner = document.getElementById('btnToggleReportBanner');
if (btnToggleReportBanner && reportBanner) {
  btnToggleReportBanner.addEventListener('click', () => {
    const isHidden = reportBanner.classList.toggle('hidden');
    if (!isHidden) {
      reportBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  });
}

const singleUrlInput = document.getElementById('singleUrlInput');
const btnExtractSingle = document.getElementById('btnExtractSingle');

const loadingIndicator = document.getElementById('loadingIndicator');
const loadingText = document.getElementById('loadingText');

const toast = document.getElementById('toast');
const toastMsg = document.getElementById('toastMsg');

// 1. Main Navigation Tabs (if present)
if (tabSkybound && tabCustomExtract) {
  tabSkybound.addEventListener('click', () => {
    tabSkybound.classList.add('active');
    tabCustomExtract.classList.remove('active');
    if (skyboundView) skyboundView.classList.remove('hidden');
    if (customExtractView) customExtractView.classList.add('hidden');
  });

  tabCustomExtract.addEventListener('click', () => {
    tabCustomExtract.classList.add('active');
    tabSkybound.classList.remove('active');
    if (customExtractView) customExtractView.classList.remove('hidden');
    if (skyboundView) skyboundView.classList.add('hidden');
  });
}


// 2. Simulator Selector Cards
const SIM_NAMES = {
  'msfs-2024': 'MSFS 2024',
  'msfs-2020': 'MSFS 2020',
  'xplane-12': 'X-Plane 12'
};

simCards.forEach(card => {
  card.addEventListener('click', () => {
    simCards.forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    currentSim = card.getAttribute('data-sim');
    activeSimLabel.textContent = SIM_NAMES[currentSim] || currentSim;
    renderCards();
  });
});

// 3. Search & Clear Search
catalogSearchInput.addEventListener('input', () => {
  if (catalogSearchInput.value.trim()) {
    btnClearSearch.classList.remove('hidden');
  } else {
    btnClearSearch.classList.add('hidden');
  }
  renderCards();
});

btnClearSearch.addEventListener('click', () => {
  catalogSearchInput.value = '';
  btnClearSearch.classList.add('hidden');
  catalogSearchInput.focus();
  renderCards();
});

// 4. Category Filter Chips
if (categoryFilterChips) {
  categoryFilterChips.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      categoryFilterChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentCatFilter = chip.getAttribute('data-cat') || 'all';
      renderCards();
    });
  });
}



// 5. Presets in Custom Extract tab
document.querySelectorAll('.preset-pill').forEach(pill => {
  pill.addEventListener('click', () => {
    const url = pill.getAttribute('data-url');
    singleUrlInput.value = url;
    triggerCustomExtract();
  });
});

btnExtractSingle.addEventListener('click', triggerCustomExtract);
singleUrlInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') triggerCustomExtract();
});

async function triggerCustomExtract() {
  const url = singleUrlInput.value.trim();
  if (!url) {
    showToast(t('toast_enter_url'), true);
    singleUrlInput.focus();
    return;
  }
  
  setLoading(true, t('loading_extracting'));
  try {
    const resp = await fetch('/api/extract', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    setLoading(false);

    if (data.results && data.results.length > 0 && data.results[0].success) {
      const item = data.results[0].data;
      if (!item.sim) item.sim = currentSim;
      // Add to list
      allAddons = allAddons.filter(x => x.slug !== item.slug);
      allAddons.unshift(item);
      updateSimCounts();
      // Switch back to Skybound tab and highlight
      tabSkybound.click();
      renderCards();
      showToast(t('toast_extract_success', { title: item.title }));
    } else {
      showToast(t('toast_extract_not_found'), true);
    }
  } catch (err) {
    setLoading(false);
    showToast(t('toast_extract_error', { error: err.message }), true);
  }
}

// 6. Load Pre-Extracted Data on Init
async function initApp() {
  setLoading(true, t('loading_archive'));
  try {
    const resp = await fetch('/extracted_cache.json');
    if (resp.ok) {
      const data = await resp.json();
      allAddons = data.results || Object.values(data) || [];
      
      // Normalize sim field
      allAddons.forEach(item => {
        if (!item.sim) item.sim = 'msfs-2024';
      });

      // Sort: items with download links first, then alphabetically
      allAddons.sort((a, b) => {
        const aHas = (a.versions && a.versions.length > 0) ? 1 : 0;
        const bHas = (b.versions && b.versions.length > 0) ? 1 : 0;
        if (aHas !== bHas) return bHas - aHas;
        return (a.title || '').localeCompare(b.title || '');
      });

      updateSimCounts();
      renderCards();
    }
  } catch (err) {
    console.warn("Error loading cache:", err);
  } finally {
    setLoading(false);
  }
}

// Update counts on simulator cards
function updateSimCounts() {
  const c2024 = allAddons.filter(x => x.sim === 'msfs-2024').length;
  const c2020 = allAddons.filter(x => x.sim === 'msfs-2020').length;
  const cXp12 = allAddons.filter(x => x.sim === 'xplane-12').length;

  const suffix = t('addons_count_suffix');
  if (countMsfs2024) countMsfs2024.textContent = `${c2024} ${suffix}`;
  if (countMsfs2020) countMsfs2020.textContent = `${c2020} ${suffix}`;
  if (countXplane12) countXplane12.textContent = `${cXp12} ${suffix}`;
}

function cleanDisplayName(title) {
  if (!title) return '';
  return title
    .replace(/\s*-\s*Microsoft Flight Simulator\s*(?:2024|2020)?/gi, '')
    .replace(/\s*-\s*X-Plane\s*(?:12|11)?/gi, '')
    .replace(/\s*\|\s*Skybound/gi, '')
    .trim();
}

function hasValidLinks(item) {
  if (!item) return false;
  const hasVer = Array.isArray(item.versions) && item.versions.some(v => v && typeof v.url === 'string' && v.url.trim().startsWith('http'));
  const hasExtra = Array.isArray(item.extra_links) && item.extra_links.some(u => u && typeof u === 'string' && u.trim().startsWith('http'));
  return hasVer || hasExtra;
}

// Update Report Banner
function updateReportBanner() {
  const simAddons = allAddons.filter(item => item.sim === currentSim);
  const withLinks = simAddons.filter(item => hasValidLinks(item));
  const locked = simAddons.filter(item => !hasValidLinks(item));

  const simTitle = SIM_NAMES[currentSim] || currentSim;
  reportRatio.textContent = t('report_ratio', { withLinks: withLinks.length, total: simAddons.length });
  reportSubtext.textContent = t('report_subtext', { withLinks: withLinks.length, locked: locked.length, sim: simTitle });

  countSuccess.textContent = withLinks.length;
  countLocked.textContent = locked.length;

  const titleSuccess = document.getElementById('titleSuccess');
  if (titleSuccess) {
    titleSuccess.innerHTML = `${t('report_col_success')} (<span id="countSuccess">${withLinks.length}</span>)`;
  }
  const titleLocked = document.getElementById('titleLocked');
  if (titleLocked) {
    titleLocked.innerHTML = `${t('report_col_locked')} (<span id="countLocked">${locked.length}</span>)`;
  }

  // Render list of success
  listSuccess.innerHTML = withLinks.map(item => {
    const validVers = (item.versions || []).filter(v => v && typeof v.url === 'string' && v.url.startsWith('http'));
    const firstUrl = (validVers[0] && validVers[0].url) || (item.extra_links && item.extra_links[0]) || '';
    const host = getHostname(firstUrl) || 'Download';
    const n = validVers.length + (item.extra_links ? item.extra_links.length : 0);
    const cleanName = cleanDisplayName(item.title) || item.title;
    const badgeText = t('report_badge_success', { n, host });
    return `
      <div class="report-item-row" onclick="scrollToCard('${escapeQuotes(item.slug)}')" title="${escapeHtml(item.title)}">
        <span class="report-item-name">${escapeHtml(cleanName)}</span>
        <span class="report-item-badge badge-success">${escapeHtml(badgeText)}</span>
      </div>
    `;
  }).join('');

  // Render list of locked
  listLocked.innerHTML = locked.map(item => {
    const cleanName = cleanDisplayName(item.title) || item.title;
    return `
      <div class="report-item-row" onclick="scrollToCard('${escapeQuotes(item.slug)}')" title="${escapeHtml(item.title)}">
        <span class="report-item-name">${escapeHtml(cleanName)}</span>
        <span class="report-item-badge badge-locked">${escapeHtml(t('report_badge_locked'))}</span>
      </div>
    `;
  }).join('');
}

window.scrollToCard = function(slug) {
  const card = document.getElementById(`addon-card-${slug}`);
  if (card) {
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.style.borderColor = 'var(--cyan)';
    card.style.boxShadow = '0 0 20px var(--cyan-glow)';
    setTimeout(() => {
      card.style.borderColor = '';
      card.style.boxShadow = '';
    }, 2000);
  }
};

window.toggleArticle = function(slug) {
  const content = document.getElementById(`article-full-${slug}`);
  const arrow = document.getElementById(`arrow-toggle-${slug}`);
  const label = document.getElementById(`label-toggle-${slug}`);
  if (content) {
    content.classList.toggle('open');
    const isOpen = content.classList.contains('open');
    if (arrow) arrow.classList.toggle('rotated', isOpen);
    if (label) {
      label.textContent = isOpen 
        ? (currentLang === 'vi' ? 'Thu gọn bài viết' : 'Collapse article') 
        : (currentLang === 'vi' ? 'Xem chi tiết bài viết & Tính năng' : 'View full article & Features');
    }
  }
};

// Category Helper & Detector
function getItemCategory(item) {
  if (item && item.category) {
    const c = String(item.category).toLowerCase().trim();
    if (c === 'aircraft' || c === 'misc' || c === 'scenery' || c === 'utilities') {
      return c;
    }
  }
  const title = (item && item.title ? item.title : '').toLowerCase();
  const slug = (item && item.slug ? item.slug : '').toLowerCase();
  if (slug.includes('airport') || slug.includes('scenery') || title.includes('airport') || title.includes('scenery') || slug.includes('helipads')) {
    return 'scenery';
  }
  if (slug.includes('gsx') || slug.includes('flow') || slug.includes('chaseplane') || slug.includes('vraas') || slug.includes('missionhub') || slug.includes('atmos')) {
    return 'utilities';
  }
  if (slug.includes('sound') || slug.includes('textures') || slug.includes('airac') || slug.includes('seasons') || slug.includes('earthfx') || slug.includes('shipping')) {
    return 'misc';
  }
  return 'aircraft';
}

// Update Category Badge Counts on Sidebar
function updateCategoryCounts(simAddons) {
  const cAll = simAddons.length;
  const cAircraft = simAddons.filter(item => getItemCategory(item) === 'aircraft').length;
  const cMisc = simAddons.filter(item => getItemCategory(item) === 'misc').length;
  const cScenery = simAddons.filter(item => getItemCategory(item) === 'scenery').length;
  const cUtilities = simAddons.filter(item => getItemCategory(item) === 'utilities').length;
  const cDirect = simAddons.filter(item => hasValidLinks(item)).length;

  const elAll = document.getElementById('countCatAll');
  const elAir = document.getElementById('countCatAircraft');
  const elMisc = document.getElementById('countCatMisc');
  const elScen = document.getElementById('countCatScenery');
  const elUtil = document.getElementById('countCatUtilities');
  const elDir = document.getElementById('countDirectLinks');

  if (elAll) elAll.textContent = cAll;
  if (elAir) elAir.textContent = cAircraft;
  if (elMisc) elMisc.textContent = cMisc;
  if (elScen) elScen.textContent = cScenery;
  if (elUtil) elUtil.textContent = cUtilities;
  if (elDir) elDir.textContent = cDirect;
}

// 7. Render Addon Cards
function renderCards() {
  updateReportBanner();
  const query = (catalogSearchInput.value || '').toLowerCase().trim();

  // Filter by active Simulator
  const simAddons = allAddons.filter(item => item.sim === currentSim);
  updateCategoryCounts(simAddons);

  // Filter by Search and Category
  const filtered = simAddons.filter(item => {
    const title = (item.title || '').toLowerCase();
    const slug = (item.slug || '').toLowerCase();
    const matchQuery = !query || title.includes(query) || slug.includes(query);

    let matchCat = true;
    if (currentCatFilter === 'has_links') {
      matchCat = hasValidLinks(item);
    } else if (currentCatFilter !== 'all') {
      matchCat = (getItemCategory(item) === currentCatFilter);
    }

    return matchQuery && matchCat;
  });


  filteredAddons = filtered;
  currentPage = 1;
  renderPage();
}


function renderPage() {
  const simAddons = allAddons.filter(item => item.sim === currentSim);
  resultsCount.textContent = `${filteredAddons.length} / ${simAddons.length}`;
  cardsGrid.innerHTML = '';

  if (filteredAddons.length === 0) {
    cardsGrid.innerHTML = `
      <div class="card" style="text-align: center; padding: 48px 24px; color: var(--text-muted); grid-column: 1 / -1;">
        <p style="font-size: 1.15rem; font-weight: 600; color: #fff; margin-bottom: 6px;">${escapeHtml(t('empty_title'))}</p>
        <p style="font-size: 0.88rem; color: var(--text-sub);">${escapeHtml(t('empty_desc'))}</p>
      </div>
    `;
    if (paginationControls) paginationControls.classList.add('hidden');
    return;
  }

  const totalPages = Math.ceil(filteredAddons.length / ITEMS_PER_PAGE);
  if (currentPage > totalPages) currentPage = totalPages;
  if (currentPage < 1) currentPage = 1;

  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, filteredAddons.length);
  const pageItems = filteredAddons.slice(startIndex, endIndex);

  pageItems.forEach(item => {
    const card = createAddonCard(item);
    cardsGrid.appendChild(card);
  });

  if (paginationControls) {
    if (totalPages > 1) {
      paginationControls.classList.remove('hidden');
      pageInfo.textContent = t('page_info', { current: currentPage, total: totalPages });
      if (btnPrevPage) {
        btnPrevPage.textContent = t('page_prev');
        btnPrevPage.disabled = currentPage === 1;
      }
      if (btnNextPage) {
        btnNextPage.textContent = t('page_next');
        btnNextPage.disabled = currentPage === totalPages;
      }
    } else {
      paginationControls.classList.add('hidden');
    }
  }
}

// Card Factory
function createAddonCard(d) {
  const card = document.createElement('div');
  card.className = 'addon-card';
  card.id = 'addon-card-' + (d.slug || '');

  const validVersions = (d.versions || []).filter(v => v && typeof v.url === 'string' && v.url.trim().startsWith('http'));
  const hasLinks = validVersions.length > 0 || (d.extra_links && d.extra_links.length > 0);

  // 1. Cover Image Banner
  const DEFAULT_THUMBNAIL = 'https://web.archive.org/web/20260519175530im_/https://skybound.cx/api/media/file/a2a-aerostar-600-1400x777.webp';
  const imgUrl = (d.image && typeof d.image === 'string' && d.image.trim().startsWith('http'))
    ? d.image.trim()
    : DEFAULT_THUMBNAIL;

  const coverHtml = `
    <div class="addon-cover-wrapper">
      <img src="${escapeHtml(imgUrl)}" class="addon-cover-img" alt="${escapeHtml(d.title)}" loading="lazy" onerror="this.onerror=null; this.src='${DEFAULT_THUMBNAIL}';">
      <div class="addon-cover-overlay"></div>
    </div>
  `;

  // 2. Versions list
  let versionsHtml = '';
  if (validVersions.length > 0) {
    versionsHtml = validVersions.map(v => {
      const ver = escapeHtml(v.versionNumber || t('card_download_fallback'));
      const link = escapeHtml(v.url.trim());
      const host = getHostname(v.url);
      return `
        <div class="version-item">
          <div class="version-info">
            <span class="version-badge">${ver}</span>
            <span class="version-host">${host}</span>
          </div>
          <div class="version-buttons">
            <a href="${link}" target="_blank" rel="noopener noreferrer" class="btn-action btn-open">
              ${escapeHtml(t('card_open_link'))}
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            </a>
          </div>
        </div>
      `;
    }).join('');
  } else {
    versionsHtml = `
      <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); padding: 12px 16px; border-radius: var(--radius-sm); font-size: 0.85rem; color: #fca5a5;">
        ${escapeHtml(t('card_locked_msg'))}
      </div>
    `;
  }

  // 3. Extra links
  let extraHtml = '';
  if (d.extra_links && d.extra_links.length > 0) {
    const pills = d.extra_links.map(l => {
      const label = getLabelForUrl(l);
      return `
        <a href="${escapeHtml(l)}" target="_blank" rel="noopener noreferrer" class="extra-link-pill">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
          ${label}
        </a>
      `;
    }).join('');

    extraHtml = `
      <div class="extra-section">
        <div class="extra-title">${escapeHtml(t('card_resources_title'))}</div>
        <div class="extra-links-list">${pills}</div>
      </div>
    `;
  }

  const statusBadge = hasLinks
    ? `<span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3);">${escapeHtml(t('card_status_has_links', { n: validVersions.length }))}</span>`
    : `<span class="badge" style="background: rgba(255, 255, 255, 0.05); color: #94a3b8;">${escapeHtml(t('card_status_locked'))}</span>`;

  const catName = getItemCategory(d).toUpperCase();
  const simBadgeText = SIM_NAMES[d.sim] || 'MSFS 2024';

  card.innerHTML = `
    ${coverHtml}
    <div class="addon-card-header">
      <div style="width: 100%; min-width: 0; overflow: hidden;">
        <div class="addon-title" title="${escapeHtml(d.title)}">${escapeHtml(d.title)}</div>
        <div class="addon-meta">
          <span class="badge badge-sim">${escapeHtml(simBadgeText)}</span>
          <span class="badge" style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); text-transform: uppercase; font-size: 0.72rem; font-weight: 700;">${escapeHtml(catName)}</span>
          ${statusBadge}
          <div class="password-box">
            <span class="password-label">${escapeHtml(t('card_pass_label'))}</span>
            <span class="password-value">${escapeHtml(d.password || 'https://skybound.cx')}</span>
            <button class="btn-icon-copy" title="${escapeHtml(t('card_pass_copy'))}" onclick="copyText('${escapeQuotes(d.password || 'https://skybound.cx')}')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            </button>
          </div>
          <span style="font-size: 0.75rem; color: #64748b; font-family: monospace;">${escapeHtml(d.slug || '')}</span>
        </div>
      </div>
    </div>
    <div class="addon-card-body">
      <div class="versions-title">${escapeHtml(t('card_versions_title'))}</div>
      <div class="versions-list">${versionsHtml}</div>
      ${extraHtml}
    </div>
  `;


  return card;
}

// 8. Copy All Links for active view
btnCopyAllRaw.addEventListener('click', () => {
  const allUrls = [];
  filteredAddons.forEach(r => {
    if (r.versions) {
      r.versions.forEach(v => { if (v && v.url) allUrls.push(v.url); });
    }
    if (r.extra_links) {
      r.extra_links.forEach(l => { if (l) allUrls.push(l); });
    }
  });

  if (allUrls.length === 0) {
    showToast(t('toast_no_links'), true);
    return;
  }

  copyText(allUrls.join('\n'));
  showToast(t('toast_copied_all', { links: allUrls.length, addons: filteredAddons.length }));
});


// Helpers
function setLoading(isLoading, text = "") {
  if (isLoading) {
    loadingIndicator.classList.remove('hidden');
    loadingText.textContent = text || t('loading_data');
  } else {
    loadingIndicator.classList.add('hidden');
  }
}

window.copyText = function(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast(t('toast_copied'));
  }).catch(() => {
    const tEl = document.createElement('textarea');
    tEl.value = text;
    document.body.appendChild(tEl);
    tEl.select();
    document.execCommand('copy');
    document.body.removeChild(tEl);
    showToast(t('toast_copied'));
  });
};

let toastTimeout;
function showToast(msg, isError = false) {
  clearTimeout(toastTimeout);
  toastMsg.textContent = msg;
  toast.style.borderColor = isError ? '#ef4444' : 'var(--emerald)';
  toast.classList.remove('hidden');
  toastTimeout = setTimeout(() => {
    toast.classList.add('hidden');
  }, 2600);
}

function getHostname(urlStr) {
  try {
    return new URL(urlStr).hostname.replace('www.', '');
  } catch {
    return 'link';
  }
}

function getLabelForUrl(urlStr) {
  if (urlStr.includes('flightsim.to')) return 'Flightsim.to Livery';
  if (urlStr.endsWith('.pdf') || urlStr.includes('manual')) return 'Pilot Manual (PDF)';
  if (urlStr.includes('binding') || urlStr.includes('download')) return 'Software Binding';
  return getHostname(urlStr);
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function escapeQuotes(str) {
  if (!str) return '';
  return str.replace(/'/g, "\\'").replace(/"/g, '\\"');
}

// --- Authentication Gate ---
const AUTH_USER = 'admin';
const AUTH_PASS = 'thunghiem123#$H';
const AUTH_STORAGE_KEY = 'skybound_admin_auth_v1';

const authModalOverlay = document.getElementById('authModalOverlay');
const authForm = document.getElementById('authForm');
const authUsername = document.getElementById('authUsername');
const authPassword = document.getElementById('authPassword');
const authErrorMsg = document.getElementById('authErrorMsg');
const authErrorText = document.getElementById('authErrorText');
const btnToggleAuthPwd = document.getElementById('btnToggleAuthPwd');
const eyeOpenIcon = document.getElementById('eyeOpenIcon');
const eyeClosedIcon = document.getElementById('eyeClosedIcon');
const userBadge = document.getElementById('userBadge');
const btnLogout = document.getElementById('btnLogout');

function isAuthenticated() {
  return localStorage.getItem(AUTH_STORAGE_KEY) === 'authenticated_admin';
}

function showAuthModal() {
  if (authModalOverlay) {
    authModalOverlay.classList.remove('hidden');
    if (authErrorMsg) authErrorMsg.classList.add('hidden');
    if (authUsername) {
      authUsername.value = '';
      setTimeout(() => authUsername.focus(), 150);
    }
    if (authPassword) authPassword.value = '';
  }
  if (userBadge) userBadge.classList.add('hidden');
}

function hideAuthModal() {
  if (authModalOverlay) {
    authModalOverlay.classList.add('hidden');
  }
  if (userBadge) userBadge.classList.remove('hidden');
}

if (btnToggleAuthPwd) {
  btnToggleAuthPwd.addEventListener('click', () => {
    const isPwd = authPassword.type === 'password';
    authPassword.type = isPwd ? 'text' : 'password';
    if (eyeOpenIcon) eyeOpenIcon.classList.toggle('hidden', isPwd);
    if (eyeClosedIcon) eyeClosedIcon.classList.toggle('hidden', !isPwd);
  });
}

if (authForm) {
  authForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const u = (authUsername.value || '').trim();
    const p = authPassword.value || '';

    if (u === AUTH_USER && p === AUTH_PASS) {
      localStorage.setItem(AUTH_STORAGE_KEY, 'authenticated_admin');
      hideAuthModal();
      showToast(t('toast_login_success'));
      if (allAddons.length === 0) {
        initApp();
      }
    } else {
      if (authErrorMsg) authErrorMsg.classList.remove('hidden');
      authPassword.value = '';
      authPassword.focus();
    }
  });
}

if (btnLogout) {
  btnLogout.addEventListener('click', () => {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    allAddons = [];
    filteredAddons = [];
    cardsGrid.innerHTML = '';
    showAuthModal();
    showToast(t('toast_logged_out'));
  });
}

// Initial Boot & Language Setup
setLanguage(currentLang);

if (isAuthenticated()) {
  hideAuthModal();
  initApp();
} else {
  showAuthModal();
}


