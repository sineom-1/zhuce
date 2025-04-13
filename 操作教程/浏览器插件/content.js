// Cursor 内容脚本

// 监听从网页到扩展的消息
window.addEventListener('message', function(event) {
  // 确保消息来源是我们期望的域名
  if (event.origin.includes('cursor.com') || 
      event.origin.includes('cursor.sh')) {
    
    // 处理来自Cursor网页的消息
    if (event.data && event.data.action === 'openAuthPopup') {
      // 发送消息给后台脚本创建弹窗
      if (event.data.params && event.data.params.challenge && event.data.params.uuid) {
        chrome.runtime.sendMessage({
          action: 'createPopup',
          params: event.data.params
        }, function(response) {
          // 将响应发送回网页
          window.postMessage({
            action: 'popupCreated',
            success: response && response.success,
            windowId: response && response.windowId,
            fromExtension: true
          }, '*');
        });
      }
    }
  }
});

// 注入辅助脚本以接收来自网页的消息
function injectHelperScript() {
  const script = document.createElement('script');
  script.textContent = `
    // 网页辅助脚本
    (function() {
      // 这个函数可以由网页调用来打开认证弹窗
      window.openCursorXAuthPopup = function(challenge, uuid) {
        window.postMessage({
          action: 'openAuthPopup',
          params: { challenge, uuid },
          fromPage: true
        }, '*');
        
        return true;
      };
    })();
  `;
  
  (document.head || document.documentElement).appendChild(script);
  script.remove();
}

// 网页加载完成后尝试注入辅助脚本
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectHelperScript);
} else {
  injectHelperScript();
}

// 监听来自后台脚本的消息
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'injectScript') {
    injectHelperScript();
    sendResponse({success: true});
  }
}); 