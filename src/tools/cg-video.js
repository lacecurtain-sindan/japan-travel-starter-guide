/* Japan Travel Starter Guide - CG video engine.
   Renders a 1080x1920 vertical video entirely in the browser:
   a 3D cloud of glowing particles that morphs between shapes (plane, train, coin, Fuji, phone...),
   glass panels and glowing type on top, encoded with WebCodecs (VP8) into a WebM file.
   No network access needed, so it can run inside TikTok Studio.

   const blob = await JCG.render(spec, { onProgress: p => ... });
   JCG.attachVideo(blob, 'name.webm')  // hand the file to TikTok Studio's video uploader
   JCG.drawFrame(ctx, spec, t)          // draw a single frame (for previews)

   spec = { fps: 30, scenes: [ { dur, shape, color?, kind: 'title'|'option'|'pick'|'cta', ...text } ] }
*/
(function () {
  const W = 1080, H = 1920;
  const N = 4200;
  const FONT = "'Segoe UI', 'Inter', 'Helvetica Neue', Arial, sans-serif";
  const CX = 540, CY = 720, SCALE = 380;

  // ---------- deterministic random ----------
  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  const gauss = () => { let u = 0, v = 0; while (!u) u = rnd(); while (!v) v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  const ease = x => { x = Math.max(0, Math.min(1, x)); return 1 - Math.pow(1 - x, 3); };
  const easeIO = x => { x = Math.max(0, Math.min(1, x)); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };

  // ---------- shapes: return {p: Float32Array(N*3), c: Uint8Array(N*3)} in roughly [-1,1] ----------
  function make(fn) {
    const p = new Float32Array(N * 3), c = new Uint8Array(N * 3);
    for (let i = 0; i < N; i++) { const r = fn(i); p[i * 3] = r[0]; p[i * 3 + 1] = r[1]; p[i * 3 + 2] = r[2]; c[i * 3] = r[3]; c[i * 3 + 1] = r[4]; c[i * 3 + 2] = r[5]; }
    return { p, c };
  }
  const jitter = s => gauss() * s;

  const SHAPES = {
    plane: () => make(i => {
      const k = rnd();
      if (k < .45) { // fuselage
        const u = rnd() * 2 - 1, a = rnd() * Math.PI * 2, r = .16 * Math.sqrt(Math.max(0, 1 - Math.pow(u, 8))) * (u > .7 ? (1 - (u - .7) * 2.2) : 1);
        return [u * 1.15, Math.sin(a) * r, Math.cos(a) * r, 235, 240, 255];
      } else if (k < .85) { // wings
        const s = rnd() < .5 ? -1 : 1, a = rnd(), b = rnd();
        const x = .15 - a * .45 + b * .25, z = s * (.15 + a * 1.05);
        return [x + jitter(.01), jitter(.012), z, 120, 210, 255];
      } else { // tail fin + stabilizers
        const a = rnd(), b = rnd();
        if (rnd() < .5) return [-1.0 + b * .25, a * .42, jitter(.01), 255, 140, 190];
        const s = rnd() < .5 ? -1 : 1; return [-1.0 + b * .22, .02, s * a * .35, 120, 210, 255];
      }
    }),
    train: (stripe) => make(i => { // Skyliner-like nose: long capsule with tapered front
      const u = rnd(), a = rnd() * Math.PI * 2;
      const x = u * 2.2 - 1.1;
      let r = .26; if (x > .45) r *= Math.max(.05, 1 - Math.pow((x - .45) / .65, 1.6));
      const y = Math.sin(a) * r * .9, z = Math.cos(a) * r;
      const isStripe = Math.abs(y + .02) < .035;
      const isWindow = y > .08 && y < .15 && ((x * 9) % 1 + 1) % 1 < .6 && x < .45;
      const col = isStripe ? stripe : isWindow ? [110, 200, 255] : [235, 238, 250];
      return [x, y, z, col[0], col[1], col[2]];
    }),
    coin: () => make(i => {
      const k = rnd(), a = rnd() * Math.PI * 2;
      if (k < .55) { const r = .95 * Math.sqrt(rnd()); return [Math.cos(a) * r, Math.sin(a) * r, (rnd() < .5 ? -1 : 1) * .07, 255, 200, 90]; }
      if (k < .8) return [Math.cos(a) * .95, Math.sin(a) * .95, rnd() * .14 - .07, 255, 170, 60];
      // yen mark on both faces
      const t = rnd(), s = rnd() < .5 ? -1 : 1, z = s * .09;
      const seg = rnd();
      if (seg < .3) return [-(.45 - t * .45), .6 - t * .55, z, 255, 245, 210];
      if (seg < .6) return [.45 - t * .45, .6 - t * .55, z, 255, 245, 210];
      if (seg < .8) return [jitter(.012), .05 - t * .7, z, 255, 245, 210];
      return [(t - .5) * .7, (rnd() < .5 ? -.05 : -.25), z, 255, 245, 210];
    }),
    fuji: () => make(i => {
      const h = Math.pow(rnd(), .7), a = rnd() * Math.PI * 2;
      const y = -.72 + h * 1.6, r = (1 - h) * 1.05 + .08;
      const snow = y > .42 + Math.sin(a * 7) * .06;
      const col = snow ? [245, 245, 255] : [150 - h * 40, 120 + h * 30, 230];
      return [Math.cos(a) * r, y, Math.sin(a) * r, col[0], col[1], col[2]];
    }),
    phone: () => make(i => {
      const k = rnd();
      if (k < .62) { // screen + body slab
        const x = (rnd() - .5) * .8, y = (rnd() - .5) * 1.5 - .1, z = (rnd() < .5 ? -1 : 1) * .05;
        const edge = Math.abs(x) > .35 || Math.abs(y + .1) > .7;
        return [x, y, z, edge ? 200 : 90, edge ? 210 : 220, 255];
      }
      // signal arcs above
      const ring = 1 + Math.floor(rnd() * 3), a = (rnd() - .5) * 1.4;
      const r = .18 + ring * .16;
      return [Math.sin(a) * r, .62 + Math.cos(a) * r, jitter(.02), 120, 255, 220];
    }),
    torii: () => make(i => {
      const k = rnd();
      if (k < .4) { const s = rnd() < .5 ? -1 : 1, a = rnd() * Math.PI * 2; return [s * .62 + Math.cos(a) * .07, -1 + rnd() * 1.75, Math.sin(a) * .07, 255, 80, 60]; }
      if (k < .75) { const x = (rnd() - .5) * 2.1; return [x, .82 + x * x * .06 + jitter(.03), jitter(.06), 255, 90, 70]; }
      const x = (rnd() - .5) * 1.6; return [x, .5 + jitter(.025), jitter(.05), 255, 140, 90];
    }),
  };
  const shapeCache = {};
  function getShape(name, color) {
    const key = name + (color || '');
    if (!shapeCache[key]) {
      seed = 1000 + key.length * 31 + key.charCodeAt(0);
      if (name === 'train') shapeCache[key] = SHAPES.train(color === 'red' ? [255, 70, 70] : [70, 140, 255]);
      else shapeCache[key] = SHAPES[name]();
    }
    return shapeCache[key];
  }

  // per-particle delays and drift (fixed)
  seed = 99;
  const DELAY = new Float32Array(N), DRIFT = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) { DELAY[i] = rnd() * .35; DRIFT[i * 3] = gauss(); DRIFT[i * 3 + 1] = gauss(); DRIFT[i * 3 + 2] = gauss(); }

  // ---------- background (pre-rendered) ----------
  let BG = null, STARS = null, BOKEH = null;
  function initBG() {
    BG = document.createElement('canvas'); BG.width = W; BG.height = H;
    const g = BG.getContext('2d');
    const lg = g.createLinearGradient(0, 0, 0, H);
    lg.addColorStop(0, '#05051a'); lg.addColorStop(.45, '#140c3a'); lg.addColorStop(.8, '#2a1250'); lg.addColorStop(1, '#3a1846');
    g.fillStyle = lg; g.fillRect(0, 0, W, H);
    const rg = g.createRadialGradient(CX, CY, 50, CX, CY, 900);
    rg.addColorStop(0, 'rgba(90,70,200,.35)'); rg.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = rg; g.fillRect(0, 0, W, H);
    seed = 4242;
    STARS = Array.from({ length: 260 }, () => [rnd() * W, rnd() * H * .95, rnd() * 1.6 + .4, rnd() * 6.28]);
    BOKEH = Array.from({ length: 16 }, () => [rnd() * W, rnd() * H, 40 + rnd() * 110, rnd() * 6.28, rnd() < .5 ? '120,160,255' : '255,120,190']);
  }
  function drawBG(x, t) {
    x.drawImage(BG, 0, 0);
    for (const s of STARS) { x.fillStyle = `rgba(255,255,255,${.25 + .35 * (.5 + .5 * Math.sin(t * 1.7 + s[3]))})`; x.fillRect(s[0], s[1], s[2], s[2]); }
    for (const b of BOKEH) {
      const bx = b[0] + Math.sin(t * .15 + b[3]) * 40, by = (b[1] - t * 18 + H * 2) % (H + 200) - 100;
      const rg = x.createRadialGradient(bx, by, 0, bx, by, b[2]);
      rg.addColorStop(0, `rgba(${b[4]},.10)`); rg.addColorStop(1, `rgba(${b[4]},0)`);
      x.fillStyle = rg; x.beginPath(); x.arc(bx, by, b[2], 0, 6.283); x.fill();
    }
  }

  // ---------- particles ----------
  let GLOW = null;
  function sceneAt(spec, t) {
    let acc = 0;
    for (let i = 0; i < spec.scenes.length; i++) { const d = spec.scenes[i].dur; if (t < acc + d || i === spec.scenes.length - 1) return { i, lt: t - acc, start: acc }; acc += d; }
  }
  function drawParticles(x, spec, t) {
    const { i, lt } = sceneAt(spec, t);
    const cur = spec.scenes[i], prev = spec.scenes[Math.max(0, i - 1)];
    const A = getShape(prev.shape, prev.color), B = getShape(cur.shape, cur.color);
    const MORPH = 1.1;
    const prog = i === 0 ? 1 : Math.min(1, lt / MORPH);
    const yaw = Math.sin(t * .55) * .75 + (cur.yaw0 || 0), pitch = -.16 + Math.sin(t * .4) * .08;
    const cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
    const intro = ease(t / 1.4);
    if (!GLOW) { GLOW = document.createElement('canvas'); GLOW.width = W / 2; GLOW.height = H / 2; }
    const gx = GLOW.getContext('2d');
    gx.globalCompositeOperation = 'source-over'; gx.clearRect(0, 0, W / 2, H / 2);
    gx.globalCompositeOperation = 'lighter';
    x.save(); x.globalCompositeOperation = 'lighter';
    for (let k = 0; k < N; k++) {
      const e = easeIO((prog - DELAY[k]) / (1 - .35));
      const burst = Math.sin(Math.PI * e) * .55;
      let px = A.p[k * 3] + (B.p[k * 3] - A.p[k * 3]) * e + DRIFT[k * 3] * burst * .5;
      let py = A.p[k * 3 + 1] + (B.p[k * 3 + 1] - A.p[k * 3 + 1]) * e + DRIFT[k * 3 + 1] * burst * .5;
      let pz = A.p[k * 3 + 2] + (B.p[k * 3 + 2] - A.p[k * 3 + 2]) * e + DRIFT[k * 3 + 2] * burst * .5;
      // gentle breathing drift
      px += Math.sin(t * 1.3 + k) * .006; py += Math.cos(t * 1.1 + k * .7) * .006;
      // intro: particles gather from a wide cloud
      if (intro < 1) { const s = (1 - intro) * 2.2; px += DRIFT[k * 3] * s; py += DRIFT[k * 3 + 1] * s; pz += DRIFT[k * 3 + 2] * s; }
      const x1 = px * cy + pz * sy, z1 = -px * sy + pz * cy;
      const y2 = py * cp - z1 * sp, z2 = py * sp + z1 * cp;
      const f = 3.4 / (3.4 + z2);
      const sx = CX + x1 * SCALE * f, sy2 = CY - y2 * SCALE * f;
      const r = A.c[k * 3] + (B.c[k * 3] - A.c[k * 3]) * e, g = A.c[k * 3 + 1] + (B.c[k * 3 + 1] - A.c[k * 3 + 1]) * e, b = A.c[k * 3 + 2] + (B.c[k * 3 + 2] - A.c[k * 3 + 2]) * e;
      const depth = Math.max(.25, Math.min(1, (1.6 - z2) / 2));
      const size = 1.5 + 1.8 * f;
      x.fillStyle = `rgba(${r | 0},${g | 0},${b | 0},${(.55 * depth).toFixed(3)})`;
      x.fillRect(sx - size / 2, sy2 - size / 2, size, size);
      gx.fillStyle = `rgba(${r | 0},${g | 0},${b | 0},${(.5 * depth).toFixed(3)})`;
      gx.fillRect(sx / 2 - 1.5, sy2 / 2 - 1.5, 3, 3);
    }
    x.restore();
    // bloom
    x.save(); x.globalCompositeOperation = 'lighter'; x.filter = 'blur(14px)'; x.globalAlpha = .9; x.drawImage(GLOW, 0, 0, W, H); x.filter = 'blur(40px)'; x.globalAlpha = .6; x.drawImage(GLOW, 0, 0, W, H); x.restore();
  }

  // ---------- UI helpers ----------
  function rr(x, a, b, w, h, r) { x.beginPath(); x.moveTo(a + r, b); x.arcTo(a + w, b, a + w, b + h, r); x.arcTo(a + w, b + h, a, b + h, r); x.arcTo(a, b + h, a, b, r); x.arcTo(a, b, a + w, b, r); x.closePath(); }
  function glass(x, a, b, w, h, alpha, tint) {
    x.save(); x.globalAlpha = alpha;
    rr(x, a, b, w, h, 40); x.fillStyle = 'rgba(14,12,40,.55)'; x.fill();
    const lg = x.createLinearGradient(a, b, a, b + h); lg.addColorStop(0, `rgba(${tint || '255,255,255'},.16)`); lg.addColorStop(1, `rgba(${tint || '255,255,255'},.04)`);
    x.fillStyle = lg; x.fill();
    x.lineWidth = 2; x.strokeStyle = `rgba(${tint || '255,255,255'},.45)`; x.stroke();
    x.fillStyle = 'rgba(255,255,255,.35)'; x.fillRect(a + 40, b + 2, w - 80, 2);
    x.restore();
  }
  function text(x, s, px, py, size, weight, color, alpha, opts) {
    opts = opts || {};
    x.save(); x.globalAlpha = alpha; x.font = `${weight} ${size}px ${FONT}`; x.textAlign = opts.align || 'left'; x.textBaseline = 'alphabetic';
    if (opts.glow) { x.shadowColor = opts.glow; x.shadowBlur = opts.blur || 30; }
    x.fillStyle = color; x.fillText(s, px, py);
    if (opts.glow) { x.shadowBlur = 0; x.fillText(s, px, py); }
    x.restore();
  }
  function wrap(x, s, size, weight, maxW) {
    x.font = `${weight} ${size}px ${FONT}`;
    const out = []; let line = '';
    for (const w of s.split(' ')) { const t = line ? line + ' ' + w : w; if (x.measureText(t).width > maxW && line) { out.push(line); line = w; } else line = t; }
    if (line) out.push(line); return out;
  }
  function pill(x, s, px, py, color, alpha) {
    x.save(); x.globalAlpha = alpha; x.font = `800 34px ${FONT}`;
    const w = x.measureText(s).width + 48;
    rr(x, px, py - 44, w, 60, 30); x.fillStyle = color; x.shadowColor = color; x.shadowBlur = 30; x.fill(); x.shadowBlur = 0;
    x.fillStyle = '#0b0b22'; x.fillText(s, px + 24, py - 3); x.restore();
    return w;
  }
  const inA = (lt, s, d) => ease((lt - s + .25) / (d || .45));

  // ---------- scene layouts ----------
  const L = 96, R = 930; // keep clear of TikTok's right-side buttons
  function drawUI(x, spec, t) {
    const { i, lt } = sceneAt(spec, t);
    const s = spec.scenes[i];
    const out = Math.min(1, Math.max(0, (s.dur - lt) / .35));
    const last = i === spec.scenes.length - 1;
    const o = last ? Math.min(1, Math.max(0, (s.dur - lt) / .6)) : out;
    const up = (lt, st) => (1 - inA(lt, st)) * 40;

    if (s.kind === 'title') {
      if (s.kicker) text(x, s.kicker, CX, 1180 + up(lt, .3), 40, 700, '#7fe3ff', inA(lt, .3) * o, { align: 'center', glow: 'rgba(80,200,255,.8)' });
      const lines = wrap(x, s.title, 104, 900, 860);
      lines.forEach((ln, k) => text(x, ln, CX, 1310 + k * 116 + up(lt, .55 + k * .18), 104, 900, '#ffffff', inA(lt, .55 + k * .18) * o, { align: 'center', glow: 'rgba(170,120,255,.9)', blur: 40 }));
      if (s.sub) text(x, s.sub, CX, 1330 + lines.length * 116 + up(lt, 1.2), 44, 500, '#c9c3ef', inA(lt, 1.2) * o, { align: 'center' });
    }

    if (s.kind === 'option') {
      const top = 1060, h = 520 + (s.small ? 70 : 0);
      const a = inA(lt, .55, .5) * o;
      glass(x, L - 20, top + (1 - a) * 60, R - L + 40, h, a, s.tint);
      let y = top + 90 + (1 - a) * 60;
      if (s.badge) pill(x, s.badge, L + 20, y, s.badgeColor || '#7fe3ff', inA(lt, .75) * o);
      y += 110;
      text(x, s.title, L + 20, y + up(lt, .85), 92, 900, '#ffffff', inA(lt, .85) * o, { glow: `rgba(${s.tint || '170,120,255'},.9)`, blur: 34 });
      y += 40;
      (s.lines || []).forEach((ln, k) => {
        const al = inA(lt, 1.15 + k * .22) * o;
        y += 78;
        text(x, ln, L + 20, y + up(lt, 1.15 + k * .22), 46, 600, '#eeeaff', al);
      });
      if (s.small) { y += 56; text(x, s.small, L + 20, y, 34, 500, '#a9a3d6', inA(lt, 1.8) * o); }
      if (s.best) { y += 84; text(x, 'Best for: ' + s.best, L + 20, y, 40, 700, `rgb(${s.tint || '170,120,255'})`, inA(lt, 2.0) * o, { glow: `rgba(${s.tint || '170,120,255'},.6)`, blur: 16 }); }
    }

    if (s.kind === 'pick') {
      text(x, s.title, CX, 1160 + up(lt, .3), 84, 900, '#ffffff', inA(lt, .3) * o, { align: 'center', glow: 'rgba(170,120,255,.9)', blur: 36 });
      (s.rows || []).forEach((row, k) => {
        const st = .7 + k * .45, a = inA(lt, st) * o, y = 1250 + k * 150;
        glass(x, L - 20, y + (1 - a) * 40, R - L + 40, 120, a, row.tint);
        text(x, row.from, L + 20, y + 76 + (1 - a) * 40, 42, 600, '#eeeaff', a);
        text(x, row.to, R - 10, y + 78 + (1 - a) * 40, 46, 900, `rgb(${row.tint || '255,255,255'})`, a, { align: 'right', glow: `rgba(${row.tint || '255,255,255'},.8)`, blur: 20 });
      });
    }

    if (s.kind === 'cta') {
      const lines = wrap(x, s.title, 96, 900, 860);
      lines.forEach((ln, k) => text(x, ln, CX, 1200 + k * 108 + up(lt, .3 + k * .15), 96, 900, '#ffffff', inA(lt, .3 + k * .15) * o, { align: 'center', glow: 'rgba(255,120,190,.9)', blur: 40 }));
      const y = 1230 + lines.length * 108;
      if (s.sub) text(x, s.sub, CX, y + up(lt, .9), 48, 700, '#7fe3ff', inA(lt, .9) * o, { align: 'center', glow: 'rgba(80,200,255,.7)' });
      if (s.handle) text(x, s.handle, CX, y + 90, 38, 500, '#c9c3ef', inA(lt, 1.3) * o, { align: 'center' });
    }

    // global fade in/out
    const total = spec.scenes.reduce((a, b) => a + b.dur, 0);
    const g = Math.min(1, t / .4, (total - t) / .5);
    if (g < 1) { x.fillStyle = `rgba(0,0,0,${1 - Math.max(0, g)})`; x.fillRect(0, 0, W, H); }
  }

  function vignette(x) {
    const rg = x.createRadialGradient(CX, H / 2, H * .35, CX, H / 2, H * .75);
    rg.addColorStop(0, 'rgba(0,0,0,0)'); rg.addColorStop(1, 'rgba(0,0,0,.55)');
    x.fillStyle = rg; x.fillRect(0, 0, W, H);
  }

  function drawFrame(x, spec, t) {
    if (!BG) initBG();
    drawBG(x, t);
    drawParticles(x, spec, t);
    vignette(x);
    drawUI(x, spec, t);
  }

  // ---------- minimal WebM (Matroska) muxer ----------
  function vint(n) { // EBML size
    for (let len = 1; len <= 8; len++) { if (n < Math.pow(2, 7 * len) - 1) { const b = new Uint8Array(len); let v = n; for (let i = len - 1; i >= 0; i--) { b[i] = v & 0xff; v = Math.floor(v / 256); } b[0] |= 1 << (8 - len); return b; } }
    throw new Error('size too large');
  }
  function cat(arrs) { let n = 0; for (const a of arrs) n += a.length; const o = new Uint8Array(n); let p = 0; for (const a of arrs) { o.set(a, p); p += a.length; } return o; }
  function idb(id) { const b = []; while (id > 0) { b.unshift(id & 0xff); id = Math.floor(id / 256); } return new Uint8Array(b); }
  function el(id, data) { return cat([idb(id), vint(data.length), data]); }
  function uint(id, v) { const b = []; do { b.unshift(v & 0xff); v = Math.floor(v / 256); } while (v > 0); return el(id, new Uint8Array(b)); }
  function str(id, s) { return el(id, new TextEncoder().encode(s)); }
  function flt(id, v) { const b = new Uint8Array(8); new DataView(b.buffer).setFloat64(0, v); return el(id, b); }
  function muxWebM(chunks, fps, codecId) {
    const durMs = chunks.length * 1000 / fps;
    const header = el(0x1A45DFA3, cat([uint(0x4286, 1), uint(0x42F7, 1), uint(0x42F2, 4), uint(0x42F3, 8), str(0x4282, 'webm'), uint(0x4287, 2), uint(0x4285, 2)]));
    const info = el(0x1549A966, cat([uint(0x2AD7B1, 1000000), str(0x4D80, 'JTSG'), str(0x5741, 'JTSG'), flt(0x4489, durMs)]));
    const tracks = el(0x1654AE6B, el(0xAE, cat([uint(0xD7, 1), uint(0x73C5, 1), uint(0x83, 1), str(0x86, codecId), el(0xE0, cat([uint(0xB0, W), uint(0xBA, H)]))])));
    const clusters = []; let cur = null, curTc = 0;
    chunks.forEach((c, i) => {
      const tc = Math.round(i * 1000 / fps);
      if (c.key || !cur) { if (cur) clusters.push(el(0x1F43B675, cat(cur))); cur = [uint(0xE7, tc)]; curTc = tc; }
      const rel = tc - curTc;
      const hdr = new Uint8Array([0x81, (rel >> 8) & 0xff, rel & 0xff, c.key ? 0x80 : 0x00]);
      cur.push(el(0xA3, cat([hdr, c.data])));
    });
    if (cur) clusters.push(el(0x1F43B675, cat(cur)));
    const segment = el(0x18538067, cat([info, tracks, ...clusters]));
    return new Blob([header, segment], { type: 'video/webm' });
  }

  // ---------- render whole video ----------
  async function render(spec, opts) {
    opts = opts || {};
    const fps = spec.fps || 30;
    const total = spec.scenes.reduce((a, b) => a + b.dur, 0);
    const frames = Math.round(total * fps);
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const x = c.getContext('2d');
    const chunks = [];
    let err = null;
    const enc = new VideoEncoder({ output: (ch) => { const d = new Uint8Array(ch.byteLength); ch.copyTo(d); chunks.push({ key: ch.type === 'key', data: d }); }, error: e => { err = e; } });
    const codec = opts.codec || 'vp8';
    enc.configure({ codec, width: W, height: H, bitrate: opts.bitrate || 9000000, framerate: fps });
    for (let f = 0; f < frames; f++) {
      if (err) throw err;
      drawFrame(x, spec, f / fps);
      const vf = new VideoFrame(c, { timestamp: Math.round(f * 1e6 / fps), duration: Math.round(1e6 / fps) });
      enc.encode(vf, { keyFrame: f % fps === 0 });
      vf.close();
      if (enc.encodeQueueSize > 8) await new Promise(r => setTimeout(r, 0));
      if (opts.onProgress && f % 15 === 0) opts.onProgress(f / frames);
    }
    await enc.flush(); enc.close();
    if (err) throw err;
    return muxWebM(chunks, fps, codec === 'vp8' ? 'V_VP8' : 'V_VP9');
  }

  function attachVideo(blob, name) {
    const input = document.querySelector('input[type=file][accept*=video]');
    if (!input) throw new Error('Video uploader input not found: open TikTok Studio upload on the Video tab');
    const dt = new DataTransfer(); dt.items.add(new File([blob], name || 'video.webm', { type: 'video/webm' }));
    input.files = dt.files; input.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  }

  window.JCG = { render, drawFrame, attachVideo, W, H };
})();
