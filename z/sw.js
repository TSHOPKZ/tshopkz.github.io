// TSHOP — уведомления о статусе заказа (работают, даже когда браузер закрыт)
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("push", e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { d = { body: e.data ? e.data.text() : "" }; }
  e.waitUntil(self.registration.showNotification(d.title || "TSHOP", {
    body: d.body || "Статус вашего заказа обновился",
    icon: "/img/icon-192.png", badge: "/img/icon-192.png",
    tag: d.tag || "tshop", renotify: true, data: { url: d.url || "/z/" }
  }));
});
self.addEventListener("notificationclick", e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || "/z/";
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(list => {
    for (const c of list) { if (c.url.includes("/z/") && "focus" in c) { c.navigate(url); return c.focus(); } }
    return self.clients.openWindow(url);
  }));
});
