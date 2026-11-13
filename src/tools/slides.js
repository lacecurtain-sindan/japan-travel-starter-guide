/* Japan Travel Starter Guide - TikTok carousel renderer.
   Draws 1080x1440 (3:4) slides on <canvas> with system fonts only (no network),
   so it can run inside TikTok Studio and hand the PNGs straight to the photo uploader.

   window.JTSG.render(post) -> Promise<File[]>
   window.JTSG.attach(files) -> puts files into the photo uploader input
   post = { id, slides: [
     {type:'cover', kicker, title, sub},
     {type:'tip', n, total, title, body:[...], note},
     {type:'cta', title, sub, code}
   ]}
   In body/note text, wrap words in [[double brackets]] to set them in red bold.
*/
(function () {
  const W = 1080, H = 1440;
  const RED = '#d32f2f', INK = '#0f0f0f', TEXT = '#2b2b2b', MUTED = '#6b6b6b';
  const HEAD = "'Segoe UI Black', 'Arial Black', 'Helvetica Neue', Arial, sans-serif";
  const BODY = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif";
  const SAFE_L = 88, SAFE_R = 930; // keep clear of TikTok's right-side buttons
  const SAFE_BOTTOM = 1180;        // keep clear of caption overlay

  function canvas() {
    const c = document.createElement('canvas');
    c.width = W; c.height = H;
    return [c, c.getContext('2d')];
  }

  // Split "a [[b c]] d" into runs: [{t:'a ',hi:false},{t:'b c',hi:true},{t:' d',hi:false}]
  function runs(s) {
    const out = []; const re = /\[\[(.+?)\]\]/g; let i = 0, m;
    while ((m = re.exec(s))) { if (m.index > i) out.push({ t: s.slice(i, m.index), hi: false }); out.push({ t: m[1], hi: true }); i = re.lastIndex; }
    if (i < s.length) out.push({ t: s.slice(i), hi: false });
    return out;
  }

  // Word-wrap rich text; returns lines of [{t,hi}] runs.
  function wrapRich(x, s, maxW, font, hiFont) {
    const words = [];
    runs(s).forEach(r => r.t.split(/(\s+)/).forEach(w => { if (w) words.push({ t: w, hi: r.hi }); }));
    const lines = []; let line = [], width = 0;
    for (const w of words) {
      x.font = w.hi ? hiFont : font;
      const ww = x.measureText(w.t).width;
      if (width + ww > maxW && line.length && !/^\s+$/.test(w.t)) { lines.push(line); line = []; width = 0; if (/^\s+$/.test(w.t)) continue; }
      if (!line.length && /^\s+$/.test(w.t)) continue;
      line.push(w); width += ww;
    }
    if (line.length) lines.push(line);
    return lines;
  }

  function drawRich(x, s, left, top, maxW, size, lh, color, weight) {
    const font = `${weight || 400} ${size}px ${BODY}`;
    const hiFont = `700 ${size}px ${BODY}`;
    const lines = wrapRich(x, s, maxW, font, hiFont);
    let y = top;
    for (const line of lines) {
      let cx = left;
      for (const w of line) {
        x.font = w.hi ? hiFont : font;
        x.fillStyle = w.hi ? RED : color;
        x.fillText(w.t, cx, y);
        cx += x.measureText(w.t).width;
      }
      y += lh;
    }
    return y;
  }

  function drawHead(x, s, left, top, maxW, size, color) {
    x.font = `900 ${size}px ${HEAD}`;
    x.fillStyle = color || INK;
    const words = s.split(' '); let line = '', y = top;
    for (const w of words) {
      const t = line ? line + ' ' + w : w;
      if (x.measureText(t).width > maxW && line) { x.fillText(line, left, y); line = w; y += size * 1.08; }
      else line = t;
    }
    if (line) { x.fillText(line, left, y); y += size * 1.08; }
    return y;
  }

  function brand(x, dark) {
    x.fillStyle = dark ? '#ffffff' : RED; x.beginPath(); x.arc(SAFE_L + 12, 92, 12, 0, Math.PI * 2); x.fill();
    x.font = `600 30px ${BODY}`; x.fillStyle = dark ? 'rgba(255,255,255,.9)' : MUTED;
    x.fillText('Japan Travel Starter Guide', SAFE_L + 38, 102);
  }

  function fuji(x, baseY, alpha) {
    x.save(); x.globalAlpha = alpha == null ? 1 : alpha;
    const g = x.createLinearGradient(0, baseY - 420, 0, H);
    g.addColorStop(0, '#5a4b72'); g.addColorStop(1, '#2a2340');
    x.fillStyle = g; x.beginPath();
    x.moveTo(-60, H); x.lineTo(360, baseY - 330); x.lineTo(470, baseY - 405); x.lineTo(540, baseY - 425);
    x.lineTo(610, baseY - 405); x.lineTo(720, baseY - 330); x.lineTo(1140, H); x.closePath(); x.fill();
    x.fillStyle = '#ffffff'; x.beginPath();
    x.moveTo(360, baseY - 330); x.lineTo(470, baseY - 405); x.lineTo(540, baseY - 425); x.lineTo(610, baseY - 405); x.lineTo(720, baseY - 330);
    x.lineTo(670, baseY - 300); x.lineTo(630, baseY - 325); x.lineTo(590, baseY - 290); x.lineTo(540, baseY - 320);
    x.lineTo(495, baseY - 285); x.lineTo(450, baseY - 322); x.lineTo(410, baseY - 296); x.closePath(); x.fill();
    x.restore();
  }

  function cover(s) {
    const [c, x] = canvas();
    const sky = x.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, '#f6eef3'); sky.addColorStop(.55, '#e3d6e8'); sky.addColorStop(1, '#c9b8d8');
    x.fillStyle = sky; x.fillRect(0, 0, W, H);
    x.fillStyle = RED; x.beginPath(); x.arc(830, 930, 105, 0, Math.PI * 2); x.fill();
    fuji(x, 1440);
    brand(x);
    let y = 250;
    if (s.kicker) { x.font = `700 44px ${BODY}`; x.fillStyle = RED; x.fillText(s.kicker, SAFE_L, y); y += 92; }
    y = drawHead(x, s.title, SAFE_L, y, SAFE_R - SAFE_L, s.size || 118);
    if (s.sub) drawRich(x, s.sub, SAFE_L, y + 30, SAFE_R - SAFE_L - 60, 52, 70, TEXT, 600);
    return c;
  }

  function tip(s) {
    const [c, x] = canvas();
    x.fillStyle = '#ffffff'; x.fillRect(0, 0, W, H);
    fuji(x, 1440, .07);
    brand(x);
    // number badge (the slides are a sequence of steps/tips)
    x.fillStyle = RED; x.beginPath(); x.arc(SAFE_L + 60, 250, 60, 0, Math.PI * 2); x.fill();
    x.fillStyle = '#fff'; x.font = `900 64px ${HEAD}`; x.textAlign = 'center'; x.fillText(String(s.n), SAFE_L + 60, 273); x.textAlign = 'left';
    if (s.total) { x.font = `600 32px ${BODY}`; x.fillStyle = MUTED; x.fillText(`of ${s.total}`, SAFE_L + 140, 262); }
    let y = drawHead(x, s.title, SAFE_L, 440, SAFE_R - SAFE_L, s.size || 88);
    y += 26;
    for (const p of s.body || []) { y = drawRich(x, p, SAFE_L, y + 18, SAFE_R - SAFE_L, 54, 76, TEXT); y += 22; }
    if (s.note) {
      const top = Math.min(y + 40, SAFE_BOTTOM - 200);
      x.fillStyle = '#f5f5f5'; x.fillRect(SAFE_L, top, SAFE_R - SAFE_L, 190);
      x.fillStyle = RED; x.fillRect(SAFE_L, top, 12, 190);
      drawRich(x, s.note, SAFE_L + 44, top + 78, SAFE_R - SAFE_L - 80, 44, 60, INK, 600);
    }
    return c;
  }

  function cta(s) {
    const [c, x] = canvas();
    x.fillStyle = RED; x.fillRect(0, 0, W, H);
    fuji(x, 1440, .18);
    brand(x, true);
    let y = drawHead(x, s.title, SAFE_L, 360, SAFE_R - SAFE_L, s.size || 96, '#ffffff');
    if (s.sub) {
      x.font = `500 46px ${BODY}`; x.fillStyle = 'rgba(255,255,255,.95)';
      y = drawRich(x, s.sub, SAFE_L, y + 30, SAFE_R - SAFE_L, 46, 64, '#ffffff', 500);
    }
    if (s.code) {
      const top = y + 40;
      x.fillStyle = '#ffffff'; x.fillRect(SAFE_L, top, SAFE_R - SAFE_L, 150);
      x.fillStyle = MUTED; x.font = `600 32px ${BODY}`; x.fillText(s.codeLabel || 'Discount code', SAFE_L + 36, top + 52);
      x.fillStyle = RED; x.font = `900 64px ${HEAD}`; x.fillText(s.code, SAFE_L + 36, top + 122);
      y = top + 150;
    }
    // pill
    const py = Math.min(y + 70, SAFE_BOTTOM - 110);
    x.fillStyle = '#ffffff'; const pw = 420, ph = 100, pr = 50;
    x.beginPath(); x.moveTo(SAFE_L + pr, py); x.arcTo(SAFE_L + pw, py, SAFE_L + pw, py + ph, pr); x.arcTo(SAFE_L + pw, py + ph, SAFE_L, py + ph, pr); x.arcTo(SAFE_L, py + ph, SAFE_L, py, pr); x.arcTo(SAFE_L, py, SAFE_L + pw, py, pr); x.fill();
    x.fillStyle = RED; x.font = `800 44px ${BODY}`; x.textAlign = 'center'; x.fillText(s.pill || 'Link in bio', SAFE_L + pw / 2, py + 66); x.textAlign = 'left';
    return c;
  }

  const DRAW = { cover, tip, cta };

  async function render(post) {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    const files = [];
    for (let i = 0; i < post.slides.length; i++) {
      const s = post.slides[i];
      const c = DRAW[s.type](s);
      const blob = await new Promise(r => c.toBlob(r, 'image/png'));
      files.push(new File([blob], `${post.id || 'post'}-${String(i + 1).padStart(2, '0')}.png`, { type: 'image/png' }));
    }
    return files;
  }

  function attach(files) {
    const input = document.querySelector('input[type=file][accept*=image]');
    if (!input) throw new Error('Photo uploader input not found: switch TikTok Studio to the Photos tab first');
    const dt = new DataTransfer(); files.forEach(f => dt.items.add(f));
    input.files = dt.files;
    input.dispatchEvent(new Event('change', { bubbles: true }));
    return files.length;
  }

  // Preview helper: show rendered slides on the current page.
  async function preview(post) {
    const files = await render(post);
    const box = document.createElement('div');
    box.style.cssText = 'position:fixed;inset:0;z-index:99999;background:#222;overflow:auto;display:flex;flex-wrap:wrap;gap:8px;padding:8px';
    files.forEach(f => { const im = new Image(); im.src = URL.createObjectURL(f); im.style.cssText = 'width:270px;height:360px'; box.appendChild(im); });
    document.body.appendChild(box);
    return files.length;
  }

  window.JTSG = { render, attach, preview };
})();
