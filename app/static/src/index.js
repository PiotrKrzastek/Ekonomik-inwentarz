import htmx from 'htmx.org';
import { v4 as uuidv4 } from 'uuid';
import tagify from '@yaireo/tagify/dist/tagify.min.js';

import '../js/global_listeners.js';

/** @type {import('htmx.org')} */
window.htmx = htmx;

/** @type {import('uuid').v4} */
window.uuid = uuidv4;

/** @type {any} */
window.tagify = tagify;

function showTemporaryAlert(tag, message, duration = 5000, container = 'alerts') {
  const uuid = uuidv4();
  const alertsContainer = document.getElementById(container);
  if (!alertsContainer) return;

  const alertEl = document.createElement('div');
  alertEl.className = `alert alert-${tag} alert-soft flex flex-col gap-2 p-2 mb-4 w-[100%]`;
  alertEl.id = `alert_${uuid}`;
  alertEl.innerHTML = `
        <div class="flex items-center gap-2 w-full">
            <div class="p-2"><span class="text-base">${message}</span></div>
        </div>
    <progress class="progress progress-${tag} w-full h-[2px]" value="100" max="100"></progress>
  `;

  alertsContainer.appendChild(alertEl);
  const alertElement = document.getElementById(`alert_${uuid}`);
  const progress = alertElement.querySelector("progress");
  let start = Date.now();
  let remaining = duration;
  let timer = null;
  let paused = false;

  const animate = () => {
    if (paused) return;
    const elapsed = Date.now() - start;
    const percent = Math.max(100 - (elapsed / duration) * 100, 0);
    progress.value = percent;
    if (percent > 0) requestAnimationFrame(animate);
  };

  const removeAlert = () => {
    alertElement.remove();
  };

  const startTimer = () => {
    start = Date.now();
    paused = false;
    requestAnimationFrame(animate);
    timer = setTimeout(removeAlert, remaining);
  };

  const pauseTimer = () => {
    paused = true;
    clearTimeout(timer);
    remaining -= Date.now() - start;
    progress.value = 100;
  };

  alertElement.addEventListener("mouseenter", pauseTimer);
  alertElement.addEventListener("mouseleave", () => {
    remaining = duration; // reset czasu i animacji
    // progress.value = 100;
    startTimer();
  });

  startTimer();
}

window.showTemporaryAlert = showTemporaryAlert;
