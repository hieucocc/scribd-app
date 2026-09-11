// State
let allAddons = [];
let currentSim = 'msfs-2024';
let currentCatFilter = 'all';

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

const singleUrlInput = document.getElementById('singleUrlInput');
const btnExtractSingle = document.getElementById('btnExtractSingle');

const loadingIndicator = document.getElementById('loadingIndicator');
const loadingText = document.getElementById('loadingText');

const toast = document.getElementById('toast');
const toastMsg = document.getElementById('toastMsg');

// 1. Main Navigation Tabs
tabSkybound.addEventListener('click', () => {
  tabSkybound.classList.add('active');
  tabCustomExtract.classList.remove('active');
  skyboundView.classList.remove('hidden');
  customExtractView.classList.add('hidden');
});

tabCustomExtract.addEventListener('click', () => {
  tabCustomExtract.classList.add('active');
  tabSkybound.classList.remove('active');
  customExtractView.classList.remove('hidden');
  skyboundView.classList.add('hidden');
});

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
categoryFilterChips.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    categoryFilterChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    currentCatFilter = chip.getAttribute('data-cat');
    renderCards();
  });
});

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
    showToast("Vui lòng nhập link Skybound!", true);
    singleUrlInput.focus();
    return;
  }
  
  setLoading(true, "Đang trích xuất snapshot...");
  try {
    const resp = await fetch('/api/extract', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    if (!resp.ok) throw new Error(`Mã lỗi HTTP ${resp.status}`);
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
      showToast(`Đã trích xuất thành công: ${item.title}`);
    } else {
      showToast("Không tìm thấy link trong bài này!", true);
    }
  } catch (err) {
    setLoading(false);
    showToast(`Lỗi: ${err.message}`, true);
  }
}

// 6. Load Pre-Extracted Data on Init
async function initApp() {
  setLoading(true, "Đang tải dữ liệu kho lưu trữ Skybound...");
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
    console.warn("Lỗi tải cache:", err);
  } finally {
    setLoading(false);
  }
}

