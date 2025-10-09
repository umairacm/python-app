// GODZEXMD Web Interactivity

document.getElementById('godzexmd-btn').onclick = function() {
  document.getElementById('godzexmd-section').style.display = 'block';
  this.style.display = 'none';
};
document.getElementById('back-btn').onclick = function() {
  document.getElementById('godzexmd-section').style.display = 'none';
  document.getElementById('godzexmd-btn').style.display = 'inline-block';
};

document.getElementById('generate-session').onclick = function() {
  const sessionId = 'GODZEXMD-' + Math.random().toString(36).substr(2, 10).toUpperCase();
  document.getElementById('session-id').value = sessionId;
};

// QR Code Generation (using a simple library)
function drawQR(text) {
  const canvas = document.getElementById('qr-canvas');
  const size = 180;
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, size, size);
  // Use a simple QR code API for demo
  const img = new window.Image();
  img.crossOrigin = 'Anonymous';
  img.onload = function() {
    ctx.drawImage(img, 0, 0, size, size);
  };
  img.src = `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodeURIComponent(text)}`;
}
document.getElementById('generate-qr').onclick = function() {
  const text = document.getElementById('qr-input').value;
  if (text.trim()) drawQR(text);
};

// Pair Code/QR Code Server Buttons (demo: alert server number)
document.querySelectorAll('.pair-server').forEach(btn => {
  btn.onclick = function() {
    alert('Pair Code Server ' + this.dataset.server + ' selected!');
  };
});
document.querySelectorAll('.qr-server').forEach(btn => {
  btn.onclick = function() {
    alert('QR Code Server ' + this.dataset.server + ' selected!');
  };
});
