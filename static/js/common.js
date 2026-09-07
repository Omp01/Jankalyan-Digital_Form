/**
 * Jankalyan Blood Bank System - Common Shared UI Logic
 */

let currentUser = null;

async function checkAuth() {
  try {
    const res = await fetch('/api/auth/me');
    const data = await res.json();
    if (!data.logged_in) {
      if (!window.location.pathname.endsWith('login.html')) {
        window.location.href = '/login.html';
      }
      return null;
    }
    currentUser = data.user;
    renderUserHeader();
    renderFooter();
    return currentUser;
  } catch (err) {
    console.error('Auth check error:', err);
    return null;
  }
}

function renderUserHeader() {
  const headerContainer = document.getElementById('appHeader');
  if (!headerContainer || !currentUser) return;

  headerContainer.innerHTML = `
    <div class="header-banner">
      <div class="header-brand">
        <div class="hospital-logo">🩸</div>
        <div>
          <h1 class="header-title" data-i18n="system_title">Jankalyan Blood Centre</h1>
          <p class="header-subtitle" data-i18n="system_subtitle">Blood Bank Digital Form System (QF/JKRP/18)</p>
        </div>
      </div>
      <div class="header-actions">
        <div class="lang-switch-box">
          <button id="btnLangEn" class="lang-btn ${currentLang === 'en' ? 'active' : ''}" onclick="setLanguage('en')">English</button>
          <button id="btnLangMr" class="lang-btn ${currentLang === 'mr' ? 'active' : ''}" onclick="setLanguage('mr')">मराठी</button>
        </div>
        <div class="user-pill">
          <span class="user-name">👤 ${currentUser.full_name} (${currentUser.role})</span>
          <button class="btn-logout" onclick="logout()"><span data-i18n="nav_logout">Logout</span> 🚪</button>
        </div>
      </div>
    </div>
    <nav class="nav-bar">
      <a href="/dashboard.html" class="nav-link ${window.location.pathname.includes('dashboard') ? 'active' : ''}">📊 <span data-i18n="nav_dashboard">Dashboard</span></a>
      <a href="/donor_form.html" class="nav-link ${window.location.pathname.includes('donor_form') ? 'active' : ''}">📝 <span data-i18n="nav_new_form">New Donor Form</span></a>
      <a href="/records.html" class="nav-link ${window.location.pathname.includes('records') ? 'active' : ''}">🔍 <span data-i18n="nav_records">Search Records</span></a>
      ${currentUser.role === 'ADMIN' ? `
        <a href="/users.html" class="nav-link ${window.location.pathname.includes('users') ? 'active' : ''}">👥 <span data-i18n="nav_users">Manage Users</span></a>
        <a href="/audit.html" class="nav-link ${window.location.pathname.includes('audit') ? 'active' : ''}">📋 <span data-i18n="nav_audit">Audit Logs</span></a>
      ` : ''}
      <a href="/profile.html" class="nav-link ${window.location.pathname.includes('profile') ? 'active' : ''}" style="margin-left: auto;">👤 Profile & Signature</a>
    </nav>
  `;
  applyTranslations();
}

function renderFooter() {
  let footerElem = document.getElementById('appFooter');
  if (!footerElem) {
    const container = document.querySelector('.app-container');
    if (container) {
      footerElem = document.createElement('footer');
      footerElem.id = 'appFooter';
      footerElem.className = 'app-footer';
      container.appendChild(footerElem);
    }
  }
  if (footerElem) {
    const currentYear = new Date().getFullYear();
    footerElem.innerHTML = `
      <div>Copyright ©${currentYear} <span class="highlight-text">Jankalyan Blood centre</span> All rights reserved.</div>
      <div style="margin-top: 4px;">Powered by <span class="highlight-text">Harbinger Group</span></div>
    `;
  }
}

async function logout() {
  try {
    await fetch('/api/auth/logout', { method: 'POST' });
    window.location.href = '/login.html';
  } catch (err) {
    console.error('Logout error:', err);
  }
}

function showToast(message, type = 'info') {
  let toastContainer = document.getElementById('toastContainer');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toastContainer';
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('show');
  }, 10);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

document.addEventListener('DOMContentLoaded', () => {
  if (!window.location.pathname.endsWith('login.html')) {
    checkAuth();
  } else {
    renderFooter();
  }
});