// Update counts on simulator cards
function updateSimCounts() {
  const c2024 = allAddons.filter(x => x.sim === 'msfs-2024').length;
  const c2020 = allAddons.filter(x => x.sim === 'msfs-2020').length;
  const cXp12 = allAddons.filter(x => x.sim === 'xplane-12').length;

  if (countMsfs2024) countMsfs2024.textContent = `${c2024} Addons`;
  if (countMsfs2020) countMsfs2020.textContent = `${c2020} Addons`;
  if (countXplane12) countXplane12.textContent = `${cXp12} Addons`;
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
  reportRatio.textContent = `${withLinks.length} / ${simAddons.length} addon lấy được link`;
  reportSubtext.textContent = `${withLinks.length} addon có link tải trực tiếp • ${locked.length} addon yêu cầu đăng nhập trên Skybound (${simTitle})`;

  countSuccess.textContent = withLinks.length;
  countLocked.textContent = locked.length;

  // Render list of success
  listSuccess.innerHTML = withLinks.map(item => {
    const validVers = (item.versions || []).filter(v => v && typeof v.url === 'string' && v.url.startsWith('http'));
    const firstUrl = (validVers[0] && validVers[0].url) || (item.extra_links && item.extra_links[0]) || '';
    const host = getHostname(firstUrl) || 'Download';
    const n = validVers.length + (item.extra_links ? item.extra_links.length : 0);
    const cleanName = cleanDisplayName(item.title) || item.title;
    return `
      <div class="report-item-row" onclick="scrollToCard('${escapeQuotes(item.slug)}')" title="${escapeHtml(item.title)}">
        <span class="report-item-name">${escapeHtml(cleanName)}</span>
        <span class="report-item-badge badge-success">${n} link (${host})</span>
      </div>
    `;
  }).join('');

  // Render list of locked
  listLocked.innerHTML = locked.map(item => {
    const cleanName = cleanDisplayName(item.title) || item.title;
    return `
      <div class="report-item-row" onclick="scrollToCard('${escapeQuotes(item.slug)}')" title="${escapeHtml(item.title)}">
        <span class="report-item-name">${escapeHtml(cleanName)}</span>
        <span class="report-item-badge badge-locked">🔒 Cần đăng nhập</span>
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
    if (label) label.textContent = isOpen ? 'Thu gọn bài viết' : 'Xem chi tiết bài viết & Tính năng';
  }
};

// 7. Render Addon Cards
function renderCards() {
  updateReportBanner();
  const query = (catalogSearchInput.value || '').toLowerCase().trim();

  // Filter by active Simulator
  const simAddons = allAddons.filter(item => item.sim === currentSim);

  // Filter by Search and Category
  const filtered = simAddons.filter(item => {
    const title = (item.title || '').toLowerCase();
    const slug = (item.slug || '').toLowerCase();
    const matchQuery = !query || title.includes(query) || slug.includes(query);

    const matchLinks = hasValidLinks(item);

    let matchCat = true;
    if (currentCatFilter === 'has_links') {
      matchCat = matchLinks;
    } else if (currentCatFilter === 'PMDG') {
      matchCat = title.includes('pmdg') || slug.includes('pmdg');
    } else if (currentCatFilter === 'Airbus') {
      matchCat = title.includes('a3') || title.includes('fenix') || title.includes('toliss') || title.includes('airbus') || slug.includes('fenix') || slug.includes('toliss') || slug.includes('a3');
    } else if (currentCatFilter === 'BlackSquare') {
      matchCat = title.includes('black square') || slug.includes('bksq');
    } else if (currentCatFilter === 'GA') {
      matchCat = title.includes('comanche') || title.includes('bonanza') || title.includes('baron') || title.includes('learjet') || title.includes('da42') || title.includes('da40') || title.includes('aw139');
    } else if (currentCatFilter === 'Military') {
      matchCat = title.includes('jaguar') || title.includes('c-130') || title.includes('sr-71') || title.includes('vulcan') || title.includes('hawk');
    } else if (currentCatFilter === 'Utility') {
      matchCat = title.includes('gsx') || title.includes('chaseplane') || title.includes('flow') || title.includes('sound') || title.includes('airac') || title.includes('seasons') || title.includes('earth fx') || title.includes('scenery');
    }

    return matchQuery && matchCat;
  });

  resultsCount.textContent = `${filtered.length} / ${simAddons.length}`;
  cardsGrid.innerHTML = '';

  if (filtered.length === 0) {
    cardsGrid.innerHTML = `
      <div class="card" style="text-align: center; padding: 48px 24px; color: var(--text-muted);">
        <p style="font-size: 1.15rem; font-weight: 600; color: #fff; margin-bottom: 6px;">Không tìm thấy addon phù hợp</p>
        <p style="font-size: 0.88rem; color: var(--text-sub);">Hãy thử tìm từ khoá khác hoặc chọn lại danh mục "Tất cả".</p>
      </div>
    `;
    return;
  }

  filtered.forEach(item => {
    const card = createAddonCard(item);
    cardsGrid.appendChild(card);
  });
}

// Card Factory
function createAddonCard(d) {
  const card = document.createElement('div');
  card.className = 'addon-card';
  card.id = 'addon-card-' + (d.slug || '');

  const validVersions = (d.versions || []).filter(v => v && typeof v.url === 'string' && v.url.trim().startsWith('http'));
  const hasLinks = validVersions.length > 0 || (d.extra_links && d.extra_links.length > 0);

  // 1. Cover Image Banner
  let coverHtml = '';
  if (d.image) {
    coverHtml = `
      <div class="addon-cover-wrapper">
        <img src="${escapeHtml(d.image)}" class="addon-cover-img" alt="${escapeHtml(d.title)}" loading="lazy" onerror="this.closest('.addon-cover-wrapper').style.display='none';">
        <div class="addon-cover-overlay"></div>
      </div>
    `;
  }

  // 2. Article & Features Section
  let articleHtml = '';
  const hasDesc = Array.isArray(d.description) && d.description.length > 0;
  const hasFeatures = Array.isArray(d.features) && d.features.length > 0;
  const hasChangelog = Array.isArray(d.changelog) && d.changelog.length > 0;

  if (hasDesc || hasFeatures || hasChangelog) {
    const excerpt = hasDesc ? escapeHtml(d.description[0]) : '';
    const otherParas = hasDesc ? d.description.slice(1).map(p => `<p class="addon-paragraph">${escapeHtml(p)}</p>`).join('') : '';

    let featuresBlock = '';
    if (hasFeatures) {
      const items = d.features.map(f => `
        <div class="feature-item">
          <span class="feature-check">✓</span>
          <span>${escapeHtml(f)}</span>
        </div>
      `).join('');
      featuresBlock = `
        <div class="addon-features-box">
          <div class="features-title">✨ Tính năng nổi bật & Mô phỏng</div>
          <div class="features-grid">${items}</div>
        </div>
      `;
    }

    let changelogBlock = '';
    if (hasChangelog) {
      const logs = d.changelog.map(c => `<div>${escapeHtml(c)}</div>`).join('');
      changelogBlock = `
        <div class="addon-changelog-box">
          <div class="changelog-title">🔄 Lịch sử cập nhật</div>
          <div>${logs}</div>
        </div>
      `;
    }

    articleHtml = `
      <div class="addon-article-box">
        ${excerpt ? `<div class="addon-excerpt">${excerpt}</div>` : ''}
        <button class="btn-toggle-article" id="btn-toggle-${escapeQuotes(d.slug)}" onclick="toggleArticle('${escapeQuotes(d.slug)}')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
          <span id="label-toggle-${escapeQuotes(d.slug)}">Xem chi tiết bài viết & Tính năng</span>
          <svg class="article-arrow" id="arrow-toggle-${escapeQuotes(d.slug)}" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </button>
        <div class="article-full-content" id="article-full-${escapeQuotes(d.slug)}">
          ${otherParas}
          ${featuresBlock}
          ${changelogBlock}
        </div>
      </div>
    `;
  }

  // 3. Versions list
  let versionsHtml = '';
  if (validVersions.length > 0) {
    versionsHtml = validVersions.map(v => {
      const ver = escapeHtml(v.versionNumber || 'Tải về');
      const link = escapeHtml(v.url.trim());
      const host = getHostname(v.url);
      return `
        <div class="version-item">
          <div class="version-info">
            <span class="version-badge">${ver}</span>
            <span class="version-host">${host}</span>
          </div>
          <div class="version-buttons">
            <button class="btn-action btn-copy" onclick="copyText('${escapeQuotes(v.url)}')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              Copy Link
            </button>
            <a href="${link}" target="_blank" rel="noopener noreferrer" class="btn-action btn-open">
              Mở link
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            </a>
          </div>
        </div>
      `;
    }).join('');
  } else {
    versionsHtml = `
      <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); padding: 12px 16px; border-radius: var(--radius-sm); font-size: 0.85rem; color: #fca5a5;">
        🔒 Link bài viết này được bảo vệ sau lớp đăng nhập Clerk trên trang gốc Skybound tại thời điểm lưu trữ.
      </div>
    `;
  }

  // 4. Extra links
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
        <div class="extra-title">Tài nguyên & Link liên quan</div>
        <div class="extra-links-list">${pills}</div>
      </div>
    `;
  }

  const statusBadge = hasLinks
    ? `<span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3);">✅ ${validVersions.length} link download</span>`
    : `<span class="badge" style="background: rgba(255, 255, 255, 0.05); color: #94a3b8;">🔒 Yêu cầu đăng nhập</span>`;

  const simBadgeText = SIM_NAMES[d.sim] || 'MSFS 2024';

  card.innerHTML = `
    ${coverHtml}
    <div class="addon-card-header">
      <div>
        <div class="addon-title">${escapeHtml(d.title)}</div>
        <div class="addon-meta">
          <span class="badge badge-sim">${escapeHtml(simBadgeText)}</span>
          ${statusBadge}
          <span style="font-size: 0.75rem; color: #64748b; font-family: monospace;">${escapeHtml(d.slug || '')}</span>
        </div>
      </div>
      <div class="password-box">
        <span class="password-label">Pass:</span>
        <span class="password-value">${escapeHtml(d.password || 'https://skybound.cx')}</span>
        <button class="btn-icon-copy" title="Sao chép mật khẩu" onclick="copyText('${escapeQuotes(d.password || 'https://skybound.cx')}')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        </button>
      </div>
    </div>
    <div class="addon-card-body">
      ${articleHtml}
      <div class="versions-title">Danh sách Link Download</div>
      <div class="versions-list">${versionsHtml}</div>
      ${extraHtml}
    </div>
  `;

  return card;
}

