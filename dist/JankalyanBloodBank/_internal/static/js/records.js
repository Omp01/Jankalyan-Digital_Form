/**
 * Jankalyan Blood Bank System - Record Search & Management Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('recordsTable')) {
    loadRecords();
  }
});

async function loadRecords() {
  const search = document.getElementById('searchQuery')?.value || '';
  const status = document.getElementById('filterStatus')?.value || '';
  const bloodGroup = document.getElementById('filterBloodGroup')?.value || '';
  const fromDate = document.getElementById('filterFromDate')?.value || '';
  const toDate = document.getElementById('filterToDate')?.value || '';

  const queryParams = new URLSearchParams({ search, status, blood_group: bloodGroup, from_date: fromDate, to_date: toDate });

  try {
    const res = await fetch(`/api/records?${queryParams.toString()}`);
    const data = await res.json();
    if (!data.success) return;

    renderRecordsTable(data.records);
  } catch (err) {
    console.error('Error fetching records:', err);
  }
}

function renderRecordsTable(records) {
  const tbody = document.getElementById('recordsTableBody');
  if (!tbody) return;

  if (records.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="text-center">No blood donation records found matching criteria.</td></tr>`;
    return;
  }

  tbody.innerHTML = records.map(r => {
    const statusClass = `badge-${(r.status || 'draft').toLowerCase()}`;
    return `
      <tr>
        <td><strong>${r.record_number}</strong></td>
        <td>${formatDate(r.donation_date)}</td>
        <td>${r.full_name || 'N/A'}<br><small class="text-muted">${r.mobile_number || ''}</small></td>
        <td><span class="blood-type-pill">${r.blood_group_known || 'N/A'}</span></td>
        <td>${r.blood_bag_number || 'Pending'}</td>
        <td><span class="badge ${statusClass}">${r.status}</span></td>
        <td class="action-buttons">
          <a href="/print/${r.id}" target="_blank" class="btn-sm btn-print">🖨️ <span data-i18n="btn_print">Print</span></a>
          <a href="/donor_form.html?id=${r.id}" class="btn-sm btn-view">👁️ <span data-i18n="btn_view">View / Edit</span></a>
          ${(currentUser && (currentUser.role === 'ADMIN' || currentUser.role === 'MEDICAL_OFFICER') && (r.status === 'SIGNED' || r.status === 'COMPLETED')) ? `
            <button class="btn-sm btn-unlock" onclick="promptUnlockRecord(${r.id}, '${r.record_number}')">✏️ <span data-i18n="btn_modify">Modify Record</span></button>
          ` : ''}
        </td>
      </tr>
    `;
  }).join('');

  applyTranslations();
}

function exportToExcel() {
  const search = document.getElementById('searchQuery')?.value || '';
  const status = document.getElementById('filterStatus')?.value || '';
  const bloodGroup = document.getElementById('filterBloodGroup')?.value || '';
  const fromDate = document.getElementById('filterFromDate')?.value || '';
  const toDate = document.getElementById('filterToDate')?.value || '';

  const queryParams = new URLSearchParams({ search, status, blood_group: bloodGroup, from_date: fromDate, to_date: toDate });
  window.location.href = `/api/export/excel?${queryParams.toString()}`;
}

async function promptUnlockRecord(recordId, recordNum) {
  const reason = prompt(`Authorized Unlock for Record ${recordNum}:\n\nPlease enter the clinical/administrative reason for unlocking this finalised record:`);
  if (!reason || !reason.trim()) return;

  try {
    const res = await fetch(`/api/records/${recordId}/unlock`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: reason.trim() })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      loadRecords();
    } else {
      showToast(data.message, 'error');
    }
  } catch (err) {
    console.error(err);
  }
}