// 8. Copy All Links for active view
btnCopyAllRaw.addEventListener('click', () => {
  const query = (catalogSearchInput.value || '').toLowerCase().trim();
  const simAddons = allAddons.filter(item => item.sim === currentSim);
  const filtered = simAddons.filter(item => {
    const title = (item.title || '').toLowerCase();
    const slug = (item.slug || '').toLowerCase();
    const matchQuery = !query || title.includes(query) || slug.includes(query);
    const hasLinks = item.versions && item.versions.length > 0;
    let matchCat = true;
    if (currentCatFilter === 'has_links') matchCat = hasLinks;
    return matchQuery && matchCat;
  });

  const allUrls = [];
  filtered.forEach(r => {
    if (r.versions) {
      r.versions.forEach(v => { if (v.url) allUrls.push(v.url); });
    }
    if (r.extra_links) {
      r.extra_links.forEach(l => allUrls.push(l));
    }
  });

  if (allUrls.length === 0) {
    showToast("Không có link nào để sao chép trong danh sách hiện tại!", true);
    return;
  }

  copyText(allUrls.join('\n'));
  showToast(`Đã sao chép ${allUrls.length} link download của ${filtered.length} addon vào bộ nhớ tạm!`);
});

// Helpers
function setLoading(isLoading, text = "") {
  if (isLoading) {
    loadingIndicator.classList.remove('hidden');
    loadingText.textContent = text;
  } else {
    loadingIndicator.classList.add('hidden');
  }
}

window.copyText = function(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast("Đã sao chép vào bộ nhớ tạm!");
  }).catch(() => {
    const t = document.createElement('textarea');
    t.value = text;
    document.body.appendChild(t);
    t.select();
    document.execCommand('copy');
    document.body.removeChild(t);
    showToast("Đã sao chép vào bộ nhớ tạm!");
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

// Start
initApp();
